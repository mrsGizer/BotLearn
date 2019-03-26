from glob import glob
import logging
from random import choice

from emoji import emojize
import ephem
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup

import settings


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


def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = 'Привет {} \nВведите /planet и название планеты на английском, \
        чтобы узнать в каком созвездии сейчас находится планета.\
        \nИли введите /cat чтобы получить фото котика'.format(emo)
    my_keyboard = ReplyKeyboardMarkup([['Прислать котика', 'Сменить аватарку']])
    update.message.reply_text(text, reply_markup=my_keyboard)


def planet_user(bot, update, user_data):
    user_planet = update.message.text.split( )[1].lower()
    if user_planet in dict_planet:
        user_planet = dict_planet[user_planet]
        text_user_planet = ephem.constellation(user_planet)
        print(text_user_planet)
        update.message.reply_text(text_user_planet)


def (bot, update, user_data):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'))


def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text('Готово: {}'.format(emo))


def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']


def main():
    mybot = Updater(settings.token, request_kwargs=settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('planet', planet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('cat', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать котика)%', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)%', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()


main()
