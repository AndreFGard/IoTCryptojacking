#!/bin/bash
echo "Starting imbalanced ML pipeline [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir -p logs/imbalanced_ml

source .venv/bin/activate

for f in src/iotcryptojacking/imbalanced/main_*_ml.py
do
    s="${f/.py/}"
    s="${s//\//.}"
    echo "Running 'python -m $s' [$(date '+%y/%m/%d - %H:%M:%S')]"
    python -m $s
done
