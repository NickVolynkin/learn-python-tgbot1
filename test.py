import bot


def test_get_planet():
    planet_names = bot.planets.keys()
    for name in planet_names:
        yield check_get_planet, name


def check_get_planet(name):
    # print(name)
    print(bot.get_planet(name))
    assert bot.get_planet(name) is not None
