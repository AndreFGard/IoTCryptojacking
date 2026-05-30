#!/bin/bash
echo "Starting malicious_benign_2 dataset pipeline [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir -p logs/mb2_dataset

source .venv/bin/activate

for f in src/paper/malicious_benign_2/main_*_dataset.py
do
    s="${f/.py/}"
    s="${s//\//.}"
    echo "Running 'python -m $s' [$(date '+%y/%m/%d - %H:%M:%S')]"
    python -m $s
done

echo "Finished malicious_benign_2 dataset pipeline [$(date '+%y/%m/%d - %H:%M:%S')]"
