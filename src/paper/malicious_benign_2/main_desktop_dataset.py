from __future__ import annotations
import pandas as pd
from paper.malicious_benign_2 import experiments
from paper.malicious_benign_2.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[35]]
    b: list[pd.DataFrame] = [d[9], d[10], d[22]]
    run_dataset("desktop_s1", m, b, folder, template)


if __name__ == "__main__":
    main()
