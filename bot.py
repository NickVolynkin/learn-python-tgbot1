import logging
import os

from telegram.ext import Updater, CommandHandler
from telegram.update import Update

PROXY = {'proxy_url': os.environ['PROXY_URL'],
         'urllib3_proxy_kwargs': {
             'username': os.environ['PROXY_USER'],
             'password': os.environ['PROXY_PASS']}
         }


def greet_user(bot, update: Update):
    update.message.reply_text('hit')


def main():
    token = os.environ['TG_TOKEN']

    bot = Updater(token, request_kwargs=PROXY)

    dispatcher = bot.dispatcher
    dispatcher.add_handler(CommandHandler("start", greet_user))
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
