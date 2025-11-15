from pydantic import BaseModel

# This model is for confluence page
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




# print(teams_message_template) # Use this line to see the final output
