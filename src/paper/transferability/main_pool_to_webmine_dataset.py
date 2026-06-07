from __future__ import annotations
import pandas as pd
from paper.transferability import experiments
from paper.transferability.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder = setup_experiment()

    raspberry_benign = pd.concat([d[13], d[14], d[15], d[16], d[17]])
    run_dataset(
        "pool_to_webmine",
        m_train=[d[6]],
        b_train=[raspberry_benign.iloc[:450000]],
        m_test=[d[5]],
        b_test=[raspberry_benign.iloc[450000:]],
        folder=folder,
    )


if __name__ == "__main__":
    main()
