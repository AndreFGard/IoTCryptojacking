import logging
import pathlib
import time
import datetime
import os
from functools import partial
from typing import Any, Callable, cast, Literal
import pandas as pd
from sklearn.svm import SVC, LinearSVC
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


def tune_svc(
    train: pd.DataFrame,
    val: pd.DataFrame,
    test: pd.DataFrame,
    selected_features: list[str],
    out_dir: str | pathlib.Path = "data/ours/",
) -> pd.DataFrame:
    import itertools
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(exist_ok=True, parents=True)

    C_values = [1, 2]
    kernels: list[Literal["linear", "poly", "rbf", "sigmoid"]] = ["linear", "poly", "rbf", "sigmoid"]
    gammas: list[Literal["scale", "auto"]] = ["scale", "auto"]

    train_x = cast(pd.DataFrame, train[selected_features].fillna(0.0))
    train_y = train["is_malicious"]
    val_x = cast(pd.DataFrame, val[selected_features].fillna(0.0))
    val_y = val["is_malicious"]
    test_x = cast(pd.DataFrame, test[selected_features].fillna(0.0))
    test_y = test["is_malicious"]

    results = []
    logging.info("Starting SVC hyperparameter tuning...")

    for C, kernel, gamma in itertools.product(C_values, kernels, gammas):
        params = [C, kernel, gamma]
        comb_name = f"SVC - {' - '.join(map(str, params))}"

        # If kernel is linear, gamma is ignored. To avoid duplicate training,
        # we copy the result of gamma == 'scale' when gamma == 'auto' is processed.
        if kernel == "linear" and gamma == "auto":
            prev_comb = f"SVC - {C} - linear - scale"
            prev_res = next((r for r in results if r["combination_name"] == prev_comb), None)
            if prev_res is not None:
                results.append({
                    "combination_name": comb_name,
                    "C": C,
                    "kernel": kernel,
                    "gamma": gamma,
                    "val_f1_macro": prev_res["val_f1_macro"],
                    "test_f1_macro": prev_res["test_f1_macro"]
                })
                logging.info(f"{comb_name} - Val F1 Macro: {prev_res['val_f1_macro']:.4f} | Test F1 Macro: {prev_res['test_f1_macro']:.4f} (copied from scale)")
                continue

        logging.info(f"Training {comb_name}...")

        if kernel == "linear":
            model = LinearSVC(C=C, loss="hinge", random_state=42, dual=True, max_iter=10000)
        else:
            model = SVC(C=C, kernel=kernel, gamma=gamma, random_state=42)

        model.fit(train_x, train_y)

        val_preds = model.predict(val_x)
        val_f1 = f1_score(val_y, val_preds, average="macro")

        test_preds = model.predict(test_x)
        test_f1 = f1_score(test_y, test_preds, average="macro")

        results.append({
            "combination_name": comb_name,
            "C": C,
            "kernel": kernel,
            "gamma": gamma,
            "val_f1_macro": val_f1,
            "test_f1_macro": test_f1
        })
        logging.info(f"{comb_name} - Val F1 Macro: {val_f1:.4f} | Test F1 Macro: {test_f1:.4f}")

    df_results = pd.DataFrame(results).sort_values("val_f1_macro")
    out_path = out_dir / "svc_tune_result.csv"
    df_results.to_csv(out_path, index=False)
    logging.info(f"Tuning finished. Results saved to {out_path}")

    # Output detailed classification report on test set for the best model based on validation F1 score
    best_result = max(results, key=lambda x: x["val_f1_macro"])
    logging.info(f"Best combination based on Validation F1: {best_result['combination_name']} (Val F1: {best_result['val_f1_macro']:.4f})")
    
    if best_result["kernel"] == "linear":
        best_model = LinearSVC(C=cast(Any, best_result["C"]), loss="hinge", random_state=42, dual=True, max_iter=10000)
    else:
        best_model = SVC(
            C=cast(Any, best_result["C"]),
            kernel=cast(Any, best_result["kernel"]),
            gamma=cast(Any, best_result["gamma"]),
            random_state=42
        )
    best_model.fit(train_x, train_y)
    best_test_preds = best_model.predict(test_x)
    
    report_str = cast(str, classification_report(test_y, best_test_preds))
    logging.info("\nTest set classification report for the best model:\n" + report_str)

    return df_results


def main():
    global dataset_df
    configure_logging()
    logging.info("Starting experiment runner...")
    ds = dataset.load_dataset()
    
    # To test with a subset, uncomment the line below:
    # dataset_df = ds.df.groupby(["activity", "vpn"]).head(500).reset_index(drop=True)
    dataset_df = ds.df
        
    tsfresh_fn = partial(transforms.pipeline_tsfresh, window_size=10, overlap=0)
    pipeline_pycatch22 = partial(transforms.pipeline_pycatch22, window_size=10, overlap=0)
    
    _, train, val, test, selected_features, _ = run_experiment("tsfresh", tsfresh_fn, SVC())
    
    # Run hyperparameter tuning on the dataset splits
    tune_svc(train, val, test, selected_features)
    
    logging.info("All experiments finished.")


if __name__ == "__main__":
    main()
