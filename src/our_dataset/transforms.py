import logging
from typing import Callable, cast
import numpy as np
import pandas as pd
import pycatch22
from sklearn import compose, preprocessing
import tsfresh
from tsfresh.feature_selection.relevance import calculate_relevance_table
from tsfresh.utilities.dataframe_functions import impute


def encode(df: pd.DataFrame) -> pd.DataFrame:
    categorical_cols = ["direction", "vpn", "activity"]
    cols_to_encode = [c for c in categorical_cols if c in df.columns]
    if not cols_to_encode:
        logging.warning("no categorical columns to encode.")
        return df.copy()

    logging.info(f"encoding categorical columns using ColumnTransformer: {cols_to_encode}")
    ct = compose.ColumnTransformer(
        [("cat_encode", preprocessing.OrdinalEncoder(), cols_to_encode)],
        remainder="passthrough"
    )
    encoded_data = ct.fit_transform(df)
    new_cols = cols_to_encode + [c for c in df.columns if c not in cols_to_encode]
    
    encoded_df = pd.DataFrame(encoded_data, columns=new_cols, index=df.index)[list(df.columns)]  
    logging.info("finished encoding")
    return encoded_df # type:ignore


def split_homogeneous_windows(
    df: pd.DataFrame,
    window_size: int,
    overlap: int,
    train_ratio: float = 0.7,
    test_ratio: float = 0.2,
) -> tuple[list[pd.DataFrame], list[pd.DataFrame]]:
    """splits windows with homgenous activity"""
    train_windows: list[pd.DataFrame] = []
    test_windows: list[pd.DataFrame] = []
    step = window_size - overlap
    if step <= 0:
        raise ValueError("Overlap must be strictly less than window_size.")

    logging.info(f"Starting homogeneous window splitting (window_size={window_size}, overlap={overlap})")
    
    for activity, group in df.groupby("activity"):
        n_rows = len(group)
        group_windows: list[pd.DataFrame] = []
        for start in range(0, n_rows - window_size + 1, step):
            window = group.iloc[start : start + window_size].copy()
            window["interarrival"] = window["interarrival"].diff().fillna(0.0)
            group_windows.append(window)

        n_windows = len(group_windows)
        n_train = int(train_ratio * n_windows)
        n_test = int(test_ratio * n_windows)

        # to avoid data leakage 
        if n_train > 1:
            train_windows.extend(group_windows[: n_train - 1])
        if n_test > 1:
            test_windows.extend(group_windows[n_train + 1 : n_train + n_test])

        logging.info(f"windows of activity '{activity}': split into {max(0, n_train - 1)} "
                     f"train and {max(0, n_test - 1)} test windows")

    logging.info(f"Window splitting complete. Total train windows: {len(train_windows)}, "
                 f"Total test windows: {len(test_windows)}")
    return train_windows, test_windows


def extract_features(windows: list[pd.DataFrame]) -> pd.DataFrame:
    """Extracts catch22 features for time series columns in each window, preserving metadata."""
    if not windows:
        logging.info("No windows provided for catch22 feature extraction.")
        return pd.DataFrame()

    logging.info(f"starting catch22 feature extraction for {len(windows)} windows")
    feature_rows = []
    for window in windows:
        row_features = {}
        
        for meta_col in ["activity", "vpn", "is_malicious"]:
            if meta_col in window.columns:
                row_features[meta_col] = window[meta_col].iloc[0]

        for col in ["interarrival", "size"]:
            if col in window.columns:
                series = window[col].tolist()
                res = pycatch22.catch22_all(series)
                for name, value in zip(res["names"], res["values"]):
                    row_features[f"{col}_{name}"] = value

        feature_rows.append(row_features)

    feature_df = pd.DataFrame(feature_rows)
    logging.info(f"feature extraction complete, shape: {feature_df.shape}")
    return feature_df


def pipeline(
    df: pd.DataFrame,
    window_size: int,
    overlap: int,
    train_ratio: float = 0.7,
    test_ratio: float = 0.2,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Executes the complete preprocessing pipeline on the dataset and extracts catch22 features."""
    logging.info("starting pipeline on df")
    encoded_df = encode(df)
    train_windows, test_windows = split_homogeneous_windows(
        encoded_df, window_size, overlap, train_ratio, test_ratio
    )
    
    train_feat = extract_features(train_windows)
    test_feat = extract_features(test_windows)
    
    logging.info(f"completed pipeline: train features: {train_feat.shape}, test features: {test_feat.shape}")
    return train_feat, test_feat


def extract_features_tsfresh(windows: list[pd.DataFrame]) -> pd.DataFrame:
    """Extracts tsfresh features for each window."""
    if not windows:
        raise ValueError("No windows provided for tsfresh feature extraction.")

    logging.info(f"starting tsfresh feature extraction for {len(windows)} windows")
    
    meta_rows = []
    for w in windows:
        meta = {}
        for col in ["activity", "vpn", "is_malicious"]:
            if col in w.columns:
                meta[col] = w[col].iloc[0]
        meta_rows.append(meta)
    meta_df = pd.DataFrame(meta_rows)

    dfs = []
    for i, w in enumerate(windows):
        w_df = pd.DataFrame()
        for col in ["interarrival", "size"]:
            if col in w.columns:
                w_df[col] = w[col].values
        w_df["id"] = i
        w_df["time"] = range(len(w))
        dfs.append(w_df)
        
    big_df = pd.concat(dfs, ignore_index=True)

    features_df = pd.DataFrame(
        tsfresh.extract_features(
            big_df,
            column_id="id",
            column_sort="time",
            impute_function=impute,
            disable_progressbar=True,
        )
    )

    features_df = features_df.reset_index(drop=True)
    
    result_df = pd.concat([meta_df, features_df], axis=1)
    logging.info(f"tsfresh feature extraction complete, shape: {result_df.shape}")
    return result_df


def pipeline_tsfresh(
    df: pd.DataFrame,
    window_size: int,
    overlap: int,
    train_ratio: float = 0.7,
    test_ratio: float = 0.2,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Preprocesses data, extracts tsfresh features, and performs relevance-based feature selection."""
    logging.info("starting pipeline_tsfresh on df")
    
    df_copy = df.copy()
    df_copy["is_malicious"] = df_copy["activity"].isin(["bitcoin", "bytecoin", "monero"]).astype(int)
    
    encoded_df = encode(df_copy)
    train_windows, test_windows = split_homogeneous_windows(
        encoded_df, window_size, overlap, train_ratio, test_ratio
    )
    
    train_feat_all = extract_features_tsfresh(train_windows)
    test_feat_all = extract_features_tsfresh(test_windows)
    
    if train_feat_all.empty or test_feat_all.empty:
        logging.warning("extracted feature dataframes are empty; returning empty dataframes")
        return train_feat_all, test_feat_all

    logging.info("starting feature selection via relevance table")
    meta_cols = ["activity", "vpn", "is_malicious"]
    feature_cols = [c for c in train_feat_all.columns if c not in meta_cols]
    
    X_train = train_feat_all[feature_cols]
    y_train = train_feat_all["is_malicious"]
    
    relevance_table = cast(pd.DataFrame, calculate_relevance_table(X_train, y_train))
    relevance_table = relevance_table[relevance_table["relevant"]]
    relevance_table = cast(pd.DataFrame, relevance_table).sort_values(by="p_value")
    
    best_features = relevance_table[relevance_table["p_value"] <= 0.05]
    selected_features = best_features["feature"].tolist()
    
    train_feat = train_feat_all[selected_features].copy().round(6)
    test_feat = test_feat_all[selected_features].copy().round(6)
    
    for col in ["activity", "vpn"]:
        if col in train_feat_all.columns:
            train_feat[col] = train_feat_all[col].values
        if col in test_feat_all.columns:
            test_feat[col] = test_feat_all[col].values
            
    logging.info(f"completed pipeline_tsfresh: train features: {train_feat.shape}, test features: {test_feat.shape}")
    assert isinstance(train_feat, pd.DataFrame) and isinstance(test_feat, pd.DataFrame)
    return train_feat, test_feat


if __name__ == '__main__':
    from sklearn.svm import SVC
    from sklearn.model_selection import GridSearchCV
    from sklearn.metrics import classification_report
    from sklearn.impute import SimpleImputer
    import pathlib
    from our_dataset import dataset

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S")

    logging.info("loading dataset")
    dataset_path = pathlib.Path("/content/drive/MyDrive/Cryptojacking Network Traffic 2021")
    #dataset = load_dataset(dataset_path)
    dataset = load_dataset()
    #df_subset = dataset.df.groupby("activity").head(5000).reset_index(drop=True)
    df_subset = dataset.df
    logging.info("starting feature extraction")
    scoring = ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted', 'roc_auc']
    train_feat, test_feat = pipeline(df_subset, window_size=10, overlap=5)
    meta_cols = ["activity", "vpn", "is_malicious"]

    X_train = train_feat.drop(columns=meta_cols)
    y_train = train_feat["is_malicious"]

    X_test = test_feat.drop(columns=meta_cols)
    y_test = test_feat["is_malicious"]

    imputer = SimpleImputer(strategy='constant', fill_value=0.0)

    X_train_clean = imputer.fit_transform(X_train)
    X_test_clean = imputer.transform(X_test)

    param_grid = {
        'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
        'C': [1, 2],
        'gamma': ['scale', 'auto']
    }

    svm_model = SVC(random_state=42)

    grid_search = GridSearchCV(
        estimator=svm_model,
        param_grid=param_grid,
        scoring=scoring,
        refit='accuracy',
        cv=5,
        n_jobs=-1,
        verbose=2
    )

    logging.info("starting tuning")
    grid_search.fit(X_train_clean, y_train)
    logging.info("finished tuning")

    print("\n" + "="*60)
    print("Classification report for all enumerations")
    print("="*60)
    logging.info("starting to enumerate results")
    for i, params in enumerate(grid_search.cv_results_['params']):
        print(f"\ntested: {params}")
        logging.info(f"testing: {params}")
        temp_svm = SVC(**params, random_state=42)
        temp_svm.fit(X_train_clean, y_train)
        y_pred_temp = temp_svm.predict(X_test_clean)

        print(f"{params}: ")
        print(classification_report(y_test, y_pred_temp))
        print("=" * 60)

    logging.info("finished ")
    print("final model: ")
    print(grid_search.best_params_)