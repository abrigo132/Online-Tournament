import httpx

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


async def get_info_gamer_wl(dota2_id: str) -> dict[str, str]:
    """
    API request for info player about win_lose, ranktier leaderboard, result last 5 matches

    """
    async with httpx.AsyncClient() as connect:
        url_win_lose = f"https://api.opendota.com/api/players/{dota2_id}/wl"
        url_info_player = f"https://api.opendota.com/api/players/{dota2_id}"
        url_info_last_matches = f"https://api.opendota.com/api/players/{dota2_id}/matches"
        result_win_lose = await connect.get(url=url_win_lose)
        result_info_player = await connect.get(url=url_info_player)
    return result_win_lose.json(), result_info_player.json()
