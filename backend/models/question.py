from extensions import db
from . import TimestampMixin, SoftDeleteMixin

class Question(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='RESTRICT'),
                        nullable=False, index=True)
    statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200), nullable=False)
    option4 = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

    # Relationships
    quiz = db.relationship('Quiz', back_populates='questions')
    answers = db.relationship('Answer', back_populates='question', cascade='all, delete-orphan')
