from sqlalchemy import select

from src.auth.schemas import GamersRegister, GamersAuth
from src.database.session import session
from src.database.models import Gamers
from src.auth.utils_jwt import hash_password
from src.database.schemasDTO import GamersGetDTO


async def insert_gamer_db(data_user: GamersRegister) -> None:
    new_gamer = Gamers(username=data_user.username,
                       password=hash_password(data_user.password),
                       steam_id=data_user.steam_id,
                       email=data_user.email,
                       age=data_user.age,
                       status="active")
    async with session() as data_db:
        gamer = data_db.add(new_gamer)
        await data_db.commit()

    return data_user


async def check_user(username: str) -> None:
    async with session() as session_db:
        stmt = select(Gamers).select_from(Gamers).filter_by(username=username)
        result = await session_db.execute(stmt)
        gamer = result.scalars().all()
    result_dto = [GamersGetDTO.model_validate(row, from_attributes=True) for row in gamer]
    return result_dto
