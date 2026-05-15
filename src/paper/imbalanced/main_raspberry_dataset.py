from __future__ import annotations
from paper import experiments
import pandas as pd

from paper.experiments import run_dataset, setup_experiment

def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[3], d[4], d[5], d[6], d[33], d[34]]
    b: list[pd.DataFrame] = [d[13], d[14], d[15], d[16], d[17]]
    run_dataset("raspberry", m, b, folder, template)

if __name__ == "__main__":
    main()
