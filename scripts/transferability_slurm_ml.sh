#!/bin/bash
# Submits all transferability ML jobs to SLURM in parallel.
# Run ONLY after all dataset jobs have finished (train/test df_ml.csv files must exist).
#
# Usage:
#   bash scripts/transferability_slurm_ml.sh
#
# To submit ML jobs automatically after dataset jobs complete, use:
#   bash scripts/transferability_slurm_ml.sh --after <job_id1,job_id2,...>

echo "Submitting transferability ML jobs [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir -p logs

source .venv/bin/activate

DEPENDENCY=""
if [[ "$1" == "--after" && -n "$2" ]]; then
    DEPENDENCY="--dependency=afterok:$(echo $2 | tr ',' ':' | sed 's/:/,afterok:/g')"
    echo "Jobs will wait for dependencies: $2"
fi

DATA_DIR="./data/transferability"
SCENARIOS_ML=(
    "webmine_to_pool:paper.transferability.main_webmine_to_pool_ml"
    "pool_to_webmine:paper.transferability.main_pool_to_webmine_ml"
    "raspberry_binary_to_webos:paper.transferability.main_raspberry_binary_to_webos_ml"
    "binary_to_inbrowser_aggressive:paper.transferability.main_binary_to_inbrowser_aggressive_ml"
    "binary_to_inbrowser_robust:paper.transferability.main_binary_to_inbrowser_robust_ml"
    "binary_to_inbrowser_stealthy:paper.transferability.main_binary_to_inbrowser_stealthy_ml"
    "inbrowser_aggressive_to_stealthy:paper.transferability.main_inbrowser_aggressive_to_stealthy_ml"
    "binary_to_server_pool_robust:paper.transferability.main_binary_to_server_pool_robust_ml"
)

MISSING=0
if [[ -z "$DEPENDENCY" ]]; then
    for ENTRY in "${SCENARIOS_ML[@]}"
    do
        NAME="${ENTRY%%:*}"
        for SUFFIX in "train_df_ml" "test_df_ml"; do
            ARTIFACT="$DATA_DIR/${NAME}_${SUFFIX}.csv"
            if [[ ! -f "$ARTIFACT" ]]; then
                echo "WARNING: Missing artifact $ARTIFACT — run transferability_slurm_dataset.sh first"
                MISSING=1
            fi
        done
    done
    if [[ $MISSING -eq 1 ]]; then
        echo "Aborting: one or more df_ml.csv files are missing."
        exit 1
    fi
fi

JOB_IDS=()

for ENTRY in "${SCENARIOS_ML[@]}"
do
    NAME="${ENTRY%%:*}"
    MODULE="${ENTRY##*:}"
    LABEL=$(echo "$MODULE" | awk -F'.' '{print $NF}')

    JOB_ID=$(sbatch \
        --job-name="trf-ml-${NAME}" \
        --cpus-per-task=8 \
        --time=04:00:00 \
        -p short-simple \
        --output="logs/transferability_ml_${NAME}_%j.out" \
        --parsable \
        $DEPENDENCY \
        scripts/run_slurm_multi.sh python -m "$MODULE")

    echo "Submitted $NAME → job $JOB_ID"
    JOB_IDS+=("$JOB_ID")
done

echo ""
echo "All ML jobs submitted:"
printf '  %s\n' "${JOB_IDS[@]}"
echo ""
echo "Monitor with: squeue -u \$USER"
echo "When all finish, run: bash scripts/pretty_print_results.sh"
