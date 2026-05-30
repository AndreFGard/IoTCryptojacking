from __future__ import annotations
import pandas as pd
from paper.malicious_benign_2 import experiments
from paper.malicious_benign_2.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[5], d[35]]
    b: list[pd.DataFrame] = [d[9], d[11], d[15]]
    run_dataset("partially_compromised_s5", m, b, folder, template)


if __name__ == "__main__":
    main()
