"""
Functions that help query the database for certain data
"""

import logging
from typing import Dict, List, Tuple
from notes_api.models import Note
from core.db import db

logger = logging.getLogger(f"NOTES_API.{__name__}")


def filter_notes_by_id(note_id: int) -> Tuple[int, str, List]:
    try:
        notes = (
            db.session.query(Note).filter(
                Note.id == note_id
            ).all()
        )
        notes_list = []
        if len(notes) > 0:
            for note in notes:
                notes_list.append(note.serialize())

        return (
            200,
            None,
            notes_list,
        )
    except Exception as e:
        err_msg = f"Note with ID {note_id} not found"
        logger.exception(e)
        return (500, err_msg, None)


def filter_all_notes() -> Tuple[int, str, List]:
    try:
        notes = (
            db.session.query(Note).all()
        )
        notes_list = []
        if len(notes) > 0:
            for note in notes:
                notes_list.append(note.serialize())

        return (
            200,
            None,
            notes_list,
        )
    except Exception as e:
        err_msg = f"Database not found"
        logger.exception(e)
        return (500, err_msg, None)