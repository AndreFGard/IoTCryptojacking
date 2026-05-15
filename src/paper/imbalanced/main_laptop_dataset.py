from __future__ import annotations
from paper import experiments

import pandas as pd

from paper.experiments import run_dataset, setup_experiment

def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[35]]
    b: list[pd.DataFrame] = [d[8], d[9], d[10], d[11], d[12]]
    run_dataset("laptop", m, b, folder, template)

if __name__ == "__main__":
    main()
