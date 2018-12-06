#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Code for the telegram-bot track."""

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
    """Run the bot."""
    token = os.environ['TG_TOKEN']
    proxy = {'proxy_url': os.environ['PROXY_URL'],
             'urllib3_proxy_kwargs': {
                 'username': os.environ['PROXY_USER'],
                 'password': os.environ['PROXY_PASS'],
             },
             }

    bot = Updater(token, request_kwargs=proxy)

    dispatcher = bot.dispatcher
    dispatcher.add_handler(CommandHandler('ping', greet_user))
    dispatcher.add_handler(CommandHandler('planet', planet_command))
    dispatcher.add_handler(MessageHandler(Filters.text, talk_to_me))

    bot.start_polling()
    bot.idle()


def greet_user(bot: Bot, update: Update):
    """React to /ping with 'pong'."""
    logging.info('command: /ping')
    update.message.reply_text('pong')


def talk_to_me(bot: Bot, update: Update):
    """Repeat user input."""
    user_text = update.message.text
    logging.info('message: {user_text}', extra={'user_text': user_text})
    update.message.reply_text(user_text)


def planet_command(bot: Bot, update: Update):
    """Tell the constellation, that a planet is in at the moment."""
    logging.info('command: {text}', extra={'text': update.message.text})
    answer = process_planet_command(update.message.text)
    update.message.reply_text(answer)


def process_planet_command(text):
    """Logic for planet_command."""
    args = text.split()
    if len(args) < 2:
        answer = "Add a planet's name, like this: /planet Mars"
    else:
        planet_name = args[1]
        planet = get_planet(planet_name)
        if planet:
            # this returns a tuple like ('Aqr', 'Aquarius')
            _, constell = ephem.constellation(planet)
            answer = '{0} is now in {1}.'.format(planet_name, constell)
        else:
            answer = "'{0}' is not a planet.".format(planet_name)
    return answer


planets = {
    'mercury': ephem.Mercury,
    'venus': ephem.Venus,
    'mars': ephem.Mars,
    'jupiter': ephem.Jupiter,
    'saturn': ephem.Saturn,
    'uranus': ephem.Uranus,
    'neptune': ephem.Neptune,
    'pluto': ephem.Pluto,
}


def get_planet(planet_name, time=None):
    """Get the planets's ephem.Planet object by its name."""
    name_lower = planet_name.lower()
    time = datetime.datetime.now() if time is None else time

    if name_lower in planets:
        return planets[name_lower](time)
    else:
        return None
