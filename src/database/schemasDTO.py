from pydantic import BaseModel


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
