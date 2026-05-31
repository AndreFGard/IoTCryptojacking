from __future__ import annotations
import pathlib
from paper.malicious_benign_2 import experiments
from paper.malicious_benign_2.experiments import run_ml


def main() -> None:
    experiments.configure_logging(__file__)
    folder = pathlib.Path("./data/malicious_benign_2")
    folder.mkdir(parents=True, exist_ok=True)
    run_ml("iot_compromised_s7", folder)


if __name__ == "__main__":
    main()
