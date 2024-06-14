from asyncpg import ConnectionDoesNotExistError
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database.session import session
from src.database.models import Gamers, Tournaments, Squads, TournamentSquads
from src.auth.utils_jwt import hash_password
from src.database.schemasDTO import GamersGetDTO, TournamentsGetDTO


async def insert_gamer_db(username: str, password: str, steam_id: str, dota2_id: str, email: str, age: int,
                          status: str = "active") -> dict:
    """
    Crud for registration gamer

    """
    new_gamer = Gamers(username=username,
                       password=hash_password(password),
                       steam_id=steam_id,
                       dota2_id=dota2_id,
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


async def check_user_auth(username: str) -> None:
    """
    Crud for read user by username

    """
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
    """
    Crud for create tournament

    """
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
    """
    Crud for read tournament info

    """
    async with session() as conn:
        stmt = select(Tournaments).filter_by(tournament_name=tournament_name)
        result = await conn.execute(stmt)
        tournament = result.scalars().all()
        result_dto = [TournamentsGetDTO.model_validate(row, from_attributes=True) for row in tournament]
    return result_dto


async def check_gamer_info(gamer_name: str):
    """
    Crud for read gamer info

    """
    async with session() as conn:
        stmt = select(Gamers).filter_by(username=gamer_name)
        result = await conn.execute(stmt)
        gamer = result.scalar_one()
    return gamer


async def create_squad(squad_name: str, about_of_team: str):
    new_squad = Squads(squad_name=squad_name, about_of_team=about_of_team)
    try:
        async with session() as data_db:
            gamer = data_db.add(new_squad)
            await data_db.commit()
    except ConnectionDoesNotExistError:
        return {
            "status": "bad"
        }

    return {
        "status": "ok"
    }


async def squad_info(squad_name: str) -> Squads:
    async with session() as connect:
        stmt = select(Squads).filter_by(squad_name=squad_name)
        result = await connect.execute(stmt)
        squad = result.scalar_one()
    return squad


async def register_squad_on_tournament_and_add_tournament_in_squad(squad_name: str, tournament_name: str) \
        -> dict[str, str]:
    squad = await squad_info(squad_name)  # type: Squads
    try:
        async with session() as db:
            register_squad = await db.scalar(select(Tournaments).filter_by(tournament_name=tournament_name).options(
                selectinload(Tournaments.squads_list))
            )
            register_squad.squads_list.append(squad)

            await db.commit()
    except ConnectionDoesNotExistError:
        return {
            "status": "bad"
        }

    return {
        "status": "ok"
    }


async def info_participants_in_tournament(tournament_name: str) -> list[Tournaments]:
    async with session() as connect_db:
        stmt = select(Tournaments).filter_by(tournament_name=tournament_name). \
            options(selectinload(Tournaments.squads_list))
        squads = await connect_db.scalars(stmt)

    return list(squads)


async def info_squads_with_tournaments(squad_name: str) -> list[Squads]:
    async with session() as connect_db:
        stmt = select(Squads).filter_by(squad_name=squad_name).options(selectinload(Squads.tournaments_list))
        tournaments = await connect_db.scalars(stmt)
    return list(tournaments)
