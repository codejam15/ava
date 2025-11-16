import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MeetingCreateRequest(BaseModel):
    title: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    created_by: uuid.UUID
    external_meeting_id: Optional[str] = None


class ConfluenceTemplateResponse(BaseModel):
    meeintg_id: str
    title: str
    meeting_date: str
    summary: str
    actionable: bool
    attendees: list[str]


class MeetingSummaryCreateRequest(BaseModel):
    meeting_id: uuid.UUID
    summary_text: str


class MeetingTranscriptCreateRequest(BaseModel):
    meeting_id: uuid.UUID
    transcript_text: str
