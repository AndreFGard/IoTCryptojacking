#!/bin/bash
echo "Starting Malicious vs Benign (All Scenarios 1) pipeline [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir -p logs/all_scenarios_1

source .venv/bin/activate

for f in src/paper/malicious_vs_benign_1/*.py
do
    s="${f/.py/}"
    s="${s//\//.}"
    echo "Running 'python -m $s' [$(date '+%y/%m/%d - %H:%M:%S')]"
    python -m $s
done
