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


class MeetingResponseModel(BaseModel):
    title: str
    meeting_date: str
    meeting_time: str
    attendees: str
    updates: str
    roadblocks: str
    nextsteps: str
    notes: str
    group_feedback: str


class TranscriptPromptModel(BaseModel):
    transcript: str
    meeting_date: str
    meeting_time: str
    attendees: Optional[list[str]] = None


class MeetingSummaryCreateRequest(BaseModel):
    meeting_id: uuid.UUID
    summary_text: str


class MeetingTranscriptCreateRequest(BaseModel):
    meeting_id: uuid.UUID
    transcript_text: str
