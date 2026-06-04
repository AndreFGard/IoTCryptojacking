#!/bin/bash
echo "Starting non_default_params ML pipeline [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir -p logs

source .venv/bin/activate

for f in src/paper/non_default_params/main_*_ml.py
do
    s="${f/.py/}"
    s="${s//\//.}"
    echo "Running 'python -m $s' [$(date '+%y/%m/%d - %H:%M:%S')]"
    python -m $s
done

echo "Finished non_default_params ML pipeline [$(date '+%y/%m/%d - %H:%M:%S')]"
