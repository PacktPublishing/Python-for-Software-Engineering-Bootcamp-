from pydantic import BaseSettings, PostgresDsn, RedisDsn


class Config(BaseSettings):
    postgres_host: PostgresDsn
    redis_host: RedisDsn

    class Config:
        env_prefix = "db_"
