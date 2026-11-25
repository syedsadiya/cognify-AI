from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import BenchmarkRun
from app.schemas.benchmark import RunOut

router = APIRouter(tags=["benchmarks"])


@router.get("/benchmarks/history", response_model=List[RunOut])
def benchmark_history(db: Session = Depends(get_db)):
    return db.query(BenchmarkRun).order_by(BenchmarkRun.id.desc()).all()
