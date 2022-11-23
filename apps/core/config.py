"""
This file contains all the constants which can be configured according to the user's peruse
"""

import sqlalchemy

CURRENT_VERSION_API = "v1"

SQLALCHEMY_DATABASE_URI = sqlalchemy.engine.url.URL.create(
    drivername="postgresql",
    username="postgres",
    password="postgres",
    host="note-taker-db",
    port=5432,
    database="postgres",
)