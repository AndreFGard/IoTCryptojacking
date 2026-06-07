from __future__ import annotations
import pathlib
from paper.non_default_params import experiments
from paper.non_default_params.experiments import run_ml


def main() -> None:
    experiments.configure_logging(__file__)
    folder = pathlib.Path("./data/non_default_params")
    folder.mkdir(parents=True, exist_ok=True)
    run_ml("iot_s1", folder)


if __name__ == "__main__":
    main()
