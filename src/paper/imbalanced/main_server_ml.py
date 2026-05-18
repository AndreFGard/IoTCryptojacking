from __future__ import annotations
import pathlib

from paper.imbalanced.experiments import run_ml
from paper.imbalanced import experiments

def main() -> None:
    experiments.configure_logging(__file__)
    folder = pathlib.Path("./data/imbalanced_dataset_experiments")
    folder.mkdir(parents=True, exist_ok=True)

    run_ml("server", folder)

if __name__ == "__main__":
    main()
