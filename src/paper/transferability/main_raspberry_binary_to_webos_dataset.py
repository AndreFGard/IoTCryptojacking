from __future__ import annotations
import pandas as pd
from paper.transferability import experiments
from paper.transferability.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder = setup_experiment()

    # Note: the original notebook uses the same benign data for both train
    # and test in this experiment (df14-17 for both splits).
    b = [d[14], d[15], d[16], d[17]]
    run_dataset(
        "raspberry_binary_to_webos",
        m_train=[d[4]],
        b_train=b,
        m_test=[d[1]],
        b_test=b,
        folder=folder,
    )


if __name__ == "__main__":
    main()
