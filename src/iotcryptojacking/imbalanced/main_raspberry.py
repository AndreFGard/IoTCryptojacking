from __future__ import annotations
from iotcryptojacking import utils
import pandas as pd

from iotcryptojacking.imbalanced.experiments import run_block, setup_experiment

def main() -> None:
    utils.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[3], d[4], d[5], d[6], d[33], d[34]]
    b: list[pd.DataFrame] = [d[13], d[14], d[15], d[16], d[17]]
    run_block("raspberry", m, b, folder, template)

if __name__ == "__main__":
    main()
