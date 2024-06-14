from pydantic import BaseModel, EmailStr


class GamerInfoApiDota(BaseModel):
    steam_id: str
    email: EmailStr
    age: int
    squad_id: int
    dota2_profile: dict[str, str]
