from typing import Optional

from pydantic import BaseModel, EmailStr


class GamersRegister(BaseModel):
    """
    Модель для регистрации игроков
    """
    username: str
    email: EmailStr = ""
    password: str
    steam_id: str
    dota2_id: str
    age: int


class GamersAuth(BaseModel):
    """
    Модель для аутентификации игроков
    """
    username: str
    password: str


class TournamentsOwnerRegister(BaseModel):
    """
    Модель для регистрации людей или компаний, которые проводят турниры
    """
    username: str
    email: EmailStr
    password: str
    company: Optional[str]


class TournamentsOwnerAuth(BaseModel):
    """
    Модель аутентификации для людей или компаний, которые проводят турниры
    """
    email: EmailStr
    password: str


class TokenInfo(BaseModel):
    """
    Модель информации о токене
    """
    access_token: str
    token_type: str
