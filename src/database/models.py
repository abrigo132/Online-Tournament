import datetime
from typing import Annotated, Optional

from sqlalchemy import text, ForeignKey

from src.database.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

idpk = Annotated[int, mapped_column(primary_key=True)]
created = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Squads(Base):
    """
    Таблица команд
    """
    __tablename__ = "squads"
    id: Mapped[idpk]
    squad_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    about_of_team: Mapped[Optional[str]]
    created_at: Mapped[created]

    tournaments_list: Mapped[list["Tournaments"]] = relationship(
        back_populates="squads_list",
        secondary="tournamentssquads",
    )


class Tournaments(Base):
    """
    Таблица с действующими турнирами
    """
    __tablename__ = "tournaments"
    id: Mapped[idpk]
    tournament_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    number_of_teams: Mapped[int] = mapped_column(nullable=False)
    tournament_type: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[created]
    finished_at: Mapped[str]

    squads_list: Mapped[list["Squads"]] = relationship(
        back_populates="tournaments_list",
        secondary="tournamentssquads",
    )
    repr_cols = ("finished_at", "created_at")


class Gamers(Base):
    """
    Таблица с игроками
    """
    __tablename__ = "gamers"
    id: Mapped[idpk]
    username: Mapped[str]
    password: Mapped[bytes] = mapped_column(unique=True)
    steam_id: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    status: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int]
    created_at: Mapped[created]
    squad_id: Mapped[int] = mapped_column(ForeignKey("squads.id"), nullable=True)

    repr_cols = ("status", "email",)


class TournamentSquads(Base):
    """
    Таблица для m2m связи между таблицами турнир и команды для отображения команд, которые участвуют в турнире
    """
    __tablename__ = "tournamentssquads"
    squad_id: Mapped[int] = mapped_column(
        ForeignKey("squads.id"),
        primary_key=True
    )
    tournament_id: Mapped[int] = mapped_column(
        ForeignKey("tournaments.id"),
        primary_key=True
    )
