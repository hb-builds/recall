import csv
import os
import uuid
from models.attempt import Attempt
from models.quiz import Quiz
from extensions import db

EXPORT_DIR = os.path.join(os.getcwd(), 'exports')
if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

def generate_attempts_csv(user_id: int) -> str:
    """
    Generate a CSV of all attempts for a given user and return the file path.
    """
    filename = f"attempts_{user_id}_{uuid.uuid4().hex}.csv"
    filepath = os.path.join(EXPORT_DIR, filename)

    attempts = (
        db.session.query(Attempt)
        .filter_by(user_id=user_id)
        .order_by(Attempt.submitted_at)
        .all()
    )
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['attempt_id','quiz_id','score','submitted_at'])
        for a in attempts:
            writer.writerow([a.id, a.quiz_id, a.score, a.submitted_at])

    return filepath

def generate_all_quizzes_csv() -> str:
    """
    Generate a CSV of all quizzes and return the file path.
    """
    filename = f"all_quizzes_{uuid.uuid4().hex}.csv"
    filepath = os.path.join(EXPORT_DIR, filename)

    quizzes = db.session.query(Quiz).all()
    
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['quiz_id', 'title', 'chapter_id', 'duration_min', 'scheduled_at'])
        for q in quizzes:
            writer.writerow([q.id, q.title, q.chapter_id, q.duration_min, q.scheduled_at])

    return filepath