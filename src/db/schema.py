import uuid
from datetime import UTC, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


def nowutc() -> datetime:
    return datetime.now(UTC)


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    display_name: Optional[str] = None
    team_id: Optional[uuid.UUID] = None
    role: Optional[str] = None
    email: Optional[str] = Field(default=None, unique=True)
    created_at: datetime = Field(default_factory=nowutc)


class Team(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, index=True)
    space_id: str
    parent_id: str


class Meeting(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    created_by: uuid.UUID = Field(foreign_key="user.id")
    external_meeting_id: Optional[str] = None
    created_at: datetime = Field(default_factory=nowutc)


class MeetingTranscript(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    meeting_id: uuid.UUID = Field(foreign_key="meeting.id")
    transcript_text: str
    created_at: datetime = Field(default_factory=nowutc)


class MeetingSummary(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    meeting_id: uuid.UUID = Field(foreign_key="meeting.id")
    summary_text: str
    created_at: datetime = Field(default_factory=nowutc)


class FeedbackEvent(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    meeting_id: uuid.UUID = Field(foreign_key="meeting.id")
    target_user_id: uuid.UUID = Field(foreign_key="user.id")
    feedback_text: str
    created_at: datetime = Field(default_factory=nowutc)


class FeedbackResponse(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    feedback_id: uuid.UUID = Field(foreign_key="feedbackevent.id")
    responder_id: uuid.UUID = Field(foreign_key="user.id")
    response_text: str
    created_at: datetime = Field(default_factory=nowutc)


class PersonalityProfile(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", unique=True)
    summary: str
    updated_at: datetime = Field(default_factory=nowutc)
