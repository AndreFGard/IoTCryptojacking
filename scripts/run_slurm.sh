#!/bin/bash
#SBATCH --job-name=iotpaper-job
#SBATCH --cpus-per-task=8
#SBATCH --time=08:00:00
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err

# Ensure the logs directory exists
mkdir -p logs

if [ $# -eq 0 ]; then
    echo "Error: No command specified."
    echo "Usage: sbatch $0 <command_to_run> [args...]"
    exit 1
fi

# Execute the passed arguments as a command
"$@"
