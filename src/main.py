from fastapi import FastAPI
import uvicorn

from src.auth.register_view import router as register_router
from src.auth.auth_view import router as auth_router
app = FastAPI()


app.include_router(register_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
