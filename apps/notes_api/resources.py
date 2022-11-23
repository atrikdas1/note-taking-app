"""Logic for RESTFUL APIs of notes"""

import logging

from notes_api import models
from notes_api import query
from notes_api.schemas import CreateNoteSchema
from core import utils as apputils
from core.db import db
from flask import jsonify, make_response, request
from flask_restful import Resource
from marshmallow import ValidationError

logger = logging.getLogger(f"NOTES_API.{__name__}")


class Notes(Resource):
    """
    Handle the following requests:
    1. POST Create a basic note
    2. GET Get all the notes in the db
    3. DELETE Remove all the notes in the db
    """

    def post(self):
        """Create a basic note"""
        # Check if request contains a json payload
        try:
            json_data = request.get_json()
        except Exception as e:
            msg = "Notes.post(): No JSON payload found."
            logger.exception(f"{e}:{msg}")
            return apputils.custom_abort(400, "Bad Request", msg)

        # Validate CreateNoteSchema request json
        try:
            logger.debug(f"CreateNoteSchema json_data: {json_data}")
            template_schema = CreateNoteSchema()
            data = template_schema.load(json_data)
        except ValidationError as err:
            logger.warning(
                f"Notes.post(): request with invalid data. Details: {err.messages}"
            )
            return apputils.custom_abort(
                400,
                "Bad Request",
                f"Please correct the highlighted errors and try again: {err.messages}",
            )

        # Creating a new note
        try:
            new_note = models.Note(
                content=data["content"],
                tags=data["tags"],
            )
            db.session.add(new_note)
            db.session.flush()

            logger.debug(f"new_note.id: {new_note.id}")

            response_code, response_msg, note_list = query.filter_notes_by_id(new_note.id)
            if note_list is None:
                return apputils.custom_abort(response_code, "Internal Server Error", "")
            if len(note_list) == 0:
                return apputils.custom_abort(404, "Not Found", "")
            result = note_list[0]
            logger.info(f"Notes.post(): Created new note. Details: {result}")
            db.session.commit()

            return make_response(jsonify(result), 201)
        except Exception as e:
            logger.exception(f"Notes.post(): Internal Server Error. Errors: {e}.")
            return apputils.custom_abort(500, "Internal Server Error", "")

    def get(self):
        """Get all the notes stored in the system"""
        try:
            response_code, response_msg, notes_list = query.filter_all_notes()
            if notes_list is None:
                return apputils.custom_abort(response_code, "Internal Server Error", "")
            return jsonify(notes=notes_list)
        except Exception as e:
            logger.exception(f"Notes.get(): internal server error. Errors: {e}.")
            return apputils.custom_abort(response_code, "Internal Server Error", "")

    def delete(self):
        """Delete all the notes stored in the system"""
        try:
            # Delete all rows in the table
            num_rows_deleted = db.session.query(models.Note).delete()
            logger.debug(f"Successfully deleted {num_rows_deleted} notes")
            db.session.commit()

            # Check if an empty array is returned when queried again
            response_code, response_msg, notes_list = query.filter_all_notes()
            if notes_list==[]:
                return make_response(jsonify(notes_list), 204)
            else:
                return apputils.custom_abort(response_code, "Internal Server Error", "Delete all notes failed")
        except Exception as e:
            logger.exception(f"Notes.delete(): internal server error. Errors: {e}.")
            return apputils.custom_abort(500, "Internal Server Error", "")