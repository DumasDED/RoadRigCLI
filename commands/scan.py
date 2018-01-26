import config
import facebook as fb
import database as db

from explorer import EventsExplorer, EventMap


def events_by_band(band_handle):

    # Check the database for the specified band (if applicable):
    if not db.check_node('band', 'username', band_handle):
        raise Exception('%s not found in the database. Import it first.' % band_handle)
    else:
        by_band = db.get_node('band', 'username', band_handle)

    # Get a list of all bands, excluding the one provided:
    bands = [band for band in db.get_all_nodes('band') if band is not by_band]

    # Get a list of all venues:
    venues = list(db.get_all_nodes('venue'))

    print "Scanning for events featuring %s..." % by_band['name']

    # Retrieve all events from the facebook graph for the given band:
    events = fb.get_attr(by_band['username'], 'events', fields=config.app_fields_events)

    # Create an event map
    event_map = [EventMap(event=event, bands=[by_band]) for event in events]

    # For each event in the event map...
    for map in event_map:

        # Search for known bands and append them where found:
        for band in bands:
            if band['name'] in map.event['name'] or band['name'] in map.event['description']:
                map.bands.append(band)

        # Search for known venues and add them where found:
        for venue in venues:
            if 'place' in map.event and 'id' in map.event['place'] and venue['id'] == map.event['place']['id']:
                map.venue = venue
                break

        # For unknown venues, mark them as new and add:
        if not map.venue:
            if 'place' in map.event:
                map.venue = map.event['place']
                map.new_venue = True

    # Rule out events without a venue:
    event_map = [e for e in event_map if e.venue]

    # Open the events explorer:
    EventsExplorer(event_map, band=by_band)


