import os
import tempfile

# Base de test isolée : à définir AVANT d'importer l'application.
os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.mkdtemp()}/test.db"

import pytest
from fastapi.testclient import TestClient

from backend.core.database import Base, engine
from backend.main import app


@pytest.fixture(autouse=True)
def base_propre():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
