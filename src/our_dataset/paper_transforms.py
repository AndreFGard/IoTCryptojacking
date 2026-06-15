import logging
import pathlib
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
import pandas as pd
from sklearn.model_selection import train_test_split

from our_dataset.transforms import Pipeline, PipelineReturn, _extract_catch22_features, _scale
from paper.malicious_vs_benign_1.dataset import load_dataset as load_paper_raw_dataset
from paper.malicious_vs_benign_1.experiments import SCENARIOS


ALLOWED_SCENARIOS = {
    "s2_thr10": "S2: THR 10 (Stealthy CPU mining throttle - 10%)",
    "s2_thr50": "S2: THR 50 (Robust CPU mining throttle - 50%)",
    "s6_single_iot": "S6: Single compromised IoT device (Raspberry - 10%)",
    "s7_iot_iot": "S7: IoT + IoT compromised devices",
}


def load_paper_dataframe(scenario: str = "s2_thr10") -> pd.DataFrame:
    """
    Loads raw dataframes from the reference paper's dataset corresponding to the
    specified scenario, cleans them, and formats them for the transforms pipeline.
    
    Parameters:
        scenario: str. The scenario slug/name to load. Available:
            - "s2_thr10": S2: THR 10 (Stealthy CPU mining throttle - 10%)
            - "s2_thr50": S2: THR 50 (Robust CPU mining throttle - 50%)
            - "s6_single_iot": S6: Single compromised IoT device (Raspberry - 10%)
            - "s7_iot_iot": S7: IoT + IoT compromised devices
            
    Returns:
        pd.DataFrame containing columns:
        ['interarrival', 'size', 'activity', 'is_malicious']
    """
    if scenario not in ALLOWED_SCENARIOS:
        raise ValueError(
            f"Unknown or disallowed scenario slug: {scenario}. Available scenarios: {list(ALLOWED_SCENARIOS.keys())}"
        )

    scenario_obj = None
    for s in SCENARIOS:
        if s.slug == scenario:
            scenario_obj = s
            break
            
    if scenario_obj is None:
        raise ValueError(f"Scenario slug '{scenario}' not found in experiments SCENARIOS.")
        
    logging.info(f"Loading reference paper's datasets for scenario: {scenario_obj.title}")
    mapping = load_paper_raw_dataset()
    
    allowed_keys = sorted(list(set(scenario_obj.malicious + scenario_obj.benign)))
    dfs = []
    
    for k in allowed_keys:
        if k not in mapping:
            logging.warning(f"Key {k} specified in scenario {scenario} but not found in raw dataset mapping.")
            continue
            
        df = mapping[k]
        df_copy = df.copy()
        # Conforming to original notebook/modular paper code which drops rows with ANY NaNs
        df_copy = df_copy.dropna()
        
        df_copy = df_copy.sort_values("Time")
        
        df_copy["activity"] = f"activity_{k}"
        df_copy["interarrival"] = df_copy["Time"].diff().fillna(0.0)
        df_copy["size"] = df_copy["Length"]
        df_copy["is_malicious"] = df_copy["Is_malicious"]
        
        df_copy = df_copy[["interarrival", "size", "activity", "is_malicious"]]
        dfs.append(df_copy)
        
    if not dfs:
        raise ValueError(f"No DataFrames were loaded for scenario: {scenario}")
        
    merged_df = pd.concat(dfs, ignore_index=True)
    logging.info(f"Loaded reference paper's dataset for scenario {scenario}. Total rows: {len(merged_df)}")
    return merged_df


def _split_windows_paper(
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
    """
    Splits the paper dataframe into consecutive windows of window_size with overlap,
    grouping by activity to prevent boundary leakage.
    Chronologically partitions the windows of each activity into train, validation, and test sets.
    """
    train_windows: list[dict[str, pd.Series]] = []
    val_windows: list[dict[str, pd.Series]] = []
    test_windows: list[dict[str, pd.Series]] = []

    step = window_size - overlap
    if step <= 0:
        raise ValueError("Overlap must be strictly less than window_size.")

    logging.info(
        f"Starting paper window splitting (window_size={window_size}, overlap={overlap})"
    )

    for activity, group in df.groupby("activity"):
        n_rows = len(group)
        if n_rows < window_size:
            continue

        windowed_cols = {}
        for col in ["interarrival", "size", "is_malicious"]:
            arr = group[col].to_numpy()
            windowed_cols[col] = sliding_window_view(arr, window_shape=window_size)[::step]

        num_windows = windowed_cols["size"].shape[0]
        group_windows = []
        for i in range(num_windows):
            group_windows.append({
                "interarrival": pd.Series(windowed_cols["interarrival"][i], copy=False),
                "size": pd.Series(windowed_cols["size"][i], copy=False),
                "is_malicious": pd.Series(windowed_cols["is_malicious"][i], copy=False),
                "activity": pd.Series([activity] * window_size, copy=False),
            })

        n_train = int(train_ratio * num_windows)
        n_val = int(val_ratio * num_windows)

        if n_train > 0:
            train_windows.extend(group_windows[:n_train])
        if n_val > 0:
            val_windows.extend(group_windows[n_train : n_train + n_val])
        if num_windows - (n_train + n_val) > 0:
            test_windows.extend(group_windows[n_train + n_val :])

        logging.info(
            f"windows of activity '{activity}': split into "
            f"{n_train} train, "
            f"{n_val} val, and "
            f"{num_windows - (n_train + n_val)} test windows"
        )

    logging.info(
        f"Window splitting complete. Total train windows: {len(train_windows)}, "
        f"Total val windows: {len(val_windows)}, Total test windows: {len(test_windows)}"
    )
    return train_windows, val_windows, test_windows


class PipelinePaperPycatch22(Pipeline):
    name = "paper_pycatch22"

    def __init__(
        self,
        df: pd.DataFrame,
        window_size: int,
        overlap: int,
        train_ratio: float = 0.7,
        val_ratio: float = 0.1,
        test_ratio: float = 0.2,
        scenario: str = "s2_thr10",
    ) -> None:
        self._df = df
        self._window_size = window_size
        self._overlap = overlap
        self._train_ratio = train_ratio
        self._val_ratio = val_ratio
        self._test_ratio = test_ratio
        self.name = f"paper_pycatch22_{scenario}"

    def run_pipeline(self) -> PipelineReturn:
        logging.info("Starting PipelinePaperPycatch22 on paper df")
        
        # 1. Split into windows chronologically per activity group
        train_wins, val_wins, test_wins = _split_windows_paper(
            self._df,
            self._window_size,
            self._overlap,
            self._train_ratio,
            self._val_ratio,
            self._test_ratio,
        )
        
        # 2. Extract features
        train_df = _extract_catch22_features(train_wins)
        val_df = _extract_catch22_features(val_wins)
        test_df = _extract_catch22_features(test_wins)
        
        if train_df.empty:
            raise ValueError("No features could be extracted from train windows.")
            
        # 3. Scale the features
        train_feat, val_feat, test_feat, scaler = _scale(train_df, val_df, test_df)
        
        logging.info(
            f"Completed PipelinePaperPycatch22: train features: {train_feat.shape}, "
            f"val features: {val_feat.shape}, test features: {test_feat.shape}"
        )
        
        feature_cols = [
            c for c in train_feat.columns if c not in ["activity", "is_malicious"]
        ]
        return train_feat, val_feat, test_feat, feature_cols


if __name__ == "__main__":
    # Self-test log setup
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    
    df = load_paper_dataframe()
    # Test on a small subset of 5000 rows to speed up self-test
    df_subset = df.iloc[:5000]
    logging.info("Testing PipelinePaperPycatch22 on subset...")
    pipeline = PipelinePaperPycatch22(df_subset, window_size=10, overlap=0)
    train, val, test, selected_features = pipeline.run_pipeline()
    logging.info(f"Self-test complete. Extracted {len(selected_features)} features.")
