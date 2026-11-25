from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dataset_id: int
    operation: str
    repetitions: int
    status: str
    created_at: datetime
