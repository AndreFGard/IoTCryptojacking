#!/bin/bash
echo "Starting transferability ML pipeline [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir -p logs/transferability_ml

source .venv/bin/activate

for f in src/paper/transferability/main_*_ml.py
do
    s="${f/.py/}"
    s="${s//\//.}"
    echo "Running 'python -m $s' [$(date '+%y/%m/%d - %H:%M:%S')]"
    python -m $s
done

echo "Finished transferability ML pipeline [$(date '+%y/%m/%d - %H:%M:%S')]"
