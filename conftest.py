import os

# Precisa vir ANTES de qualquer import de app ou model
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from model import Base, engine


@pytest.fixture(autouse=True)
def banco_limpo():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield