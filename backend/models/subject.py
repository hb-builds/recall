from extensions import db
from . import TimestampMixin, SoftDeleteMixin

class Subject(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Relationships
    chapters = db.relationship('Chapter', back_populates='subject', cascade='all, delete-orphan')