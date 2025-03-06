from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_MAIN = 'postgresql+asyncpg://admin:admin@localhost/diploma'

engine = create_async_engine(URL_MAIN, echo=False)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
session = async_session()

Base = declarative_base()
