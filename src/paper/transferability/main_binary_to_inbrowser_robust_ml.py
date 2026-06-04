from __future__ import annotations
import pathlib
from paper.transferability import experiments
from paper.transferability.experiments import run_ml


def main() -> None:
    experiments.configure_logging(__file__)
    folder = pathlib.Path("./data/transferability")
    folder.mkdir(parents=True, exist_ok=True)
    run_ml("binary_to_inbrowser_robust", folder)


if __name__ == "__main__":
    main()
