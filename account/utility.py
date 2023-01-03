import os
from email.message import EmailMessage
from .password import password
import ssl
import smtplib
import re


def upload_dir_path(instance, filename):
    return 'profile_pic/{0}/{1}'.format(instance.user.pk, filename)


def send_email(email_receiver,user_code):
    email_sender = 'shahranrifat2@gmail.com'
    subject = "Travelogram verification code"
    body = "Verification Code:"+" "+user_code

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, password)
        smtp.sendmail(email_sender,email_receiver,em.as_string())

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def secure_password(password):
    is_lower = False
    is_upper = False
    length_okay = False
    has_digit = False
    has_symbols = False
    password_okay = False

    if len(password) > 8:
        length_okay = True

    for c in password:
        if c.islower():
            is_lower = True
            break
    
    for c in password:
        if c.isupper():
            is_upper = True
            break

    for c in password:
        if c.isdigit():
            has_digit = True
            break

    if password.isalnum() == False:
        has_symbols = True

    if length_okay is True and is_lower is True and is_upper is True and has_digit is True and has_symbols is True:
        password_okay = True
        return password_okay
    else:
        return password_okay

    



