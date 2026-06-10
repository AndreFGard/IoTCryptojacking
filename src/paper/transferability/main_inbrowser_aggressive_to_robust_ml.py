from __future__ import annotations
import pathlib
from paper.transferability import experiments
from paper.transferability.experiments import run_ml
 
 
def main() -> None:
    """ML step for the In-Browser-2 transferability experiment.
 
    Reads the pre-computed feature CSVs produced by
    ``main_inbrowser_aggressive_to_robust_dataset.py`` and runs the four
    classifiers (LogReg, KNN, SVM, GNB).
 
    Output artefacts in ``data/transferability/``:
        inbrowser_aggressive_to_robust_results.csv     — 5-fold CV metrics
        inbrowser_aggressive_to_robust_test_report.csv — test-set metrics
                                                         (compare to Table XV)
        inbrowser_aggressive_to_robust_{model}_model.joblib
        inbrowser_aggressive_to_robust_encoder.joblib
 
    Expected paper result (SVM, weighted avg, Table XV):
        accuracy=0.97, precision=0.96, recall=0.97, f1=0.96, roc_auc=0.99
    """
    experiments.configure_logging(__file__)
    folder = pathlib.Path("./data/transferability")
    folder.mkdir(parents=True, exist_ok=True)
    run_ml("inbrowser_aggressive_to_robust", folder)
 
 
if __name__ == "__main__":
    main()
