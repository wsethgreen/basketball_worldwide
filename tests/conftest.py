import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Fixture that provides a TestClient for the entire test module."""
    with TestClient(app) as c:
        yield c
