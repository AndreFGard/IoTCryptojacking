from __future__ import annotations
import pandas as pd
from paper.non_default_params import experiments
from paper.non_default_params.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[32], d[33], d[34], d[35]]
    b: list[pd.DataFrame] = [d[8], d[9], d[11], d[10], d[12], d[13], d[15], d[16], d[17], d[18], d[19], d[20], d[21], d[22], d[23], d[24], d[25], d[30], d[27], d[29]]
    run_dataset("all_combined_s0", m, b, folder, template)


if __name__ == "__main__":
    main()
