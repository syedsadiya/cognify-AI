from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class DatasetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_name: str
    file_type: str
    size_bytes: int
    row_count: int
    column_count: int
    uploaded_at: datetime


class ColumnProfile(BaseModel):
    name: str
    dtype: str
    missing: int
    missing_pct: float
    unique: int


class ProfileOut(BaseModel):
    rows: int
    columns_count: int
    total_missing: int
    duplicate_rows: int
    columns: List[ColumnProfile]
    statistics: Dict[str, Dict[str, Optional[float]]]


class PreviewOut(BaseModel):
    columns: List[str]
    rows: List[List[Any]]
    total_rows: int
