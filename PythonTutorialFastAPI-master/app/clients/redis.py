import logging
import pickle
from typing import Any, Union

import aioredis
import snappy

from app.config import Config

logger = logging.getLogger(__name__)


class RedisCache:
    user_prefix = "user"
    pagination_prefix = "pagination"

    def __init__(self, config: Config, ttl: int = 60 * 60):
        self._host = config.redis_host
        self.redis = aioredis.from_url(self._host, db=0)
        self.ttl = ttl

    async def get(self, key: Union[str, int], prefix: str) -> Any:
        try:
            storage_key = f"{prefix}:{key}"
            compressed_val = await self.redis.get(storage_key)
            decompressed_value = snappy.decompress(compressed_val)
            return pickle.loads(decompressed_value)
        except Exception as e:
            logger.error(
                f"Encountered error {str(e)} when trying to"
                f" read prefix: {prefix} and key:{key}"
            )
        return

    async def set(self, key: Union[str, int], value: Any, prefix: str) -> None:
        try:
            storage_key = f"{prefix}:{key}"
            serialized_value = pickle.dumps(value)
            compressed_value = snappy.compress(serialized_value)
            await self.redis.set(storage_key, compressed_value, ex=self.ttl)
        except Exception as e:
            logger.error(
                f"Encountered error {str(e)} when trying to"
                f" save: {value} to {storage_key}"
            )
        return

    async def delete(self, *args: Any, prefix: Any) -> None:
        prefixed_args = [f"{prefix}:{key}" for key in args]
        await self.redis.delete(*prefixed_args)
        return

    async def hget(self, name: str, key: Union[str, int], prefix: str) -> Any:
        try:
            storage_name = self.create_storage_name(name, prefix)
            compressed_val = await self.redis.hget(storage_name, key)
            decompressed_val = snappy.decompress(compressed_val)
            return pickle.loads(decompressed_val)
        except Exception as e:
            logger.error(
                f"Encountered error {str(e)} when trying to"
                f" read prefix: {prefix} and key:{key}"
            )
        return

    async def hset(
        self, name: Any, mapping: dict[Union[str, int], Any], prefix: Any
    ) -> None:
        storage_name = self.create_storage_name(name, prefix)
        compressed_serialized_mapping = {}
        for key in mapping:
            compressed_serialized_mapping[key] = self.serialize_and_compress(
                mapping[key]
            )
        await self.redis.hset(storage_name, mapping=compressed_serialized_mapping)
        await self.redis.expire(storage_name, self.ttl)

    async def hdel(self, name: str, key: str, prefix: str) -> None:
        storage_name = self.create_storage_name(name, prefix)
        await self.redis.hdel(storage_name, key)

    async def sadd(self, name: str, key: Union[str, int], prefix: str) -> None:
        storage_name = self.create_storage_name(name, prefix)
        await self.redis.sadd(storage_name, key)

    def get_pagination_key(self, limit: int) -> str:
        return f"{self.pagination_prefix}:{limit}"

    def get_pagination_set_key(self) -> str:
        return f"{self.pagination_prefix}"

    async def clear_pagination_cache(self, prefix: str) -> None:
        set_storage_name = self.create_storage_name(
            self.get_pagination_set_key(), prefix
        )
        limits = await self.redis.smembers(set_storage_name)
        for limit in limits:
            # user:pagination:{limit}
            pagination_storage_key = f"{prefix}:{self.get_pagination_key(limit)}"
            await self.redis.delete(pagination_storage_key)
            await self.redis.srem(set_storage_name, limit)

    async def flushdb(self) -> None:
        await self.redis.flushdb(asynchronous=True)

    @staticmethod
    def create_storage_name(key: str, prefix: str) -> str:
        return f"{prefix}:{key}"

    @staticmethod
    def serialize_and_compress(value: Any) -> bytes:
        ser_val = pickle.dumps(value)
        return snappy.compress(ser_val)
