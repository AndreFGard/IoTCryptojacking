from __future__ import annotations
import pathlib
from timeit import default_timer as timer
import logging
import joblib

import pandas as pd

from iotcryptojacking.dataset import load_dataset
from iotcryptojacking.utils import run_process, ML_Process


def run_block(
    name: str,
    m_list: list[pd.DataFrame],
    b_list: list[pd.DataFrame],
    folder: pathlib.Path,
    template: pd.DataFrame,
    oversample: bool = False,
) -> None:
    """Concatenate, process, and save results for an experiment block."""
    df_m, df_b = pd.concat(m_list), pd.concat(b_list)
    if oversample:
        df_m = df_m.sample(len(df_b), replace=True)

    print(f"\n--- {name} ---")
    print(f"malicious: {len(df_m)}, benign: {len(df_b)}")
    logging.info(f"--- Starting experiment block: {name} ---")
    logging.info(f"Initial row counts - Malicious: {len(df_m)}, Benign: {len(df_b)}")
    
    m_nans = df_m.isna().any(axis=1).sum()
    b_nans = df_b.isna().any(axis=1).sum()
    print(f"{m_nans} NAN in malicious!")
    print(f"{b_nans} NAN in benign!")
    if m_nans > 0:
        logging.warning(f"Found {m_nans} rows with NaN in malicious dataset (will be dropped)")
    if b_nans > 0:
        logging.warning(f"Found {b_nans} rows with NaN in benign dataset (will be dropped)")

    df_m, df_b = df_m.dropna(), df_b.dropna()

    start = timer()
    df_ml_path = folder / f"{name}_df_ml.csv"
    if df_ml_path.exists():
        logging.info(f"Artifact {df_ml_path.name} exists. Loading df_ml...")
        print(f"Artifact {df_ml_path.name} exists. Loading df_ml...")
        df_ml = pd.read_csv(df_ml_path)
    else:
        logging.info(f"Running feature extraction for {name}...")
        df_ml = run_process(df_m, df_b)
        df_ml.to_csv(df_ml_path, index=False)
    
    results_path = folder / f"{name}_results.csv"
    if results_path.exists():
        logging.info(f"Artifact {results_path.name} exists. Skipping ML_Process...")
        print(f"Artifact {results_path.name} exists. Skipping ML_Process...")
    else:
        logging.info("starting ML process")
        results, models, encoder = ML_Process(df_ml)
        results.to_csv(results_path, index=False)
        
        for model_name, model in models.items():
            joblib.dump(model, folder / f"{name}_{model_name}_model.joblib")
        joblib.dump(encoder, folder / f"{name}_encoder.joblib")

    elapsed = timer() - start
    logging.info(f"Finished {name} successfully in {elapsed:.2f}s")
    print(f"took {elapsed:.2f}s")


def get_dataset_dict() -> dict[int, pd.DataFrame]:
    keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 32, 33, 34, 35]
    return {k: v for k, v in zip(keys, load_dataset())}


def setup_experiment() -> tuple[dict[int, pd.DataFrame], pathlib.Path, pd.DataFrame]:
    folder = pathlib.Path("./data/imbalanced_dataset_experiments")
    folder.mkdir(parents=True, exist_ok=True)
    template = pd.DataFrame()
    return get_dataset_dict(), folder, template
