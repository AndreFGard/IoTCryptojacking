import logging
from typing import Any, Callable
import pandas as pd
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import f1_score, precision_score, recall_score

def tune_model(
    model_factory: Callable[..., tuple[str, Any]],
    param_grids: list[dict[str, list[Any]]],
    train_x: pd.DataFrame,
    train_y: pd.Series,
    val_x: pd.DataFrame,
    val_y: pd.Series,
    test_x: pd.DataFrame,
    test_y: pd.Series,
) -> pd.DataFrame:
    """
    Tune a model over a grid of hyperparameters.
    
    Args:
        model_factory: A callable that returns (combination_name, model) when passed
                       the hyperparameters as kwargs (e.g., model_factory(**params)).
        param_grids: List of parameter grids (dicts) to try.
        
    Returns:
        pd.DataFrame containing the parameters and metrics for all combinations.
    """
    results = []
    logging.info("Starting hyperparameter tuning...")

    for params in ParameterGrid(param_grids):
        # Instantiate model and name from factory
        comb_name, model = model_factory(**params)
        
        logging.info(f"Training combination: {comb_name}")

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
            **params,
            "val_f1_macro": val_f1,
            "val_precision_macro": val_prec,
            "val_recall_macro": val_rec,
            "test_f1_macro": test_f1,
            "test_precision_macro": test_prec,
            "test_recall_macro": test_rec,
        }

        results.append(res_d)
        logging.info(f"Results for {comb_name}: Val F1={val_f1:.4f}, Test F1={test_f1:.4f}")

    return pd.DataFrame(results)
