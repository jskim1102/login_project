# app/db/session.py

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 비동기 엔진 생성
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 비동기 세션 생성
AsyncSessionFactory = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
)

# API 요청마다 독립적인 DB 세션을 생성하고, 끝나면 닫아주는 의존성 함수
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session