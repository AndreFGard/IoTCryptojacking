import datetime
import logging
import pathlib
from typing import Any, cast
import pandas as pd
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score

def tune_svc(
    train: pd.DataFrame,
    val: pd.DataFrame,
    test: pd.DataFrame,
    selected_features: list[str],
    param_grids: list[dict[str, list[Any]]],
    out_dir: str | pathlib.Path = "data/ours/",
) -> pd.DataFrame:
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(exist_ok=True, parents=True)

    train_x = cast(pd.DataFrame, train[selected_features].fillna(0.0))
    train_y = train["is_malicious"]
    val_x = cast(pd.DataFrame, val[selected_features].fillna(0.0))
    val_y = val["is_malicious"]
    test_x = cast(pd.DataFrame, test[selected_features].fillna(0.0))
    test_y = test["is_malicious"]

    results = []
    logging.info("Starting SVC hyperparameter tuning...")

    for params in ParameterGrid(param_grids):
        C = params["C"]
        kernel = params["kernel"]
        gamma = params.get("gamma", "scale")
        class_weight = params.get("class_weight", None)

        comb_name = f"SVC - {C} - {kernel} - {gamma} - {class_weight}"

        logging.info(f"Training {comb_name}...")

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

        model.fit(train_x, train_y)

        val_preds = model.predict(val_x)
        val_f1 = f1_score(val_y, val_preds, average="macro")
        val_prec = precision_score(val_y, val_preds, average="macro")
        val_rec = recall_score(val_y, val_preds, average="macro")

        test_preds = model.predict(test_x)
        test_f1 = f1_score(test_y, test_preds, average="macro")
        test_prec = precision_score(test_y, test_preds, average="macro")
        test_rec = recall_score(test_y, test_preds, average="macro")

        res_d = {
            "combination_name": comb_name,
            "C": C,
            "kernel": kernel,
            "gamma": gamma,
            "class_weight": class_weight,
            "val_f1_macro": val_f1,
            "val_precision_macro": val_prec,
            "val_recall_macro": val_rec,
            "test_f1_macro": test_f1,
            "test_precision_macro": test_prec,
            "test_recall_macro": test_rec,
        }
        results.append(res_d)
        logging.info(f"{comb_name} - {res_d}")

    df_results = pd.DataFrame(results).sort_values("val_f1_macro")
    out_path = (
        out_dir / f"svc_tune_result_{datetime.datetime.now().strftime('%H-%M')}.csv"
    )
    df_results.to_csv(out_path, index=False)
    logging.info(f"Tuning finished. Results saved to {out_path}")

    # Output detailed classification report on test set for the best model based on validation F1 score
    best_result = max(results, key=lambda x: x["val_f1_macro"])
    logging.info(
        f"Best combination based on Validation F1: {best_result['combination_name']} (Val F1: {best_result['val_f1_macro']:.4f})"
    )

    if best_result["kernel"] == "linear":
        best_model = LinearSVC(
            C=cast(Any, best_result["C"]),
            loss="hinge",
            class_weight=cast(Any, best_result["class_weight"]),
            random_state=42,
            dual=True,
            max_iter=10000,
        )
    else:
        best_model = SVC(
            C=cast(Any, best_result["C"]),
            kernel=cast(Any, best_result["kernel"]),
            gamma=cast(Any, best_result["gamma"]),
            class_weight=cast(Any, best_result["class_weight"]),
            random_state=42,
        )
    best_model.fit(train_x, train_y)
    best_test_preds = best_model.predict(test_x)

    report_str = cast(str, classification_report(test_y, best_test_preds))
    logging.info("\nTest set classification report for the best model:\n" + report_str)

    return df_results
