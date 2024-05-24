from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette import status
from fastapi.security import OAuth2PasswordBearer

from src.auth.schemas import GamersAuth, TokenInfo
from src.auth.utils_jwt import check_password, encoded_jwt
from src.database.session import session
from src.crud.crud import check_user

router = APIRouter(prefix="/login", tags=["login"])
# bearer = OAuth2PasswordBearer(url="/login/gamers/create/accesstoken/")


async def check_auth_user(username: str = Form(), password: str = Form()):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
    )
    data_db: tuple = await check_user(username)

    if username != data_db[1]:
        return exception
    elif not check_password(password, data_db[2]):
        return exception
    elif data_db[5] == "inactive":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )
    return data_db[1], data_db[4]


@router.post("/gamers/create/accesstoken/")
def access_token_for_true_user(user: GamersAuth = Depends(check_auth_user)):
    payload = {
        "sub": user.username,
        "email": user.email
    }
    token = encoded_jwt(payload=payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )
