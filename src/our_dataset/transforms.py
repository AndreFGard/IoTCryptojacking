import logging
import pandas as pd
import pycatch22
from sklearn import compose, preprocessing


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
            window["interarrival"] -= window["interarrival"].iloc[-1]
            group_windows.append(window)

        n_windows = len(group_windows)
        n_train = int(train_ratio * n_windows)
        n_test = int(test_ratio * n_windows)

        # to avoid data leakage 
        if n_train > 1:
            train_windows.extend(group_windows[: n_train - 1])
        if n_test > 1:
            test_windows.extend(group_windows[n_train + 1 : n_train + n_test])

        logging.info(f"windows of activity '{activity}': split into {max(0, n_train - 1)}" 
                        "train and {max(0, n_test - 1)} test windows")

    logging.info(f"Window splitting complete. Total train windows: {len(train_windows)}, "
                        "Total test windows: {len(test_windows)}")
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
        
        for meta_col in ["activity", "vpn"]:
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


if __name__ == '__main__':
    # Simple self-test log setup
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S")
    from our_dataset import dataset
    dataset = dataset.load_dataset()
    pipeline(dataset.bitcoin, window_size=10, overlap=5)