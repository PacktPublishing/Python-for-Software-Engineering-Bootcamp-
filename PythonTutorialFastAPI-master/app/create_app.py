from fastapi import FastAPI

from app.clients.db import DatabaseClient
from app.clients.redis import RedisCache
from app.config import Config
from app.exeption_handlers import add_exception_handlers
from app.routes.user import create_user_router


def create_application() -> FastAPI:
    config = Config()
    redis_cache = RedisCache(config)
    database_client = DatabaseClient(config)
    user_router = create_user_router(database_client, redis_cache)

    app = FastAPI()
    app.include_router(user_router)
    add_exception_handlers(app)

    return app
