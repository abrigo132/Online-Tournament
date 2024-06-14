from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from src.crud.crud import create_squad, info_squads_with_tournaments, add_gamer_into_squad
from src.squads_view.schemas import NewSquad
from src.database.models import Squads

router = APIRouter(prefix="/squad", tags=["Squad"])


async def check_register_new_squad(squad_info: NewSquad):
    response_db: dict[str, str] = await create_squad(squad_info.squad_name, squad_info.about_of_team)
    if response_db.get("status") == "bad":
        return HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,
                             detail="Произошла ошибка, попробуйте позднее")
    return squad_info.squad_name


@router.post("/add/")
def add_new_squad(squad_name: str = Depends(check_register_new_squad)):
    return {
        "message": f"Поздравляю, вы зарегистрировали команду с названием {squad_name=}"
    }


async def check_info_squad(squad_name: str) -> list[Squads]:
    response_db = await info_squads_with_tournaments(squad_name)
    return response_db


@router.post("/info/{squad_name}")
async def squad_info(squad_name: list[Any] = Depends(check_info_squad)):
    tournaments = []
    gamers = []
    for value in squad_name[0].tournaments_list:
        tournaments.append(value.tournament_name)
    for value in squad_name[0].gamers:
        gamers.append(value.username)
    return {
        "squad_name": squad_name[0].squad_name,
        "about": squad_name[0].about_of_team,
        "created_at": squad_name[0].created_at,
        "members": gamers,
        "tournaments": tournaments,
    }


async def check_add_gamer_into_squad(gamer_name: str, squad_name: str):
    result_db = await add_gamer_into_squad(gamer_name=gamer_name, squad_name=squad_name)
    return gamer_name, squad_name


@router.post("/add/gamer/squad")
def add_gamer_squad(check_info=Depends(check_add_gamer_into_squad)):
    return {
        "message": f"Поздравляю {check_info[0]}, вы вступили в команду: {check_info[1]}"
    }
