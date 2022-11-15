from typing import Any, Tuple
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from app.clients.db import DatabaseClient
from app.config import Config
from app.schemas.user import FullUserProfile
from app.services.user import UserService
from models import LikedPost, User, recreate_postgres_tables


@pytest.fixture
def _profile_infos() -> dict[int, dict[str, str]]:
    val = {
        0: {
            "short_description": "My bio description",
            "long_bio": "This is our longer bio",
        }
    }
    return val


@pytest.fixture
def _users_content() -> dict:
    val = {
        0: {
            "liked_posts": [1] * 9,
        }
    }
    return val


@pytest.fixture(scope="session")
def sample_full_user_profile() -> FullUserProfile:
    return FullUserProfile(
        short_description="short descr",
        long_bio="def",
        name="abc",
        liked_posts=[1, 2, 3],
    )


@pytest.fixture(scope="session")
def testing_config() -> Config:
    return Config()


@pytest_asyncio.fixture
async def testing_db_client(testing_config: Config) -> DatabaseClient:  # type: ignore
    recreate_postgres_tables()
    database_client = DatabaseClient(testing_config)
    await database_client.connect()
    yield database_client
    await database_client.disconnect()


@pytest.fixture
def user_service(testing_db_client: DatabaseClient) -> UserService:
    user_service = UserService(testing_db_client)
    return user_service


@pytest.fixture
def mocking_database_client() -> DatabaseClient:
    def side_effect(*args: Any, **kwargs: Any) -> Tuple[int]:
        return (1,)

    mock = AsyncMock()
    mock.user = User.__table__
    mock.liked_post = LikedPost.__table__
    mock.get_first.side_effect = side_effect  # AsyncMock(side_effect=[(1, ), (2, )])
    return mock


@pytest.fixture
def user_service_mocked_db(mocking_database_client: DatabaseClient) -> UserService:
    user_service = UserService(mocking_database_client)
    return user_service
