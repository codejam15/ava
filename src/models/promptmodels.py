from pydantic import BaseModel

class TranscriptPromptModel(BaseModel):
    transcript: str
    attendees: str
    meeting_date: str
    meeting_time: str
