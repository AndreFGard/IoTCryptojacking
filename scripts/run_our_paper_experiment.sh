#!/bin/bash
#SBATCH --job-name=svc-tuning
#SBATCH --cpus-per-task=18
#SBATCH --time=12:00:00
#SBATCH -p short-simple
#SBATCH --output=logs/%j.out

# Ensure the logs directory exists
mkdir -p logs

# Run the tuning experiment
.venv/bin/python -m src.our_dataset.paper_experiment
