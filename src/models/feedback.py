import uuid
from typing import Optional

from pydantic import BaseModel


class FeedbackEventCreateRequest(BaseModel):
    meeting_id: uuid.UUID
    target_user_id: uuid.UUID
    feedback_text: str


class FeedbackResponseCreateRequest(BaseModel):
    feedback_id: uuid.UUID
    responder_id: uuid.UUID
    response_text: str


class PersonalityProfileCreateRequest(BaseModel):
    user_id: uuid.UUID
    summary: str


class PersonalityProfileUpdateRequest(BaseModel):
    summary: Optional[str] = None
