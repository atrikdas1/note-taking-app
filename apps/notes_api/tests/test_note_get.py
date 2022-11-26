"""
Test GET /v1/note and /v1/note/{id}
"""

import json
import logging
import logging.config
from notes_api.tests.fixtures import create_notes
from core.config import LOG_CONFIG, CURRENT_VERSION_API
from core.tests.test_client import jwt_app, jwt_client, jwt_context

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(f"NOTES_API.{__name__}")


def test_get_a_note_from_empty_db(jwt_client):
    """Try to get a note from an empty database"""
    rsp = jwt_client.get(
        f"{CURRENT_VERSION_API}/note/1"
    )
    data = json.loads(rsp.get_data())
    logger.warning(data)
    assert rsp.status_code == 404


def test_get_a_note_from_populated_db(jwt_client, create_notes): 
    """Get a note from a populated database"""
    rsp = jwt_client.get(
        f"{CURRENT_VERSION_API}/note/1"
    )
    data = json.loads(rsp.get_data())
    logger.warning(json.dumps(data, indent=4))
    assert rsp.status_code == 200
    assert "content" in data


def test_get_notes_from_empty_db(jwt_client):
    """Get notes from an empty database"""
    rsp = jwt_client.get(
        f"{CURRENT_VERSION_API}/note"
    )
    data = json.loads(rsp.get_data())
    logger.warning(data)
    assert rsp.status_code == 200
    assert len(data.get("notes")) == 0


def test_get_notes_from_populated_db(jwt_client, create_notes):
    """Get notes from a populated database"""
    rsp = jwt_client.get(
        f"{CURRENT_VERSION_API}/note"
    )
    data = json.loads(rsp.get_data())
    logger.warning(json.dumps(data, indent=4))
    assert rsp.status_code == 200
    logger.warning(f"len(data.get('notes')): {len(data.get('notes'))}")
    assert len(data.get("notes")) == 3