# Swarm Simulation MVP

A graph-first multi-agent simulation MVP with deterministic run loops.

## Run Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -e .
pytest tests -v
python run.py
```

## Run Frontend
```bash
cd frontend
npm install
npm test
npm run dev
```
