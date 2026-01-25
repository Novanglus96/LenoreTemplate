import pytest
from options.models import Version
from unittest.mock import patch


@pytest.mark.django_db
@pytest.mark.api
def test_list_version_success(api_client):
    Version.objects.create(
        id=1,
        version_number="1.2.3",
    )

    response = api_client.get(
        "/options/version/list",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 200
    assert response.json()["version_number"] == "1.2.3"


@pytest.mark.django_db
@pytest.mark.api
def test_list_version_not_found(api_client):
    response = api_client.get(
        "/options/version/list",
        headers={"Authorization": "Bearer test-api-key"},
    )

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.api
def test_list_version_internal_error(api_client):
    with patch("options.api.views.version.get_object_or_404") as mock_get:
        mock_get.side_effect = Exception("boom")

        response = api_client.get(
            "/options/version/list",
            headers={"Authorization": "Bearer test-api-key"},
        )

    assert response.status_code == 500
    assert response.json()["detail"] == "Record retrieval error"
