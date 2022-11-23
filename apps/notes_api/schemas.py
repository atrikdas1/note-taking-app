"""
This file contains all the validation schemas for the Note resource
"""

from core.utils import must_not_be_blank
from marshmallow import Schema, fields, validate


class NoteSchema(Schema):
    """Validate request to create/update a note"""

    content = fields.String(required=True, validate=must_not_be_blank)
    
    tags = fields.List(
        fields.String(required=True, validate=must_not_be_blank),
        required=True,
        validate=validate.Length(min=1),
    )