import database as db


def band_to_city(band, city):
    """
    Create an 'is_from' relationship between a band and city.

    :param band: the username of the band.
    :param city: the name of the city.
    """
    band = db.get_node('band', 'username', band)
    city = db.get_node('city', 'name', city)
    if not db.check_relationship(band, 'is_from'):
        print 'Connecting %s to %s...' % (band['name'], city['name'])
        db.add_relationship(band, 'is_from', city)


def venue_to_city(venue, city):
    """
    Create an 'is_in' relationship between a venue and a city.

    :param venue: the username/handle of the venue.
    :param city:  the name of the city.
    """
    venue = db.get_node('venue', 'username', venue)
    city = db.get_node('city', 'name', city)
    if not db.check_relationship(venue, 'is_in'):
        print 'Connecting %s to %s...' % (venue['name'], city['name'])
        db.add_relationship(venue, 'is_in', city)


def city_to_state(city, state):
    """
    Create an 'is_in' relationship between a city and a state.

    :param city: the name of the city.
    :param state:  the name or abbreviation of the state.
    """
    city = db.get_node('city', 'name', city)
    if len(state) == 2:
        state = db.get_node('state', 'abbr', state)
    else:
        state = db.get_node('state', 'name', state)
    if not db.check_relationship(city, 'is_in'):
        print 'Connecting %s to %s...' % (city['name'], state['name'])
        db.add_relationship(city, 'is_in', state)