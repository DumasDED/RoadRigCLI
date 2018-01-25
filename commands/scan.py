import config
import sys, tools
import facebook as fb
import database as db

from asciimatics.exceptions import StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Widget, Frame, Layout, Button, ListBox, Divider, Label
from asciimatics.exceptions import ResizeScreenError

import palette


class EventMap:
    def __init__(self, event=None, venue=None, bands=[]):
        self.event = event
        self.venue = venue
        self.new_venue = False
        self.bands = bands


class EventsByBand:
    def __init__(self, band_handle=None):
        self._band_handle = band_handle

        if not db.check_node('band', 'username', self._band_handle):
            raise Exception('%s not found in the database.' % self._band_handle)
        else:
            by_band = db.get_node('band', 'username', self._band_handle)

        bands = [band for band in db.get_all_nodes('band') if band is not by_band]
        venues = list(db.get_all_nodes('venue'))

        print "Scanning for events featuring %s..." % by_band['name']

        events = fb.get_attr(by_band['username'], 'events', fields=config.app_fields_events)

        self.event_map = [EventMap(event=event, bands=[by_band]) for event in events]

        for map in self.event_map:
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

        self.event_map = [e for e in self.event_map if e.venue]

        last_scene = None
        while True:
            try:
                Screen.wrapper(self.demo, catch_interrupt=True, arguments=[last_scene])
                sys.exit(0)
            except ResizeScreenError as e:
                last_scene = e.scene

    def demo(self, screen, scene):
        scenes = [
            Scene([EventList(screen, self.event_map, band_handle=self._band_handle)], -1, name="Event List")
        ]

        screen.play(scenes, stop_on_resize=True, start_scene=scene)


class EventList(Frame):
    def __init__(self, screen, events, band_handle=None, venue_handle=None):
        super(EventList, self).__init__(screen,
                                        screen.height // 2,
                                        screen.width // 2,
                                        has_border=False)

        self.palette = palette.palette

        self._events = events
        self._band_handle = band_handle
        self._venue_handle = venue_handle

        layout1 = Layout([100])
        self.add_layout(layout1)

        layout1.add_widget(Label("EVENT LIST"))
        layout1.add_widget(Divider(draw_line=False))
        layout1.add_widget(Label("%i events found%s%s." % (
            len(self._events),
            (' at %s' % self._venue_handle) if self._venue_handle is not None else '',
            (' featuring %s' % self._band_handle) if self._band_handle is not None else ''
        )))
        layout1.add_widget(Label(
            "%i additional bands featured." %
            len(set([band for map in self._events for band in map.bands]))
        ))
        layout1.add_widget(Label(
            "%i distinct venues featured." %
            len(set([map.venue['name'] for map in self._events]))
        ))
        layout1.add_widget(Label(
            "%i venues not currently in the database." %
            len(set([map.venue['name'] for map in self._events if map.new_venue]))
        ))
        layout1.add_widget(Divider(draw_line=False))

        layout2 = Layout([100], fill_frame=True)
        self.add_layout(layout2)

        layout2.add_widget(ListBox(
            Widget.FILL_FRAME, [
                ('%s %s' % ('*' if event.new_venue else ' ', event.event['name']), i)
                for i, event in enumerate(self._events)
                ]))
        layout2.add_widget(Divider(draw_line=False))

        layout3 = Layout([1, 1, 1, 1])
        self.add_layout(layout3)

        layout3.add_widget(Button("OK", self._quit), 1)
        layout3.add_widget(Button("Cancel", self._quit), 2)

        self.fix()

    @staticmethod
    def _quit():
        raise StopApplication("User quit.")


