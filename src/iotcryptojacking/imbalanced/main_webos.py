from __future__ import annotations
from iotcryptojacking import utils
import pandas as pd

from iotcryptojacking.imbalanced.experiments import run_block, setup_experiment

def main() -> None:
    utils.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[1]]
    b: list[pd.DataFrame] = [d[23]]
    run_block("webos", m, b, folder, template)

if __name__ == "__main__":
    main()
