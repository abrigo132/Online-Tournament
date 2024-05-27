import datetime

from pydantic import BaseModel


class NewTournament(BaseModel):
    tournament_name: str
    number_of_teams: int
    type: str
    finished_at: datetime
