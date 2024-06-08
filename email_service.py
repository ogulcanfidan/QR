# email_service.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Çevre değişkenlerini yükleyin
load_dotenv()

def init_email_service():
    from_email = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, password)
    return server, from_email

def send_email(server, from_email, to_email, subject, message):
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))
    server.sendmail(from_email, to_email, msg.as_string())

def close_email_service(server):
    server.quit()

def send_email_template(name, phone, complaint, to_email):
    subject = "Yeni Şikayet"
    message = f"Ad: {name}\nTelefon: {phone}\nŞikayet: {complaint}"
    server, from_email = init_email_service()
    send_email(server, from_email, to_email, subject, message)
    close_email_service(server)
