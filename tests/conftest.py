import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


# Snapshot the original in-memory activities so tests can reset state
_ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture
def client():
    """Provides a TestClient for the FastAPI app."""
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory `activities` dictionary before each test.

    This keeps tests isolated and deterministic using an original snapshot.
    """
    app_module.activities = copy.deepcopy(_ORIGINAL_ACTIVITIES)
    yield
    app_module.activities = copy.deepcopy(_ORIGINAL_ACTIVITIES)
