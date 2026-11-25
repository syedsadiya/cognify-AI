from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Dataset
from app.schemas.dataset import DatasetOut, PreviewOut, ProfileOut
from app.services import dataset_service, profiling_service
from app.services.dataset_service import DatasetError

router = APIRouter(tags=["datasets"])


def fail(error: DatasetError):
    return HTTPException(status_code=error.status_code, detail=error.message)


@router.post("/datasets/upload", response_model=DatasetOut, status_code=201)
def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        return dataset_service.save_upload(db, file)
    except DatasetError as e:
        raise fail(e)


@router.get("/datasets", response_model=List[DatasetOut])
def list_datasets(db: Session = Depends(get_db)):
    return db.query(Dataset).order_by(Dataset.id.desc()).all()


@router.get("/datasets/{dataset_id}", response_model=DatasetOut)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    try:
        return dataset_service.get_dataset(db, dataset_id)
    except DatasetError as e:
        raise fail(e)


@router.get("/datasets/{dataset_id}/preview", response_model=PreviewOut)
def preview(dataset_id: int, rows: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    try:
        dataset = dataset_service.get_dataset(db, dataset_id)
        df = dataset_service.load_dataset(dataset)
    except DatasetError as e:
        raise fail(e)
    return profiling_service.preview_dataframe(df, rows)


@router.get("/datasets/{dataset_id}/profile", response_model=ProfileOut)
def profile(dataset_id: int, db: Session = Depends(get_db)):
    try:
        dataset = dataset_service.get_dataset(db, dataset_id)
        df = dataset_service.load_dataset(dataset)
    except DatasetError as e:
        raise fail(e)
    return profiling_service.profile_dataframe(df)


@router.get("/datasets/{dataset_id}/download")
def download(dataset_id: int, db: Session = Depends(get_db)):
    try:
        dataset = dataset_service.get_dataset(db, dataset_id)
        path = dataset_service.dataset_path(dataset)
    except DatasetError as e:
        raise fail(e)
    return FileResponse(path, filename=dataset.original_name)


@router.delete("/datasets/{dataset_id}", status_code=204)
def delete(dataset_id: int, db: Session = Depends(get_db)):
    try:
        dataset = dataset_service.get_dataset(db, dataset_id)
    except DatasetError as e:
        raise fail(e)
    dataset_service.delete_dataset(db, dataset)
    return Response(status_code=204)
