import datetime
import logging
import pathlib
from typing import cast
import pandas as pd

from our_dataset.tuning import tune_model


def configure_logging() -> None:
    log_dir = pathlib.Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )


def run_experiment(
    train: pd.DataFrame,
    val: pd.DataFrame,
    test: pd.DataFrame,
    selected_features: list[str],
    output_dir: str | pathlib.Path,
    factories: list,
    prefix: str = "",
) -> None:
    """
    Generic runner to tune model factories on provided dataset splits and log/save results.
    """
    configure_logging()
    logging.info("Starting experiment model tuning...")

    train_x = cast(pd.DataFrame, train[selected_features].fillna(0.0))
    train_y = train["is_malicious"]
    val_x = val[selected_features].fillna(0.0)
    val_y = val["is_malicious"]
    test_x = test[selected_features].fillna(0.0)
    test_y = test["is_malicious"]

    logging.info(f"Columns in input training DataFrame: {list(train.columns)}")
    logging.info("Target column: 'is_malicious'")
    logging.info(f"Features selected for training ({len(selected_features)}): {selected_features}")

    all_dfs = []
    out_dir = pathlib.Path(output_dir)
    out_dir.mkdir(exist_ok=True, parents=True)
    prefix_str = f"{prefix}_" if prefix else ""
    out_path = (
        out_dir / f"{prefix_str}tune_result_{datetime.datetime.now().strftime('%d-%m-%y_%H:%M')}.csv"
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
