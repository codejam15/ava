from pydantic import BaseModel


class ConfluenceTemplateResponse(BaseModel):
    meeintg_id: str
    title: str
    meeting_date: str
    summary: str
    actionable: bool
    attendees: list[str]
