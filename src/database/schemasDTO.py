from pydantic import BaseModel


class GamersPostDTO(BaseModel):
    id: int


class GamersGetDTO(GamersPostDTO):
    username: str
    hashed_password: bytes
