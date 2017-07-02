import config
import facebook
import database
import error


def band(*args):
    print "Adding band '%s'..." % args[0]
    try:
        r = facebook.get(args[0], **{'fields': config.app_fields_band})
        database.add_node('band', **r)
    except error.types as e:
        error.handle(e, args[0])
    else:
        print "%s successfully added to database." % r['name']


def venue(*args):
    print "Adding venue '%s'..." % args[0]
    try:
        r = facebook.get(args[0], **{'fields': config.app_fields_venue})
        database.add_node('venue', **r)
    except error.types as e:
        error.handle(e, args[0])
    else:
        print "%s successfully added to database." % r['name']
