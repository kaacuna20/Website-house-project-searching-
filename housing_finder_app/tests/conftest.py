import pytest
from housing_finder_app.__ini__ import create_app
from housing_finder_app.models import db
from config import TestingConfig


@pytest.fixture
def app():
    """Create and configure a new app instance for each test using TestingConfig."""
    app = create_app(settings_module=TestingConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app, initializing the database within test_client."""
    with app.test_client() as client:
        yield client







