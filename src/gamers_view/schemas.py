from pydantic import BaseModel


class GamerInfo(BaseModel):
    username: str
    steam_id: str
    email: str
    age: int
    squad_id: int
    win_lose: dict
