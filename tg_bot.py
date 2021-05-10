import telebot
import schedule
from threading import Thread
from telebot import types
from datetime import date, datetime
from time import sleep
from rate_check import *

#Enter API_KEY from file 'Keys'
API_KEY = ''
bot = telebot.TeleBot(API_KEY)
url_bank = 'https://bank.gov.ua/ua/markets/exchangerates?date=23.04.2021&period=daily'
dollar_rate_position = ('td', 34)
emails = set()
users = set()

markup_for_yes_no = types.InlineKeyboardMarkup()
item_yes = types.InlineKeyboardButton(text='YES', callback_data='yes')
item_no = types.InlineKeyboardButton(text='NO', callback_data='no')
markup_for_yes_no.add(item_yes, item_no)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi, I'm DollarCurrencyGrowthBot. I will send You Dollar Currency, if it has grown since your last check.")
    users.add(message.chat.id)
    today = date.today().strftime("%d/%m/%Y").replace('/','.')
    actual_url_bank = url_bank[:49] + today + url_bank[:-13]
    dollar_value = starter(actual_url_bank, dollar_rate_position)
    text = f'Now 1 USD costs {dollar_value} UAH'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['addmail'])
def add_mail(message):
    bot.send_message(message.chat.id, 'Your Email is:')
    bot.register_next_step_handler(message, mail)


@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, 'Your Email is:')
        bot.register_next_step_handler(call.message, mail)
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Fine. if you want to add mail, send /addmail')


def mail(message):
    recipient = message.text
    if not  check_correctness_mail(recipient):
        bot.send_message(message.chat.id, "Invalid mail")
        bot.send_message(message.chat.id, "Do you want to get Dollar Currency Growth also on Your mail?",
            reply_markup=markup_for_yes_no
        )
    else:
        emails.add(recipient)
        bot.send_message(message.chat.id, "Now you will get Dollar Currency Growth on Your mail")


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


def function_to_run():
    today = date.today().strftime("%d/%m/%Y").replace('/','.')
    actual_url_bank = url_bank[:49] + today + url_bank[:-13]
    dollar_value = starter(actual_url_bank, dollar_rate_position)
    text = f'Now 1 USD costs {dollar_value} UAH'
    for user in users:
        try:
            bot.send_message(user, text)
        except Exception:
            pass
    for recipient in emails:
        index(text, recipient)


if __name__ == "__main__":
    schedule.every().day.at("16:01").do(function_to_run)
    Thread(target=schedule_checker).start() 
    bot.polling()
