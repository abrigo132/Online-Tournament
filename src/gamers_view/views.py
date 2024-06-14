import json
from typing import Any

from fastapi import APIRouter, Depends

from src.crud.crud import check_gamer_info
from src.gamers_view.schemas import GamerInfo
from src.dota2_api.gamers import get_info_gamer_wl

router = APIRouter(prefix="/gamers", tags=["Gamers"])


@router.get("/about/{gamer_name}/")
async def return_gamer_info(gamer_info=Depends(check_gamer_info),
                            ) -> dict[str, Any]:
    """
    View для выведения информации на карточку игрока. Содержит информацию о steam_id, email, age, squad_id,
    dota2_profile

    """
    win_lose_info: dict[str, Any] = await get_info_gamer_wl(gamer_info.dota2_id)
    return {
        "steam_id": gamer_info.steam_id,
        "email": gamer_info.email,
        "age": gamer_info.age,
        "squad": gamer_info.squad.squad_name,
        "dota2_profile": {"win": win_lose_info[0]["win"],
                          "lose": win_lose_info[0]["lose"],
                          "rank_tier": win_lose_info[1]["rank_tier"],
                          "leaderboard_rank": win_lose_info[1]["leaderboard_rank"]},
    }
