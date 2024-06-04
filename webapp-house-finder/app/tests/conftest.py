import pytest
from app import create_app
from app.models import db
from os import environ
import time


time.sleep(5)
@pytest.fixture
def app():
    """Create and configure a new app instance for each test using TestingConfig."""
    app = create_app(settings_module=environ.get('TEST_CONFIGURATION_SETUP'))

    with app.app_context():
        db.create_all()
        yield app
       

@pytest.fixture
def client(app):
    """A test client for the app, initializing the database within test_client."""
    with app.test_client() as client:
        yield client







