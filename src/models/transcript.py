from pydantic import BaseModel
import uuid

class MeetingTranscriptCreateRequest(BaseModel):
    meeting_id: uuid.UUID
    transcript_text: str
