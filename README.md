# CremaBench
**Intelligent Data. Smarter Performance.**

Multi-engine data analytics and benchmarking platform (Pandas, Polars, DuckDB, FireDucks).

## Phase 1 setup

### Backend (run inside `cremabench/backend`)
```
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Mac/Linux
pip install -r requirements.txt
pip install -r requirements-optional.txt   # optional, FireDucks (may fail on Windows)
copy ..\.env.example .env       # Mac/Linux: cp ../.env.example .env
uvicorn app.main:app --reload --port 8000
```
Open http://localhost:8000/api/health

### Frontend (run inside `cremabench/frontend`)
```
npm install
npm run dev
```
Open http://localhost:5173

### Tests (inside `cremabench/backend`)
```
pytest
```
