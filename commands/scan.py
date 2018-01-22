import config
import tools
import facebook as fb
import database as db

class EventMap():
    def __init__(self, event=None, venue=None, bands=[]):
        self.event = event
        self.venue = venue
        self.new_venue = False
        self.bands = bands


def events_by_band(username):

    if not db.check_node('band', 'username', username):
        raise Exception('%s not found in the database.' % username)
    else:
        by_band = db.get_node('band', 'username', username)

    bands = [band for band in db.get_all_nodes('band') if band is not by_band]
    venues = list(db.get_all_nodes('venue'))

    print "Scanning for events featuring %s..." % by_band['name']

    events = fb.get_attr(by_band['username'], 'events', fields=config.app_fields_events)

    event_map = [EventMap(event=event, bands=[by_band]) for event in events]

    for map in event_map:
        for band in bands:
            if band['name'] in map.event['name'] or band['name'] in map.event['description']:
                map.bands.append(band)

        for venue in venues:
            if 'place' in map.event and 'id' in map.event['place'] and venue['id'] == map.event['place']['id']:
                map.venue = venue
                break

        if not map.venue:
            if 'place' in map.event:
                map.venue = map.event['place']
                map.new_venue = True

    event_map = [e for e in event_map if e.venue]

    print len(events), "events found featuring %s." % by_band['name']
    print len(set([band for map in event_map for band in map.bands])), "additional bands featured."
    print len(set([map.venue['name'] for map in event_map])), "distinct venues featured."
    print len(set([map.venue['name'] for map in event_map if map.new_venue])), "venues not currently in the database."

    while True:
        print ""

        print "Choose an option:"
        print "1 - Show event map."
        print "2 - Import all events at venues currently in the database; omit venues not currently in the database."
        print "3 - Add all new venues and add all events to database."
        print "   (press any other key to abort)"

        x = tools.getch()

        if x == "1":
            print ""
            print "Event Map:"

            for i, map in enumerate(event_map):
                print "%i\t || Event:   %s" % (i + 1, map.event['name'])
                print '\t || Venue: %s %s' % (
                        '*' if map.new_venue else ' ',
                        map.venue['name'],
                    )
                if map.bands:
                    print '\t || Bands:   %s' % ', '.join([band['name'] for band in map.bands])
                print ""
        else:
            break
