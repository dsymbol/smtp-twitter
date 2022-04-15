import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(sender, password, receiver, subject, message):
    email = MIMEMultipart("alternative")
    email["Subject"] = subject
    email["From"] = sender
    email["To"] = receiver
    message = message
    email.attach(MIMEText(message))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(
            sender, receiver, email.as_string()
        )
