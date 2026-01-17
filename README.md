# sublevel-stoping-model

Modelo de optimización Sublevel Stoping (Python + Gurobi) con inputs/outputs en Excel.

## Estructura
- `src/sublevel_stoping_model/`: código del modelo (sets, params, vars, constraints, reporting)
- `data/input/`: Excel(s) de entrada
- `data/output/`: resultados (no se versiona)
- `scripts/run_model.py`: script de ejecución

## Cómo correr
```bash
python -m venv .venv
source .venv/bin/activate  # mac/linux
pip install -r requirements.txt
python scripts/run_model.py
