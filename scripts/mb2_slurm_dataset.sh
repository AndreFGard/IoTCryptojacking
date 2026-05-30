#!/bin/bash
# Submits all malicious_benign_2 dataset jobs to SLURM in parallel.
# Each scenario runs independently on its own node.
#
# Usage:
#   bash scripts/mb2_slurm_dataset.sh
#
# After all jobs finish, run:
#   bash scripts/mb2_slurm_ml.sh

echo "Submitting malicious_benign_2 dataset jobs [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir -p logs

source .venv/bin/activate

SCENARIOS=(
    "paper.malicious_benign_2.main_all_dataset"
    "paper.malicious_benign_2.main_server_dataset"
    "paper.malicious_benign_2.main_desktop_dataset"
    "paper.malicious_benign_2.main_raspberry_dataset"
    "paper.malicious_benign_2.main_webos_dataset"
    "paper.malicious_benign_2.main_thr10_dataset"
    "paper.malicious_benign_2.main_thr50_dataset"
    "paper.malicious_benign_2.main_thr100_dataset"
    "paper.malicious_benign_2.main_inbrowser_dataset"
    "paper.malicious_benign_2.main_binary_dataset"
    "paper.malicious_benign_2.main_fully_compromised_dataset"
    "paper.malicious_benign_2.main_partially_compromised_dataset"
    "paper.malicious_benign_2.main_single_compromised_dataset"
    "paper.malicious_benign_2.main_iot_compromised_dataset"
)

JOB_IDS=()

for MODULE in "${SCENARIOS[@]}"
do
    # extract short name for job label (e.g. main_all_dataset)
    LABEL=$(echo "$MODULE" | awk -F'.' '{print $NF}')

    JOB_ID=$(sbatch \
        --job-name="mb2-ds-${LABEL}" \
        --cpus-per-task=8 \
        --time=12:00:00 \
        -p short-simple \
        --output="logs/mb2_dataset_${LABEL}_%j.out" \
        --parsable \
        scripts/run_slurm_multi.sh python -m "$MODULE")

    echo "Submitted $LABEL → job $JOB_ID"
    JOB_IDS+=("$JOB_ID")
done

# Print all submitted IDs for reference
echo ""
echo "All dataset jobs submitted:"
printf '  %s\n' "${JOB_IDS[@]}"
echo ""
echo "Monitor with: squeue -u \$USER"
echo "When all finish, run: bash scripts/mb2_slurm_ml.sh"
