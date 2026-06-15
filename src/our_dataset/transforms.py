import logging
import pathlib
from dataclasses import dataclass
from typing import Any, cast
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
import pandas as pd
import pycatch22
from sklearn import compose, preprocessing
import tsfresh
from tsfresh.feature_selection.relevance import calculate_relevance_table
from tsfresh.utilities.dataframe_functions import impute

PipelineReturn = tuple[
    pd.DataFrame, pd.DataFrame, pd.DataFrame, list[str]
]

CPU_COUNT = 8


def _encode(
    df: pd.DataFrame, encoder=None
) -> tuple[pd.DataFrame, compose.ColumnTransformer]:
    categorical_cols = ["direction", "vpn", "activity"]
    cols_to_encode = [c for c in categorical_cols if c in df.columns]
    if not cols_to_encode:
        raise ValueError("no categorical columns to encode.")

    logging.info(
        f"encoding categorical columns using ColumnTransformer: {cols_to_encode}"
    )
    if encoder is None:
        ct = compose.ColumnTransformer(
            [("cat_encode", preprocessing.OrdinalEncoder(), cols_to_encode)],
            remainder="passthrough",
        )
        encoded_data = ct.fit_transform(df)
    else:
        ct = encoder
        encoded_data = ct.transform(df)
    new_cols = cols_to_encode + [c for c in df.columns if c not in cols_to_encode]

    encoded_df = pd.DataFrame(encoded_data, columns=new_cols, index=df.index)[
        list(df.columns)
    ]
    logging.info("finished encoding")
    return encoded_df, ct  # type:ignore


def _split_windows(
    df: pd.DataFrame,
    window_size: int,
    overlap: int,
    train_ratio: float = 0.7,
    val_ratio: float = 0.1,
    test_ratio: float = 0.2,
) -> tuple[
    list[dict[str, pd.Series]],
    list[dict[str, pd.Series]],
    list[dict[str, pd.Series]],
]:
    """Splits windows (internally homogenous in activity) into train, val, and test sets"""
    train_windows: list[dict[str, pd.Series]] = []
    val_windows: list[dict[str, pd.Series]] = []
    test_windows: list[dict[str, pd.Series]] = []
    
    step = window_size - overlap
    if step <= 0:
        raise ValueError("Overlap must be strictly less than window_size.")

    logging.info(
        f"Starting homogeneous window splitting (window_size={window_size}, overlap={overlap})"
    )

    columns = df.columns.tolist()

    for key, group in df.groupby(["activity", "vpn"]):
        activity, vpn = cast(tuple[Any, Any], key)
        n_rows = len(group)
        
        if n_rows < window_size:
            continue

        windowed_cols = {}
        for col in columns:
            arr = group[col].to_numpy()
            windowed_cols[col] = sliding_window_view(arr, window_shape=window_size)[::step]

        if "interarrival" in windowed_cols:
            interarrival_windows = windowed_cols["interarrival"]
            diffs = np.diff(interarrival_windows, axis=1)
            zeros = np.zeros((interarrival_windows.shape[0], 1), dtype=diffs.dtype)
            windowed_cols["interarrival"] = np.concatenate((zeros, diffs), axis=1)

        num_windows = windowed_cols[columns[0]].shape[0]
        
        group_windows = [
            {col: pd.Series(windowed_cols[col][i], copy=False) for col in columns}
            for i in range(num_windows)
        ]

        n_train = int(train_ratio * num_windows)
        n_val = int(val_ratio * num_windows)
        n_test = int(test_ratio * num_windows)

        train_end = max(0, n_train - 1)
        if train_end > 0:
            train_windows.extend(group_windows[:train_end])

        val_start = n_train + 1
        val_end = val_start + max(0, n_val - 1)
        if val_start < num_windows and n_val > 1:
            val_windows.extend(group_windows[val_start:val_end])

        test_start = n_train + n_val + 1
        test_end = test_start + max(0, n_test - 1)
        if test_start < num_windows and n_test > 1:
            test_windows.extend(group_windows[test_start:test_end])

        logging.info(
            f"windows of activity '{activity}' and vpn {vpn}: split into "
            f"{len(group_windows[:train_end])} train, "
            f"{len(group_windows[val_start:val_end])} val, and "
            f"{len(group_windows[test_start:test_end])} test windows"
        )

    logging.info(
        f"Window splitting complete. Total train windows: {len(train_windows)}, "
        f"Total val windows: {len(val_windows)}, Total test windows: {len(test_windows)}"
    )
    
    return train_windows, val_windows, test_windows

def _extract_catch22_features(windows: list[dict[str, pd.Series]]) -> pd.DataFrame:
    """Extracts catch22 features for time series columns in each window, preserving metadata."""
    if not windows:
        logging.info("No windows provided for catch22 feature extraction.")
        return pd.DataFrame()

    logging.info(f"starting catch22 feature extraction for {len(windows)} windows")
    feature_rows = []
    for window in windows:
        row_features = {}

        for meta_col in ["activity", "vpn", "is_malicious"]:
            if meta_col in window:
                row_features[meta_col] = window[meta_col].values[0]

        for col in ["interarrival", "size"]:
            if col in window:
                series = window[col].tolist()
                res = pycatch22.catch22_all(series)
                for name, value in zip(res["names"], res["values"]):
                    row_features[f"{col}_{name}"] = value

        feature_rows.append(row_features)

    feature_df = pd.DataFrame(feature_rows)
    logging.info(f"feature extraction complete, shape: {feature_df.shape}")
    return feature_df


def _extract_features_tsfresh(windows: list[dict[str, pd.Series]]) -> pd.DataFrame:
    """Extracts tsfresh features for each window."""
    if not windows:
        raise ValueError("No windows provided for tsfresh feature extraction.")

    logging.info(f"starting tsfresh feature extraction for {len(windows)} windows")

    meta_rows = []
    for w in windows:
        meta = {}
        for col in ["activity", "vpn", "is_malicious"]:
            if col in w:
                meta[col] = w[col].values[0]
        meta_rows.append(meta)
    meta_df = pd.DataFrame(meta_rows)

    dfs = []
    for i, w in enumerate(windows):
        w_df = pd.DataFrame()
        for col in ["interarrival", "size"]:
            if col in w:
                w_df[col] = w[col].values
        w_df["id"] = i
        w_df["time"] = range(len(next(iter(w.values()))))
        dfs.append(w_df)

    big_df = pd.concat(dfs, ignore_index=True)

    features_df = pd.DataFrame(
        tsfresh.extract_features(
            big_df,
            column_id="id",
            column_sort="time",
            impute_function=impute,
            disable_progressbar=True,
            n_jobs=CPU_COUNT,
        )
    )

    features_df = features_df.reset_index(drop=True)

    result_df = pd.concat([meta_df, features_df], axis=1)
    logging.info(f"tsfresh feature extraction complete, shape: {result_df.shape}")
    return result_df


def _scale(
    train: pd.DataFrame, val: pd.DataFrame, test: pd.DataFrame, scaler=None
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, preprocessing.StandardScaler]:
    """Applies StandardScaler to non-metadata columns of train, val, and test."""
    feature_cols: list[str] = [
        c for c in train.columns if c not in ["activity", "vpn", "is_malicious"]
    ]
    if scaler is None:
        scaler = preprocessing.StandardScaler()
        fit_scaler = True
    else:
        fit_scaler = False

    if not feature_cols or train.empty:
        raise ValueError(
            f"No feature_cols ({feature_cols}) or train size insufficient ({len(train)})"
        )

    train_copy = train.copy()
    val_copy = val.copy()
    test_copy = test.copy()
    if fit_scaler:
        train_copy[feature_cols] = scaler.fit_transform(cast(pd.DataFrame, train_copy[feature_cols]))
    else:
        train_copy[feature_cols] = scaler.transform(cast(pd.DataFrame, train_copy[feature_cols]))
    if not val_copy.empty:
        val_copy[feature_cols] = scaler.transform(cast(pd.DataFrame, val_copy[feature_cols]))
    if not test_copy.empty:
        test_copy[feature_cols] = scaler.transform(cast(pd.DataFrame, test_copy[feature_cols]))
    return train_copy, val_copy, test_copy, scaler

class Pipeline:
    name: str

    def load_cache_or_run(self, dir: pathlib.Path | str) -> PipelineReturn:
        try:
            return self.load_cache(dir)
        except FileNotFoundError:
            train, val, test, selected_features = self.run_pipeline()
            self.save_cache(dir, train, val, test, selected_features)
            return train, val, test, selected_features

    def load_cache(self, dir: pathlib.Path | str) -> PipelineReturn:
        dir_path = pathlib.Path(dir)
        required_files = [dir_path / f"{self.name}_{s}.csv" for s in ["train", "val", "test"]]
        features_file = dir_path / f"{self.name}_selected_features.txt"
        
        if not (all(f.exists() for f in required_files) and features_file.exists()):
            raise FileNotFoundError(f"Cache files for pipeline '{self.name}' not found in {dir_path}")
            
        train = pd.read_csv(required_files[0])
        val = pd.read_csv(required_files[1])
        test = pd.read_csv(required_files[2])
        
        with open(features_file, "r") as f:
            selected_features = [line.strip() for line in f if line.strip()]
            
        return train, val, test, selected_features

    def save_cache(
        self,
        dir: pathlib.Path | str,
        train: pd.DataFrame,
        val: pd.DataFrame,
        test: pd.DataFrame,
        selected_features: list[str],
    ) -> None:
        dir_path = pathlib.Path(dir)
        dir_path.mkdir(exist_ok=True, parents=True)
        required_files = [dir_path / f"{self.name}_{s}.csv" for s in ["train", "val", "test"]]
        features_file = dir_path / f"{self.name}_selected_features.txt"
        
        for df, file in zip([train, val, test], required_files):
            df.to_csv(file, index=False)
            
        with open(features_file, "w") as f:
            for feat in selected_features:
                f.write(f"{feat}\n")

    def run_pipeline(self) -> PipelineReturn:
        raise NotImplementedError


class PipelinePycatch22(Pipeline):
    name = "pycatch22"

    def __init__(
        self,
        df: pd.DataFrame,
        window_size: int,
        overlap: int,
        train_ratio: float = 0.7,
        val_ratio: float = 0.1,
        test_ratio: float = 0.2,
    ) -> None:
        self._df = df
        self._window_size = window_size
        self._overlap = overlap
        self._train_ratio = train_ratio
        self._val_ratio = val_ratio
        self._test_ratio = test_ratio

    def run_pipeline(self) -> PipelineReturn:
        logging.info("starting pipeline on df")
        encoded_df, ct = _encode(self._df)
        train_windows, val_windows, test_windows = _split_windows(
            encoded_df, self._window_size, self._overlap, self._train_ratio, self._val_ratio, self._test_ratio
        )

        train_feat = _extract_catch22_features(train_windows)
        val_feat = _extract_catch22_features(val_windows)
        test_feat = _extract_catch22_features(test_windows)

        train_feat, val_feat, test_feat, scaler = _scale(train_feat, val_feat, test_feat)

        logging.info(
            f"completed pipeline: train features: {train_feat.shape}, "
            f"val features: {val_feat.shape}, test features: {test_feat.shape}"
        )
        feature_cols = [
            c for c in train_feat.columns if c not in ["activity", "vpn", "is_malicious"]
        ]
        return train_feat, val_feat, test_feat, feature_cols


class PipelineTsfresh(Pipeline):
    name = "tsfresh"

    def __init__(
        self,
        df: pd.DataFrame,
        window_size: int,
        overlap: int,
        train_ratio: float = 0.7,
        val_ratio: float = 0.1,
        test_ratio: float = 0.2,
    ) -> None:
        self._df = df
        self._window_size = window_size
        self._overlap = overlap
        self._train_ratio = train_ratio
        self._val_ratio = val_ratio
        self._test_ratio = test_ratio

    def run_pipeline(self) -> PipelineReturn:
        logging.info("starting pipeline_tsfresh on df")

        df_copy = self._df.copy()
        df_copy["is_malicious"] = (
            df_copy["activity"].isin(["bitcoin", "bytecoin", "monero"]).astype(int)
        )

        encoded_df, ct = _encode(df_copy)
        train_windows, val_windows, test_windows = _split_windows(
            encoded_df, self._window_size, self._overlap, self._train_ratio, self._val_ratio, self._test_ratio
        )

        train_feat_all = _extract_features_tsfresh(train_windows)
        val_feat_all = _extract_features_tsfresh(val_windows)
        test_feat_all = _extract_features_tsfresh(test_windows)

        if train_feat_all.empty or val_feat_all.empty or test_feat_all.empty:
            logging.warning(
                "one of the extracted feature dataframes is empty; returning empty dataframes"
            )
            scaler = preprocessing.StandardScaler()
            scaler.fit(np.zeros((1, 1)))
            return train_feat_all, val_feat_all, test_feat_all, []

        logging.info("starting feature selection via relevance table")
        meta_cols = ["activity", "vpn", "is_malicious"]
        feature_cols = [c for c in train_feat_all.columns if c not in meta_cols]

        X_train = train_feat_all[feature_cols]
        y_train = train_feat_all["is_malicious"]

        relevance_table = cast(
            pd.DataFrame, calculate_relevance_table(X_train, y_train, n_jobs=CPU_COUNT)
        )
        relevance_table = relevance_table[relevance_table["relevant"]]
        relevance_table = cast(pd.DataFrame, relevance_table).sort_values(by="p_value")

        best_features = relevance_table[relevance_table["p_value"] <= 0.05]
        selected_features = best_features["feature"].tolist()
        if not selected_features:
            selected_features = feature_cols

        train_feat = train_feat_all[selected_features].copy().round(6)
        val_feat = val_feat_all[selected_features].copy().round(6)
        test_feat = test_feat_all[selected_features].copy().round(6)

        for col in ["activity", "vpn", "is_malicious"]:
            if col in train_feat_all.columns:
                train_feat[col] = train_feat_all[col].values
            if col in val_feat_all.columns:
                val_feat[col] = val_feat_all[col].values
            if col in test_feat_all.columns:
                test_feat[col] = test_feat_all[col].values

        train_feat, val_feat, test_feat, scaler = _scale(
            cast(pd.DataFrame, train_feat),
            cast(pd.DataFrame, val_feat),
            cast(pd.DataFrame, test_feat),
        )

        logging.info(
            f"completed pipeline_tsfresh: train features: {train_feat.shape}, "
            f"val features: {val_feat.shape}, test features: {test_feat.shape}"
        )
        assert (
            isinstance(train_feat, pd.DataFrame)
            and isinstance(val_feat, pd.DataFrame)
            and isinstance(test_feat, pd.DataFrame)
        )
        return train_feat, val_feat, test_feat, selected_features




if __name__ == "__main__":
    # Simple self-test log setup
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    from our_dataset import dataset

    dataset = dataset.load_dataset()
    logging.info("Testing catch22 pipeline...")
    PipelinePycatch22(dataset.df.iloc[:200], window_size=10, overlap=5).run_pipeline()
    logging.info("Testing tsfresh pipeline...")
    PipelineTsfresh(dataset.df.iloc[:200], window_size=10, overlap=5).run_pipeline()

