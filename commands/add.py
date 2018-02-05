import config
import facebook as fb
import database as db


def band(username):
    """
    Add a band to the Neo4J database.

    :param username: the username for the band being added to the database
    :return b: the band node returned from the database
    :return l: the band's location object from the facebook node, if it exists
    """
    username = username.lower()

    print "Adding band '%s'..." % username

    r = fb.get(username, fields=config.app_fields_band)
    l = r.pop('location', None)

    dr = db.get_node('band', 'username', username)

    if dr is None:
        r['username'] = r['username'].lower()
        db.add_node('band', **r)
        print "%s successfully added to database." % r['name']
    else:
        print "%s already exists in the database." % r['name']

    dr = db.get_node('band', 'username', username)

    return dr, l


def venue(username=None, id=None):
    """
    Add a venue to the Neo4J database.

    :param username: the username/handle for the venue being added to the database
    :param id: the id for the venue being added to the database
    :return v: the venue node returned from the database
    :return l: the venue's location object from the facebook node
    """
    if username is not None:
        username = username.lower()
        search_value = username
        search_by = 'username'
    else:
        search_value = id
        search_by = 'id'

    print "Adding venue with %s '%s'..." % (search_by, search_value)

    r = fb.get(search_value, fields=config.app_fields_venue)
    l = r.pop('location', None)

    dr = db.get_node('venue', search_by, search_value)

    if dr is None:
        if 'username' in r.keys():
            r['username'] = r['username'].lower()
        db.add_node('venue', **r)
        print "%s successfully added to database." % r['name']
    else:
        print "%s already exists in the database." % r['name']

    dr = db.get_node('venue', search_by, search_value)

    return dr, l


def event(event):
    """
    Add an event to the Neo4J database.

    :param event: the id of the event being added to the database
    :return: the event node returned from the database
    """
    print "Adding event '%s' to database..." % event['name']

    e = fb.get(event['id'], fields=config.app_fields_events)

    # Strip place property:
    if 'place' in e.keys():
        del e['place']

    dr = db.get_node('event', 'id', e['id'])

    if dr is None:
        db.add_node('event', **e)
        print "Event '%s' successfully added to database." % e['name']
    else:
        print "Event '%s' already exists in the database." % e['name']

    dr = db.get_node('event', 'id', e['id'])

    return dr


def city(name):
    """
    Add a city to the Neo4J database.

    :param name: the name of the city being added
    :return c: the city node returned from the database
    """
    c = db.get_node('city', 'name', name)

    if c is None:
        print "Adding city '%s'..." % name
        db.add_node('city', name=name)
        c = db.get_node('city', 'name', name)

    return c
