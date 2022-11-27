"""
This file contains helper functions used throughout the other files
"""
import os
from alembic.command import upgrade, stamp
from alembic.config import Config
from flask import jsonify
from marshmallow import ValidationError


def must_not_be_blank(data):
    if not data:
        raise ValidationError("Field cannot be blank")
    if len(data) == 0 and isinstance(data, str):
        raise ValidationError("Field cannot be an empty string")


def get_path(relative_path=None):
    """Get absolute path to resource. If relative_path is not specified, return the current working directory
    """
    base_path = os.getcwd()

    if relative_path:
        joined_path = os.path.join(base_path, relative_path)
    else:
        joined_path = base_path

    return joined_path


def alembic_upgrade_to_head():
    """Auto-upgrade alembic head to the final database revision
    """
    # Changing the working directory is required as alembic use relative path
    alembic_ini_path = get_path("database/alembic.ini")
    alembic_config = Config(alembic_ini_path)
    upgrade(alembic_config, "head")


def alembic_stamp_to_base():
    """Auto-upgrade alembic head to the first database revision
    """
    # Changing the working directory is required as alembic use relative path,
    alembic_ini_path = get_path("database/alembic.ini")
    alembic_config = Config(alembic_ini_path)
    stamp(alembic_config, "base")


def custom_abort(code: int, title: str, msg: str):
    """Abort and return an error code json response.

    Args:
        code -- The error code.
        msg -- The error message.
    Returns:
        The response in JSON
        {
            "error": {
                "title": "string",
                "message": "string"
            }
        }
    """
    res = jsonify({"error": {"title": str(title), "message": str(msg)}})
    res.status_code = code
    return res


def custom_abort_with_id(code: int, msg: str, id:int):
    """Abort and return an error code json response.

    Args:
        code -- The error code.
        msg -- The error message.
        id -- ID of the resource
    Returns:
        The response in JSON
        {
            "error": {
                "id": "integer",
                "message": "string",

            }
        }
    """
    res = jsonify({"error": {"id": id, "message": str(msg)}})
    res.status_code = code
    return res