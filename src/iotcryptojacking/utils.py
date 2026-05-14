import datetime
import logging
import pathlib
from typing import Dict, List, Tuple, cast

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


def ML_Process(
    df_ml: pd.DataFrame, n_jobs: int = -1
) -> Tuple[pd.DataFrame, Dict[str, BaseEstimator], OrdinalEncoder]:
    """Train and evaluate ML models using extracted features.

    Args:
        df_ml: Feature matrix containing a 'class' target column.
        n_jobs: Number of CPUs to use for cross-validation.

    Returns:
        Tuple containing:
        - Cross-validation metrics for the evaluated models.
        - Dictionary of trained models.
        - Fitted OrdinalEncoder.
    """
    print("Starting ML process...")
    logging.info("Starting ML process...")

    X: np.ndarray = df_ml.drop("class", axis=1).to_numpy().copy()
    y: np.ndarray = df_ml["class"].to_numpy().copy()

    # Note: The original paper implemented this step using a LabelEncoder in a loop over
    # columns. We use OrdinalEncoder instead because it produces the exact same transformed
    # 2D matrix (behaviorally identical), but preserves the learned mappings for ALL columns.
    # This allows us to save the encoder object and properly use it for future inference.
    # We cast to string before encoding to avoid floating-point precision mismatches 
    # when loading the features back from CSV for evaluation.
    X_str = X.astype(str)
    encoder = OrdinalEncoder()
    X = encoder.fit_transform(X_str)

    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=8675309
    )
    y_train = y_train.ravel()

    models: List[Tuple[str, BaseEstimator]] = [("SVM", SVC())]
    scoring: List[str] = [
        "accuracy",
        "precision_weighted",
        "recall_weighted",
        "f1_weighted",
        "roc_auc",
    ]
    target_names: List[str] = ["malignant", "benign"]

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

        logging.info("training model")
        clf = model.fit(x_train, y_train)  # type: ignore
        trained_models[name] = clf
        y_pred: np.ndarray = clf.predict(x_test)  # type: ignore

        print(f"\nModel: {name}")
        report = classification_report(y_test, y_pred, target_names=target_names)
        print(report)
        logging.info(f"Evaluating Model: {name}")
        logging.info(f"Classification report for {name}:\n{report}")

        this_df = pd.DataFrame(cv_results)
        this_df["model"] = name
        dfs.append(this_df)

    final = pd.DataFrame(pd.concat(dfs, ignore_index=True))
    print(final)
    logging.info(f"Final cross-validation results:\n{final}")
    return final, trained_models, encoder


def run_process(
    a: pd.DataFrame, b: pd.DataFrame, n_jobs: int = -1
) -> pd.DataFrame:
    """Run feature extraction, selection, and evaluation pipeline.

    Args:
        a: Malicious traffic dataset.
        b: Benign traffic dataset.
        n_jobs: Number of CPUs to use for feature extraction.

    Returns:
        Selected features DataFrame.
    """
    logging.info("starting feature extraction")
    df_malicious = a.copy().reset_index(drop=True)
    df_benign = b.copy().reset_index(drop=True)

    df_malicious["id"] = np.floor(df_malicious.index.to_numpy() / 10)
    df_benign["id"] = np.floor(df_benign.index.to_numpy() / 10)

    # Feature extraction
    tf1 = pd.DataFrame(
        tsfresh.extract_features(
            df_malicious,
            impute_function=impute,
            column_kind="Is_malicious",
            column_id="id",
            column_sort="Time",
            column_value="Length",
            n_jobs=n_jobs,
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
            n_jobs=n_jobs,
        )
    )
    tf2["class"] = 0
    tf2.columns = tf1.columns

    features = pd.DataFrame(pd.concat([tf1, tf2])).reset_index(drop=True)
    y = features["class"]

    # Feature selection
    logging.info("starting feature selection")
    relevance_table = cast(pd.DataFrame, calculate_relevance_table(features, y))
    relevance_table = relevance_table[relevance_table["relevant"]]
    relevance_table = cast(pd.DataFrame, relevance_table).sort_values(by="p_value")

    best_features = relevance_table[relevance_table["p_value"] <= 0.05]

    feature_names: List[str] = best_features["feature"].tolist()
    df_ml = pd.DataFrame(features[feature_names].copy())
    df_ml = df_ml.round(6)
    df_ml["class"] = features["class"].values

    logging.info(f"finished feature extraction and selection, run_process over")
    return df_ml

def configure_logging(filename):
    log_dir = pathlib.Path("logs/imbalanced")
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )