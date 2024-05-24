import jwt
import bcrypt
from datetime import datetime, timedelta
from config import settings


def encoded_jwt(payload: dict,
                private_key: str = settings.auth_jwt.private_key.read_text(),
                algorithm: str = settings.auth_jwt.algorithm,
                expire_minutes: int = settings.auth_jwt.expire_minutes_access_token) -> jwt.encode:
    """
    Создание jwt токена
    :param payload:
    :param private_key:
    :param algorithm:
    :param expire_minutes:
    :return: jwt.encode токен
    """
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)

    return encoded


def decoded_jwt(token: str | bytes,
                public_key: str = settings.auth_jwt.public_key.read_text(),
                algorithm: str = settings.auth_jwt.algorithm) -> jwt.decode:
    """
    Расшифровка jwt токена
    :param token:
    :param public_key:
    :param algorithm:
    :return: jwt.decode
    """
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])

    return decoded


def hash_password(user_password: str) -> bytes:
    """
    Хэширование пароля
    :param user_password:
    :return: bytes
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(user_password.encode(), salt)


def check_password(user_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(user_password.encode(), hashed_password)
