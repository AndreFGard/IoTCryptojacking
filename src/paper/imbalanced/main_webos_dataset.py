from __future__ import annotations
from paper import experiments
import pandas as pd

from paper.experiments import run_dataset, setup_experiment

def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[1]]
    b: list[pd.DataFrame] = [d[23]]
    run_dataset("webos", m, b, folder, template)

if __name__ == "__main__":
    main()
