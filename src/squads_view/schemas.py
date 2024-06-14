from datetime import datetime

from pydantic import BaseModel


class NewSquad(BaseModel):
    id: int
    squad_name: str
    about_of_team: str
    created_at: datetime
