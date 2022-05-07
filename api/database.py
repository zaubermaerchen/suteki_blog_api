# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+asyncmy://bpuser:password@db/bpdb?charset=utf8mb4"

engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
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