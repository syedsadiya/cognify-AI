import logging
import os
import uuid
import pandas as pd
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.models import Dataset, BenchmarkRun, EngineMetric

logger = logging.getLogger(__name__)

ALLOWED_TYPES = {".csv": "csv", ".xlsx": "xlsx", ".parquet": "parquet"}
CHUNK_SIZE = 1024 * 1024  # 1 MB


class DatasetError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def upload_dir():
    return settings.upload_dir


def clean_name(filename):
    """Keep only the file name (no folders) and limit its length."""
    name = os.path.basename((filename or "").replace("\\", "/"))
    return name[:150] or "dataset"


def load_dataframe(path, file_type):
    if file_type == "csv":
        try:
            df = pd.read_csv(path)
        except UnicodeDecodeError:
            df = pd.read_csv(path, encoding="latin-1")
    elif file_type == "xlsx":
        df = pd.read_excel(path)
    else:
        df = pd.read_parquet(path)
    df.columns = [str(c) for c in df.columns]
    return df


def save_upload(db: Session, upload):
    original = clean_name(upload.filename)
    ext = os.path.splitext(original)[1].lower()
    if ext not in ALLOWED_TYPES:
        raise DatasetError("Unsupported file type. Please upload a CSV, Excel (.xlsx) or Parquet file.")

    folder = upload_dir()
    folder.mkdir(parents=True, exist_ok=True)
    stored_name = uuid.uuid4().hex + ext  # safe server-side name
    path = folder / stored_name
    max_bytes = settings.max_upload_mb * 1024 * 1024
    file_type = ALLOWED_TYPES[ext]
    size = 0

    try:
        with open(path, "wb") as f:
            while True:
                chunk = upload.file.read(CHUNK_SIZE)
                if not chunk:
                    break
                size += len(chunk)
                if size > max_bytes:
                    raise DatasetError(
                        "File is too large. Maximum size is %d MB." % settings.max_upload_mb, 413
                    )
                f.write(chunk)

        if size == 0:
            raise DatasetError("The file is empty.")

        try:
            df = load_dataframe(path, file_type)
        except Exception:
            logger.exception("Could not read uploaded file %s", original)
            raise DatasetError(
                "The file could not be read. Check that it is a valid CSV, Excel or Parquet file."
            )

        if df.shape[0] == 0 or df.shape[1] == 0:
            raise DatasetError("The dataset has no data rows or no columns.")
    except Exception:
        if path.exists():
            path.unlink()  # clean up the partial file
        raise

    dataset = Dataset(
        original_name=original,
        stored_name=stored_name,
        file_type=file_type,
        size_bytes=size,
        row_count=int(df.shape[0]),
        column_count=int(df.shape[1]),
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    logger.info("Dataset %s uploaded (%d rows)", dataset.id, dataset.row_count)
    return dataset


def get_dataset(db: Session, dataset_id: int):
    dataset = db.get(Dataset, dataset_id)
    if dataset is None:
        raise DatasetError("Dataset not found.", 404)
    return dataset


def dataset_path(dataset):
    path = upload_dir() / dataset.stored_name
    if not path.exists():
        raise DatasetError("The dataset file is missing on the server.", 404)
    return path


def load_dataset(dataset):
    return load_dataframe(dataset_path(dataset), dataset.file_type)


def delete_dataset(db: Session, dataset):
    for run in db.query(BenchmarkRun).filter(BenchmarkRun.dataset_id == dataset.id).all():
        for metric in db.query(EngineMetric).filter(EngineMetric.run_id == run.id).all():
            db.delete(metric)
        db.delete(run)
    path = upload_dir() / dataset.stored_name
    if path.exists():
        path.unlink()
    db.delete(dataset)
    db.commit()
