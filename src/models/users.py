from typing import Optional
from pydantic import BaseModel, EmailStr
import uuid

class UserCreateRequest(BaseModel):
    username: str
    display_name: Optional[str] = None
    team_id: Optional[uuid.UUID] = None
    role: Optional[str] = None
    email: Optional[EmailStr] = None
