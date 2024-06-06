import datetime

from pydantic import BaseModel


class NewTournament(BaseModel):
    tournament_name: str
    number_of_teams: int
    tournament_type: str
    finished_at: str


class TournamentInfo(BaseModel):
    name: str
