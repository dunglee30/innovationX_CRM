import os
import smtplib
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT, GMAIL_USERNAME, GMAIL_PASSWORD
from app.repositories.email_logs_repository import EmailLogsRepository

# Gmail SMTP sender using credentials from .env
def send_email(to_email: str, subject: str, body: str, from_email: str = None):
    if not from_email:
        from_email = GMAIL_USERNAME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    email_logs_repo = EmailLogsRepository()
    email_id = str(uuid.uuid4())
    try:
        with smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT) as server:
            server.starttls()
            server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
            server.sendmail(from_email, to_email, msg.as_string())
        email_logs_repo.log_email_status(email_id, to_email, "sent")
    except Exception as e:
        email_logs_repo.log_email_status(email_id, to_email, f"failed: {e}")
        raise RuntimeError(f"Failed to send email: {e}")
