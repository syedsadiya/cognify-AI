from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import UserSetting
from app.schemas.settings import SettingUpdate

router = APIRouter(tags=["settings"])

# Only these keys can be saved, with their default values and allowed values.
ALLOWED = {
    "default_engine": {"default": "auto", "options": ["auto", "pandas", "polars", "duckdb", "fireducks"]},
    "repetitions": {"default": "5", "options": ["3", "5", "10"]},
    "warmup_runs": {"default": "1", "options": ["1", "2", "3"]},
}


@router.get("/settings")
def get_settings(db: Session = Depends(get_db)):
    result = {}
    for key, info in ALLOWED.items():
        result[key] = info["default"]
    for row in db.query(UserSetting).all():
        if row.key in ALLOWED:
            result[row.key] = row.value
    return result


@router.put("/settings")
def update_setting(item: SettingUpdate, db: Session = Depends(get_db)):
    if item.key not in ALLOWED:
        raise HTTPException(status_code=400, detail="Unknown setting: " + item.key)
    if item.value not in ALLOWED[item.key]["options"]:
        raise HTTPException(status_code=400, detail="Invalid value for " + item.key)

    row = db.get(UserSetting, item.key)
    if row is None:
        row = UserSetting(key=item.key, value=item.value)
        db.add(row)
    else:
        row.value = item.value
    db.commit()
    return {"key": item.key, "value": item.value}
