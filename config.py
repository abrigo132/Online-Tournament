from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv

BASE_DIR = Path(__file__).parent


class JWTSettings(BaseModel):
    """
    Настройки для создания и расшифровки jwt токена
    """
    private_key: Path = BASE_DIR / "certs" / "private.pem"
    public_key: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    expire_minutes_access_token: int = 15


class DbSettings(BaseSettings):
    """
    Настройки для подключения к бд
    """
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=find_dotenv())


class Settings(BaseSettings):
    """
    Глобальные настройки
    """
    db: DbSettings = DbSettings()

    auth_jwt: JWTSettings = JWTSettings()


settings = Settings()
