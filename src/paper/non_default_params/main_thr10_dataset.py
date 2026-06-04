from __future__ import annotations
import pandas as pd
from paper.non_default_params import experiments
from paper.non_default_params.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[33]]
    b: list[pd.DataFrame] = [d[8], d[10]]
    run_dataset("thr_10_s2", m, b, folder, template)


if __name__ == "__main__":
    main()
