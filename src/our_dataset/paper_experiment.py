import logging
import pathlib
import time
import datetime
import os
from functools import partial
from typing import Any, Callable, cast
import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import classification_report, f1_score
from joblib import Parallel, delayed

from our_dataset import dataset, transforms

dataset_df: pd.DataFrame | None = None


def configure_logging() -> None:
    log_dir = pathlib.Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )


def run_experiment(
    name: str,
    pipeline: Callable[[pd.DataFrame], transforms.PipelineReturn],
    model,
    out_dir="data/ours/",
):
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(exist_ok=True, parents=True)

    required_dataset_files = [
        out_dir / (name + suffix) for suffix in ["_train.csv", "_val.csv", "_test.csv"]
    ]
    features_file = out_dir / (name + "_selected_features.txt")

    global dataset_df
    logging.info(f"starting experiment '{name}")
    if not (all(f.exists() for f in required_dataset_files) and features_file.exists()):
        logging.info(
            f"Artifacts not found in {out_dir}. Running pipeline to generate datasets..."
        )
        if dataset_df is None:
            dataset_df = dataset.load_dataset().df
            logging.info(f"Loaded dataset with shape: {dataset_df.shape}")

        logging.info(f"Executing feature extraction pipeline '{name}'...")
        start_time = time.time()
        train, val, test, shit = pipeline(dataset_df)
        elapsed = time.time() - start_time
        logging.info(f"Pipeline execution finished in {elapsed:.2f} seconds.")

        # save features name one by line
        with open(features_file, "w") as f:
            for feat in shit.selected_features:
                f.write(f"{feat}\n")

        logging.info(f"Saving train/val/test CSV datasets to {out_dir}...")
        for df, file in zip([train, val, test], required_dataset_files):
            df.to_csv(file, index=False)

        selected_features = shit.selected_features
    else:
        logging.info(f"Loading cached dataset artifacts from {out_dir}...")
        train, val, test = [pd.read_csv(f) for f in required_dataset_files]
        logging.info(
            f"Loaded cached splits: train={train.shape}, val={val.shape}, test={test.shape}"
        )
        with open(features_file, "r") as f:
            selected_features = [line.strip() for line in f if line.strip()]
        logging.info(
            f"Loaded {len(selected_features)} selected features from {features_file}"
        )

    train_x = train[selected_features].fillna(0.0)
    train_y = train["is_malicious"]

    logging.info(f"Fitting model on train set with shape {train_x.shape}...")
    model.fit(train_x, train_y)
    logging.info("Model fitting complete.")

    val_x = val[selected_features].fillna(0.0)
    val_y = val["is_malicious"]
    test_x = test[selected_features].fillna(0.0)
    test_y = test["is_malicious"]

    logging.info("Calculating metrics...")
    train_preds = model.predict(train_x)
    val_preds = model.predict(val_x)
    test_preds = model.predict(test_x)

    metrics = {
        "train": cast(dict[str, Any], classification_report(train_y, train_preds, output_dict=True)),
        "val": cast(dict[str, Any], classification_report(val_y, val_preds, output_dict=True)),
        "test": cast(dict[str, Any], classification_report(test_y, test_preds, output_dict=True)),
    }

    logging.info(
        f"Metrics - Train F1: {metrics['train']['macro avg']['f1-score']:.4f} | "
        f"Val F1: {metrics['val']['macro avg']['f1-score']:.4f} | "
        f"Test F1: {metrics['test']['macro avg']['f1-score']:.4f}"
    )

    return model, train, val, test, selected_features, metrics


def main():
    global dataset_df
    configure_logging()
    logging.info("Starting experiment runner...")
    ds = dataset.load_dataset()
    dataset_df = ds.df
    tsfresh_fn = partial(transforms.pipeline_tsfresh, window_size=10, overlap=0)
    pipeline_pycatch22 = partial(transforms.pipeline_pycatch22, window_size=10, overlap=0)
    run_experiment("tsfresh",tsfresh_fn, SVC(), )
    logging.info("All experiments finished.")


if __name__ == "__main__":
    main()
