import sys

from asciimatics.exceptions import StopApplication, ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Widget, Frame, Layout, Button, ListBox, Divider, Label


def demo(screen, scene):
    frame = Frame(screen,
                  screen.height // 3,
                  screen.width // 3,
                  hover_focus=True,
                  has_border=False,
                  title="Main Menu")

    frame.palette['background'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
    frame.palette['borders'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
    frame.palette['button'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
    frame.palette['focus_button'] = (Screen.COLOUR_WHITE, Screen.A_REVERSE, Screen.COLOUR_BLACK)
    frame.palette['control'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
    frame.palette['disabled'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
    frame.palette['field'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
    frame.palette['focus_field'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
    frame.palette['selected_field'] = (Screen.COLOUR_WHITE, Screen.A_REVERSE, Screen.COLOUR_BLACK)
    frame.palette['selected_focus_field'] = (Screen.COLOUR_WHITE, Screen.A_REVERSE, Screen.COLOUR_BLACK)
    frame.palette['edit_text'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
    frame.palette['focus_edit_text'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
    frame.palette['scroll'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
    frame.palette['title'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
    frame.palette['label'] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)

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

    layout2.add_widget(Button("OK", button), 1)
    layout2.add_widget(Button("Cancel", button), 2)

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

