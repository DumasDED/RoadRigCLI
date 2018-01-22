from time import sleep

from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Button


def demo(screen):
    screen.print_at('Hello, world!', 0, 0)
    screen.refresh()

    i = 1

    while True:
        x = screen.get_event()
        if x is not None:
            if x.key_code == screen.KEY_UP:
                screen.print_at("UP", 0, i)
                i += 1
            elif x.key_code == screen.KEY_LEFT:
                screen.print_at("LEFT", 0, i)
                i += 1
            elif x.key_code == screen.KEY_DOWN:
                screen.print_at("DOWN", 0, i)
                i += 1
            elif x.key_code == screen.KEY_RIGHT:
                screen.print_at("RIGHT", 0, i)
                i += 1
        screen.refresh()


Screen.wrapper(demo)
