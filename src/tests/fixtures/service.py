from typing import Generator, Any

import pytest
from flask import Flask
from flask.testing import FlaskClient

from src import create_app


@pytest.fixture(autouse=True, scope="session")
def app() -> Flask:
    return create_app("testing")


@pytest.fixture()
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def app_context(app: Flask) -> Generator[Any, Any, None]:
    with app.app_context():
        yield app
