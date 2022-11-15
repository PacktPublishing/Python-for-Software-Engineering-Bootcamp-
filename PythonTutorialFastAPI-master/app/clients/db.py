import os
from typing import Optional, Union

from databases import Database
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Row
from sqlalchemy.sql.expression import Delete, Insert, Select

from app.config import Config


class DatabaseClient:
    def __init__(self, config: Config):
        self.config = config
        self.engine = create_engine(self.config.postgres_host, future=True)
        self.metadata = MetaData(self.engine)
        self._reflect_metadata()  # metadata.tables["user"]

        self._set_internal_database_tables()
        if os.getenv("app_env") == "test":
            self.database = Database(self.config.postgres_host, force_rollback=True)
        else:
            self.database = Database(self.config.postgres_host)

    def _reflect_metadata(self) -> None:
        self.metadata.reflect()

    async def connect(self) -> None:
        await self.database.connect()

    async def disconnect(self) -> None:
        await self.database.disconnect()

    def _set_internal_database_tables(self) -> None:
        self.user = self.metadata.tables["user"]
        self.liked_post = self.metadata.tables["liked_post"]

    async def get_first(self, query: Union[Select, Insert]) -> Optional[Row]:
        async with self.database.transaction():
            res = await self.database.fetch_one(query)
        return res

    async def get_all(self, query: Select) -> list[Row]:
        async with self.database.transaction():
            res = await self.database.fetch_all(query)
        return res

    async def get_paginated(self, query: Select, limit: int, offset: int) -> list[Row]:
        query = query.limit(limit).offset(offset)
        return await self.get_all(query)

    async def execute_in_transaction(self, query: Delete) -> None:
        async with self.database.transaction():
            await self.database.execute(query)
