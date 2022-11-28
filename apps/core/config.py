"""
This file contains all the constants which can be configured according to the user's peruse
"""

import sqlalchemy
import logging

CURRENT_VERSION_API = "v1"

SQLALCHEMY_DATABASE_URI = sqlalchemy.engine.url.URL.create(
    drivername="postgresql",
    username="postgres",
    password="postgres",
    host="note-taker-db",
    port=5432,
    database="postgres",
)

LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": (
                "%(asctime)s %(levelname)-8s [MOD %(module)s:LNE"
                "%(lineno)d:FUN %(funcName)s: PID %(process)d: TID %(thread)d] %(message)s"
            )
        }
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
        }
    },
    "loggers": {
        "NOTES_API": {
            "level": logging.DEBUG,
            "handlers": ["default"],
            "propagate": True,
        }
    },
}

RAND_USER_GEN_URL = "https://randomuser.me/api"

RAND_CHUCK_NORRIS_JOKE_URL = "https://api.chucknorris.io/jokes/random"

GCP_API_KEY = "AIzaSyBQ5h-MLT7Bj1ASNccdlrbF_jwVlZ6Hvfs"

GCP_API_URL = f"https://language.googleapis.com/v1/documents:analyzeEntities?key={GCP_API_KEY}"
