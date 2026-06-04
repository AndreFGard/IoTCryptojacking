from __future__ import annotations
import pandas as pd
from paper.non_default_params import experiments
from paper.non_default_params.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[2], d[7], d[32]]
    b: list[pd.DataFrame] = [d[10], d[11], d[13], d[15], d[16], d[17], d[18], d[19], d[21], d[22], d[23], d[26], d[30], d[28]]
    run_dataset("server_s1", m, b, folder, template)


if __name__ == "__main__":
    main()
