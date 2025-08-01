from datetime import datetime
from extensions import db

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

class SoftDeleteMixin:
    """
    Adds a deleted_at column for soft deletes. Records with deleted_at != None are considered deleted.
    """
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)

# Import all models for Alembic or Fla
from .user import User
from .subject import Subject
from .chapter import Chapter
from .quiz import Quiz
from .question import Question
from .attempt import Attempt
from .answer import Answer