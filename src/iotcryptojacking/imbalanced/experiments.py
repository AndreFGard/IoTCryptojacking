from __future__ import annotations
import pathlib
from timeit import default_timer as timer
import logging

import pandas as pd

from iotcryptojacking.dataset import load_dataset
from iotcryptojacking.utils import run_process


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
    print(f"{df_m.isna().any(axis=1).sum()} NAN in malicious!")
    print(f"{df_b.isna().any(axis=1).sum()} NAN in benign!")

    df_m, df_b = df_m.dropna(), df_b.dropna()

    start = timer()
    df_ml, results = run_process(df_m, df_b, template)
    df_ml.to_csv(folder / f"{name}_df_ml.csv", index=False)
    results.to_csv(folder / f"{name}_results.csv", index=False)

    logging.info(f"Finished {name}")
    print(f"took {timer() - start:.2f}s")


def get_dataset_dict() -> dict[int, pd.DataFrame]:
    keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 32, 33, 34, 35]
    return {k: v for k, v in zip(keys, load_dataset())}


def setup_experiment() -> tuple[dict[int, pd.DataFrame], pathlib.Path, pd.DataFrame]:
    folder = pathlib.Path("./data/imbalanced_dataset_experiments")
    folder.mkdir(parents=True, exist_ok=True)
    template = pd.DataFrame()
    return get_dataset_dict(), folder, template
