from __future__ import annotations
import logging
from sklearn.model_selection import GridSearchCV
from sklearn.base import BaseEstimator
from typing import Any, Dict


def tune_hyperparameters(
    model: BaseEstimator,
    param_grid: Dict[str, list[Any]],
    X,
    y,
    cv: int = 5,
    n_jobs: int = -1,
) -> GridSearchCV:
    logging.info("Starting hyperparameter tuning")
    search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=cv,
        scoring="roc_auc",
        n_jobs=n_jobs,
        verbose=1,
    )
    search.fit(X, y)
    logging.info(f"Best params found: {search.best_params_}")
    return search
