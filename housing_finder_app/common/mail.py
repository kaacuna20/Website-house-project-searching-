from smtplib import SMTPException
from threading import Thread
from flask import current_app
from flask_mail import Message
from housing_finder_app.__ini__ import mail


def send_email(subject, sender, recipients, text_body,
               cc=None, bcc=None, html_body=None):
    msg = Message(subject, sender=sender, recipients=recipients, cc=cc, bcc=bcc)
    msg.body = text_body
    mail.send(msg)
    if html_body:
        msg.html = html_body
    mail.send(msg)
