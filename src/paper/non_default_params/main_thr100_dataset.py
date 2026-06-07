from __future__ import annotations
import pandas as pd
from paper.non_default_params import experiments
from paper.non_default_params.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[1], d[2], d[4], d[5], d[6], d[7], d[35]]
    b: list[pd.DataFrame] = [d[11], d[12], d[13], d[14], d[16], d[17], d[21], d[23], d[26], d[27], d[28], d[29], d[30], d[31]]
    run_dataset("thr_100_s2", m, b, folder, template)


if __name__ == "__main__":
    main()
