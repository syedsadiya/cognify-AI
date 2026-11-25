from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Dataset, BenchmarkRun
from app.engines.registry import engine_status
from app.schemas.dashboard import DashboardSummary

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard/summary", response_model=DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db)):
    engines = []
    for e in engine_status():
        if e["available"]:
            engines.append(e["name"])

    recent = db.query(BenchmarkRun).order_by(BenchmarkRun.id.desc()).limit(5).all()

    return {
        "total_datasets": db.query(Dataset).count(),
        "total_benchmark_runs": db.query(BenchmarkRun).count(),
        "available_engines": engines,
        "recent_runs": recent,
    }
