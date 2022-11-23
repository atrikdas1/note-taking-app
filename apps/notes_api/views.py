from notes_api.resources import Notes, Note, FunnyNote, Tag
from flask import Blueprint
from flask_restful import Api

notes_bp = Blueprint("notes", __name__)

api = Api(notes_bp)

api.add_resource(Notes, "/note")
api.add_resource(Note, "/note/<id>")
api.add_resource(FunnyNote, "/note/funny")
api.add_resource(Tag, "/note/tag/<tag>")