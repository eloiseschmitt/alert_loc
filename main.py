import requests
import time
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)


def monitor_url(url, check_interval=3600):
    last_hash = get_content_hash(url)

    while True:
        time.sleep(check_interval)
        current_hash = get_content_hash(url)

        if current_hash != last_hash:
            send_email_alert(url)
            last_hash = current_hash
        else:
            print("send_email")
            send_email_alert(url)


def get_content_hash(url):
    response = requests.get(url)
    return hashlib.md5(response.content).hexdigest()


def send_email_alert(url):
    sender_email = os.getenv("GMAIL")
    receiver_email = os.getenv("EMAIL")
    password = os.getenv("PWD")
    # Création du message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Alert: URL Content Changed"
    # Corps du message
    body = f"The content of the URL {url} has changed. Please check it."
    message.attach(MIMEText(body, "plain"))
    # Envoi de l'e-mail
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(message)
            print("Email sent successfully")
    except smtplib.SMTPAuthenticationError:
        logging.error("Authentication failed. Please check your email and password.")
    except Exception as e:
        logging.error(f"Une erreur s'est produite : {str(e)}")


if __name__ == '__main__':
    monitor_url(
        'https://www.bienici.com/recherche/location/dessin-670e9d9783b82e00b1799bb5/4-pieces-et-plus?prix-max=1800&surface-min=80&chambres-min=3')
