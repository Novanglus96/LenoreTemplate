import pytest


@pytest.mark.django_db
@pytest.mark.api
def test_health_check(api_client):
    response = api_client.get(
        "/options/health/",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_check_does_not_require_auth(api_client):
    response = api_client.get("/options/health/")
    assert response.status_code == 200
