from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import DeclarativeBase
from config import settings

engine = create_async_engine(url=settings.db.DATABASE_URL_asyncpg,
                                          echo=True,
                                          )

session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass
