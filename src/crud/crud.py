from asyncpg import ConnectionDoesNotExistError
from sqlalchemy import select

from src.auth.schemas import GamersRegister
from src.database.session import session
from src.database.models import Gamers
from src.auth.utils_jwt import hash_password
from src.database.schemasDTO import GamersGetDTO


async def insert_gamer_db(username: str, password: str, steam_id: str, email: str, age: int,
                          status: str = "active") -> None:
    new_gamer = Gamers(username=username,
                       password=hash_password(password),
                       steam_id=steam_id,
                       email=email,
                       age=age,
                       status=status)
    try:
        async with session() as data_db:
            gamer = data_db.add(new_gamer)
            await data_db.commit()
    except ConnectionDoesNotExistError:
        return {
            "status": "bad"
        }

    return {
        "status": "ok"
    }


async def check_user(username: str) -> None:
    async with session() as session_db:
        stmt = select(Gamers).select_from(Gamers).filter_by(username=username)
        result = await session_db.execute(stmt)
        gamer = result.scalars().all()
    result_dto = [GamersGetDTO.model_validate(row, from_attributes=True) for row in gamer]
    return result_dto
