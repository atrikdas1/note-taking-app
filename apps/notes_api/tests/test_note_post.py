"""
Test POST /v1/note
"""

import json
import logging
import logging.config
import string
import random
import pytest
from typing import Dict
from notes_api.tests.fixtures import post_notes_payload
from core.config import LOG_CONFIG, CURRENT_VERSION_API
from core.tests.test_client import jwt_app, jwt_client, jwt_context

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(f"NOTES_API.{__name__}")


def post_note_pl() -> Dict:
    # get random string consisting of letters, digits, and symbols
    characters = string.ascii_letters + string.digits + string.punctuation
    return post_notes_payload(
        ''.join(random.choice(characters) for i in range(20)),
        # Generate 5 nonsensical tags
        [random.choice([(''.join(random.choice(string.ascii_letters) for i in range(8))) for n in range(5)])],
        None,
        None,
    )


def test_post_a_note(jwt_client):
    """POST /note"""
    pl = post_note_pl()
    logger.warning(f"payload: {pl}")
    rsp = jwt_client.post(
        f"{CURRENT_VERSION_API}/note",
        data=json.dumps(pl),
        content_type="application/json",
    )
    data = json.loads(rsp.get_data())
    logger.warning(json.dumps(data, indent=4))
    assert rsp.status_code == 201


def test_post_note_without_JSON_payload(jwt_client):
    """Try POST /note without JSON payload"""
    rsp = jwt_client.post(
        f"{CURRENT_VERSION_API}/note"
    )
    data = json.loads(rsp.get_data())
    logger.warning(data)
    assert rsp.status_code == 400


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
    indirect=["jwt_client"],
)
def test_post_note_invalid_payload(
    jwt_client,
    content,
    tags,
    invalid_key,
    invalid_key_value,
):
    """Try POST /note where payload does not satisfy NoteSchema()"""
    pl = post_notes_payload(
        content,
        tags,
        invalid_key,
        invalid_key_value,
    )
    rsp = jwt_client.post(
        f"{CURRENT_VERSION_API}/note",
        data=json.dumps(pl),
        content_type="application/json",
    )
    data = json.loads(rsp.get_data())
    logger.warning(data)
    assert rsp.status_code == 400
