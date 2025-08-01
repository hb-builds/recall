from extensions import db
from . import TimestampMixin

class Attempt(db.Model, TimestampMixin):
    __tablename__ = 'attempts'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='RESTRICT'),
                        nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'),
                        nullable=False, index=True)
    started_at = db.Column(db.DateTime, nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=True)
    score = db.Column(db.Integer, nullable=True)

    # Relationships
    user = db.relationship('User', back_populates='attempts')
    quiz = db.relationship('Quiz', back_populates='attempts')
    answers = db.relationship('Answer', back_populates='attempt', cascade='all, delete-orphan')
