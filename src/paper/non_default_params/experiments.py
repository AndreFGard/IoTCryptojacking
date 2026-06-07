from __future__ import annotations

import pathlib
import logging
import warnings
from timeit import default_timer as timer
from typing import Dict, List, Protocol, Tuple, cast

import joblib
import numpy as np
import pandas as pd
import tsfresh
from sklearn import model_selection
from sklearn.base import BaseEstimator
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from tsfresh.feature_selection.relevance import calculate_relevance_table
from tsfresh.utilities.dataframe_functions import impute

from paper.non_default_params.dataset import get_dataset_dict


class SklearnClassifier(Protocol):
    def fit(self, X: np.ndarray, y: np.ndarray) -> "SklearnClassifier": ...
    def predict(self, X: np.ndarray) -> np.ndarray: ...


def setup_experiment() -> tuple[dict[int, pd.DataFrame], pathlib.Path, pd.DataFrame]:
    folder = pathlib.Path("./data/non_default_params")
    folder.mkdir(parents=True, exist_ok=True)
    template = pd.DataFrame()
    return get_dataset_dict(), folder, template


def run_dataset(
    name: str,
    m_list: list[pd.DataFrame],
    b_list: list[pd.DataFrame],
    folder: pathlib.Path,
    template: pd.DataFrame,
) -> None:
    df_m, df_b = pd.concat(m_list), pd.concat(b_list)

    print(f"\n--- {name} ---")
    print(f"malicious: {len(df_m)}, benign: {len(df_b)}")
    logging.info(f"--- Starting dataset generation: {name} ---")
    logging.info(f"Initial row counts - Malicious: {len(df_m)}, Benign: {len(df_b)}")

    m_nans = int(df_m.isna().any(axis=1).sum())
    b_nans = int(df_b.isna().any(axis=1).sum())
    print(f"{m_nans} NAN in malicious!")
    print(f"{b_nans} NAN in benign!")
    df_m, df_b = df_m.dropna(), df_b.dropna()

    start = timer()
    df_ml_path = folder / f"{name}_df_ml.csv"
    if df_ml_path.exists():
        logging.info(f"Artifact {df_ml_path.name} exists. Skipping dataset generation...")
        print(f"Artifact {df_ml_path.name} exists. Skipping dataset generation...")
    else:
        logging.info(f"Running feature extraction for {name}...")
        df_ml = run_process(df_m, df_b)
        df_ml.to_csv(df_ml_path, index=False)

    elapsed = timer() - start
    logging.info(f"Finished dataset generation for {name} successfully in {elapsed:.2f}s")
    print(f"Dataset generation took {elapsed:.2f}s")


def run_ml(name: str, folder: pathlib.Path) -> None:
    print(f"\n--- ML Process: {name} ---")
    logging.info(f"--- Starting ML process: {name} ---")

    start = timer()
    df_ml_path = folder / f"{name}_df_ml.csv"
    if not df_ml_path.exists():
        raise FileNotFoundError(
            f"Dataset file {df_ml_path} not found. Run dataset generation first."
        )

    results_path = folder / f"{name}_results.csv"
    if results_path.exists():
        logging.info(f"Artifact {results_path.name} exists. Skipping ML_Process...")
        print(f"Artifact {results_path.name} exists. Skipping ML_Process...")
    else:
        df_ml = pd.read_csv(df_ml_path)
        template = pd.DataFrame()
        logging.info(f"Running ML_Process for {name}...")
        results, models, encoder = ML_Process(df_ml, template)
        results.to_csv(results_path, index=False)
        for model_name, model in models.items():
            joblib.dump(model, folder / f"{name}_{model_name}_model.joblib")
        joblib.dump(encoder, folder / f"{name}_encoder.joblib")

    elapsed = timer() - start
    logging.info(f"Finished ML process for {name} successfully in {elapsed:.2f}s")
    print(f"ML process took {elapsed:.2f}s")


def ML_Process(
    df_ML: pd.DataFrame,
    x: pd.DataFrame,
    n_jobs: int = -1,
) -> Tuple[pd.DataFrame, Dict[str, SklearnClassifier], LabelEncoder]:
    # Preserved from original notebook: template parameter received but not used
    df_results = x.copy()
    logging.info("Starting ML process...")

    X = df_ML.drop("class", axis=1).to_numpy()
    y = df_ML["class"].to_numpy()

    # Preserved from original notebook: LabelEncoder applied column by column
    # Note: only the last column's fitted state is retained in Le
    Le = LabelEncoder()
    for i in range(len(X[0])):
        X[:, i] = Le.fit_transform(X[:, i])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=8675309
    )
    y_train = y_train.ravel()

    # 16 SVM variants: 4 kernels x 2 gamma x 2 C values
    models: List[Tuple[str, SklearnClassifier]] = [
        ("SVM-linear-scale-1", SVC(C=1, kernel="linear", gamma="scale")),
        ("SVM-poly-scale-1",   SVC(C=1, kernel="poly",   gamma="scale")),
        ("SVM-rbf-scale-1",    SVC(C=1, kernel="rbf",    gamma="scale")),
        ("SVM-sigmoid-scale-1",SVC(C=1, kernel="sigmoid",gamma="scale")),
        ("SVM-linear-auto-1",  SVC(C=1, kernel="linear", gamma="auto")),
        ("SVM-poly-auto-1",    SVC(C=1, kernel="poly",   gamma="auto")),
        ("SVM-rbf-auto-1",     SVC(C=1, kernel="rbf",    gamma="auto")),
        ("SVM-sigmoid-auto-1", SVC(C=1, kernel="sigmoid",gamma="auto")),
        ("SVM-linear-scale-2", SVC(C=2, kernel="linear", gamma="scale")),
        ("SVM-poly-scale-2",   SVC(C=2, kernel="poly",   gamma="scale")),
        ("SVM-rbf-scale-2",    SVC(C=2, kernel="rbf",    gamma="scale")),
        ("SVM-sigmoid-scale-2",SVC(C=2, kernel="sigmoid",gamma="scale")),
        ("SVM-linear-auto-2",  SVC(C=2, kernel="linear", gamma="auto")),
        ("SVM-poly-auto-2",    SVC(C=2, kernel="poly",   gamma="auto")),
        ("SVM-rbf-auto-2",     SVC(C=2, kernel="rbf",    gamma="auto")),
        ("SVM-sigmoid-auto-2", SVC(C=2, kernel="sigmoid",gamma="auto")),
    ]
    scoring = [
        "accuracy",
        "precision_weighted",
        "recall_weighted",
        "f1_weighted",
        "roc_auc",
    ]
    target_names = ["malignant", "benign"]

    dfs: List[pd.DataFrame] = []
    trained_models: Dict[str, SklearnClassifier] = {}

    for name, model in models:
        kfold = model_selection.KFold(n_splits=5, shuffle=True, random_state=90210)
        cv_results = cast(
            Dict[str, np.ndarray],
            model_selection.cross_validate(
                cast(BaseEstimator, model),
                X_train, y_train, cv=kfold, scoring=scoring, n_jobs=n_jobs,
            ),
        )

        logging.info(f"training model {name}")
        clf = model.fit(X_train, y_train)
        trained_models[name] = clf

        y_pred = clf.predict(X_test)
        report = classification_report(y_test, y_pred, target_names=target_names)
        print(f"\nModel: {name}")
        print(report)
        logging.info(f"Classification report for {name}:\n{report}")

        this_df = pd.DataFrame(cv_results)
        this_df["model"] = name
        dfs.append(this_df)

    final = pd.DataFrame(pd.concat(dfs, ignore_index=True))
    print(final)
    logging.info(f"Final cross-validation results:\n{final}")
    return final, trained_models, Le


def run_process(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    logging.info("Starting feature extraction")
    df_malicious = a.copy().reset_index(drop=True)
    df_benign    = b.copy().reset_index(drop=True)

    df_malicious["id"] = np.floor(df_malicious.index.to_numpy() / 10)
    df_benign["id"]    = np.floor(df_benign.index.to_numpy() / 10)

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
    # Preserved from original notebook: aligns benign columns to malicious columns
    tf2.columns = tf1.columns

    features = pd.DataFrame(pd.concat([tf1, tf2])).reset_index(drop=True)
    y = pd.Series(data=features["class"], index=features.index)

    logging.info("Starting feature selection")
    relevance_table = cast(pd.DataFrame, calculate_relevance_table(features, y))
    relevance_table = relevance_table[relevance_table.relevant]
    relevance_table.sort_values("p_value", inplace=True)
    best_features = relevance_table[relevance_table["p_value"] <= 0.05]

    # Preserved from original notebook: loop is redundant but behaviour unchanged
    df_ML = pd.DataFrame()
    for pkt in best_features:
        df_ML[best_features.feature] = features[best_features.feature]

    df_ML = df_ML.round(6)
    logging.info("Finished feature extraction and selection")
    return df_ML


def configure_logging(filename: str) -> None:
    log_dir = pathlib.Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
