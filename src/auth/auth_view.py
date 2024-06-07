from fastapi import APIRouter, Depends, HTTPException, Form
from starlette import status
from fastapi.security import OAuth2PasswordBearer

from src.auth.schemas import GamersAuth, TokenInfo
from src.auth.utils_jwt import check_password, encoded_jwt, decoded_jwt
from src.database.schemasDTO import GamersGetDTO
from src.crud.crud import check_user_auth

router = APIRouter(prefix="/login", tags=["login"])

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/login/gamers/create/accesstoken/")


async def check_auth_user(username: str = Form(), password: str = Form()) -> tuple:
    """

    :param username:
    :param password:
    :return: typle

    Функция для проверки логина и пароля внутри БД, если логина не существует, то выбрасывается ошибка,
    пароль сравнивается по хэшу, если юзер inactive, то тоже исключение.
    """

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
    )
    data_db: GamersGetDTO = await check_user_auth(username)  # Pydantic схема списком
    if not data_db:
        raise exception
    elif not check_password(password, data_db[0].password):
        raise exception
    elif data_db[0].status == "inactive":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )
    return data_db[0].username, data_db[0].email


@router.post("/gamers/create/accesstoken/")
def access_token_for_true_user(user: GamersAuth = Depends(check_auth_user)):
    """
    Вью для генерации JWT токена, содержит информацию о юзернейме, почте, когда создан и время жизни (смотреть в настройках
    JWT токена utils_jwt.py)

    """
    payload = {
        "sub": user[0],
        "email": user[1]
    }
    token = encoded_jwt(payload=payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )


def get_current_payload(token: str = Depends(oauth2_bearer)) -> dict:
    """
    Функция для автоматического выпуска JWT токена, используется OAuth2PasswordBearer
    Для закрытых вью использовать данную функцию для проверки, что токен выпущен и валиден

    :param token:
    :return: dict token payload
    """
    payload = decoded_jwt(token)

    return payload


