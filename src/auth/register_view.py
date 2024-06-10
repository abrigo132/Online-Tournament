from fastapi import APIRouter, Depends, Form, HTTPException
from starlette import status

from src.crud.crud import insert_gamer_db
from src.auth.schemas import GamersRegister

router = APIRouter(prefix="/register", tags=["register"])


async def check_register_user(username: str = Form(), password: str = Form(), steam_id: str = Form(),
                              dota2_id: str = Form(),
                              email: str = Form(), age: int = Form(), ):
    db_response: dict = await insert_gamer_db(username, password, steam_id, dota2_id, email, age)
    if db_response["status"] == "bad":
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="К сожалению, произошла ошибка. Попробуйте позднее"
        )
    return username


@router.post("/gamers")
async def response_register_gamers(username: GamersRegister = Depends(check_register_user)):
    return {
        "message": f"Поздравляю,{username}! Вы зарегистрировались, как игрок! Успехов на турнирах",
    }
