from celery import shared_task
from extensions import cache, db
from models.user import User
from models.attempt import Attempt
from models.quiz import Quiz
from services.report_service import generate_monthly_report
from services.email_service import send_email
import datetime

@shared_task
def send_daily_reminders():
    """
    Send reminders to users who haven't attempted any quiz in the last 24 hours
    or if new quizzes exist since their last visit.
    """
    now = datetime.datetime.utcnow()
    since = now - datetime.timedelta(days=1)
    users = User.query.filter_by(role='user').all()
    for user in users:
        last_attempt = (
            Attempt.query
            .filter(Attempt.user_id == user.id)
            .order_by(Attempt.submitted_at.desc())
            .first()
        )
        
        last_active = last_attempt.submitted_at if last_attempt else since
        
        new_quizzes_count = Quiz.query.filter(Quiz.created_at > last_active).count()

        if new_quizzes_count > 0:
            subject = "New Quizzes Available!"
            body = f"Hi {user.full_name},\n\nThere are {new_quizzes_count} new quizzes available for you to attempt. Log in now to check them out!"
            send_email(user.email, subject, body)
        elif not last_attempt or last_attempt.submitted_at < since:
            subject = "Quiz Reminder"
            body = f"Hi {user.full_name},\n\nIt's been a while since your last quiz attempt. Please log in to take new quizzes!"
            send_email(user.email, subject, body)

@shared_task
def send_monthly_reports():
    """
    Generate and send monthly activity reports for all users.
    """
    today = datetime.datetime.utcnow()
    year = today.year
    month = today.month - 1 or 12
    if month == 12:
        year -= 1

    users = User.query.filter_by(role='user').all()
    for user in users:
        report_path = generate_monthly_report(user.id, year, month)
        subject = f"Your Activity Report for {year}-{month:02d}"
        # Read HTML content
        with open(report_path, 'r') as f:
            html_body = f.read()
        send_email(user.email, subject, html_body, attachments=[report_path])