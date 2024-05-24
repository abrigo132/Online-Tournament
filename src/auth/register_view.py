from fastapi import APIRouter, Depends

from src.auth.schemas import GamersRegister
from src.database import session
from src.crud.crud import insert_gamer_db

router = APIRouter(prefix="/register", tags=["register"])


@router.post("/gamers")
async def response_register_gamers(data: GamersRegister = Depends(insert_gamer_db)):
    return {
        "message": f"Поздравляю,{data.username}! Вы зарегистрировались, как игрок! Успехов на турнирах",
    }
