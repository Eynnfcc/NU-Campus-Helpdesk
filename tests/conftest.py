"""Shared test setup.

Every test gets its own empty tickets.json in a temporary folder,
so tests never touch the real data/tickets.json and never affect each other.
"""
import pytest
from fastapi.testclient import TestClient

from backend import storage
from backend.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Point storage at a temporary file instead of data/tickets.json
    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "tickets.json")
    return TestClient(app)


@pytest.fixture
def sample_ticket():
    return {
        "student_name": "Ahmed",
        "title": "WiFi not working",
        "category": "IT",
        "description": "No WiFi in Building B since morning",
    }
