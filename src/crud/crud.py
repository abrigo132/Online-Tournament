from sqlalchemy import select

from src.auth.schemas import GamersRegister, GamersAuth
from src.database.session import session
from src.database.models import Gamers
from src.auth.utils_jwt import hash_password


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
        stmt = select(Gamers).filter_by(username=username)
        result = await session_db.execute(stmt)
        gamer = result.scalars().first()
    print(gamer)
    return gamer
