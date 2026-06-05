import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient and restore `activities` after each test.

    Uses deepcopy to snapshot the in-memory state so tests remain isolated.
    """
    original = deepcopy(activities)
    client = TestClient(app)
    try:
        yield client
    finally:
        activities.clear()
        activities.update(original)
