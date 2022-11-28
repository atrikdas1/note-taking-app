"""
This file contains the various possible APIs supported
"""
from notes_api.resources import Notes, Note, FunnyNote, Tag, Tags, Entity
from flask import Blueprint
from flask_restful import Api

notes_bp = Blueprint("notes", __name__)

api = Api(notes_bp)

api.add_resource(Notes, "/note")
api.add_resource(Note, "/note/<id>")
api.add_resource(FunnyNote, "/note/funny")
api.add_resource(Tag, "/note/tag/<tag>")
api.add_resource(Tags, "/tags")
api.add_resource(Entity, "/note/entity/<entity>")