from fastapi.testclient import TestClient
import pytest

from app.app import app


@pytest.fixture
def client():
    return TestClient(app)
