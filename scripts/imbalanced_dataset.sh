#!/bin/bash
echo "Starting imbalanced dataset pipeline [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir -p logs/imbalanced_dataset

source .venv/bin/activate

for f in src/paper/imbalanced/main_*_dataset.py
do
    s="${f/.py/}"
    s="${s//\//.}"
    echo "Running 'python -m $s' [$(date '+%y/%m/%d - %H:%M:%S')]"
    python -m $s
done
