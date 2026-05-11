from __future__ import annotations
import logging
import pathlib
from timeit import default_timer as timer
import pandas as pd

from iotcryptojacking.dataset import load_dataset
from iotcryptojacking.utils import run_process

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)


def _run_block(
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


def run_timely_balanced(d: dict[int, pd.DataFrame], folder: pathlib.Path, template: pd.DataFrame) -> None:
    m: list[pd.DataFrame] = [
        d[1].iloc[:2832], d[2].iloc[:4680], d[3].iloc[:271], d[4].iloc[:48],
        d[5].iloc[:69], d[6].iloc[:72], d[7].iloc[:170], d[32].iloc[:175],
        d[33].iloc[:76], d[34].iloc[:48], d[35].iloc[:1300]
    ]
    b: list[pd.DataFrame] = [
        d[8].iloc[:422784], d[9].iloc[:44376], d[10].iloc[:14784], d[11].iloc[:3576],
        d[12].iloc[:34728], d[13].iloc[:269400], d[14].iloc[:73], d[15].iloc[:24144],
        d[16].iloc[:7320], d[17].iloc[:21240], d[18].iloc[:544416], d[19].iloc[:2664],
        d[20].iloc[:27480], d[21].iloc[:30888], d[22].iloc[:12168], d[23].iloc[:174648]
    ]
    _run_block("timely", m, b, folder, template)


def run_timely_oversampling(d: dict[int, pd.DataFrame], folder: pathlib.Path, template: pd.DataFrame) -> None:
    m: list[pd.DataFrame] = [d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[32], d[33], d[34], d[35]]
    b: list[pd.DataFrame] = [d[8], d[9], d[10], d[11], d[12], d[13], d[14], d[15], d[16], d[17], d[18], d[19], d[20], d[21], d[22], d[23]]
    _run_block("timely_oversampling", m, b, folder, template, oversample=True)


def run_server_experiment(d: dict[int, pd.DataFrame], folder: pathlib.Path, template: pd.DataFrame) -> None:
    _run_block("server", [d[2], d[7], d[32]], [d[19], d[20], d[21], d[22]], folder, template)


def run_laptop_experiment(d: dict[int, pd.DataFrame], folder: pathlib.Path, template: pd.DataFrame) -> None:
    _run_block("laptop", [d[35]], [d[8], d[9], d[10], d[11], d[12]], folder, template)


def run_raspberry_experiment(d: dict[int, pd.DataFrame], folder: pathlib.Path, template: pd.DataFrame) -> None:
    m: list[pd.DataFrame] = [d[3], d[4], d[5], d[6], d[33], d[34]]
    b: list[pd.DataFrame] = [d[13], d[14], d[15], d[16], d[17]]
    _run_block("raspberry", m, b, folder, template)


def run_webos_experiment(d: dict[int, pd.DataFrame], folder: pathlib.Path, template: pd.DataFrame) -> None:
    _run_block("webos", [d[1]], [d[23]], folder, template)


def run_experiments() -> None:
    """Run all imbalanced dataset experiments."""
    folder = pathlib.Path("./data/imbalanced_dataset_experiments")
    folder.mkdir(parents=True, exist_ok=True)
    template = pd.DataFrame()

    keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 32, 33, 34, 35]
    d: dict[int, pd.DataFrame] = {k: v for k, v in zip(keys, load_dataset())}

    run_timely_balanced(d, folder, template)
    run_timely_oversampling(d, folder, template)
    run_server_experiment(d, folder, template)
    run_laptop_experiment(d, folder, template)
    run_raspberry_experiment(d, folder, template)
    run_webos_experiment(d, folder, template)


if __name__ == "__main__":
    run_experiments()

