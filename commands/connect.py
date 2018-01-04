import database as db


def band_to_city(band, city):
    print city['name']
    if isinstance(city, type(str)):
        city = db.get_node('city', 'name', city)
    db.add_relationship(band, 'is_from', city)


def city_to_state(city, state):
    if isinstance(state, type(str)):
        if len(state) == 2:
            state = db.get_node('state', 'abbr', state)
        else:
            state = db.get_node('state', 'name', state)
    db.add_relationship(city, 'is_in', state)
