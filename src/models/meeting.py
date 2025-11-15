from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class MeetingCreateRequest(BaseModel):
    title: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    created_by: uuid.UUID
    external_meeting_id: Optional[str] = None
