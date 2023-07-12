import os
from dotenv import load_dotenv
from random import randrange
from email.message import EmailMessage
import ssl
import smtplib
load_dotenv()


def sending_activation_number(email_receiver):
    email_sender = os.getenv("EMAIL_SENDER")
    email_password = os.getenv("EMAIL_SENDER_PASSWORD")
    email_receiver = email_receiver

    activation_number = []
    for i in range(6):
        activation_number.append(str(randrange(10)))

    activation_number = "".join(activation_number)

    subject = "Activate your account in Millionaire.app"

    body = f"""
    Hello, {email_receiver}!
    
    Your activation number: {activation_number}.
    
    Type this number into Millionaire.app user activation window.
    If you didn't request this code, you can safely ignore this email. Someone else may have entered your email address by mistake.
    
    Thank You!
    Millionaire.app team
    """

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    except smtplib.SMTPException:
        return "Error with sending number"
    else:
        return {"activation_number": activation_number}
