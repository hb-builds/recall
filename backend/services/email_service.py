import smtplib
import os
from email.message import EmailMessage

SMTP_HOST = os.getenv('SMTP_HOST', 'localhost')
SMTP_PORT = int(os.getenv('SMTP_PORT', 25))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'no-reply@example.com')


def send_email(to: str, subject: str, body: str, attachments: list = None):
    """
    Send an email with optional attachments.
    """
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to
    msg.set_content(body, subtype='html')

    # Attach files if any
    attachments = attachments or []
    for file_path in attachments:
        with open(file_path, 'rb') as f:
            data = f.read()
            maintype, subtype = 'application', 'octet-stream'
            filename = os.path.basename(file_path)
            msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        if SMTP_USER and SMTP_PASSWORD:
            smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)