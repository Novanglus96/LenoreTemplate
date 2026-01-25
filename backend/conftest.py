import pytest
from ninja.testing import TestClient
from backend.api import api


@pytest.fixture(scope="session")
def api_client():
    return TestClient(api)
