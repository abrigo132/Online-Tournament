from fastapi import APIRouter, Depends

from src.crud.crud import check_gamer_info
from src.gamers_view.schemas import GamerInfo
from src.dota2_api.gamers import get_info_gamer_wl

router = APIRouter(prefix="/gamers", tags=["Gamers"])


@router.get("/about/{gamer_name}/")
async def return_gamer_info(gamer_info: GamerInfo = Depends(check_gamer_info),
                            win_lose_info: dict = Depends(get_info_gamer_wl)):
    """
    View для выведения информации на карточку игрока. Содержит информацию о steam_id, email, age and squad_id

    """
    return {
        "steam_id": gamer_info.steam_id,
        "email": gamer_info.email,
        "age": gamer_info.age,
        "squad_id": gamer_info.squad_id,
        "dota2_profile": {"win": win_lose_info[0]["win"],
                          "lose": win_lose_info[0]["lose"],
                          "rank_tier": win_lose_info[1]["rank_tier"],
                          "leaderboard_rank": win_lose_info[1]["leaderboard_rank"]},
    }
