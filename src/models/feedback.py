from pydantic import BaseModel
import uuid

class FeedbackEventCreateRequest(BaseModel):
    meeting_id: uuid.UUID
    target_user_id: uuid.UUID
    feedback_text: str
