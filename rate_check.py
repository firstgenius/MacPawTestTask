from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import re
import smtplib
from mail_sender import index
import telebot
from datetime import date, datetime

def to_html(url):
    page = urlopen(url)
    return page

def finder(html, position):
    soup = BeautifulSoup(html, 'lxml')
    all_matches = soup.find_all(position[0])
    needed_line = all_matches[position[1]]
    byte_dollar_rate = needed_line.encode_contents()
    str_dollar_rate = byte_dollar_rate.decode("utf-8")
    new_str_dollar_rate = str_dollar_rate.replace(',','.')
    float_dollar_rate = '{:.4f}'.format(float(new_str_dollar_rate))
    return float_dollar_rate

def check_correctness_rate(rate) -> bool:
    value = re.findall(r"[0-9]+.[0-9]{4}", rate)
    if value != []:
        return value[0] == rate
    return False

def check_correctness_mail(email) -> bool:
    regexp = r'(?!.*?[ \'.-]{2})([\w\d!#$%&\'*+\/=?^_`{|.}~-]+@(?:[\w\d](?:[\w\d-]*[\w\d])?\.)+)([com]{3}|[org]{3}|[edu]{3}|[gov]{3}|[net]{3}|[ua]{2})*'
    try:
        return email == re.match(regexp, email).group()
    except AttributeError:
        return False

def starter(url_bank, dollar_rate_position):
    html_bank = to_html(url_bank)
    dollar_value = finder(html_bank, dollar_rate_position)

    while not check_correctness_rate(dollar_value):
        time.sleep(60)
        html_bank = to_html(url_bank)
        dollar_value = finder(html_bank, dollar_rate_position)
    
    return dollar_value


if __name__ == '__main__':
    # If run this program, you can send JUST emails with it
    today = date.today().strftime("%d/%m/%Y").replace('/','.')
    url_bank = 'https://bank.gov.ua/ua/markets/exchangerates?date=23.04.2021&period=daily'
    actual_url_bank = url_bank[:49] + today + url_bank[:-13]
    dollar_rate_position = ('td', 34)
    recipient = input('Recipient:')
    while not check_correctness_mail(recipient):
        recipient = input('Recipient:')

    dollar_value = starter(actual_url_bank, dollar_rate_position)
    
    message = f'Hi, now 1 USD costs {dollar_value} UAH'
    index(message, recipient)

    while True:
        time.sleep(900)
        prev_dollar_rate = dollar_value
        dollar_value = starter(actual_url_bank, dollar_rate_position)
        if dollar_value > prev_dollar_rate:
            message = f'Hi, the dollar rose, now 1 USD costs {dollar_value} UAH'
            index(message, recipient)
