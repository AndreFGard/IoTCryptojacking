from __future__ import annotations
import pandas as pd
from paper.non_default_params import experiments
from paper.non_default_params.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[5], d[35]]
    b: list[pd.DataFrame] = [d[14], d[16], d[18], d[19], d[20]]
    run_dataset("partially_compromised_s5", m, b, folder, template)


if __name__ == "__main__":
    main()
