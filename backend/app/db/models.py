from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


def now():
    return datetime.now(timezone.utc)


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)
    original_name = Column(String, nullable=False)
    stored_name = Column(String, nullable=False)  # safe server-side filename
    file_type = Column(String, nullable=False)    # csv / xlsx / parquet
    size_bytes = Column(Integer, default=0)
    row_count = Column(Integer, default=0)
    column_count = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=now)

    runs = relationship("BenchmarkRun", back_populates="dataset")


class BenchmarkRun(Base):
    __tablename__ = "benchmark_runs"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    operation = Column(String, nullable=False)
    repetitions = Column(Integer, default=5)
    status = Column(String, default="completed")
    environment = Column(String, default="")  # JSON text: OS, CPU, library versions
    created_at = Column(DateTime, default=now)

    dataset = relationship("Dataset", back_populates="runs")
    metrics = relationship("EngineMetric", back_populates="run")


class EngineMetric(Base):
    __tablename__ = "engine_metrics"

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("benchmark_runs.id"), nullable=False)
    engine = Column(String, nullable=False)
    load_time_ms = Column(Float)
    median_time_ms = Column(Float)
    std_time_ms = Column(Float)
    memory_mb = Column(Float)
    throughput_rows_s = Column(Float)
    cpu_percent = Column(Float)
    output_valid = Column(Boolean, default=True)

    run = relationship("BenchmarkRun", back_populates="metrics")


class UserSetting(Base):
    __tablename__ = "user_settings"

    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=now)
