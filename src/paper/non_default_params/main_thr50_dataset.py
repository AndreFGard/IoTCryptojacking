from __future__ import annotations
import pandas as pd
from paper.non_default_params import experiments
from paper.non_default_params.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[3], d[34]]
    b: list[pd.DataFrame] = [d[29], d[31]]
    run_dataset("thr_50_s2", m, b, folder, template)


if __name__ == "__main__":
    main()
