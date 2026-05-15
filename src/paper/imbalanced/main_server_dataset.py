from __future__ import annotations
from paper import experiments
import pandas as pd

from paper.experiments import run_dataset, setup_experiment

def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[2], d[7], d[32]]
    b: list[pd.DataFrame] = [d[19], d[20], d[21], d[22]]
    run_dataset("server", m, b, folder, template)

if __name__ == "__main__":
    main()
