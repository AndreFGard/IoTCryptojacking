import argparse
import logging
import pathlib
import pandas as pd

from our_dataset.paper_transforms import load_paper_dataframe, PipelinePaperPycatch22
from our_dataset.models import SVCFactory, RandomForestFactory
from our_dataset.runner import run_experiment
from paper.malicious_vs_benign_1.experiments import SCENARIOS

dataset_df: pd.DataFrame | None = None
def configure_logging() -> None:
    log_dir = pathlib.Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

def main():
    global dataset_df
    configure_logging()
    final_df:pd.DataFrame|None = None
    for scenario in ["s2_thr10", "s2_thr50", "s6_single_iot", "s7_iot_iot"]:
        logging.basicConfig(level=logging.INFO)
        logging.info(f"Starting reference paper's experiment runner for scenario: {scenario}...")
        dataset_df = load_paper_dataframe(scenario=scenario)

        pipeline_obj = PipelinePaperPycatch22(
            dataset_df, window_size=10, overlap=0, scenario=scenario
        )

        train, val, test, selected_features = pipeline_obj.load_cache_or_run("data/paper/")

        factories = [SVCFactory(), RandomForestFactory()]
        df = run_experiment(
            train=train,
            val=val,
            test=test,
            selected_features=selected_features,
            output_dir="data/paper/",
            factories=factories,
            prefix=scenario,
        )
        df["scenario"] = scenario
        if final_df is not None:
            final_df = pd.concat([final_df, df])
        else:
            final_df = df
        final_df.to_csv("data/paper/paper_experiment_tune.csv", index=False)
    


if __name__ == "__main__":
    main()
