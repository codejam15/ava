from pydantic import BaseModel

# This model is for confluence page
class BaseMeetingResponseModel(BaseModel):
    meeintg_id: str
    title: str
    meeting_date: str
    actionable: bool
    attendees: list[str]
    summary: str

# This model is used for teams message
class GroupResponseModel(BaseMeetingResponseModel):
    group_feedback: str
