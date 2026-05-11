from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.config import DATABASE_URL
import asyncio

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)


async def init_db(Base):

    for _ in range(10):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            print("DB CONNECTED")
            return

        except Exception as e:
            print("DB retry...", e)
            await asyncio.sleep(3)

    raise RuntimeError("DB connection failed")
