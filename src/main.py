from fastapi import FastAPI
import uvicorn

from src.auth.register_view import router as register_router
from src.auth.auth_view import router as auth_router
from src.tournament_view.views import router as tournament_router
from src.gamers_view.views import router as gamer_router
from src.squads_view.views import router as squad_router
app = FastAPI()


app.include_router(register_router)
app.include_router(auth_router)
app.include_router(tournament_router)
app.include_router(gamer_router)
app.include_router(squad_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=6385, reload=True)
