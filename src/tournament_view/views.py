from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.tournament_view.schemas import NewTournament, TournamentInfo
from src.crud.crud import (insert_tournament_into_db, check_tournament_info,
                           register_squad_on_tournament_and_add_tournament_in_squad, info_participants_in_tournament)

router = APIRouter(prefix="/tournament", tags=["tournament"])


async def check_register_new_tournament(tournament_data: NewTournament) -> str:
    response_db: dict = await insert_tournament_into_db(tournament_data.tournament_name,
                                                        tournament_data.number_of_teams,
                                                        tournament_data.tournament_type,
                                                        tournament_data.finished_at)
    if response_db.get("status") == "bad":
        return HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,
                             detail="Произошла ошибка, попробуйте позднее")
    return tournament_data.tournament_name


@router.post("/add/")
def add_new_tournament(tournament_name: str = Depends(check_register_new_tournament)):
    return {
        "message": f"Поздравляю, вы зарегистрировали свой турнир с названием {tournament_name}"
    }


async def about_tournament(tournament_data: TournamentInfo):
    response_db = await check_tournament_info(tournament_data.name)
    return response_db


async def about_squads_in_tournament(tournament_name: str):
    squad_list = await info_participants_in_tournament(tournament_name)
    return squad_list


@router.post("/info/{tournament_name}/")
def get_tournament_by_id(squads_info: list = Depends(about_squads_in_tournament)):
    squads_in_tournaments = []
    for value in squads_info[0].squads_list:
        squads_in_tournaments.append(value.squad_name)
    return {
        "name": squads_info[0].tournament_name,
        "teams": squads_info[0].number_of_teams,
        "type": squads_info[0].tournament_type,
        "created_at": squads_info[0].created_at,
        "finished_at": squads_info[0].finished_at,
        "participants": squads_in_tournaments

    }


@router.post("/register/squad/")
async def register_squad_on_tournament(tournament_name: str, squad_name: str) -> dict:
    add_squad_on_tournament: dict[str, str] = await register_squad_on_tournament_and_add_tournament_in_squad(
        tournament_name=tournament_name,
        squad_name=squad_name)
    if add_squad_on_tournament.get("status") == "bad":
        return {
            HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Произошла ошибка, попробуйте позднее"
            )
        }
    else:
        return {
            "message": f"Поздравляю, ваша команда {squad_name} зарегистрировалась на турнир {tournament_name}. Успехов!"
        }
