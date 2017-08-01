import config
import connect
import parse
import facebook
import database as db
import error


def band(*args):
    print "Adding band '%s'..." % args[0]
    try:
        r = facebook.get(args[0], **{'fields': config.app_fields_band})
        if len(args) == 3:
            r = parse.location(r)[0]
            c, s = args[1:3]
        else:
            r, c, s = parse.location(r)

        db.add_node('band', **r)
        if c is not None and s is not None:
            if not db.check_node('city', 'name', c):
                city(c)
            if not db.check_relationship(db.get_node('city', c, 'name'), 'is_in', db.get_node('state', s, 'abbr')):
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
        db.add_node('venue', **r)
        if c is not None and s is not None:
            if not db.check_node('city', 'name', c):
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
        db.add_node('city', name=name)
    except error.types as e:
        error.handle(e, name)
    else:
        print "%s successfully added to database." % name


