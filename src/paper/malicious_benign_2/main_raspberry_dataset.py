from __future__ import annotations
import pandas as pd
from paper.malicious_benign_2 import experiments
from paper.malicious_benign_2.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[3], d[4], d[5], d[6], d[33], d[34]]
    b: list[pd.DataFrame] = [d[16], d[19]]
    run_dataset("raspberry_s1", m, b, folder, template)


if __name__ == "__main__":
    main()
