from asyncpg import ConnectionDoesNotExistError
from sqlalchemy import select

from src.database.session import session
from src.database.models import Gamers, Tournaments
from src.auth.utils_jwt import hash_password
from src.database.schemasDTO import GamersGetDTO, TournamentsGetDTO


async def insert_gamer_db(username: str, password: str, steam_id: str, email: str, age: int,
                          status: str = "active") -> dict:
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


async def insert_tournament_into_db(tournament_name: str,
                                    number_of_teams: int,
                                    tournament_type: str,
                                    finished_at: str) -> dict:
    new_tournament = Tournaments(tournament_name=tournament_name,
                                 number_of_teams=number_of_teams,
                                 tournament_type=tournament_type,
                                 finished_at=finished_at)
    try:
        async with session() as conn:
            tournament = conn.add(new_tournament)
            await conn.commit()
    except ConnectionDoesNotExistError:
        return {
            "status": "bad"
        }
    return {
        "status": "ok"
    }


async def check_tournament_info(tournament_name: str) -> list:
    async with session() as conn:
        stmt = select(Tournaments).filter_by(id=tournament_name)
        result = await conn.execute(stmt)
        tournament = result.scalars().all()
        result_dto = [TournamentsGetDTO.model_validate(row, from_attributes=True) for row in tournament]
        return result_dto
