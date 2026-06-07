#!/bin/bash
echo "Submitting non_default_params dataset jobs [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir -p logs

source .venv/bin/activate

SCENARIOS=(
    "paper.non_default_params.main_all_dataset"
    "paper.non_default_params.main_server_dataset"
    "paper.non_default_params.main_laptop_dataset"
    "paper.non_default_params.main_iot_dataset"
    "paper.non_default_params.main_thr10_dataset"
    "paper.non_default_params.main_thr50_dataset"
    "paper.non_default_params.main_thr100_dataset"
    "paper.non_default_params.main_inbrowser_dataset"
    "paper.non_default_params.main_binary_dataset"
    "paper.non_default_params.main_fully_compromised_dataset"
    "paper.non_default_params.main_partially_compromised_dataset"
    "paper.non_default_params.main_single_compromised_dataset"
    "paper.non_default_params.main_iot_compromised_dataset"
)

JOB_IDS=()

for MODULE in "${SCENARIOS[@]}"
do
    LABEL=$(echo "$MODULE" | awk -F'.' '{print $NF}')
    JOB_ID=$(sbatch \
        --job-name="nd-ds-${LABEL}" \
        --cpus-per-task=8 \
        --time=24:00:00 \
        -p short-simple \
        --output="logs/non_default_dataset_${LABEL}_%j.out" \
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
echo "When all finish, run: bash scripts/non_default_slurm_ml.sh"
