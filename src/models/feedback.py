import uuid

from pydantic import BaseModel, Field


class FeedbackPromptModel(BaseModel):
    transcript: str = Field(description="The full transcript of the meeting.")
    target_user_id: uuid.UUID = Field(
        description="The unique identifier of the user to provide feedback for."
    )


class FeedbackEventModel(BaseModel):
    meeting_id: uuid.UUID = Field(description="The unique identifier of the meeting.")
    target_id: uuid.UUID = Field(
        description="The unique identifier of the user to provide feedback for."
    )
    text: str = Field(
        description="The constructive feedback text provided to the user."
    )


class FeedbackResponseModel(BaseModel):
    feedback_id: uuid.UUID = Field(description="The unique identifier of the feedback.")
    issuer_id: uuid.UUID = Field(
        description="The unique identifier of the user who provided the feedback."
    )
    text: str = Field(
        description="The response text from the user who received the feedback."
    )


class PersonalityProfileModel(BaseModel):
    user_id: uuid.UUID = Field(description="The unique identifier of the user.")
    profile_id: uuid.UUID = Field(
        description="The unique identifier of the personality profile."
    )
    summary: str = Field(
        description="A brief summary of the user's personality, this is based on analysis of their previous responses to feedback."
    )
