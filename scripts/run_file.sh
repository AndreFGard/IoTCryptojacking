#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Error: No module specified."
    echo "Usage: $0 <module_name>"
    exit 1
fi

source .venv/bin/activate
echo "Running 'python -m $1' [$(date '+%y/%m/%d - %H:%M:%S')]"
python -m "$1"
