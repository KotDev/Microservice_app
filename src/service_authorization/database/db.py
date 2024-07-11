from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker


class DB:
    def __init__(self, url_db: str, echo: bool, class_session,
                 expire_on_commit: bool, autoflush: bool,
                 autocommit: bool):
        self.engine = create_async_engine(url=url_db,
                                          echo=echo)
        self.async_session = async_sessionmaker(bind=self.engine,
                                                class_=class_session,
                                                expire_on_commit=expire_on_commit,
                                                autoflush=autoflush,
                                                autocommit=autocommit)


db = DB(url_db="postgresql+asyncpg://root:root@localhost:5433/authorization_db",
        echo=True,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        class_session=AsyncSession)
Base = declarative_base()

