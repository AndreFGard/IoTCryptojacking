#!/bin/bash
echo "Starting malicious_benign_2 ML pipeline [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir -p logs/mb2_ml

source .venv/bin/activate

for f in src/paper/malicious_benign_2/main_*_ml.py
do
    s="${f/.py/}"
    s="${s//\//.}"
    echo "Running 'python -m $s' [$(date '+%y/%m/%d - %H:%M:%S')]"
    python -m $s
done

echo "Finished malicious_benign_2 ML pipeline [$(date '+%y/%m/%d - %H:%M:%S')]"
