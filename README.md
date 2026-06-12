# IoT Cryptojacking Detection

Reproduction and evaluation of a lightweight network-traffic-based cryptojacking detection system for IoT environments, as proposed in the reference paper. Includes experiments on the original dataset and on the new *Cryptojacking Network Traffic 2021* (CNT21) dataset.

## Setup

Requires Python 3.11+ and [`uv`](https://github.com/astral-sh/uv), as well as a GNU/Linux environment.

```bash

bash start.sh            # installs uv, creates .venv, installs dependencies
source .venv/bin/activate
mkdir -p logs
```

`start.sh` is equivalent to:
```bash
uv venv -p 3.11 && uv pip install -e .
```

## Running

Each experiment has two steps which save and recover artifacts: **dataset** (feature extraction) and **ml** (model training/eval). Scripts prefixed `run_slurm_*` submit to a SLURM cluster; plain `.sh` scripts run locally. For example:

### Reference paper — all scenarios (local)
```bash
sbatch scripts/all_scenarios_1.sh
```


## Project layout

| Path | Description |
|------|-------------|
| `src/paper/` | Modules reproducing the reference paper's pipeline |
| `src/our_dataset/` | Pipeline adapted for the CNT21 dataset |
| `scripts/` | Shell entry-points (dataset + ML steps, local + SLURM variants) |
| `notebooks/` | Exploratory analysis |
| `report/` | Typst source for the final report |

## Development

Everything we change from a given notebook when converting it to this new structure is documented. The behaviour of the original code was not changed, including not fixing problems, most of which were documented in the report.