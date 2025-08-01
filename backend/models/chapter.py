from extensions import db
from . import TimestampMixin, SoftDeleteMixin

class Chapter(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='RESTRICT'),
                           nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Relationships
    subject = db.relationship('Subject', back_populates='chapters')
    quizzes = db.relationship('Quiz', back_populates='chapter', cascade='all, delete-orphan')
