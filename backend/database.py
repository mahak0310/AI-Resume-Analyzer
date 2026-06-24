# from pydantic_settings import BaseSettings
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker, declarative_base


# class Settings(BaseSettings):
#     DATABASE_URL: str
#     GROQ_API_KEY: str
#     GROQ_MODEL: str

#     class Config:
#         env_file = ".env"


# settings = Settings()

# engine = create_async_engine(settings.DATABASE_URL, echo=True)

# AsyncSessionLocal = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )

# Base = declarative_base()


# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import ssl


class Settings(BaseSettings):
    DATABASE_URL: str
    GROQ_API_KEY: str
    GROQ_MODEL: str

    class Config:
        env_file = ".env"


settings = Settings()

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args={"ssl": ssl_context},
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session