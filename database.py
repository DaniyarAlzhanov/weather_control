from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

DATABASE_URL = "sqlite+aiosqlite:///weather_data.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(
    expire_on_commit=False, bind=engine, class_=AsyncSession
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
