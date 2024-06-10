import httpx

from config import settings
from httpx import AsyncClient
from src.crud.crud import check_gamer_info

"""
Подсказка по ранжированию в дота2
Первые цифры:
1 - Рекрут
2 - Страж
3 - Рыцарь
4 - Герой
5 - Легенда
6 - Властелин
7 - Божество
8 - Бессмертный

"""


async def get_info_gamer_wl(gamer_name: str):
    dota_id = await check_gamer_info(gamer_name)
    async with httpx.AsyncClient() as connect:
        url_win_lose = f"https://api.opendota.com/api/players/{dota_id.dota2_id}/wl"
        url_info_player = f"https://api.opendota.com/api/players/{dota_id.dota2_id}"
        result_win_lose = await connect.get(url=url_win_lose)
        result_info_player = await connect.get(url=url_info_player)
    return result_win_lose.json(), result_info_player.json()

