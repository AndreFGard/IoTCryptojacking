from __future__ import annotations
import pandas as pd
from paper.malicious_benign_2 import experiments
from paper.malicious_benign_2.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[1], d[2], d[4]]
    b: list[pd.DataFrame] = [d[10], d[11], d[12], d[18], d[20], d[21], d[22], d[23]]
    run_dataset("binary_s3", m, b, folder, template)


if __name__ == "__main__":
    main()
