from datetime import datetime

from pydantic import BaseModel, EmailStr


class GamersPostDTO(BaseModel):
    """
    Модель для преобразования ответа sqlalchemy в pydantic модель Data transfer object

    """
    id: int


class GamersGetDTO(GamersPostDTO):
    """
    Модель для преобразования ответа sqlalchemy в pydantic модель Data transfer object

    """
    username: str
    password: bytes
    status: str
    email: EmailStr


class TournamentsPostDTO(BaseModel):
    id: int


class TournamentsGetDTO(TournamentsPostDTO):
    tournament_name: str
    teams: int = None
    tournament_type: str
    created_at: datetime
    finished_at: str
