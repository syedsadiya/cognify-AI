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
Set `XAI_API_KEY` in `backend/.env` to enable Grok chat. Keep the key private and do not commit it.
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

## Phase 2 additions
- Database: SQLite via SQLAlchemy (tables are created automatically on startup).
- API: `/api/dashboard/summary`, `/api/datasets`, `/api/benchmarks/history`, `/api/settings`.
- Frontend: sidebar layout, routing for all 11 pages, working Dashboard and Settings.

## Phase 3 additions
- Upload CSV / XLSX / Parquet (size and type validation, safe server-side filenames).
- Preview, profiling (types, missing values, duplicates, statistics), download, delete.
- API: `POST /api/datasets/upload`, `GET /api/datasets/{id}/preview`, `/profile`, `/download`, `DELETE /api/datasets/{id}`.
- Sample data in `sample_data/`. Create larger files (100k and 1M rows) from `backend`:
  `python scripts/generate_sample_data.py --all`

## AI assistant
- Open **AI Data Assistant** in the app to chat with Grok (`grok-4.7` by default).
- Set `XAI_API_KEY` in `backend/.env` and restart the backend. `XAI_MODEL` can override the model. OpenAI is also supported through `OPENAI_API_KEY` and `OPENAI_MODEL`; XAI settings take precedence if both keys are present.
- Optional dataset context includes its profile and numeric statistics; this profile is sent to the configured AI provider with the chat request.
- Chat API: `POST /api/assistant/chat`.
