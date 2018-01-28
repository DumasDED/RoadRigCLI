import sys

from asciimatics.exceptions import StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Widget, Frame, Layout, Button, ListBox, Divider, Label
from asciimatics.exceptions import NextScene, ResizeScreenError

from palette import palette


# TODO: build db/graph retrieval directly into the class?
class EventMap:
    def __init__(self, event=None, venue=None, bands=[]):
        self.event = event
        self.venue = venue
        self.new_venue = False
        self.bands = bands


class EventGraph(list):
    def __init__(self, events):
        for e in events:
            assert e is EventMap
        super(EventGraph, self).__init__(events)
        self.selected_event = None


class EventsExplorer:
    def __init__(self, event_graph, band=None, venue=None):
        self.event_graph = event_graph
        self.band = band
        self.venue = venue

        last_scene = None
        while True:
            try:
                Screen.wrapper(self.explorer, catch_interrupt=True, arguments=[last_scene])
                sys.exit(0)
            except ResizeScreenError as e:
                last_scene = e.scene

    def explorer(self, screen, scene):
        scenes = [
            Scene([EventList(screen, self.event_graph, self.band, self.venue)], -1, name="Event List")
        ]

        screen.play(scenes, stop_on_resize=True, start_scene=scene)


class EventList(Frame):
    def __init__(self, screen, events, band=None, venue=None):
        super(EventList, self).__init__(screen,
                                        screen.height // 2,
                                        screen.width // 2,
                                        has_border=False,
                                        reduce_cpu=True)

        self.palette = palette

        self.event_graph = events
        self.band = band
        self.venue = venue

        self.event_listbox = ListBox(
            Widget.FILL_FRAME, [
                ('%s%s %s' % (
                    '!' if [b for b in event.bands if b is not self.band] else ' ',
                    '*' if event.new_venue else ' ',
                    event.event['name']
                ), i)
                for i, event in enumerate(self.event_graph)
                ])

        self.selected = 0

        layout0 = Layout([100])
        self.add_layout(layout0)

        layout0.add_widget(Label("EVENT LIST"))
        layout0.add_widget(Divider(draw_line=False))

        layout1 = Layout([50, 50])
        self.add_layout(layout1)

        stipulation = '%s%s' % (
            (' at %s' % self.venue['venue']) if self.venue is not None else '',
            (' featuring %s' % self.band['name']) if self.band is not None else ''
        )

        layout1.add_widget(Label("%i events found%s." % (len(self.event_graph), stipulation)))
        layout1.add_widget(Label(
            "%i other known bands featured (!)." %
            len(set([band for map in self.event_graph for band in map.bands if band is not self.band]))
        ))
        layout1.add_widget(Label(
            "%i distinct venues featured." %
            len(set([map.venue['name'] for map in self.event_graph]))
        ))
        layout1.add_widget(Label(
            "%i venues not currently in the database (*)." %
            len(set([map.venue['name'] for map in self.event_graph if map.new_venue]))
        ))
        layout1.add_widget(Divider(draw_line=False))

        # listbox value isn't working, not sure why....
        # layout1.add_widget(Label("%i of %i events" % (self.selected or 0, len(self.event_map))), 1)

        layout2 = Layout([100], fill_frame=True)
        self.add_layout(layout2)

        layout2.add_widget(self.event_listbox)
        layout2.add_widget(Divider(draw_line=False))

        layout3 = Layout([1, 1, 1, 1])
        self.add_layout(layout3)

        layout3.add_widget(Button("OK", self._quit), 1)
        layout3.add_widget(Button("Cancel", self._quit), 2)

        self.fix()

    def _on_pick(self):
        self.event_graph.selected_event = self.event_listbox.value

    def _select(self):
        raise NextScene("Event Details")

    @staticmethod
    def _quit():
        raise StopApplication("User quit.")