from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from app.config import db_settings

engine = create_async_engine(db_settings.POSTGRES_URL, echo=True)

async def create_db_tables():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async_session = async_sessionmaker(
        bind=engine, expire_on_commit=False,
    )
    async with async_session() as session:
        yield session

