

```bash
bash start.sh
source .venv/bin/activate
mkdir logs

sbatch scripts/run_slum_multi.sh ./scripts/imbalanced_dataset.sh
sbatch scripts/run_slum_single.sh ./scripts/imbalanced_ml.sh

sbatch scripts/run_slum_multi.sh ./scripts/all_scenarios_1.sh
```

and this might be useful too:

```bash
srun --jobid=JOBID --pty bash
```


## Development

Everything we change from a given notebook when converting it to scripts was justified and documented. The behaviour of the original code was not changed, including not fixing their bugs.