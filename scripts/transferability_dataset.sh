#!/bin/bash
echo "Starting transferability dataset pipeline [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir -p logs/transferability_dataset

source .venv/bin/activate

for f in src/paper/transferability/main_*_dataset.py
do
    s="${f/.py/}"
    s="${s//\//.}"
    echo "Running 'python -m $s' [$(date '+%y/%m/%d - %H:%M:%S')]"
    python -m $s
done

echo "Finished transferability dataset pipeline [$(date '+%y/%m/%d - %H:%M:%S')]"
