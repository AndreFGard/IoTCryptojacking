from __future__ import annotations
import pathlib
import logging
import warnings
from timeit import default_timer as timer
from typing import Dict, List, Tuple, cast
 
import joblib
import numpy as np
import pandas as pd
import tsfresh
from sklearn import model_selection
from sklearn.base import BaseEstimator
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from tsfresh.feature_selection.relevance import calculate_relevance_table
from tsfresh.utilities.dataframe_functions import impute
 
from paper.transferability.dataset import get_dataset_dict
 
 
def run_dataset(
    name: str,
    m_train: list[pd.DataFrame],
    b_train: list[pd.DataFrame],
    m_test: list[pd.DataFrame],
    b_test: list[pd.DataFrame],
    folder: pathlib.Path,
) -> None:
    """Extract and save train/test feature datasets for a transferability experiment.
 
    Args:
        name: Experiment identifier (used as filename prefix).
        m_train: Malicious DataFrames for training.
        b_train: Benign DataFrames for training.
        m_test: Malicious DataFrames for testing.
        b_test: Benign DataFrames for testing (may be same objects as b_train).
        folder: Output directory.
    """
    df_m_train = pd.concat(m_train)
    df_b_train = pd.concat(b_train)
    df_m_test = pd.concat(m_test)
    df_b_test = pd.concat(b_test)
 
    print(f"\n--- {name} ---")
    logging.info(f"--- Starting dataset generation: {name} ---")
    print(f"malicious train: {len(df_m_train)}, benign train: {len(df_b_train)}")
    print(f"malicious test:  {len(df_m_test)},  benign test:  {len(df_b_test)}")
    logging.info(
        f"Train - Malicious: {len(df_m_train)}, Benign: {len(df_b_train)} | "
        f"Test - Malicious: {len(df_m_test)}, Benign: {len(df_b_test)}"
    )
 
    for label, df in [
        ("malicious train", df_m_train),
        ("benign train", df_b_train),
        ("malicious test", df_m_test),
        ("benign test", df_b_test),
    ]:
        n_nans = int(df.isna().any(axis=1).sum())
        print(f"{n_nans} NAN in {label}!")
        if n_nans > 0:
            logging.warning(f"Found {n_nans} rows with NaN in {label} (will be dropped)")
 
    df_m_train = df_m_train.dropna()
    df_b_train = df_b_train.dropna()
    df_m_test = df_m_test.dropna()
    df_b_test = df_b_test.dropna()
 
    train_path = folder / f"{name}_train_df_ml.csv"
    test_path = folder / f"{name}_test_df_ml.csv"
 
    if train_path.exists() and test_path.exists():
        logging.info(f"Artifacts for {name} exist. Skipping dataset generation...")
        print(f"Artifacts for {name} exist. Skipping dataset generation...")
        return
 
    start = timer()
    logging.info(f"Running feature extraction for {name}...")
    df_train_ml, df_test_ml = run_process(df_m_train, df_b_train, df_m_test, df_b_test)
    df_train_ml.to_csv(train_path, index=False)
    df_test_ml.to_csv(test_path, index=False)
 
    elapsed = timer() - start
    logging.info(f"Finished dataset generation for {name} in {elapsed:.2f}s")
    print(f"Dataset generation took {elapsed:.2f}s")
 
 
def run_ml(name: str, folder: pathlib.Path) -> None:
    """Run ML process on saved train/test datasets.
 
    Saves two artefacts:
    - ``{name}_results.csv``      — 5-fold cross-validation metrics on the training set
    - ``{name}_test_report.csv``  — classification_report metrics on the held-out test
                                    set (the values comparable to paper Table XV)
 
    Args:
        name: Experiment identifier matching the saved CSV filenames.
        folder: Directory containing the CSVs.
    """
    print(f"\n--- ML Process: {name} ---")
    logging.info(f"--- Starting ML process: {name} ---")
 
    start = timer()
 
    train_path = folder / f"{name}_train_df_ml.csv"
    test_path = folder / f"{name}_test_df_ml.csv"
 
    for path in (train_path, test_path):
        if not path.exists():
            raise FileNotFoundError(
                f"Dataset file {path} not found. Run dataset generation first."
            )
 
    results_path = folder / f"{name}_results.csv"
    test_report_path = folder / f"{name}_test_report.csv"
 
    if results_path.exists() and test_report_path.exists():
        logging.info(f"Artifacts for {name} exist. Skipping ML_Process...")
        print(f"Artifacts for {name} exist. Skipping ML_Process...")
    else:
        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)
        logging.info(f"Running ML_Process for {name}...")
        results, models, encoder, test_report = ML_Process(df_train, df_test)
        results.to_csv(results_path, index=False)
        test_report.to_csv(test_report_path, index=False)
        for model_name, model in models.items():
            joblib.dump(model, folder / f"{name}_{model_name}_model.joblib")
        joblib.dump(encoder, folder / f"{name}_encoder.joblib")
 
    elapsed = timer() - start
    logging.info(f"Finished ML process for {name} in {elapsed:.2f}s")
    print(f"ML process took {elapsed:.2f}s")
 
 
def setup_experiment() -> tuple[dict[int, pd.DataFrame], pathlib.Path]:
    """Load dataset and set up output folder.
 
    Returns:
        Tuple of (dataset dict keyed by integer index, output folder path).
    """
    folder = pathlib.Path("./data/transferability")
    folder.mkdir(parents=True, exist_ok=True)
    return get_dataset_dict(), folder
 
 
def run_process(
    m_train: pd.DataFrame,
    b_train: pd.DataFrame,
    m_test: pd.DataFrame,
    b_test: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Extract tsfresh features and select relevant ones from train, apply to test.
 
    Feature selection is performed on the training set only. The selected feature
    names are then used to slice the test feature matrix, ensuring no information
    from the test set leaks into the feature selection step.
 
    Args:
        m_train: Malicious traffic for training.
        b_train: Benign traffic for training.
        m_test: Malicious traffic for testing.
        b_test: Benign traffic for testing.
 
    Returns:
        Tuple of (train_df_ml, test_df_ml) with selected features and class column.
    """
    logging.info("Starting feature extraction")
 
    df_m_train = m_train.copy().reset_index(drop=True)
    df_b_train = b_train.copy().reset_index(drop=True)
    df_m_test = m_test.copy().reset_index(drop=True)
    df_b_test = b_test.copy().reset_index(drop=True)
 
    df_m_train["id"] = np.floor(df_m_train.index.to_numpy() / 10)
    df_b_train["id"] = np.floor(df_b_train.index.to_numpy() / 10)
    df_m_test["id"] = np.floor(df_m_test.index.to_numpy() / 10)
    df_b_test["id"] = np.floor(df_b_test.index.to_numpy() / 10)
 
    extract_kwargs = dict(
        impute_function=impute,
        column_kind="Is_malicious",
        column_id="id",
        column_sort="Time",
        column_value="Length",
    )
 
    tf_m_train = pd.DataFrame(tsfresh.extract_features(df_m_train, **extract_kwargs))
    tf_m_train["class"] = 1
 
    tf_b_train = pd.DataFrame(tsfresh.extract_features(df_b_train, **extract_kwargs))
    tf_b_train["class"] = 0
    tf_b_train.columns = tf_m_train.columns
 
    tf_m_test = pd.DataFrame(tsfresh.extract_features(df_m_test, **extract_kwargs))
    tf_m_test["class"] = 1
 
    tf_b_test = pd.DataFrame(tsfresh.extract_features(df_b_test, **extract_kwargs))
    tf_b_test["class"] = 0
    tf_b_test.columns = tf_m_test.columns
 
    features_train = pd.DataFrame(pd.concat([tf_m_train, tf_b_train])).reset_index(drop=True)
    features_test = pd.DataFrame(pd.concat([tf_m_test, tf_b_test])).reset_index(drop=True)
 
    # Feature selection on train only — no information from test set used here.
    logging.info("Starting feature selection (train set only)")
    y_train = features_train["class"]
    relevance_table = cast(pd.DataFrame, calculate_relevance_table(features_train, y_train))
    relevant = relevance_table[relevance_table["relevant"]].sort_values(by="p_value")
    best_features = relevant[relevant["p_value"] <= 0.05]
    feature_names: list[str] = best_features["feature"].tolist()
 
    df_train_ml = pd.DataFrame(features_train[feature_names].copy())
    df_train_ml = df_train_ml.round(6)
    df_train_ml["class"] = features_train["class"].values
 
    # Apply the same feature names selected from train to the test set.
    # Test columns that don't appear in feature_names are discarded;
    # any feature_name missing from test columns is filled with NaN.
    df_test_ml = pd.DataFrame(features_test.reindex(columns=feature_names).copy())
    df_test_ml = df_test_ml.round(6)
    df_test_ml["class"] = features_test["class"].values
 
    logging.info("Finished feature extraction and selection")
    return df_train_ml, df_test_ml
 
 
def ML_Process(
    df_train: pd.DataFrame,
    df_test: pd.DataFrame,
    n_jobs: int = -1,
) -> Tuple[pd.DataFrame, Dict[str, BaseEstimator], LabelEncoder, pd.DataFrame]:
    """Train on df_train and evaluate transferability on df_test.
 
    Encoding strategy — matches the original notebook (Cell 5):
        LabelEncoder.fit_transform() is called independently on every column of
        X_train and again independently on every column of X_test.  Each split
        therefore gets its own compact ordinal mapping with no unknown-value
        problem, which is exactly what the notebook does.  This differs from
        fitting on train and transforming test (OrdinalEncoder approach) and is
        necessary to reproduce the paper's Table XV numbers.
 
    Saved artefacts (via run_ml):
        ``_results.csv``     — 5-fold CV metrics on the training set
        ``_test_report.csv`` — per-class + weighted-avg metrics on the test set
                               (these are the values reported in Table XV)
 
    Args:
        df_train: Feature matrix with 'class' column for training.
        df_test:  Feature matrix with 'class' column for evaluation.
        n_jobs:   Number of CPUs for cross-validation (-1 = all).
 
    Returns:
        Tuple of (cv_results_df, trained_models_dict, fitted_encoder, test_report_df).
    """
    logging.info("Starting ML process...")
 
    X_train = df_train.drop("class", axis=1).to_numpy().copy()
    y_train = df_train["class"].to_numpy().copy()
 
    X_test = df_test.drop("class", axis=1).to_numpy().copy()
    y_test = df_test["class"].to_numpy().copy()
 
    # ------------------------------------------------------------------
    # Encoding: independent LabelEncoder per column — matches notebook.
    # Replace any residual NaNs with 0 before encoding (edge-case guard).
    # ------------------------------------------------------------------
    X_train = np.nan_to_num(X_train, nan=0.0)
    X_test = np.nan_to_num(X_test, nan=0.0)
 
    Le = LabelEncoder()
    for i in range(X_train.shape[1]):
        X_train[:, i] = Le.fit_transform(X_train[:, i])
 
    for i in range(X_test.shape[1]):
        X_test[:, i] = Le.fit_transform(X_test[:, i])
 
    encoder = Le  # kept for API compatibility (saved via joblib)
    # ------------------------------------------------------------------
 
    y_train = y_train.ravel()
 
    models: List[Tuple[str, BaseEstimator]] = [
        ("LogReg", LogisticRegression()),
        ("KNN", KNeighborsClassifier()),
        ("SVM", SVC()),
        ("GNB", GaussianNB()),
    ]
    scoring = [
        "accuracy",
        "precision_weighted",
        "recall_weighted",
        "f1_weighted",
        "roc_auc",
    ]
    target_names = ["malignant", "benign"]
 
    cv_dfs: List[pd.DataFrame] = []
    test_report_dfs: List[pd.DataFrame] = []
    trained_models: Dict[str, BaseEstimator] = {}
 
    for name, model in models:
        kfold = model_selection.KFold(n_splits=5, shuffle=True, random_state=90210)
 
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            cv_results = cast(
                Dict[str, np.ndarray],
                model_selection.cross_validate(
                    model, X_train, y_train, cv=kfold, scoring=scoring, n_jobs=n_jobs
                ),
            )
        conv_warns = [w for w in caught if issubclass(w.category, ConvergenceWarning)]
        if conv_warns:
            logging.warning(
                f"Model {name}: ConvergenceWarning em {len(conv_warns)} fold(s) "
                f"durante cross-validation. Considere aumentar max_iter ou normalizar os dados."
            )
 
        logging.info(f"Training model {name}")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            clf = model.fit(X_train, y_train)
        conv_warns = [w for w in caught if issubclass(w.category, ConvergenceWarning)]
        if conv_warns:
            logging.warning(f"Model {name}: ConvergenceWarning no treino final.")
 
        trained_models[name] = clf
        y_pred = clf.predict(X_test)
 
        # ---- Classification report on the held-out TEST set ----------------
        # These are the metrics shown in paper Table XV (weighted avg for SVM).
        report_str = classification_report(y_test, y_pred, target_names=target_names)
        report_dict = classification_report(
            y_test, y_pred, target_names=target_names, output_dict=True
        )
        print(f"\nModel: {name}")
        print(report_str)
        logging.info(f"Classification report for {name} (test set):\n{report_str}")
 
        report_df = pd.DataFrame(report_dict).T.reset_index()
        report_df.rename(columns={"index": "class"}, inplace=True)
        report_df["model"] = name
        test_report_dfs.append(report_df)
        # --------------------------------------------------------------------
 
        this_df = pd.DataFrame(cv_results)
        this_df["model"] = name
        cv_dfs.append(this_df)
 
    final_cv = pd.DataFrame(pd.concat(cv_dfs, ignore_index=True))
    final_test_report = pd.DataFrame(pd.concat(test_report_dfs, ignore_index=True))
 
    print(final_cv)
    logging.info(f"Final cross-validation results:\n{final_cv}")
    return final_cv, trained_models, encoder, final_test_report
 
 
def configure_logging(filename: str) -> None:
    log_dir = pathlib.Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

