#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os

import ephem
from telegram.bot import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.update import Update

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
    dispatcher.add_handler(CommandHandler("planet", planet_command))
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


def planet_command(bot: Bot, update: Update):
    logging.info('command: ' + update.message.text)

    answer = process_planet_command(update.message.text)

    update.message.reply_text(answer)


def process_planet_command(text):
    args = text.split()
    if len(args) < 2:
        answer = "Add a planet's name, like this: /planet Mars"
    else:
        planet_name = args[1]
        planet = get_planet(planet_name)
        if planet:
            constell = get_constellation_name(planet)
            answer = "{} is now in {}.".format(planet_name, constell)
        else:
            answer = "'{}' is not a planet.".format(planet_name)
    return answer


planets = {
    'mercury': ephem.Mercury,
    'venus': ephem.Venus,
    'mars': ephem.Mars,
    'jupiter': ephem.Jupiter,
    'saturn': ephem.Saturn,
    'uranus': ephem.Uranus,
    'neptune': ephem.Neptune,
    'pluto': ephem.Pluto
}


def get_planet(planet_name, time=datetime.datetime.now()):
    name_lower = planet_name.lower()

    if name_lower in planets:
        return planets[name_lower](time)
    else:
        return None


def get_constellation_name(planet):
    # tuple like ('Aqr', 'Aquarius')
    constell = ephem.constellation(planet)

    return constell[1]


if __name__ == '__main__':
    main()
