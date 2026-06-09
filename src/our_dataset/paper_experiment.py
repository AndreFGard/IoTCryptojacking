import logging
import pathlib
import time
import datetime
import os
from functools import partial
from typing import Callable
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

def run_experiment(name:str, pipeline:Callable[[pd.DataFrame], transforms.PipelineReturn], model, out_dir = "data/ours/" ):
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(exist_ok=True, parents=True)
    
    required_dataset_files = [out_dir / (name + suffix) for suffix in ["_train.csv", "_val.csv", "_test.csv"]]
    features_file = out_dir / (name + "_selected_features.txt")
    
    global dataset_df
    logging.info(f"starting experiment '{name}")
    if not (all(f.exists() for f in required_dataset_files) and features_file.exists()):
        logging.info(f"Artifacts not found in {out_dir}. Running pipeline to generate datasets...")
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
        logging.info(f"Loaded cached splits: train={train.shape}, val={val.shape}, test={test.shape}")
        with open(features_file, "r") as f:
            selected_features = [line.strip() for line in f if line.strip()]
        logging.info(f"Loaded {len(selected_features)} selected features from {features_file}")
            
    train_x = train[selected_features]
    train_y = train["is_malicious"]
    
    logging.info(f"Fitting model on train set with shape {train_x.shape}...")
    model.fit(train_x, train_y)
    logging.info(f"Model fitting complete.")

    return model, train, val, test


def _evaluate_single_svc(C, kernel, gamma, train_x, train_y, val_x, val_y, test_x, test_y, model_name):
    model = SVC(C=C, kernel=kernel, gamma=gamma, random_state=42)
    logging.info(f"Fitting model: {model_name}...")
    model.fit(train_x, train_y)
    
    val_preds = model.predict(val_x)
    test_preds = model.predict(test_x)
    
    val_f1 = f1_score(val_y, val_preds, average="weighted")
    test_f1 = f1_score(test_y, test_preds, average="weighted")
    
    logging.info(f"Model {model_name} Results - Val Weighted F1: {val_f1:.4f}, Test Weighted F1: {test_f1:.4f}")
    report = classification_report(test_y, test_preds, target_names=["benign", "malicious"])
    logging.info(f"Classification Report for {model_name}:\n{report}")
    
    return {
        "model_name": model_name,
        "C": C,
        "kernel": kernel,
        "gamma": gamma,
        "val_f1": val_f1,
        "test_f1": test_f1
    }


def run_svc_tuning(
    pipeline_name: str = "tsfresh",
    pipeline_fn: Callable[[pd.DataFrame], transforms.PipelineReturn] = partial(transforms.pipeline_tsfresh, window_size=10, overlap=0)
):
    logging.info("--- Starting SVC Hyperparameter Tuning Grid ---")
    c_values = [1, 2]
    kernels = ['linear', 'poly', 'rbf', 'sigmoid']
    gammas = ['scale', 'auto']
    
    # 1. Warm up cache to avoid race conditions when generating files in parallel
    dummy_model = SVC(C=1, kernel='linear', random_state=42)
    run_experiment(
        name=pipeline_name,
        pipeline=pipeline_fn,
        model=dummy_model
    )
    
    # 2. Load cached features for parallel processing
    required_dataset_files = [pathlib.Path("data/ours") / (pipeline_name + suffix) for suffix in ["_train.csv", "_val.csv", "_test.csv"]]
    features_file = pathlib.Path("data/ours/") / (pipeline_name + "_selected_features.txt")
    
    train, val, test = [pd.read_csv(f) for f in required_dataset_files]
    with open(features_file, "r") as f:
        selected_features = [line.strip() for line in f if line.strip()]
        
    val_x = val[selected_features]
    val_y = val["is_malicious"]
    test_x = test[selected_features]
    test_y = test["is_malicious"]
    train_x = train[selected_features]
    train_y = train["is_malicious"]
    
    n_jobs = transforms.CPU_COUNT
    logging.info(f"Using {n_jobs} cores for parallel model evaluation.")
    
    tasks = []
    for C in c_values:
        for kernel in kernels:
            for gamma in gammas:
                model_name = f"SVM-{kernel}-{gamma}-{C}"
                tasks.append(
                    delayed(_evaluate_single_svc)(
                        C, kernel, gamma, train_x, train_y, val_x, val_y, test_x, test_y, model_name
                    )
                )
                
    results = Parallel(n_jobs=n_jobs)(tasks)
                
    results_df = pd.DataFrame(results).set_index("model_name")
    logging.info("--- SVC Tuning Complete! Summary: ---")
    logging.info(f"\n{results_df}")
    
    # Save the dataframe to data/hour:minute-our_dataset_tune.csv
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M")
    out_dir = pathlib.Path("data")
    out_dir.mkdir(exist_ok=True, parents=True)
    csv_file = out_dir / f"{time_str}-our_dataset_tune.csv"
    results_df.to_csv(csv_file)
    logging.info(f"Saved tuning results to {csv_file}")
    
    return results_df


def main():
    global dataset_df
    configure_logging()
    logging.info("Starting experiment runner...")
    ds = dataset.load_dataset()
    dataset_df = ds.df
    run_svc_tuning()
    logging.info("All experiments finished.")


if __name__ == '__main__':
    main()