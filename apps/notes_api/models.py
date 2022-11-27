from database.models import Base
from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    String
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type

class Note(Base):
    """Model for a note"""

    __tablename__ = "notes"
    __table_args__ = (PrimaryKeyConstraint("id"),)

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="id of the note",
    )

    content = Column(String, nullable=False, comment="content of the note")

    tags = Column(
        mutable_json_type(dbtype=JSONB, nested=True),
        nullable=False,
        comment="JSON formatted array of tags, each one is a string",
        server_default='["random"]',
    )

    def serialize(self):
        """Create dictionary containing Note info"""
        out = dict()
        out["id"] = int(self.id)
        out["content"] = str(self.content)
        out["tags"] = self.tags
        return out