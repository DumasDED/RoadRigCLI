import unicodedata

import database as db


# TODO: modify all of these to take value dicts instead of strings
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

    :param venue: the venue dictionary.
    :param city:  the city dictionary.
    """
    if 'username' in venue.keys():
        venue = db.get_node('venue', 'username', venue['username'])
    else:
        venue = db.get_node('venue', 'id', venue['id'])
    city = db.get_node('city', 'name', city['name'])
    if not db.check_relationship(venue, 'is_in'):
        print 'Connecting %s to %s...' % (unicodedata.normalize('NFKD', venue['name']), city['name'])
        db.add_relationship(venue, 'is_in', city)


def event_to_venue(event, venue):
    """
    Create an 'at' relationship between an event and a venue.

    :param event: the event dictionary.
    :param venue: the venue dictionary.
    """
    e = db.get_node('event', 'id', event['id'])
    v = db.get_node('venue', 'id', venue['id'])
    if not db.check_relationship(e, 'at'):
        print "Connecting event to %s..." % unicodedata.normalize('NFKD', v['name'])
        db.add_relationship(e, 'at', v)


def event_to_band(event, band):
    """
    create a 'featuring' relationship between an event and a band.

    :param event: the event dictionary.
    :param band: the band dictionary.
    """
    e = db.get_node('event', 'id', event['id'])
    b = db.get_node('band', 'username', band['username'])
    if not db.check_relationship(e, 'featuring', b):
        print "Connecting event to %s..." % unicodedata.normalize('NFKD', b['name'])
        db.add_relationship(e, 'featuring', b)


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
