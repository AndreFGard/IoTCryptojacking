#!/bin/bash
# Submits all malicious_benign_2 ML jobs to SLURM in parallel.
# Run ONLY after all dataset jobs have finished (df_ml.csv files must exist).
#
# Usage:
#   bash scripts/mb2_slurm_ml.sh
#
# To submit ML jobs automatically after dataset jobs complete, use:
#   bash scripts/mb2_slurm_ml.sh --after <job_id1,job_id2,...>

echo "Submitting malicious_benign_2 ML jobs [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir -p logs

source .venv/bin/activate

# Parse optional --after dependency argument
DEPENDENCY=""
if [[ "$1" == "--after" && -n "$2" ]]; then
    DEPENDENCY="--dependency=afterok:$(echo $2 | tr ',' ':' | sed 's/:/,afterok:/g')"
    echo "Jobs will wait for dependencies: $2"
fi

# Check that df_ml artifacts exist before submitting ML jobs
# (skipped if --after is passed, since jobs will wait anyway)
DATA_DIR="./data/malicious_benign_2"
SCENARIOS_ML=(
    "all_combined_s0:paper.malicious_benign_2.main_all_ml"
    "server_s1:paper.malicious_benign_2.main_server_ml"
    "desktop_s1:paper.malicious_benign_2.main_desktop_ml"
    "raspberry_s1:paper.malicious_benign_2.main_raspberry_ml"
    "webos_s1:paper.malicious_benign_2.main_webos_ml"
    "thr_10_s2:paper.malicious_benign_2.main_thr10_ml"
    "thr_50_s2:paper.malicious_benign_2.main_thr50_ml"
    "thr_100_s2:paper.malicious_benign_2.main_thr100_ml"
    "inbrowser_s3:paper.malicious_benign_2.main_inbrowser_ml"
    "binary_s3:paper.malicious_benign_2.main_binary_ml"
    "fully_compromised_s4:paper.malicious_benign_2.main_fully_compromised_ml"
    "partially_compromised_s5:paper.malicious_benign_2.main_partially_compromised_ml"
    "single_compromised_s6:paper.malicious_benign_2.main_single_compromised_ml"
    "iot_compromised_s7:paper.malicious_benign_2.main_iot_compromised_ml"
)

MISSING=0
if [[ -z "$DEPENDENCY" ]]; then
    for ENTRY in "${SCENARIOS_ML[@]}"
    do
        NAME="${ENTRY%%:*}"
        ARTIFACT="$DATA_DIR/${NAME}_df_ml.csv"
        if [[ ! -f "$ARTIFACT" ]]; then
            echo "WARNING: Missing artifact $ARTIFACT — run mb2_slurm_dataset.sh first"
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
    LABEL=$(echo "$MODULE" | awk -F'.' '{print $NF}')

    JOB_ID=$(sbatch \
        --job-name="mb2-ml-${NAME}" \
        --cpus-per-task=8 \
        --time=04:00:00 \
        -p short-simple \
        --output="logs/mb2_ml_${NAME}_%j.out" \
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
