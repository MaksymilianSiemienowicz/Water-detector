import requests
import os
import time
import re
from email.message import EmailMessage
import ssl
import smtplib
from email.header import decode_header
import logging

api_url = os.environ['API_URL']
email = os.environ['EMAIL']
email_password = os.environ['EMAIL_PASSWORD']
response_template = r"Poziom wody: (\d+\.\d+)"
was_mail_send = 0
logger = logging.getLogger(__name__)
logging.basicConfig(filename='./logs/app.log', level=logging.INFO)


def send_mail(email_login, email_pass, value):
        email = EmailMessage()
        email['From'] = email_login
        email['To'] = "eMail"
        email['Subject'] = "AWARIA AKWARIUM!"
        email.set_content("WODA SIE LEJE!\n Wartosc na czujniku: " + str(value))

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_login, email_pass)
                smtp.sendmail(email_login, "EMAIL", email.as_string())
        return("Mail sent")



while True:
        try:
                regex = re.search(response_template, requests.get(api_url).text)
                value = float(regex.group(1))
                logger.info("Wartosc to: "+ str(value))
                if value > 0.215073 and was_mail_send == 0:
                        send_mail(email, email_password, value)
                        was_mail_send = 1
                        logger.waring("Wartosc jest za wysoka! : " + str(value))
        except Exception as e:
                loggger.ERROR(f"Wystąpił błąd!: {e}")
        time.sleep(60)
