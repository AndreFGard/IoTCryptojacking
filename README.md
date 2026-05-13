

```bash
bash start.sh
source .venv


sbatch scripts/run_slurm.sh ./scripts/imbalanced.sh
```

and this might be useful too:

```bash
srun --jobid=JOBID --pty bash
```


## Development

Everything we change from a given notebook when converting it to scripts was justified and documented. The behaviour of the original code was not changed, including not fixing their bugs.