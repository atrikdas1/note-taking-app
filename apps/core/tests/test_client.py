"""
This file is used to initialize the test flask client for the unit tests
"""
import flask_sqlalchemy
import pytest
import sqlalchemy
from core.utils import alembic_stamp_to_base, alembic_upgrade_to_head
from core import config
from core.app import create_app
from database.models import Base
from dotenv import load_dotenv
from flask.testing import FlaskClient
from sqlalchemy_utils import create_database, database_exists

db = flask_sqlalchemy.SQLAlchemy()
load_dotenv()


class JWTClient(FlaskClient):
    """Test client
    """

    def open(self, *args, **kwargs):
        # Add fields to the request headers
        if "headers" not in kwargs:
            kwargs["headers"] = {}
            kwargs["headers"]["Content-Type"] = "application/json"
        # Continue the request as usual
        return FlaskClient.open(self, *args, **kwargs)


@pytest.fixture
def jwt_app():
    app = create_app()
    app.test_client_class = JWTClient

    # Create tables in database
    with app.app_context():
        engine = sqlalchemy.create_engine(config.SQLALCHEMY_DATABASE_URI)
        if not database_exists(engine.url):
            create_database(engine.url)

        alembic_upgrade_to_head()

    yield app

    # remove tables in database once testing completes
    with app.app_context():
        engine = db.get_engine(bind=None)
        Base.metadata.drop_all(engine)
        alembic_stamp_to_base()


@pytest.fixture
def jwt_client(jwt_app):
    return jwt_app.test_client()


@pytest.fixture
def jwt_context(jwt_app):
    return jwt_app.app_context()
