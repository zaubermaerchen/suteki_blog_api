# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from api.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url, 
    echo=settings.debug,
    future=True
)

session = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    autoflush=False, 
    autocommit=False, 
    future=True
)

Base = declarative_base()

async def get_session() -> AsyncSession:
    async with session() as s:
        yield s