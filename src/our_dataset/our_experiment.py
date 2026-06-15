import logging
import pathlib
import pandas as pd

from our_dataset import dataset, transforms
from our_dataset.models import SVCFactory, RandomForestFactory
from our_dataset.runner import run_experiment

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
    logging.info("Starting experiment runner...")
    ds = dataset.load_dataset()

    # To test with a subset, uncomment the line below:
    #dataset_df = ds.df.groupby(["activity", "vpn"]).head(500).reset_index(drop=True)
    dataset_df = ds.df

    pipeline_obj = transforms.PipelinePycatch22(dataset_df, window_size=10, overlap=0)

    train, val, test, selected_features = pipeline_obj.load_cache_or_run("data/ours/")

    factories = [SVCFactory(), RandomForestFactory()]

    run_experiment(
        train=train,
        val=val,
        test=test,
        selected_features=selected_features,
        output_dir="data/ours/",
        factories=factories,
    )


if __name__ == "__main__":
    main()
