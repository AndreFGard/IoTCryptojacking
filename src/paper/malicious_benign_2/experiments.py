from __future__ import annotations
import pathlib
import logging
from timeit import default_timer as timer
from typing import Dict, List, Tuple, cast

import joblib
import numpy as np
import pandas as pd
import tsfresh
from sklearn import model_selection
from sklearn.base import BaseEstimator
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.svm import SVC
from tsfresh.feature_selection.relevance import calculate_relevance_table
from tsfresh.utilities.dataframe_functions import impute

from paper.malicious_benign_2.dataset import get_dataset_dict, load_dataset


def run_dataset(
    name: str,
    m_list: list[pd.DataFrame],
    b_list: list[pd.DataFrame],
    folder: pathlib.Path,
    template: pd.DataFrame,
    oversample: bool = False,
) -> None:
    df_m, df_b = pd.concat(m_list), pd.concat(b_list)
    if oversample:
        df_m = df_m.sample(len(df_b), replace=True)

    print(f"\n--- {name} ---")
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
        raise FileNotFoundError(f"Dataset file {df_ml_path} not found. Run dataset generation first.")

    results_path = folder / f"{name}_results.csv"
    if results_path.exists():
        logging.info(f"Artifact {results_path.name} exists. Skipping ML_Process...")
        print(f"Artifact {results_path.name} exists. Skipping ML_Process...")
    else:
        df_ml = pd.read_csv(df_ml_path)
        logging.info(f"Running ML_Process for {name}...")
        results, models, encoder = ML_Process(df_ml)
        results.to_csv(results_path, index=False)
        for model_name, model in models.items():
            joblib.dump(model, folder / f"{name}_{model_name}_model.joblib")
        joblib.dump(encoder, folder / f"{name}_encoder.joblib")

    elapsed = timer() - start
    logging.info(f"Finished ML process for {name} successfully in {elapsed:.2f}s")
    print(f"ML process took {elapsed:.2f}s")


def setup_experiment() -> tuple[dict[int, pd.DataFrame], pathlib.Path, pd.DataFrame]:
    folder = pathlib.Path("./data/malicious_benign_2")
    folder.mkdir(parents=True, exist_ok=True)
    template = pd.DataFrame()
    return get_dataset_dict(), folder, template


def ML_Process(
    df_ml: pd.DataFrame, n_jobs: int = -1
) -> Tuple[pd.DataFrame, Dict[str, BaseEstimator], OrdinalEncoder]:
    logging.info("Starting ML process...")
    X = df_ml.drop("class", axis=1).to_numpy().copy()
    y = df_ml["class"].to_numpy().copy()

    X_str = X.astype(str)
    encoder = OrdinalEncoder()
    X = encoder.fit_transform(X_str)

    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=8675309
    )
    y_train = y_train.ravel()

    models: List[Tuple[str, BaseEstimator]] = [("SVM", SVC())]
    scoring = [
        "accuracy",
        "precision_weighted",
        "recall_weighted",
        "f1_weighted",
        "roc_auc",
    ]
    target_names = ["malignant", "benign"]

    dfs: List[pd.DataFrame] = []
    trained_models: Dict[str, BaseEstimator] = {}
    for name, model in models:
        kfold = model_selection.KFold(n_splits=5, shuffle=True, random_state=90210)
        cv_results = cast(
            Dict[str, np.ndarray],
            model_selection.cross_validate(
                model, x_train, y_train, cv=kfold, scoring=scoring, n_jobs=n_jobs
            ),
        )
        clf = model.fit(x_train, y_train)
        trained_models[name] = clf
        y_pred = clf.predict(x_test)

        report = classification_report(y_test, y_pred, target_names=target_names)
        print(f"\nModel: {name}")
        print(report)
        logging.info(f"Classification report for {name}:\n{report}")

        this_df = pd.DataFrame(cv_results)
        this_df["model"] = name
        dfs.append(this_df)

    final = pd.DataFrame(pd.concat(dfs, ignore_index=True))
    return final, trained_models, encoder


def run_process(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    logging.info("Starting feature extraction")
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

    features = pd.DataFrame(pd.concat([tf1, tf2])).reset_index(drop=True)
    y = features["class"]

    logging.info("Starting feature selection")
    relevance_table = cast(pd.DataFrame, calculate_relevance_table(features, y))
    relevant = relevance_table[relevance_table["relevant"]].sort_values(by="p_value")
    best_features = relevant[relevant["p_value"] <= 0.05]

    feature_names = best_features["feature"].tolist()
    df_ml = pd.DataFrame(features[feature_names].copy())
    df_ml["class"] = features["class"].values
    df_ml = df_ml.round(6)

    logging.info("Finished feature extraction and selection")
    return df_ml


def configure_logging(filename: str) -> None:
    log_dir = pathlib.Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
