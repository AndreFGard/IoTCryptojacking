from __future__ import annotations
import pandas as pd

from iotcryptojacking.experiments import run_dataset, setup_experiment
from iotcryptojacking import experiments

def main() -> None:
    experiments.configure_logging(__file__)
    d, folder, template = setup_experiment()

    m: list[pd.DataFrame] = [
        d[1].iloc[:2832], d[2].iloc[:4680], d[3].iloc[:271], d[4].iloc[:48],
        d[5].iloc[:69], d[6].iloc[:72], d[7].iloc[:170], d[32].iloc[:175],
        d[33].iloc[:76], d[34].iloc[:48], d[35].iloc[:1300]
    ]
    b: list[pd.DataFrame] = [
        d[8].iloc[:422784], d[9].iloc[:44376], d[10].iloc[:14784], d[11].iloc[:3576],
        d[12].iloc[:34728], d[13].iloc[:269400], d[14].iloc[:73], d[15].iloc[:24144],
        d[16].iloc[:7320], d[17].iloc[:21240], d[18].iloc[:544416], d[19].iloc[:2664],
        d[20].iloc[:27480], d[21].iloc[:30888], d[22].iloc[:12168], d[23].iloc[:174648]
    ]
    run_dataset("timely", m, b, folder, template)

if __name__ == "__main__":
    main()
