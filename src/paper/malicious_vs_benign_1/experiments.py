from __future__ import annotations

import logging
import pathlib
from dataclasses import dataclass
from timeit import default_timer as timer
from typing import Dict, List, Sequence, Tuple

import numpy as np
import pandas as pd
import tsfresh
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report
from tsfresh.feature_selection.relevance import calculate_relevance_table
from tsfresh.utilities.dataframe_functions import impute

from paper.malicious_vs_benign_1.dataset import load_dataset


@dataclass(frozen=True)
class Scenario:
    slug: str
    title: str
    malicious: Tuple[int, ...]
    benign: Tuple[int, ...]


DATA_ROOT = pathlib.Path("data/malicious_vs_benign_1")

SCENARIOS: Sequence[Scenario] = (
    Scenario("s0_all_combined", "S0: All Combined", (1, 2, 3, 4, 5, 6, 7, 32, 33, 34, 35), (8, 9, 11, 10, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 27, 29)),
    Scenario("s1_server", "S1: Server", (2, 7, 32), (10, 11, 13, 15, 16, 17, 18, 19, 21, 22, 23, 26, 30, 28)),
    Scenario("s1_laptop", "S1: Laptop", (35,), (8, 20, 19, 30)),
    Scenario("s1_iot", "S1: IoT", (4, 5, 6, 33, 34), (8, 9, 10, 11, 12, 15, 16, 17, 21)),
    Scenario("s2_thr10", "S2: THR 10", (33,), (8, 10)),
    Scenario("s2_thr50", "S2: THR 50", (3, 34), (29, 31)),
    Scenario("s2_thr100", "S2: THR 100", (1, 2, 4, 5, 6, 7, 35), (11, 12, 13, 14, 16, 17, 21, 23, 26, 27, 28, 29, 30, 31)),
    Scenario("s3_in_browser", "S3: In-browser", (3, 5, 6, 7, 32, 33, 34, 35), (8, 9, 14, 15, 16, 17, 18, 19, 20, 14)),
    Scenario("s3_binary", "S3: Binary", (1, 2, 4), (12, 13, 15, 17, 22, 23, 27, 28, 29)),
    Scenario("s4_fully_compromised", "S4: Fully Compromised", (1, 2, 3, 4, 5, 6, 7, 32, 33, 34, 35), (8, 9, 11, 10, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 27, 29)),
    Scenario("s5_iot_laptop", "S5: IoT + Laptop", (5, 35), (14, 16, 18, 19, 20)),
    Scenario("s6_single_iot", "S6: Single IoT", (5,), (8, 9, 10)),
    Scenario("s7_iot_iot", "S7: IoT + IoT", (1, 34), (8, 9, 10, 11, 12, 21)),
)


def configure_logging(filename: str) -> None:
    log_dir = pathlib.Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    logging.info("Logging configured for %s", filename)


def _scenario_folder(s: Scenario) -> pathlib.Path:
    folder = DATA_ROOT / s.slug
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _collect(dataset_map: Dict[int, pd.DataFrame], keys: Sequence[int]) -> pd.DataFrame:
    return pd.concat([dataset_map[k] for k in keys], ignore_index=True)


def _save(df: pd.DataFrame, path: pathlib.Path) -> None:
    if path.exists():
        logging.info("Skipping existing artifact: %s", path.name)
        return
    df.to_csv(path, index=False)
    logging.info("Saved %s", path)


def _prepare(s: Scenario, dataset_map: Dict[int, pd.DataFrame]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_m = _collect(dataset_map, s.malicious)
    df_b = _collect(dataset_map, s.benign)

    print(f"\n--- {s.title} ---")
    print(f"malicious: {len(df_m)}")
    print(f"benign: {len(df_b)}")
    print(f"{int(df_m.isna().any(axis=1).sum())} NAN in malicious!")
    print(f"{int(df_b.isna().any(axis=1).sum())} NAN in benign!")

    df_m = df_m.dropna().reset_index(drop=True)
    df_b = df_b.dropna().reset_index(drop=True)

    print("After droppping NAN rows: ")
    print(f"malicious: {len(df_m)}")
    print(f"benign: {len(df_b)}")

    return df_m, df_b


def run_process(a: pd.DataFrame, b: pd.DataFrame, folder: pathlib.Path) -> pd.DataFrame:
    logging.info("starting feature extraction")
    df_malicious = a.copy().reset_index(drop=True)
    df_benign = b.copy().reset_index(drop=True)

    df_malicious["id"] = np.floor(df_malicious.index.to_numpy() / 10)
    df_benign["id"] = np.floor(df_benign.index.to_numpy() / 10)

    tf1 = pd.DataFrame(
        tsfresh.extract_features(
            df_malicious,
            impute_function=impute,
            column_kind="Is_malicious",
            column_id="id",
            column_sort="Time",
            column_value="Length",
        )
    )
    tf1["class"] = 1

    tf2 = pd.DataFrame(
        tsfresh.extract_features(
            df_benign,
            impute_function=impute,
            column_kind="Is_malicious",
            column_id="id",
            column_sort="Time",
            column_value="Length",
        )
    )
    tf2["class"] = 0
    tf2.columns = tf1.columns

    features = pd.concat([tf1, tf2], ignore_index=True)
    _save(features, folder / "features.csv")

    features2 = features.copy().reset_index(drop=True)
    y = pd.Series(data=features2["class"], index=features2.index)

    relevance_table = calculate_relevance_table(features2, y)
    relevance_table = relevance_table[relevance_table.relevant]
    relevance_table.sort_values("p_value", inplace=True)
    _save(relevance_table, folder / "relevance_table.csv")

    best_features = relevance_table[relevance_table["p_value"] <= 0.05]
    feature_names = best_features["feature"].tolist()

    df_ML = pd.DataFrame(features[feature_names].copy())
    df_ML["class"] = features["class"].values
    df_ML = df_ML.round(6)
    _save(df_ML, folder / "df_ml.csv")

    logging.info("finished feature extraction and selection")
    return df_ML


def ML_Process(df_ML: pd.DataFrame) -> pd.DataFrame:
    print("let the ml starts")
    X = df_ML.drop("class", axis=1).to_numpy()
    y = df_ML["class"].to_numpy()

    # original notebook used LabelEncoder per column
    for i in range(X.shape[1]):
        le = LabelEncoder()
        X[:, i] = le.fit_transform(X[:, i])

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.25, random_state=8675309)

    models = [
        ("LogReg", LogisticRegression()),
        ("KNN", KNeighborsClassifier()),
        ("SVM", SVC()),
        ("GNB", GaussianNB()),
    ]

    scoring = ["accuracy", "precision_weighted", "recall_weighted", "f1_weighted", "roc_auc"]
    target_names = ["malignant", "benign"]

    dfs: List[pd.DataFrame] = []
    for name, model in models:
        kfold = model_selection.KFold(n_splits=5, shuffle=True, random_state=90210)
        cv_results = model_selection.cross_validate(model, X_train, y_train, cv=kfold, scoring=scoring)

        clf = model.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        print(name)
        print(classification_report(y_test, y_pred, target_names=target_names))

        this_df = pd.DataFrame(cv_results)
        this_df["model"] = name
        dfs.append(this_df)

    final = pd.concat(dfs, ignore_index=True)
    print(final)
    return final


def run_dataset_stage() -> None:
    dataset_map = load_dataset()
    for s in SCENARIOS:
        folder = _scenario_folder(s)
        df_m, df_b = _prepare(s, dataset_map)
        _save(df_m, folder / "malicious.csv")
        _save(df_b, folder / "benign.csv")
        run_process(df_m, df_b, folder)


def run_ml_stage() -> None:
    for s in SCENARIOS:
        folder = _scenario_folder(s)
        df_ml = folder / "df_ml.csv"
        results = folder / "results.csv"
        if not df_ml.exists():
            raise FileNotFoundError(f"{df_ml} not found; run dataset stage first")
        if results.exists():
            logging.info("Skipping existing results: %s", results.name)
            continue
        df = pd.read_csv(df_ml)
        res = ML_Process(df)
        _save(res, results)


def main() -> None:
    run_dataset_stage()
    run_ml_stage()


if __name__ == "__main__":
    configure_logging(__file__)
    main()
