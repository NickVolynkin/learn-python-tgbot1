import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.update import Update
from telegram.bot import Bot

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():
    token = os.environ['TG_TOKEN']
    proxy = {'proxy_url': os.environ['PROXY_URL'],
             'urllib3_proxy_kwargs': {
                 'username': os.environ['PROXY_USER'],
                 'password': os.environ['PROXY_PASS']}
             }

    bot = Updater(token, request_kwargs=proxy)

    dispatcher = bot.dispatcher
    dispatcher.add_handler(CommandHandler("ping", greet_user))
    dispatcher.add_handler(MessageHandler(Filters.text, talk_to_me))

    bot.start_polling()
    bot.idle()


def greet_user(bot: Bot, update: Update):
    logging.info('command: /ping')
    update.message.reply_text('pong')


def talk_to_me(bot: Bot, update: Update):
    user_text = update.message.text
    logging.info('message: ' + user_text)
    update.message.reply_text(user_text)


if __name__ == '__main__':
    main()
