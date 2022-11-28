"""Logic for RESTFUL APIs of notes"""

import logging
import requests

from notes_api import models
from notes_api import query
from notes_api.schemas import NoteSchema
from core import utils as apputils
from core.db import db
from core import config
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

        # Validate NoteSchema request json
        try:
            logger.debug(f"NoteSchema json_data: {json_data}")
            template_schema = NoteSchema()
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

        # Use GCP Natural Language API to do Entity Recognition
        try:
            # Prepare payload for the cloud API
            payload = {
                'encodingType': 'UTF8',
                'document': {
                    'type': 'PLAIN_TEXT',
                    'content': data['content']
                    }}
            headers = {"Content-Type": "application/json; charset=utf-8"}
            res = requests.post(config.GCP_API_URL, headers=headers, json=payload)
            entities = []
            if res.ok:
                cloud_data = res.json()
                logger.debug(f"cloud_data: {cloud_data}")
                
                if "entities" in cloud_data:
                    # Sort the array by key=salience
                    entities_list = cloud_data["entities"]
                    sorted(entities_list, key = lambda x: x['salience'], reverse=True)
                    logger.debug(f"sorted_cloud_data: {entities_list}")
                    # Only include top 3 entities to avoid clutter in the frontend
                    if len(entities_list) <= 3:
                        for obj in entities_list:
                            entities.append(obj["name"])
                    else:
                        entities.append(entities_list[0]["name"])
                        entities.append(entities_list[1]["name"])
                        entities.append(entities_list[2]["name"])

        except Exception as e:
            logger.exception(f"Notes.post(): Internal Server Error. Errors: {e}.")
            return apputils.custom_abort(500, "Internal Server Error", "Error with GCP API call")

        # Creating a new note
        try:
            new_note = models.Note(
                content=data["content"],
                tags=[x.lower() for x in data["tags"]],  # lowercase all tags to prevent distinguishing between 'Funny' and 'funny'
                entities=[x.lower() for x in entities],  # same reason as above
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
            logger.exception(f"Notes.get(): Internal server error. Errors: {e}.")
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
            logger.exception(f"Notes.delete(): Internal server error. Errors: {e}.")
            return apputils.custom_abort(500, "Internal Server Error", "")


class Note(Resource):
    """
    Handle the following requests:
    1. GET Get a note stored in the system
    2. PUT Update a note
    3. DELETE Delete a note
    """

    def get(self, id):
        """Get a note"""
        try:
            response_code, response_message, notes_list = query.filter_notes_by_id(id)
            if notes_list is None:
                return apputils.custom_abort(response_code, "Internal Server Error", "")
            if len(notes_list) == 0:
                return apputils.custom_abort_with_id(404, f"Note with ID {id} not found", id)
            return jsonify(notes_list[0])
        except Exception as e:
            logger.exception(f"Note.get(): Internal server error. Errors: {e}.")
            return apputils.custom_abort(response_code, "Internal Server Error", "")


    def put(self, id):
        """Update a note"""
        try:
            json_data = request.get_json()
        except Exception:
            msg = "Notes.put(): No JSON payload found."
            logger.warning(msg)
            return apputils.custom_abort(400, "Bad Request", msg)

        # Validate NoteSchema request json
        try:
            template_schema = NoteSchema()
            data = template_schema.load(json_data)
        except ValidationError as err:
            logger.warning(
                f"Note.put(): request with invalid data.\n"
                f"Details: {json_data}\n"
                f"Errors: {err.messages}\n"
            )
            return apputils.custom_abort(
                400,
                "Bad Request",
                f"Please correct the highlighted errors and try again: {err.messages}",
            )

        logger.debug(f"Validated data: {data}")

        try:
            response_code, response_msg, new_note = query.update_note(
                int(id),
                data.get("content", None),
                data.get("tags", None),
            )
            if new_note is None:
                return apputils.custom_abort_with_id(404, f"Note with ID {id} not found", id)
            logger.info(f"Updated note: {new_note}")

            return jsonify(new_note)
        except Exception as e:
            logger.exception(f"Note.put(): Internal server error. Errors: {e}.")
            return apputils.custom_abort(response_code, "Internal Server Error", "")


    def delete(self, id):
        """Delete all the notes stored in the system"""
        try:
            # Query the required note first by id
            note = (
                db.session.query(models.Note)
                .filter_by(id=int(id))
                .one_or_none()
            )
            if note is None:
                return apputils.custom_abort_with_id(404, f"Note with ID {id} not found", id)

            # If found, delete it
            db.session.delete(note)
            db.session.commit()

            # Check if an empty array is returned when queried again
            response_code, response_msg, notes_list = query.filter_notes_by_id(id)
            if notes_list==[]:
                return make_response(jsonify(notes_list), 204)
            else:
                return apputils.custom_abort(response_code, "Internal Server Error", f"Deleting note {id} failed")
        except Exception as e:
            logger.exception(f"Note.delete(): Internal server error. Errors: {e}.")
            return apputils.custom_abort(500, "Internal Server Error", "")


class FunnyNote(Resource):
    """
    Create a funny note based on two APIs.
    """

    def post(self):
        # Call the random user generator API and store the first and last names
        try:
            res = requests.get(config.RAND_USER_GEN_URL)
            if res.ok:
                data = res.json()
                logger.debug(f"data: {data}")
                first_name = str(data["results"][0]["name"]["first"])
                last_name = str(data["results"][0]["name"]["last"])
            else:
                logger.debug(f"[NOT SUCCEED] Error: {res.json()}")
        except Exception as e:
            logger.exception(f"Random user generation failed. Errors: {e}.")
            return apputils.custom_abort(500, "Internal Server Error", "Random user generation failed")

        # Call the random Chuck Norris joke API and replace it with the saved user name
        try:
            res = requests.get(config.RAND_CHUCK_NORRIS_JOKE_URL, params={'name': f"{first_name} {last_name}"})
            if res.ok:
                data = res.json()
                logger.debug(f"data: {data}")
                joke = str(data["value"])
            else:
                logger.debug(f"[NOT SUCCEED] Error: {res.json()}")
        except Exception as e:
            logger.exception(f"Random joke generation failed. Errors: {e}.")
            return apputils.custom_abort(500, "Internal Server Error", "Random joke generation failed")

        # Use GCP Natural Language API to do Entity Recognition
        try:
            # Prepare payload for the cloud API
            payload = {
                'encodingType': 'UTF8',
                'document': {
                    'type': 'PLAIN_TEXT',
                    'content': joke
                    }}
            headers = {"Content-Type": "application/json; charset=utf-8"}
            res = requests.post(config.GCP_API_URL, headers=headers, json=payload)
            entities = []
            if res.ok:
                cloud_data = res.json()
                logger.debug(f"cloud_data: {cloud_data}")

                if "entities" in cloud_data:
                    # Sort the array by key=salience
                    entities_list = cloud_data["entities"]
                    sorted(entities_list, key = lambda x: x['salience'], reverse=True)
                    logger.debug(f"sorted_cloud_data: {entities_list}")
                    # Only include top 3 entities to avoid clutter in the frontend
                    if len(entities_list) <= 3:
                        for obj in entities_list:
                            entities.append(obj["name"])
                    else:
                        entities.append(entities_list[0]["name"])
                        entities.append(entities_list[1]["name"])
                        entities.append(entities_list[2]["name"])

        except Exception as e:
            logger.exception(f"FunnyNote.post(): Internal Server Error. Errors: {e}.")
            return apputils.custom_abort(500, "Internal Server Error", "Error with GCP API call")

        # Creating a new note
        try:
            new_note = models.Note(
                content=joke,
                tags=["funny"],
                entities=[x.lower() for x in entities],
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
            logger.info(f"FunnyNote.post(): Created new note. Details: {result}")
            db.session.commit()

            return make_response(jsonify(result), 201)
        except Exception as e:
            logger.exception(f"FunnyNote.post(): Internal Server Error. Errors: {e}.")
            return apputils.custom_abort(500, "Internal Server Error", "")


class Tag(Resource):
    """
    Get all the notes with the same tag
    """

    def get(self, tag):
        try:
            tag = str(tag)
            response_code, response_msg, notes_list = query.filter_notes_by_tag(tag)
            if notes_list is None:
                return apputils.custom_abort(response_code, "Internal Server Error", "")
            return jsonify(notes=notes_list)
        except Exception as e:
            logger.exception(f"Tag.get(): Internal server error. Errors: {e}.")
            return apputils.custom_abort(response_code, "Internal Server Error", "")


class Entity(Resource):
    """
    Get all the notes with the same entity
    """

    def get(self, entity):
        try:
            entity = str(entity)
            response_code, response_msg, notes_list = query.filter_notes_by_entity(entity)
            if notes_list is None:
                return apputils.custom_abort(response_code, "Internal Server Error", "")
            return jsonify(notes=notes_list)
        except Exception as e:
            logger.exception(f"Entity.get(): Internal server error. Errors: {e}.")
            return apputils.custom_abort(response_code, "Internal Server Error", "")


class Tags(Resource):
    """
    Get all the tags stored in the system
    """

    def get(self):
        try:
            response_code, response_msg, tags_list = query.filter_all_tags()
            if tags_list is None:
                return apputils.custom_abort(response_code, "Internal Server Error", "")
            return jsonify(tags=tags_list)
        except Exception as e:
            logger.exception(f"Tags.get(): Internal server error. Errors: {e}.")
            return apputils.custom_abort(response_code, "Internal Server Error", "")
