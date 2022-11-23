from notes_api.resources import Notes
from flask import Blueprint
from flask_restful import Api

notes_bp = Blueprint("notes", __name__)

api = Api(notes_bp)

api.add_resource(Notes, "/note")