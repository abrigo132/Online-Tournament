from fastapi import APIRouter, Depends

from src.crud.crud import check_gamer_info
from src.gamers_view.schemas import GamerInfo

router = APIRouter(prefix="/gamers", tags=["Gamers"])


@router.get("/about/{gamer_name}")
def return_gamer_info(gamer_info: GamerInfo = Depends(check_gamer_info)):
    """
    View для выведения информации на карточку игрока. Содержит информацию о steam_id, email, age and squad_id

    """
    return {
        "steam_id": gamer_info.steam_id,
        "email": gamer_info.email,
        "age": gamer_info.age,
        "squad_id": gamer_info.squad_id
    }
