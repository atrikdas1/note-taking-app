"""
Test PUT /v1/note/{id}
"""

import json
import logging
import logging.config
import string
import random
import pytest
from typing import Dict
from notes_api.tests.fixtures import put_notes_payload, create_notes
from core.config import LOG_CONFIG, CURRENT_VERSION_API
from core.tests.test_client import jwt_app, jwt_client, jwt_context

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(f"NOTES_API.{__name__}")


def put_note_pl() -> Dict:
    return put_notes_payload(
        "Content has been changed",
        ["mystery", "surprise"],
        None,
        None,
    )


def test_update_a_note_from_empty_db(jwt_client):
    """Try to update note from an empty database"""
    rsp = jwt_client.put(
        f"{CURRENT_VERSION_API}/note/1"
    )
    data = json.loads(rsp.get_data())
    logger.warning(data)
    assert rsp.status_code == 404


def test_update_note_without_JSON_payload(
    jwt_client, create_notes
):  # noqa: F811
    """Try PUT /note/{id} without JSON payload"""
    rsp = jwt_client.put(
        f"{CURRENT_VERSION_API}/note/1"
    )
    data = json.loads(rsp.get_data())
    logger.warning(data)
    assert rsp.status_code == 400


def test_update_note_from_populated_db(jwt_client, create_notes):
    """Update note from a populated database."""
    pl = put_note_pl()
    rsp = jwt_client.put(
        f"{CURRENT_VERSION_API}/note/1",
        data=json.dumps(pl),
        content_type="application/json",
    )
    data = json.loads(rsp.get_data())
    logger.warning(json.dumps(data, indent=4))
    assert rsp.status_code == 200
    assert pl["content"] == data["content"]
    assert pl["tags"] == data["tags"]


@pytest.mark.parametrize(
    (
        "jwt_client, content, tags, invalid_key, invalid_key_value"
    ),
    [
        (
            "",  # jwt_client
            None,  # content required
            [random.choice([(''.join(random.choice(string.ascii_letters) for i in range(8))) for n in range(5)])],  # tags,
            None,  # invalid_key,
            None,  # invalid_key_value,
        ),
        (
            "",  # jwt_client
            "",  # content cannot be empty string
            [random.choice([(''.join(random.choice(string.ascii_letters) for i in range(8))) for n in range(5)])],  # tags,
            None,  # invalid_key,
            None,  # invalid_key_value,
        ),
        (
            "",  # jwt_client
            ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(20)),  # content,
            None,  # tags required,
            None,  # invalid_key,
            None,  # invalid_key_value,
        ),
        (
            "",  # jwt_client
            ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(20)),  # content,
            [],  # tags cannot be empty,
            None,  # invalid_key,
            None,  # invalid_key_value,
        ),
        (
            "",  # jwt_client
            ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(20)),  # content,
            [random.choice([(''.join(random.choice(string.ascii_letters) for i in range(8))) for n in range(5)])],  # tags,
            "".join(
                random.choice(string.ascii_letters + string.digits) for i in range(8)
            ),  # invalid_key,: There is an unknown field
            "".join(
                random.choice(string.ascii_letters + string.digits) for i in range(8)
            ),  # invalid_key_value,
        ),
    ],
    indirect=["jwt_client", "create_notes"],
)
def test_update_note_invalid_payload(
    jwt_client,
    content,
    tags,
    invalid_key,
    invalid_key_value,
):
    """Try PUT /note/{id} where payload does not satisfy NoteSchema()"""
    pl = put_notes_payload(
        content,
        tags,
        invalid_key,
        invalid_key_value,
    )
    rsp = jwt_client.put(
        f"{CURRENT_VERSION_API}/note/1",
        data=json.dumps(pl),
        content_type="application/json",
    )
    data = json.loads(rsp.get_data())
    logger.warning(data)
    assert rsp.status_code == 400
