"""
Test GET /v1/note/tag/{tag} and /v1/tags
"""

import json
import logging
import logging.config
from notes_api.tests.fixtures import create_notes
from core.config import LOG_CONFIG, CURRENT_VERSION_API
from core.tests.test_client import jwt_app, jwt_client, jwt_context

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(f"NOTES_API.{__name__}")


def test_get_a_non_existing_tag(jwt_client):
    """Try to get notes for a tag from an empty database or not existing"""
    rsp = jwt_client.get(
        f"{CURRENT_VERSION_API}/note/tag/work"
    )
    data = json.loads(rsp.get_data())
    logger.warning(data)
    assert rsp.status_code == 200
    assert len(data.get("notes")) == 0


def test_get_a_tag_from_populated_db(jwt_client, create_notes): 
    """Get notes for a tag from a populated database"""
    rsp = jwt_client.get(
        f"{CURRENT_VERSION_API}/note/tag/test"
    )
    data = json.loads(rsp.get_data())
    logger.warning(json.dumps(data, indent=4))
    assert rsp.status_code == 200
    assert len(data.get("notes")) == 3


def test_get_tags_from_empty_db(jwt_client):
    """Get tags from an empty database"""
    rsp = jwt_client.get(
        f"{CURRENT_VERSION_API}/tags"
    )
    data = json.loads(rsp.get_data())
    logger.warning(data)
    assert rsp.status_code == 200
    assert len(data.get("tags")) == 0


def test_get_tags_from_populated_db(jwt_client, create_notes):
    """Get tags from a populated database"""
    rsp = jwt_client.get(
        f"{CURRENT_VERSION_API}/tags"
    )
    data = json.loads(rsp.get_data())
    logger.warning(json.dumps(data, indent=4))
    assert rsp.status_code == 200
    logger.warning(f"len(data.get('tags')): {len(data.get('tags'))}")
    assert len(data.get("tags")) == 3
    assert "test" in data.get("tags")
    assert "boring" in data.get("tags")
    assert "lame" in data.get("tags")
