from __future__ import annotations
import pandas as pd
from paper.non_default_params import experiments
from paper.non_default_params.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[1], d[2], d[4]]
    b: list[pd.DataFrame] = [d[12], d[13], d[15], d[17], d[22], d[23], d[27], d[28], d[29]]
    run_dataset("binary_s3", m, b, folder, template)


if __name__ == "__main__":
    main()
