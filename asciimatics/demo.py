import sys

from time import sleep

from asciimatics.effects import Cycle, Stars
from asciimatics.exceptions import StopApplication, ResizeScreenError
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Button


def demo(screen, scene):
    frame = Frame(screen, screen.height * 2 // 3, screen.width * 2 // 3, has_border=False)

    layout = Layout([1, 1, 1, 1], fill_frame=True)
    frame.add_layout(layout)

    layout.add_widget(Button("OK", button), 1)
    layout.add_widget(Button("Cancel", button), 2)

    frame.fix()

    scenes = [
        Scene([frame], -1, name="Test")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene)


def button():
    raise StopApplication("User quit.")


last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene

