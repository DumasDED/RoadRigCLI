import config
import connect
import parse
import facebook
import database
import error


def band(*args):
    print "Adding band '%s'..." % args[0]
    try:
        r = facebook.get(args[0], **{'fields': config.app_fields_band})
        r, c, s = parse.location(r)
        if c is None and len(args) >= 2:
            c == args[1]
        if s is None and len(args) >= 3:
            s == args[2]
        database.add_node('band', **r)
        if c is not None and s is not None:
            if not database.check_node('city', 'name', c):
                city(c)
                connect.city_to_state(c, s)
            connect.band_to_city(r['username'], c)
    except error.types as e:
        error.handle(e, args[0])
    else:
        print "%s successfully added to database." % r['name']


def venue(*args):
    print "Adding venue '%s'..." % args[0]
    try:
        r = facebook.get(args[0], **{'fields': config.app_fields_venue})
        r, c, s = parse.location(r)
        database.add_node('venue', **r)
        if c is not None and s is not None:
            if not database.check_node('city', 'name', c):
                city(c)
                connect.city_to_state(c, s)
            connect.venue_to_city(r['username'], c)
    except error.types as e:
        error.handle(e, args[0])
    else:
        print "%s successfully added to database." % r['name']


def city(name):
    print "Adding city '%s'..." % name
    try:
        database.add_node('city', name=name)
    except error.types as e:
        error.handle(e, name)
    else:
        print "%s successfully added to database." % name


