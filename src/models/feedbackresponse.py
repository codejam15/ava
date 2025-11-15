from pydantic import BaseModel
import uuid

class FeedbackResponseCreateRequest(BaseModel):
    feedback_id: uuid.UUID
    responder_id: uuid.UUID
    response_text: str
