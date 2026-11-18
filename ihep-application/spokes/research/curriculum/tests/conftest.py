"""Shared test setup for the IHEP Curriculum API."""

import os
import sys
from pathlib import Path

# Settings are built when app.core.config is imported, so the required values
# must be in the environment first. These point at nothing; no test connects.
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/ihep_curriculum_test")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
# "development" keeps the lifespan from creating tables (that needs a live DB).
os.environ.setdefault("ENVIRONMENT", "development")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture
def client():
    from app.main import app

    with TestClient(app) as c:
        yield c
