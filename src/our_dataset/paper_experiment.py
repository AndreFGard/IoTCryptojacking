import logging
import pathlib
import time
import datetime
import os
from functools import partial
from typing import Any, Callable, cast, Literal
import pandas as pd
from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import classification_report
from joblib import Parallel, delayed

from our_dataset import dataset, transforms
from our_dataset.tuning import tune_model

dataset_df: pd.DataFrame | None = None


class SVCFactory:
    name = "SVC"
    def __init__(self):
        self.param_grids = [
            {
                "C": [1, 2],
                "kernel": ["linear"],
                "gamma": ["scale"],
                "class_weight": ["balanced", None],
            },
            {
                "C": [1, 2],
                "kernel": ["poly", "rbf", "sigmoid"],
                "gamma": ["scale", "auto"],
                "class_weight": ["balanced", None],
            },
        ]

    def make_model(self, **params):
        C = params["C"]
        kernel = params["kernel"]
        class_weight = params.get("class_weight", None)
        gamma = params.get("gamma", "scale")
        comb_name = f"SVC - {C} - {kernel} - {gamma} - {class_weight}"

        if kernel == "linear":
            model = LinearSVC(
                C=C,
                loss="hinge",
                class_weight=class_weight,
                random_state=42,
                dual=True,
                max_iter=10000,
            )
        else:
            model = SVC(
                C=C,
                kernel=kernel,
                gamma=gamma,
                class_weight=class_weight,
                random_state=42,
            )
        return self.name, comb_name, model


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
    dataset_df = ds.df.groupby(["activity", "vpn"]).head(500).reset_index(drop=True)
    # dataset_df = ds.df

    pipeline_obj = transforms.PipelinePycatch22(dataset_df, window_size=10, overlap=0)

    train, val, test, selected_features = pipeline_obj.load_cache_or_run("data/ours/")

    factory = SVCFactory()

    train_x = cast(pd.DataFrame, train[selected_features].fillna(0.0))
    train_y = train["is_malicious"]
    val_x = val[selected_features].fillna(0.0)
    val_y = val["is_malicious"]
    test_x = test[selected_features].fillna(0.0)
    test_y = test["is_malicious"]

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

    df_results = df_results.sort_values("val_f1_macro")

    out_dir = pathlib.Path("data/ours/")
    out_dir.mkdir(exist_ok=True, parents=True)
    out_path = (
        out_dir / f"svc_tune_result_{datetime.datetime.now().strftime('%d-%m-%y_%H:%M')}.csv"
    )
    df_results.to_csv(out_path, index=False)
    logging.info(f"Tuning finished. Results saved to {out_path}")

    best_row = df_results.iloc[-1]
    logging.info(
        f"Best combination based on Validation F1: {best_row['combination_name']} (Val F1: {best_row['val_f1_macro']:.4f})"
    )

    logging.info("All experiments finished.")


if __name__ == "__main__":
    main()
