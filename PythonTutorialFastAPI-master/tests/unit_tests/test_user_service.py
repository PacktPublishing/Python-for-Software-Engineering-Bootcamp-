from typing import cast
from unittest.mock import Mock

import pytest

from app.clients.db import DatabaseClient
from app.exceptions import UserNotFound
from app.schemas.user import FullUserProfile
from app.services.user import UserService


@pytest.mark.asyncio
async def test_delete_user_works_properly(
    user_service: UserService, sample_full_user_profile: FullUserProfile
) -> None:
    user_id = await user_service.create_user(sample_full_user_profile)
    assert user_id is not None
    await user_service.delete_user(user_id)
    with pytest.raises(UserNotFound):
        await user_service.get_user_info(user_id)


@pytest.mark.asyncio
async def test_create_user_works_properly(
    user_service_mocked_db: UserService,
    mocking_database_client: DatabaseClient,
    sample_full_user_profile: FullUserProfile,
) -> None:
    user_id = await user_service_mocked_db.create_user(sample_full_user_profile)
    mocked_function = cast(Mock, mocking_database_client.get_first)

    assert mocked_function.called
    mocked_function.assert_awaited_once()
    assert user_id == 1


@pytest.mark.asyncio
async def test_get_all_users_with_pagination_works_properly(
    user_service_mocked_db: UserService,
    sample_full_user_profile: FullUserProfile,
    mocking_database_client: DatabaseClient,
) -> None:
    offset = 3
    limit = 5
    await user_service_mocked_db.get_all_users_with_pagination(offset, limit)

    get_paginated_function = cast(Mock, mocking_database_client.get_paginated)
    assert get_paginated_function.called
    get_paginated_function.assert_awaited_once()

    assert get_paginated_function.call_args[0][0].compare(
        user_service_mocked_db._get_user_info_query()
    )
    assert get_paginated_function.call_args[0][1] == limit
    assert get_paginated_function.call_args[1]["offset"] == offset
