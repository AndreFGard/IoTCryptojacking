

```bash
bash start.sh
source .venv


sbatch scripts/run_slurm.sh ./scripts/imbalanced.sh
```

and this might be useful too:

```bash
srun --jobid=JOBID --pty bash
```


