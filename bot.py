import logging

from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler, Filters, MessageHandler

from handlers import *
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO, filename='bot.log')


def main():
    mybot = Updater(settings.token, request_kwargs=settings.PROXY)
    logging.info('Бот запускается')

    dp = mybot.dispatcher

    anketa = ConversationHandler(
        entry_points=[RegexHandler('^(Заполнить анкету)$', anketa_start, pass_user_data=True)],
        states={
        "name": [MessageHandler(Filters.text, anketa_get_name, pass_user_data=True)],
        "rating": [RegexHandler('^(1|2|3|4|5)$', anketa_rating, pass_user_data=True)],
        "comment": [MessageHandler(Filters.text, anketa_comment, pass_user_data=True),
                    CommandHandler('cancel', anketa_skip_comment, pass_user_data=True)],
        },
        fallbacks=[MessageHandler(
            Filters.text | Filters.video | Filters.photo | Filters.document,
            dontknow,
            pass_user_data=True
        )]
    )
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler('planet', planet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('cat', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
