import pandas as pd
from sklearn import compose, preprocessing


def encode(df: pd.DataFrame) -> pd.DataFrame:
    categorical_cols = ["direction", "vpn", "activity"]
    cols_to_encode = [c for c in categorical_cols if c in df.columns]
    if not cols_to_encode:
        return df.copy()

    ct = compose.ColumnTransformer(
        [("cat_encode", preprocessing.OrdinalEncoder(), cols_to_encode)],
        remainder="passthrough"
    )
    encoded_data = ct.fit_transform(df)
    new_cols = cols_to_encode + [c for c in df.columns if c not in cols_to_encode]
    
    return pd.DataFrame(encoded_data, columns=new_cols, index=df.index)[list(df.columns)] #type:ignore


def split_homogeneous_windows(
    df: pd.DataFrame,
    window_size: int,
    overlap: int,
    train_ratio: float = 0.7,
    test_ratio: float = 0.2,
) -> tuple[list[pd.DataFrame], list[pd.DataFrame]]:
    """Splits a DataFrame into homogeneous windows, then splits into leakage-free train and test sets."""
    train_windows: list[pd.DataFrame] = []
    test_windows: list[pd.DataFrame] = []
    step = window_size - overlap
    if step <= 0:
        raise ValueError("Overlap must be strictly less than window_size.")

    for _, group in df.groupby("activity"):
        n_rows = len(group)
        group_windows: list[pd.DataFrame] = []
        for start in range(0, n_rows - window_size + 1, step):
            window = group.iloc[start : start + window_size].copy()

            window["interarrival"] -= window["interarrival"].iloc[-1]
            group_windows.append(window)

        n_windows = len(group_windows)
        n_train = int(train_ratio * n_windows)
        n_test = int(test_ratio * n_windows)

        #to avoid data leakage 
        if n_train > 1:
            train_windows.extend(group_windows[: n_train - 1])
        if n_test > 1:
            test_windows.extend(group_windows[n_train + 1 : n_train + n_test])

    return train_windows, test_windows


def pipeline(
    df: pd.DataFrame,
    window_size: int,
    overlap: int,
    train_ratio: float = 0.7,
    test_ratio: float = 0.2,
) -> tuple[list[pd.DataFrame], list[pd.DataFrame]]:
    """Executes the complete preprocessing pipeline on the dataset."""
    encoded_df = encode(df)
    return split_homogeneous_windows(encoded_df, window_size, overlap, train_ratio, test_ratio)
