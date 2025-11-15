from pydantic import BaseModel

class TeamCreateRequest(BaseModel):
    name: str
