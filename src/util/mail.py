import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
logger = logging.getLogger(__name__)


def send_mail(subject: str, body: str, body_type: str, to_user: str) -> None:
    """send mail function

    Args:
        subject (str): subject of the mail
        body (str): body of the mail
        body_type (str): body type
        to_user (str): rec's mail
    """
    SENDER_EMAIL = os.environ['SENDER_EMAIL']
    SENDER_PASSWD = os.environ['SENDER_PASSWD']
    PORT = 465
    SMTP_SERVER = "smtp.gmail.com"
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = SENDER_EMAIL
    message["To"] = to_user

    if body_type == "html":
        body_part = MIMEText(body, "html")
    else:
        body_part = MIMEText(body, "text")

    message.attach(body_part)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWD)
        server.sendmail(
            SENDER_EMAIL, to_user, message.as_string()
        )
