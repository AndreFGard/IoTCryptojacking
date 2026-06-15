import logging
import pathlib
import time
import datetime
import os
from functools import partial
from typing import Any, Callable, cast, Literal
import pandas as pd
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from our_dataset import dataset, transforms
from our_dataset.tuning import tune_model
from our_dataset.models import SVCFactory, RandomForestFactory
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

    train_x = cast(pd.DataFrame, train[selected_features].fillna(0.0))
    train_y = train["is_malicious"]
    val_x = val[selected_features].fillna(0.0)
    val_y = val["is_malicious"]
    test_x = test[selected_features].fillna(0.0)
    test_y = test["is_malicious"]

    all_dfs = []
    out_dir = pathlib.Path("data/ours/")
    out_dir.mkdir(exist_ok=True, parents=True)
    out_path = (
        out_dir / f"tune_result_{datetime.datetime.now().strftime('%d-%m-%y_%H:%M')}.csv"
    )
    for factory in factories:
        df_results = tune_model(
            factory.make_model,
            factory.param_grids,
            train_x,
            train_y,
            val_x,
            val_y,
            test_x,
            test_y,
        )
        all_dfs.append(df_results)

        final_df = pd.concat(all_dfs, ignore_index=True)
        final_df = final_df.sort_values("val_f1_macro")
        final_df.to_csv(out_path, index=False)
    logging.info(f"Tuning finished. Results saved to {out_path}")

    best_row = final_df.iloc[-1]
    logging.info(
        f"Best combination based on Validation F1: {best_row['combination_name']} from {best_row['model']} (Val F1: {best_row['val_f1_macro']:.4f})"
    )

    logging.info("All experiments finished.")


if __name__ == "__main__":
    main()
