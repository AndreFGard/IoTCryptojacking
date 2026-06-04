#!/bin/bash
# Run ONLY after all dataset jobs have finished.
# Usage: bash scripts/non_default_slurm_ml.sh
#    or: bash scripts/non_default_slurm_ml.sh --after <job_id1,job_id2,...>

echo "Submitting non_default_params ML jobs [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir -p logs

source .venv/bin/activate

DEPENDENCY=""
if [[ "$1" == "--after" && -n "$2" ]]; then
    DEPENDENCY="--dependency=afterok:$(echo $2 | tr ',' ':' | sed 's/:/,afterok:/g')"
    echo "Jobs will wait for dependencies: $2"
fi

DATA_DIR="./data/non_default_params"
SCENARIOS_ML=(
    "all_combined_s0:paper.non_default_params.main_all_ml"
    "server_s1:paper.non_default_params.main_server_ml"
    "laptop_s1:paper.non_default_params.main_laptop_ml"
    "iot_s1:paper.non_default_params.main_iot_ml"
    "thr_10_s2:paper.non_default_params.main_thr10_ml"
    "thr_50_s2:paper.non_default_params.main_thr50_ml"
    "thr_100_s2:paper.non_default_params.main_thr100_ml"
    "inbrowser_s3:paper.non_default_params.main_inbrowser_ml"
    "binary_s3:paper.non_default_params.main_binary_ml"
    "fully_compromised_s4:paper.non_default_params.main_fully_compromised_ml"
    "partially_compromised_s5:paper.non_default_params.main_partially_compromised_ml"
    "single_compromised_s6:paper.non_default_params.main_single_compromised_ml"
    "iot_compromised_s7:paper.non_default_params.main_iot_compromised_ml"
)

MISSING=0
if [[ -z "$DEPENDENCY" ]]; then
    for ENTRY in "${SCENARIOS_ML[@]}"; do
        NAME="${ENTRY%%:*}"
        ARTIFACT="$DATA_DIR/${NAME}_df_ml.csv"
        if [[ ! -f "$ARTIFACT" ]]; then
            echo "WARNING: Missing artifact $ARTIFACT"
            MISSING=1
        fi
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
    JOB_ID=$(sbatch \
        --job-name="nd-ml-${NAME}" \
        --cpus-per-task=8 \
        --time=08:00:00 \
        -p short-simple \
        --output="logs/non_default_ml_${NAME}_%j.out" \
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
