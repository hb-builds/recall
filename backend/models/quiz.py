from extensions import db
from . import TimestampMixin, SoftDeleteMixin

class Quiz(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id', ondelete='RESTRICT'),
                           nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=True)
    duration_min = db.Column(db.Integer, nullable=False)

    # Relationships
    chapter = db.relationship('Chapter', back_populates='quizzes')
    questions = db.relationship('Question', back_populates='quiz', cascade='all, delete-orphan')
    attempts = db.relationship('Attempt', back_populates='quiz', cascade='all, delete-orphan')
