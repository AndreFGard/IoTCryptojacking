from __future__ import annotations
from iotcryptojacking import utils
import pandas as pd

from iotcryptojacking.imbalanced.experiments import run_block, setup_experiment

def main() -> None:
    utils.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[32], d[33], d[34], d[35]]
    b: list[pd.DataFrame] = [d[8], d[9], d[10], d[11], d[12], d[13], d[14], d[15], d[16], d[17], d[18], d[19], d[20], d[21], d[22], d[23]]
    run_block("timely_oversampling", m, b, folder, template, oversample=True)

if __name__ == "__main__":
    main()
