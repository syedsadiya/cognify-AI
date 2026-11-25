from typing import List
from pydantic import BaseModel
from app.schemas.benchmark import RunOut


class DashboardSummary(BaseModel):
    total_datasets: int
    total_benchmark_runs: int
    available_engines: List[str]
    recent_runs: List[RunOut]
