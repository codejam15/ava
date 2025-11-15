
from pydantic import BaseModel
import uuid

class MeetingSummaryCreateRequest(BaseModel):
    meeting_id: uuid.UUID
    summary_text: str
