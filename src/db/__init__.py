from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import settings as s

# NOTE: PostgreSQL Database layer is managed with sqlmodel/sqlalchemy:

db_engine = create_async_engine(
    url=s.DATABASE_URL,
)


async def get_session():
    Session = AsyncSession(
        db_engine, expire_on_commit=False, autoflush=False, autocommit=False
    )
    async with Session as session:
        yield session
