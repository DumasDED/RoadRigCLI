import sys

from asciimatics.exceptions import StopApplication, ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Widget, Frame, Layout, Button, ListBox, Divider, Label

from pallette import pallette


def demo(screen, scene):
    frame = Frame(screen,
                  screen.height // 3,
                  screen.width // 3,
                  hover_focus=True,
                  has_border=False,
                  title="Main Menu")

    frame.palette = pallette

    layout3 = Layout([100])
    frame.add_layout(layout3)

    layout3.add_widget(Label("Test"), 0)
    layout3.add_widget(Divider(draw_line=False))

    layout1 = Layout([100], fill_frame=True)
    frame.add_layout(layout1)

    layout1.add_widget(ListBox(
        Widget.FILL_FRAME, [
            ("One", 1), ("Two", 3), ("Three", 2), ("Four", 4), ("Five", 5),
            ("Six", 6), ("Seven", 7), ("Eight", 8), ("Nine", 9), ("Ten", 10),
            ("Eleven", 11), ("Twelve", 12), ("Thirteen", 13), ("Fourteen", 14), ("Fifteen", 15),
            ("Sixteen", 16), ("Seventeen", 17), ("Eighteen", 18), ("Nineteen", 19), ("Twenty", 20),
            ("Loop", 1)
        ], name="List Thing"))
    layout1.add_widget(Divider(draw_line=False))

    layout2 = Layout([1, 1, 1, 1])
    frame.add_layout(layout2)

    layout2.add_widget(Button("OK", leave), 1)
    layout2.add_widget(Button("Cancel", leave), 2)

    frame.fix()

    scenes = [
        Scene([frame], -1, name="Test")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene)


class EventList(Frame):
    def __init__(self, screen, events):
        super(EventList, self).__init__(screen,
                                        screen.height // 3,
                                        screen.width // 3,
                                        has_border=False)

        self._events = events

        self.pallette = pallette

        layout1 = Layout([100])
        self.add_layout(layout1)

        layout1.add_widget(Label("Event List"))
        layout1.add_widget(Divider(draw_line=False))
        layout1.add_widget(Label("%i events found." % len(self._events)))

        layout2 = Layout([100], fill_frame=True)
        self.add_layout(layout1)

        layout2.add_widget(ListBox(
            Widget.FILL_FRAME, [(event.event['name'], i) for event, i in enumerate(self._events)]))
        layout2.add_widget(Divider(draw_line=False))

        layout3 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)

        layout3.add_widget(Button("OK", leave), 1)
        layout3.add_widget(Button("Cancel", leave), 2)


def leave():
    raise StopApplication("User quit.")


last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene

