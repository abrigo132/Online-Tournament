from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.tournament_view.schemas import NewTournament, TournamentInfo
from src.crud.crud import insert_tournament_into_db, check_tournament_info

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


async def about_tournament(tournament_data: NewTournament):
    response_db = await check_tournament_info(tournament_data.tournament_name)
    

@router.get("/info/{tournament_name}/")
def get_tournament_by_id(tournament_name: TournamentInfo = Depends(about_tournament)):
    return {
        tournament_name
    }
