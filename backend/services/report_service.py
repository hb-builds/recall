from jinja2 import Environment, FileSystemLoader
import os
import uuid
import datetime
from extensions import db
from models.attempt import Attempt
from models.user import User
from weasyprint import HTML

TEMPLATES_DIR = os.path.join(os.getcwd(), 'templates')
REPORTS_DIR = os.path.join(os.getcwd(), 'reports')
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)


def generate_monthly_report(user_id: int, year: int, month: int) -> str:
    """
    Generates a PDF monthly activity report for the user and returns the file path.
    Includes quiz count, average score, and ranking.
    """
    # Fetch user and their attempts in the month
    start = datetime.datetime(year, month, 1)
    end = datetime.datetime(year + (month // 12), ((month % 12) + 1), 1)

    user = User.query.get(user_id)
    attempts = (Attempt.query.filter(Attempt.user_id == user_id,
                                     Attempt.submitted_at >= start,
                                     Attempt.submitted_at < end).all())
    total = len(attempts)
    avg_score = sum(a.score for a in attempts) / total if total > 0 else 0

    # Determine ranking among all users
    scores_by_user = (db.session.query(
        Attempt.user_id,
        db.func.avg(Attempt.score).label('avg')).filter(
            Attempt.submitted_at >= start, Attempt.submitted_at
            < end).group_by(Attempt.user_id).order_by(db.desc('avg')).all())
    ranking = next(
        (idx + 1
         for idx, (uid, _) in enumerate(scores_by_user) if uid == user_id),
        None)

    # Render HTML via Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template('monthly_report.html')
    html = template.render(user=user,
                           year=year,
                           month=month,
                           total_quizzes=total,
                           average_score=avg_score,
                           ranking=ranking,
                           attempts=attempts)
    filename = f"report_{user_id}_{year}_{month}_{uuid.uuid4().hex}.pdf"
    filepath = os.path.join(REports_DIR, filename)
    HTML(string=html).write_pdf(filepath)
    return filepath
