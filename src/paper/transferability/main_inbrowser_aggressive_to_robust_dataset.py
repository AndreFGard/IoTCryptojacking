from paper.transferability import experiments
from paper.transferability.experiments import run_dataset, setup_experiment
 
 
def main() -> None:
    """Dataset generation for the In-Browser-2 transferability experiment.
 
    Paper Table XIV — "In-Browser-2":
        Train malicious : df5  = Raspberry_Webmine_Aggressive (12 871 rows)
        Test  malicious : df3  = Raspberry_Webmine_Robust      (3 519 rows)
        Benign (both)   : df13-17 = Raspberry benign (same split for train & test,
                          matching the notebook pattern for this experiment)
 
    This experiment was missing from the original code.  The file
    ``main_binary_to_server_pool_robust_dataset.py`` that existed previously
    was created from a misread of notebook Cell 13 (the comment said
    "in-browser aggressive" but the code used df4/df32).  That file should
    be deleted from the cluster.
    """
    experiments.configure_logging(__file__)
    d, folder = setup_experiment()
 
    b = [d[13], d[14], d[15], d[16], d[17]]
    run_dataset(
        "inbrowser_aggressive_to_robust",
        m_train=[d[5]],   # Raspberry_Webmine_Aggressive
        b_train=b,
        m_test=[d[3]],    # Raspberry_Webmine_Robust
        b_test=b,
        folder=folder,
    )
 
 
if __name__ == "__main__":
    main()
