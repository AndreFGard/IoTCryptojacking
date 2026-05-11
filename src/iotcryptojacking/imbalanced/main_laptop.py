from __future__ import annotations
from iotcryptojacking import utils
import pandas as pd

from iotcryptojacking.imbalanced.experiments import _run_block, setup_experiment

def main() -> None:
    utils.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[35]]
    b: list[pd.DataFrame] = [d[8], d[9], d[10], d[11], d[12]]
    _run_block("laptop", m, b, folder, template)

if __name__ == "__main__":
    main()
