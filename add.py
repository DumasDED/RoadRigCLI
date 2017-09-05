import config
import connect
import parse
import facebook
import database as db
import error
import PushPin


def band(*args):
    print "Adding band '%s'..." % args[0]
    try:
        r = facebook.get(args[0], fields=config.app_fields_band)
        l, c, s = r.pop('location', None), None, None

        if l is not None:
            c = dict(name=l['city'])
            s = dict(abbr=l['state'])
        elif 'hometown' in r:
            c, s = PushPin.locate(r['hometown'])

        while c is None or s is None:
            l = raw_input('Location for %s could not be determined. Please provide: ' % r['name'])
            c, s = PushPin.locate(l)
            if c is None or s is None: print "Invalid location"

        db.add_node('band', **r)
        if c is not None and s is not None:
            if not db.check_node('city', 'name', c['name']):
                city(c)
            if not db.check_relationship(db.get_node('city', 'name', c['name']), 'is_in', db.get_node('state', 'abbr', s['abbr'])):
                connect.city_to_state(c['name'], s['abbr'])
            connect.band_to_city(r['username'], c['name'])
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


def city(c):
    print "Adding city '%s'..." % c['name']
    try:
        db.add_node('city', **c)
    except error.types as e:
        error.handle(e, c['name'])
    else:
        print "%s successfully added to database." % c['name']


