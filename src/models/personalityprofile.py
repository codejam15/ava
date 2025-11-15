from pydantic import BaseModel
import uuid
from typing import Optional

class PersonalityProfileCreateRequest(BaseModel):
    user_id: uuid.UUID
    summary: str


class PersonalityProfileUpdateRequest(BaseModel):
    summary: Optional[str] = None
