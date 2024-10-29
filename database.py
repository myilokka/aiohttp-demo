from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from config import db_settings

engine = create_async_engine(url=db_settings.get_db_url(),
                             pool_size=5,
                             max_overflow=10)

Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def orm_context(app):
    print("START")
    await init_orm()
    yield
    await engine.dispose()
    print("FINISH")
