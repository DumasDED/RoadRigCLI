import config
import commands

import facebook as fb
import database as db

from explorer import EventsExplorer, EventModel, EventMap


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
    event_maps = [EventMap(event=event, bands=[by_band]) for event in events]

    # For each event in the event map...
    for map in event_maps:

        # Search for known bands and append them where found:
        for band in bands:
            if band['name'] in map.event['name']\
                    or (
                        band['name'] in map.event['description']
                        if 'description' in map.event
                        else False):
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
    event_maps = [e for e in event_maps if e.venue and 'id' in e.venue.keys()]

    # Rule out events that are already in the database:
    database_event_ids = [e['id'] for e in db.get_all_nodes('event')]
    event_maps = [e for e in event_maps if e.event['id'] not in database_event_ids]

    # Create Event Model
    event_model = EventModel(event_maps, band=by_band)

    # Open the events explorer:
    try:
        EventsExplorer(event_model, band=by_band)
    except:
        pass

    # Show the results of the explorer:
    print "Results:"
    print "%i events found." % event_model.count
    print "%i events excluded." % (event_model.count - event_model.count_included)
    print "%i events to be imported." % event_model.count_included
    print ""

    # If specified, commit all events and their respective relationships:
    if event_model.commit_all is True:
        print "Adding %i events to the database:" % event_model.count_included
        for map in [e for e in event_model.events if e.commit is True]:
            # Add new venues where applicable:
            if map.new_venue is True:
                print "Venue not found in database."
                map.venue, l = commands.add.venue(id=map.venue['id'])
                c = commands.add.city(l['city'])
                commands.connect.venue_to_city(map.venue, c)
                commands.connect.city_to_state(c['name'], l['state'])
            e = commands.add.event(map.event)
            commands.connect.event_to_venue(e, map.venue)
            for b in map.bands:
                # print b['name'], b['include']
                if map.bands.is_included(b):
                    commands.connect.event_to_band(e, b)
                    # b['include'] = True
                # print b['name'], b['include']
    else:
        print "Cancelling..."


