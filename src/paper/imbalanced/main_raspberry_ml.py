from __future__ import annotations
from paper import experiments
import pathlib

from paper.experiments import run_ml

def main() -> None:
    experiments.configure_logging(__file__)
    folder = pathlib.Path("./data/imbalanced_dataset_experiments")
    folder.mkdir(parents=True, exist_ok=True)

    run_ml("raspberry", folder)

if __name__ == "__main__":
    main()
