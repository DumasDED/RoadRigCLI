import database
import error


def band_to_band(band1, band2):
    print "Connecting %s and %s..." % (band1, band2)
    try:
        band1 = database.get_node('band', band1)
        band2 = database.get_node('band', band2)

        database.add_relationship(band1, 'knows', band2)
    except error.types as e:
        error.handle(e)
    else:
        print "Done."


def venue_to_city(venue, city):
    print "Connecting %s to %s..." % (venue, city)
    try:
        venue = database.get_node('venue', venue)
        city = database.get_node('city', city, 'name')

        database.add_relationship(venue, 'is_in', city)
    except error.types as e:
        error.handle(e)
    else:
        print "Done."


def city_to_state(city, state):
    print "Connecting %s to %s..." % (city, state)
    try:
        city = database.get_node('city', city, 'name')
        state = database.get_node('state', state, 'abbr')

        database.add_relationship(city, 'is_in', state)
    except error.types as e:
        error.handle(e)
    else:
        print "Done."
