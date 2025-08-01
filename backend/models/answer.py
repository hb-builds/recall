from extensions import db
from . import TimestampMixin

class Answer(db.Model, TimestampMixin):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempts.id', ondelete='RESTRICT'),
                            nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='RESTRICT'),
                             nullable=False, index=True)
    selected_option = db.Column(db.Integer, nullable=False)

    # Relationships
    attempt = db.relationship('Attempt', back_populates='answers')
    question = db.relationship('Question', back_populates='answers')
