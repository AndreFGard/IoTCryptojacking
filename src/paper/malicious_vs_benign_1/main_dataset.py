from __future__ import annotations

from paper.malicious_vs_benign_1 import experiments


def main() -> None:
    experiments.configure_logging(__file__)
    experiments.run_dataset_stage()


if __name__ == "__main__":
    main()
