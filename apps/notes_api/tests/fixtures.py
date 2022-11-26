import logging
import logging.config
from datetime import datetime, timedelta
from typing import Any, Dict, List

import pytest
from notes_api.models import Note
from core.config import LOG_CONFIG
from core.db import db
from core.tests.test_client import jwt_app, jwt_client, jwt_context

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(f"NOTES_API.{__name__}")


def post_notes_payload(
    content: str,
    tags: List[str],
    invalid_key: str,
    invalid_key_value: Any,
) -> Dict:
    """JSON payload for POST /note"""
    d = {}
    if content is not None:
        d["content"] = content
    if tags is not None:
        d["tags"] = tags
    if invalid_key is not None:
        d[invalid_key] = invalid_key_value
    return d


def put_notes_payload(
    content: str,
    tags: List[str],
    invalid_key: str,
    invalid_key_value: Any,
) -> Dict:
    """JSON payload for PUT /note/{id}"""
    d = {}
    if content is not None:
        d["content"] = content
    if tags is not None:
        d["tags"] = tags
    if invalid_key is not None:
        d[invalid_key] = invalid_key_value
    return d


def note_db_entry(
    content: str,
    tags: List[str],
) -> Dict:
    """Create database entry for Note"""
    d = {}
    if content is not None:
        d["content"] = content
    if tags is not None:
        d["tags"] = tags
    return d


@pytest.fixture
def create_notes(jwt_client, jwt_context):
    """Blueprint to create random test notes"""
    try:
        with jwt_context:
            note_1 = note_db_entry(
                "This is a test note",
                ["test"],
            )
            mock_note_1 = Note(**note_1)
            db.session.add(mock_note_1)

            note_2 = note_db_entry(
                "This is another test note",
                ["test", "boring"],
            )
            mock_note_2 = Note(**note_2)
            db.session.add(mock_note_2)

            note_3 = note_db_entry(
                "This is yet another lame test note",
                ["test", "lame"],
            )
            mock_note_3 = Note(**note_3)
            db.session.add(mock_note_3)

            db.session.commit()
            logger.info("Generated notes")

    except Exception as e:
        logger.exception(e)
        assert False