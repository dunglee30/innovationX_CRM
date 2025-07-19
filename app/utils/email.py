import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT, GMAIL_USERNAME, GMAIL_PASSWORD

# Gmail SMTP sender using credentials from .env
def send_email(to_email: str, subject: str, body: str, from_email: str = None):
    if not from_email:
        from_email = GMAIL_USERNAME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT) as server:
            server.starttls()
            server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
            server.sendmail(from_email, to_email, msg.as_string())
    except Exception as e:
        raise RuntimeError(f"Failed to send email: {e}")
