"""
This file initializes the SQLAlchemy extension for Flask in its own file so that
it's easier to import the initialized extension in various other files later on
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()