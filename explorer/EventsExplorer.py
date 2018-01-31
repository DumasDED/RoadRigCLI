import sys

from asciimatics.exceptions import StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Widget, Frame, Layout, Button, ListBox, Divider, Label, Text, TextBox, DatePicker
from asciimatics.exceptions import NextScene, ResizeScreenError

from palette import palette


class EventMap:
    def __init__(self, event=None, venue=None, bands=[]):
        self.event = event
        self.venue = venue
        self.new_venue = False
        self.bands = bands
        # This isn't going to work if the event map is instantiated without any bands present.
        # Need to find a better solution.
        for b in self.bands:
            b['include'] = True


class EventModel:
    def __init__(self, events, band=None, venue=None):
        self._events = events
        self._band = band
        self._venue = venue

        self._selected_index = 0

    @property
    def selected_index(self):
        return self._selected_index

    @selected_index.setter
    def selected_index(self, value):
        self._selected_index = value

    @property
    def band(self):
        return self._band

    @property
    def venue(self):
        return self._venue

    @property
    def count(self):
        return len(self._events)

    @property
    def count_of_other_bands(self):
        return len(set([band for m in self._events for band in m.bands if band is not self._band]))

    @property
    def count_of_venues(self):
        return len(set([m.venue['name'] for m in self._events]))

    @property
    def count_of_new_venues(self):
        return len(set([m.venue['name'] for m in self._events if m.new_venue]))

    @property
    def event_list(self):
        return [('%s%s %s' % (
                    '!' if [b for b in event.bands if b is not self._band] else ' ',
                    '*' if event.new_venue else ' ',
                    event.event['name']
                ), i) for i, event in enumerate(self._events)]

    @property
    def current_event(self):
        x = self._events[self.selected_index]
        e = {}
        for k in ['name', 'start_time', 'description']:
            e[k] = x.event[k]
        e['place'] = x.event['place']['name']
        e['other_bands'] = [
                ((u'\u2714 ' if b['include'] is True else u'\u2717 ') + b['name'], i)
                for i, b in enumerate(x.bands)
                if b['id'] is not self.band['id']
            ]
        return e

    def flip_band(self, index):
        x = self._events[self.selected_index]
        x.bands[index]['include'] = not x.bands[index]['include']


class EventsExplorer:
    def __init__(self, event_model, band=None, venue=None):
        self._model = event_model
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
            Scene([EventList(screen, self._model)], -1, name="Event List"),
            Scene([EventDetails(screen, self._model)], -1, name="Event Details")
        ]

        screen.play(scenes, stop_on_resize=True, start_scene=scene)


class EventList(Frame):
    def __init__(self, screen, event_model):
        super(EventList, self).__init__(screen,
                                        screen.height // 2,
                                        screen.width // 2,
                                        has_border=False,
                                        reduce_cpu=True)

        self.palette = palette

        self._model = event_model

        self.event_listbox = ListBox(Widget.FILL_FRAME,
                                     self._model.event_list,
                                     name="events",
                                     on_change=self._on_pick,
                                     on_select=self._select)

        layout0 = Layout([100])
        self.add_layout(layout0)

        layout0.add_widget(Label("EVENT LIST"))
        layout0.add_widget(Divider(draw_line=False))

        layout1 = Layout([50, 50])
        self.add_layout(layout1)

        stipulation = '%s%s' % (
            (' at %s' % self._model.venue['venue']) if self._model.venue is not None else '',
            (' featuring %s' % self._model.band['name']) if self._model.band is not None else ''
        )

        layout1.add_widget(Label("%i events found%s." % (self._model.count, stipulation)))
        layout1.add_widget(Label(
            "%i other known bands featured (!)." % self._model.count_of_other_bands
        ))
        layout1.add_widget(Label(
            "%i distinct venues featured." % self._model.count_of_venues
        ))
        layout1.add_widget(Label(
            "%i venues not currently in the database (*)." % self._model.count_of_new_venues
        ))
        layout1.add_widget(Divider(draw_line=False))

        layout2 = Layout([100], fill_frame=True)
        self.add_layout(layout2)

        layout2.add_widget(self.event_listbox)
        layout2.add_widget(Divider(draw_line=False))

        layout3 = Layout([1, 1, 1, 1, 1])
        self.add_layout(layout3)

        layout3.add_widget(Button("OK", self._womp), 1)
        layout3.add_widget(Button("Exit", self._quit), 2)

        self.fix()

    def reset(self):
        super(EventList, self).reset()
        self.event_listbox.value = self._model.selected_index

    def _on_pick(self):
        self._model.selected_index = self.event_listbox.value

    def _womp(self):
        self.event_listbox.value = 5

    @staticmethod
    def _select():
        raise NextScene("Event Details")

    @staticmethod
    def _quit():
        raise StopApplication("User quit.")


class EventDetails(Frame):
    def __init__(self, screen, event_model):
        super(EventDetails, self).__init__(screen,
                                           screen.height // 2,
                                           screen.width // 2,
                                           on_load=self.reload_band_list,
                                           has_border=False,
                                           reduce_cpu=True)

        self.palette = palette

        self._model = event_model

        layout0 = Layout([100, 2, 50])
        self.add_layout(layout0)

        layout0.add_widget(Label("EVENT DETAILS"))
        layout0.add_widget(Divider(draw_line=False))

        layout0.add_widget(Label("OTHER KNOWN BANDS FEATURED"), 2)

        layout1 = Layout([100, 2, 50])
        self.add_layout(layout1)

        layout2 = Layout([100], fill_frame=True)
        self.add_layout(layout2)

        w_name = Text("Name:", "name")
        w_place = Text("Place:", "place")
        w_date = Text("Date:", "start_time")
        w_description = TextBox(Widget.FILL_FRAME, "Description:", "description", as_string=True)

        self.w_other_bands = ListBox(4, self._model.current_event['other_bands'], on_select=self.flip_band)

        w_name.disabled = True
        w_place.disabled = True
        w_date.disabled = True
        w_description.disabled = True

        layout1.add_widget(w_name)
        layout1.add_widget(w_place)
        layout1.add_widget(w_date)

        layout1.add_widget(self.w_other_bands, 2)

        layout2.add_widget(Divider(draw_line=False))
        layout2.add_widget(w_description)
        layout2.add_widget(Divider(draw_line=False))

        layout3 = Layout([100])
        self.add_layout(layout3)

        layout3.add_widget(Button("OK", self._exit))

        self.fix()

    def flip_band(self):
        i = self.w_other_bands.value
        self._model.flip_band(i)
        self.reload_band_list()
        self.w_other_bands.value = i

    def reload_band_list(self):
        self.w_other_bands.options = self._model.current_event['other_bands']

    def reset(self):
        super(EventDetails, self).reset()
        self.data = self._model.current_event

    @staticmethod
    def _exit():
        raise NextScene("Event List")
