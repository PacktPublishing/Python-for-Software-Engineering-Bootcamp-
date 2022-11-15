from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.schemas.user import FullUserProfile


def test_delete_user_success(base_testing_app: FastAPI) -> None:
    user_id = 1
    with TestClient(base_testing_app) as testing_app:
        response = testing_app.delete(f"/user/{user_id}")
        assert response.status_code == 200


def test_put_user_returns_correct_results(
    base_testing_app: FastAPI,
    sample_full_user_profile: FullUserProfile,
) -> None:
    with TestClient(base_testing_app) as testing_app:
        user_id = 1
        response = testing_app.put(f"/user/{user_id}", json=sample_full_user_profile)

        assert response.status_code == 200


def test_put_user_twice_returns_correct_results(
    base_testing_app: FastAPI, sample_full_user_profile: FullUserProfile
) -> None:
    with TestClient(base_testing_app) as testing_app:
        user_id = 1
        response = testing_app.put(f"/user/{user_id}", json=sample_full_user_profile)

        assert response.status_code == 200

        second_response = testing_app.put(
            f"/user/{user_id}", json=sample_full_user_profile
        )

        assert second_response.status_code == 200


def test_rate_limit_works(
    base_testing_app: FastAPI,
    testing_rate_limit: int,
    sample_full_user_profile: FullUserProfile,
) -> None:
    user_id = 1
    with TestClient(base_testing_app) as testing_app:
        testing_app.put(f"/user/{user_id}", json=sample_full_user_profile)
        for i in range(testing_rate_limit * 2):
            response = testing_app.get(f"/user/{user_id}")
            if "x-app-rate-limit" not in response.headers:
                assert response.status_code == 429
