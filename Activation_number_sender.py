# Modules import.
import os
from dotenv import load_dotenv
from random import randrange
from email.message import EmailMessage
import ssl
import smtplib
# Loading environment variables.
load_dotenv()


def sending_activation_number(email_receiver):
    """The function responsible for directly sending the activation number in an email to the user and returning
    the generated number."""
    # Assigning values from environment variables to local variables.
    email_sender = os.getenv("EMAIL_SENDER")
    email_password = os.getenv("EMAIL_SENDER_PASSWORD")
    # Assigning email provided by the user to the local variable.
    email_receiver = email_receiver

    # Generating activation number for user.
    activation_number = []
    for i in range(6):
        activation_number.append(str(randrange(10)))

    # Converting activation number into string.
    activation_number = "".join(activation_number)
    # Creating subject of e-mail.
    subject = "Activate your account in Millionaire.app"
    # Creating body of e-mail.
    body = f"""
    Hello, {email_receiver}!
    
    Your activation number: {activation_number}.
    
    Type this number into Millionaire.app user activation window.
    If you didn't request this code, you can safely ignore this email. Someone else may have entered your email address by mistake.
    
    Thank You!
    Millionaire.app team
    """
    # Creating object of e-mail, declaring "From", "To", "Subject", and setting content of email.
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)

    # Creating context.
    context = ssl.create_default_context()

    # Trying to send email object by smtp server. First program logging in by name of email and password, then sending
    # an e-mail with email_sender, email_receiver and object od e-mail as a string.
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    # When error with sending, program returning error.
    except smtplib.SMTPException:
        return "Error with sending number"

    # When everything ok, program returning activation number in dictionary.
    else:
        return {"activation_number": activation_number}
