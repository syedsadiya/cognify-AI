import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from openai import OpenAI, OpenAIError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.database import get_db
from app.schemas.assistant import ChatRequest, ChatResponse
from app.services import dataset_service, profiling_service
from app.services.dataset_service import DatasetError

logger = logging.getLogger(__name__)
router = APIRouter(tags=["assistant"])


def dataset_context(db: Session, dataset_id: int) -> str:
    try:
        dataset = dataset_service.get_dataset(db, dataset_id)
        dataframe = dataset_service.load_dataset(dataset)
    except DatasetError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message) from error

    profile = profiling_service.profile_dataframe(dataframe)
    profile["columns"] = profile["columns"][:100]
    profile["statistics"] = dict(list(profile["statistics"].items())[:20])
    return (
        "Selected dataset: %s\nProfile (column details are limited to 100 columns and "
        "statistics to 20 numeric columns):\n%s"
        % (dataset.original_name, json.dumps(profile, allow_nan=False))
    )


@router.post("/assistant/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    if settings.xai_api_key:
        client = OpenAI(api_key=settings.xai_api_key, base_url=settings.xai_base_url)
        model = settings.xai_model
    elif settings.openai_api_key:
        client = OpenAI(api_key=settings.openai_api_key)
        model = settings.openai_model
    else:
        raise HTTPException(
            status_code=503,
            detail="AI chat is not configured. Add XAI_API_KEY (Grok) or OPENAI_API_KEY to backend/.env and restart the backend.",
        )

    system_prompt = (
        "You are CremaBench's AI data assistant. Help users understand datasets, data "
        "quality, analysis, and benchmarking. Be clear about uncertainty and do not claim "
        "to have computed values that are not present in the supplied context."
    )
    if request.dataset_id is not None:
        system_prompt += "\n\n" + dataset_context(db, request.dataset_id)

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(item.model_dump() for item in request.history[-20:])
    messages.append({"role": "user", "content": request.message})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
    except OpenAIError as error:
        logger.exception("AI assistant request failed")
        raise HTTPException(
            status_code=502,
            detail="The AI service could not complete your request. Check the API configuration and try again.",
        ) from error

    answer = response.choices[0].message.content
    if not answer:
        raise HTTPException(status_code=502, detail="The AI service returned an empty response.")
    return ChatResponse(answer=answer)
