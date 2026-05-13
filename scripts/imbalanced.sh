#!/bin/bash
echo "Starting imbalanced pipeline [$(date '+%y/%m/%d - %H:%M:%S')]"
mkdir logs/imbalanced -p

source .venv/bin/activate
for f in  src/iotcryptojacking/imbalanced/main_*.py
do  s="${f/.py/}"
    s="${s//\//.}"
    echo "running 'python $s' [$(date '+%y/%m/%d - %H:%M:%S')]"
    python -m $s
    break
done;