

```bash
git lfs install
bash start.sh
source .venv/bin/activate
mkdir logs

sbatch scripts/run_slurm_multi.sh ./scripts/imbalanced_dataset.sh
sbatch scripts/run_slurm_single.sh ./scripts/imbalanced_ml.sh

sbatch scripts/run_slurm_multi.sh ./scripts/all_scenarios_1.sh
bash scripts/all_scenarios_1.sh |& tee logs/all_scenarios_1/run.log
sbatch scripts/run_slurm_multi.sh ./scripts/all_scenarios_1.sh |& tee logs/all_scenarios_1/run.log
```

and this might be useful too:

```bash
srun --jobid=JOBID --pty bash
```


## Development

Everything we change from a given notebook when converting it to scripts was justified and documented. The behaviour of the original code was not changed, including not fixing their bugs.