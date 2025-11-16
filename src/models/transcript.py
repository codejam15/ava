from pydantic import BaseModel

class MeetingTranscript(BaseModel):
    transcript: str
