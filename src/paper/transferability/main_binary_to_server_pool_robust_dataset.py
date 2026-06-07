from __future__ import annotations
import pandas as pd
from paper.transferability import experiments
from paper.transferability.experiments import run_dataset, setup_experiment


def main() -> None:
    experiments.configure_logging(__file__)
    d, folder = setup_experiment()

    # NOTE: The notebook cell 13 comment reads "Train: in-browser (aggressive)"
    # but the code sets df_malicious_Train = pd.concat([df4]) (Raspberry_Binary).
    # We follow the code rather than the misleading comment.
    b = [d[13], d[14], d[15], d[16], d[17]]
    run_dataset(
        "binary_to_server_pool_robust",
        m_train=[d[4]],
        b_train=b,
        m_test=[d[32]],
        b_test=b,
        folder=folder,
    )


if __name__ == "__main__":
    main()
