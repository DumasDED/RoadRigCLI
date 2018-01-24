import config
import sys, tools
import facebook as fb
import database as db

from asciimatics.exceptions import StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Widget, Frame, Layout, Button, ListBox, Divider, Label
from asciimatics.exceptions import ResizeScreenError

import pallette

event_map = []


class EventMap:
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

    print len(event_map), "events found."

    last_scene = None
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene

    """
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
    """


def demo(screen, scene):
    scenes = [
        Scene([EventList(screen, event_map)], -1, name="Event List")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene)


class EventList(Frame):
    def __init__(self, screen, events):
        super(EventList, self).__init__(screen,
                                        screen.height // 3,
                                        screen.width // 3,
                                        has_border=False)

        self._events = events

        self.pallette = pallette.pallette

        layout1 = Layout([100])
        self.add_layout(layout1)

        layout1.add_widget(Label("Event List"))
        layout1.add_widget(Divider(draw_line=False))
        layout1.add_widget(Label("%i events found." % len(self._events)))

        layout2 = Layout([100], fill_frame=True)
        self.add_layout(layout2)

        layout2.add_widget(ListBox(
            Widget.FILL_FRAME, [(event.event['name'], i) for event, i in enumerate(self._events)]))
        layout2.add_widget(Divider(draw_line=False))

        layout3 = Layout([1, 1, 1, 1])
        self.add_layout(layout3)

        layout3.add_widget(Button("OK", self._quit), 1)
        layout3.add_widget(Button("Cancel", self._quit), 2)

        self.fix()

    @staticmethod
    def _quit():
        raise StopApplication("User quit.")


