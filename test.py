#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for the telegram-bot track.

Run with ``python3 -m nose``.
"""

import bot


def test_get_planet():
    """Test that all planet names have assigned ephem objects."""
    planet_names = bot.planets.keys()
    for name in planet_names:
        yield _check_get_planet, name


def _check_get_planet(name):
    assert bot.get_planet(name) is not None
