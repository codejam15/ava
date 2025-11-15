from pydantic import BaseModel


class ConfluenceTemplateResponse(BaseModel):
    id: str
    name: str
    body: str
    created_at: str
    updated_at: str
