import os
import smtplib
import imghdr
from email.message import EmailMessage

#Enter EMAIL_ADDRESS from file 'Keys'
EMAIL_ADDRESS = 'dollar.currency.exchange@gmail.com'
#Enter EMAIL_PASSWORD from file 'Keys'
EMAIL_PASSWORD = 'DollarCurrency'


def index(message, recipient):
    msg = EmailMessage()
    msg['Subject'] = 'Dollar Currency'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient

    msg.set_content(message)


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
