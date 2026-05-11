import logging
from typing import Dict, List, Tuple, cast

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


def ML_Process(df_ml: pd.DataFrame, x: pd.DataFrame) -> pd.DataFrame:
    """Train and evaluate ML models using extracted features.

    Args:
        df_ml: Feature matrix containing a 'class' target column.
        x: Template DataFrame for results.

    Returns:
        Cross-validation metrics for the evaluated models.
    """
    print("Starting ML process...")

    X: np.ndarray = df_ml.drop("class", axis=1).to_numpy()
    y: np.ndarray = df_ml["class"].to_numpy()

    le = LabelEncoder()
    for i in range(X.shape[1]):
        X[:, i] = le.fit_transform(X[:, i])

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
    for name, model in models:
        kfold = model_selection.KFold(n_splits=5, shuffle=True, random_state=90210)
        cv_results = cast(
            Dict[str, np.ndarray],
            model_selection.cross_validate(
                model, x_train, y_train, cv=kfold, scoring=scoring
            ),
        )

        clf = cast(SVC, model).fit(x_train, y_train)
        y_pred: np.ndarray = clf.predict(x_test)

        print(f"\nModel: {name}")
        print(classification_report(y_test, y_pred, target_names=target_names))

        this_df = pd.DataFrame(cv_results)
        this_df["model"] = name
        dfs.append(this_df)

    final = pd.DataFrame(pd.concat(dfs, ignore_index=True))
    print(final)
    return final


def run_process(
    a: pd.DataFrame, b: pd.DataFrame, x: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Run feature extraction, selection, and evaluation pipeline.

    Args:
        a: Malicious traffic dataset.
        b: Benign traffic dataset.
        x: Template DataFrame for results.

    Returns:
        Tuple of (selected features DataFrame, evaluation results).
    """
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

    # Feature selection
    relevance_table = cast(pd.DataFrame, calculate_relevance_table(features, y))
    relevance_table = relevance_table[relevance_table["relevant"]]
    relevance_table = cast(pd.DataFrame, relevance_table).sort_values(by="p_value")

    best_features = relevance_table[relevance_table["p_value"] <= 0.05]

    # Select only relevant features
    feature_names: List[str] = best_features["feature"].tolist()
    df_ml = pd.DataFrame(features[feature_names].copy())
    df_ml["class"] = features["class"].values

    final = ML_Process(df_ml, x)

    return df_ml, final

