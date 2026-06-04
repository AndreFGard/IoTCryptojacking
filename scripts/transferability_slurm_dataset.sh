#!/bin/bash
# Submits all transferability dataset jobs to SLURM in parallel.
# Each experiment runs independently on its own node.
#
# Usage:
#   bash scripts/transferability_slurm_dataset.sh
#
# After all jobs finish, run:
#   bash scripts/transferability_slurm_ml.sh

echo "Submitting transferability dataset jobs [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir -p logs

source .venv/bin/activate

SCENARIOS=(
    "paper.transferability.main_webmine_to_pool_dataset"
    "paper.transferability.main_pool_to_webmine_dataset"
    "paper.transferability.main_raspberry_binary_to_webos_dataset"
    "paper.transferability.main_binary_to_inbrowser_aggressive_dataset"
    "paper.transferability.main_binary_to_inbrowser_robust_dataset"
    "paper.transferability.main_binary_to_inbrowser_stealthy_dataset"
    "paper.transferability.main_inbrowser_aggressive_to_stealthy_dataset"
    "paper.transferability.main_binary_to_server_pool_robust_dataset"
)

JOB_IDS=()

for MODULE in "${SCENARIOS[@]}"
do
    LABEL=$(echo "$MODULE" | awk -F'.' '{print $NF}')

    JOB_ID=$(sbatch \
        --job-name="trf-ds-${LABEL}" \
        --cpus-per-task=8 \
        --time=12:00:00 \
        -p short-simple \
        --output="logs/transferability_dataset_${LABEL}_%j.out" \
        --parsable \
        scripts/run_slurm_multi.sh python -m "$MODULE")

    echo "Submitted $LABEL → job $JOB_ID"
    JOB_IDS+=("$JOB_ID")
done

echo ""
echo "All dataset jobs submitted:"
printf '  %s\n' "${JOB_IDS[@]}"
echo ""
echo "Monitor with: squeue -u \$USER"
echo "When all finish, run: bash scripts/transferability_slurm_ml.sh"
