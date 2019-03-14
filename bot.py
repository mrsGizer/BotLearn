from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

import ephem
import datetime

PROXY = {'proxy_url': 'socks5://t2.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

date_now = datetime.datetime.now()
now = date_now.strftime('%Y/%m/%d')

dict_planet = {
    'mercury': ephem.Mercury(now),
    'venus': ephem.Venus(now),
    'mars': ephem.Mars(now),
    'pluto': ephem.Pluto(now),
    'jupiter': ephem.Jupiter(now),
    'saturn': ephem.Saturn(now),
    'uranus': ephem.Uranus(now),
    'neptune': ephem.Neptune(now)
}
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO, filename='bot.log')

def greet_user(bot, update):
    text = 'Введите /planet и название планеты на английском: '
    print(text)
    update.message.reply_text(text)

def planet_user(bot, update):
    user_planet = update.message.text.split( )[1].lower()
    if user_planet in dict_planet:
        user_planet = dict_planet[user_planet]
        text_user_planet = ephem.constellation(user_planet)
        print(text_user_planet)
        update.message.reply_text(text_user_planet)

def main():
    mybot = Updater('741279091:AAE_VCv1AKxkcD2v7GbqkTZfiv8B-qr6A5M', request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', planet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    mybot.start_polling()
    mybot.idle()

def talk_to_me(bot, update):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)

main()
