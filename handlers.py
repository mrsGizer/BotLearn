from glob import glob
import os
from random import choice

import ephem
import datetime
from utils import get_keyboard, get_user_emo, is_cat
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ParseMode
from bot import ConversationHandler

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


def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = 'Привет {} \nВведите /planet и название планеты на английском,\
        \nчтобы узнать в каком созвездии сейчас находится планета.\
        \nИли введите /cat чтобы получить фото котика'.format(emo)
    contact_button = KeyboardButton('Прислать контакт', request_contact=True)
    location_button = KeyboardButton('Прислать локацию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
        ['Прислать котика', 'Сменить аватарку'],
        [contact_button, location_button]
        ]
        )
    update.message.reply_text(text, reply_markup=get_keyboard())


def planet_user(bot, update, user_data):
    user_planet = update.message.text.split( )[1].lower()
    if user_planet in dict_planet:
        user_planet = dict_planet[user_planet]
        text_user_planet = ephem.constellation(user_planet)
        print(text_user_planet)
        update.message.reply_text(text_user_planet)


def talk_to_me(bot, update, user_data):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(
        chat_id=update.message.chat.id,
        photo=open(cat_pic, 'rb'),
        reply_markup=get_keyboard()
        )


def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text(
        'Готово: {}'.format(emo),
        reply_markup=get_keyboard()
        )


def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text(
        'Готово: {}'.format(get_user_emo(user_data)),
        reply_markup=get_keyboard()
        )


def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text(
        'Готово: {}'.format(get_user_emo(user_data)),
        reply_markup=get_keyboard()
        )


def check_user_photo(bot, update, user_data):
    update.message.reply_text("Обрабатываю фото")
    os.makedirs('downloads', exist_ok=True)
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id))
    photo_file.download(filename)
    if is_cat(filename):
        update.message.reply_text("Обнаружен котик, добавляю в библиотеку.")
        new_filename = os.path.join(
            'images',
            'cat_{}.jpg'.format(photo_file.file_id)
            )
        os.rename(filename, new_filename)
    else:
        os.remove(filename)
        update.message.reply_text("Тревога, котик не обнаружен!")


def anketa_start(bot, update, user_data):
    update.message.reply_text(
        "Как вас зовут? Напишите имя и фамилию",
        reply_markup=ReplyKeyboardRemove()
        )
    return "name"


def anketa_get_name(bot, update, user_data):
    user_name = update.message.text
    if len(user_name.split(" ")) < 2:
        update.message.reply_text("Пожалуйста, напишите имя и фамилию")
        return "name"
    else:
        user_data["anketa_name"] = user_name
        reply_keyboard = [["1", "2", "3", "4", "5"]]

        update.message.reply_text(
            "Понравился ли вам курс? Оцените по шкале от 1 до 5",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True)
        )
        return "rating"


def anketa_rating(bot, update, user_data):
    user_data["anketa_rating"] = update.message.text

    update.message.reply_text("""
Оставьте комментарий в свободной форме 
или пропустите этот шаг, введя /cancel
    """)
    return "comment"


def anketa_comment(bot, update, user_data):
    user_data["anketa_comment"] = update.message.text
    user_text = """
<b>Имя Фамилия:</b> {anketa_name}
<b>Оценка:</b> {anketa_rating}
<b>Комментарий:</b> {anketa_comment}""".format(**user_data)

    update.message.reply_text(
        user_text,
        reply_markup=get_keyboard(),
        parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def anketa_skip_comment(bot, update, user_data):
    user_text = """
<b>Имя Фамилия:</b> {anketa_name}
<b>Оценка:</b> {anketa_rating}""".format(**user_data)

    update.message.reply_text(
        user_text,
        reply_markup=get_keyboard(),
        parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def dontknow(bot, update, user_data):
    update.message.reply_text('Не понимаю')
