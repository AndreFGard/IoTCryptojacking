from __future__ import annotations
import pandas as pd
from paper.malicious_benign_2 import experiments
from paper.malicious_benign_2.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[3], d[5], d[6], d[7], d[32], d[33], d[34], d[35]]
    b: list[pd.DataFrame] = [d[10], d[20], d[21]]
    run_dataset("inbrowser_s3", m, b, folder, template)


if __name__ == "__main__":
    main()
