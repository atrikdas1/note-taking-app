"""
This file creates the Flask application with the appropriate configurations
"""
from core.db import db
from core import config
from flask import Flask


def create_app():
    app = Flask(__name__)

    # This field is disabled to avoid sorting the JSON objects alphabetically,
    # which saves time on caching thus improving performance
    app.config["JSON_SORT_KEYS"] = False

    # Use debug mode for now in development environment
    app.config["FLASK_DEBUG"] = 1

    # Disabled to save memory
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # configure the Postgres database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI

    # Initialize the database
    db.init_app(app)

    return app