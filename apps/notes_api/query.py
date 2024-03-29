"""
Functions that help query the database for certain data
"""

import logging
from typing import Dict, List, Tuple
from notes_api.models import Note
from core.db import db
from sqlalchemy import desc

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
            db.session.query(Note)
            .order_by(Note.modified.desc())
            .all()
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
        err_msg = f"filter_all_notes() failed. Errors: {e}"
        logger.exception(e)
        return (500, err_msg, None)


def filter_notes_by_tag(tag: str) -> Tuple[int, str, List]:
    try:
        # Query all notes first
        notes = (
            db.session.query(Note)
            .order_by(Note.modified.desc())
            .all()
        )
        notes_list = []

        # Loop through them and check existence of tag
        if len(notes) > 0:
            for note in notes:
                note_obj = note.serialize()
                if tag in note_obj["tags"]:
                    notes_list.append(note_obj)

        return (
            200,
            None,
            notes_list,
        )
    except Exception as e:
        err_msg = f"filter_notes_by_tag({tag}) failed. Errors: {e}"
        logger.exception(e)
        return (500, err_msg, None)


def filter_notes_by_entity(entity: str) -> Tuple[int, str, List]:
    try:
        # Query all notes first
        notes = (
            db.session.query(Note)
            .order_by(Note.modified.desc())
            .all()
        )
        notes_list = []

        # Loop through them and check existence of entity
        if len(notes) > 0:
            for note in notes:
                note_obj = note.serialize()
                if entity in note_obj["entities"]:
                    notes_list.append(note_obj)

        return (
            200,
            None,
            notes_list,
        )
    except Exception as e:
        err_msg = f"filter_notes_by_entity({entity}) failed. Errors: {e}"
        logger.exception(e)
        return (500, err_msg, None)


def filter_all_tags() -> Tuple[int, str, List]:
    try:
        # First query all the notes
        notes = (
            db.session.query(Note)
            .order_by(Note.modified.desc())
            .all()
        )
        # Loop through each note and store each tag in a set to get unique tags
        tags_set = set()
        if len(notes) > 0:
            for note in notes:
                note_obj = note.serialize()
                for tag in note_obj["tags"]:
                    tags_set.add(tag)

        return (
            200,
            None,
            list(tags_set),
        )
    except Exception as e:
        err_msg = f"filter_all_tags() failed. Errors: {e}"
        logger.exception(e)
        return (500, err_msg, None)


def update_note(id: int, content: str, tags: List[str], entities: List[str]) -> Tuple[int, str, Dict]:
    try:
        # Query the db with the id to get the note which requires updating first
        note = (
            db.session.query(Note)
            .filter_by(id=int(id))
            .one_or_none()
        )

        # Change the relevant fields based on what the user wants
        if note is None:
            return (404, f"Note {id} not found", None)
        if content is not None:
            note.content = content
        if tags is not None:
            note.tags = tags
        if entities is not None:
            note.entities = entities

        db.session.add(note)
        db.session.commit()

        # Get the updated note back by id
        response_code, response_msg, notes_list = filter_notes_by_id(id)
        if notes_list is None:
            return (response_code, response_msg, None)
        if len(notes_list) == 0:
            return (404, "Not Found", None)
        result = notes_list[0]
        return (200, None, result)

    except Exception as e:
        err_msg = f"update_note({id}) failed: {e}"
        logger.exception(err_msg)
        return (500, err_msg, None)
