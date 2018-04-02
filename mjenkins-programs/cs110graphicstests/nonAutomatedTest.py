from cs110graphics import *
import random


def colorGen():
    def r():
        return random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())


class Button(EventHandler):
    def __init__(self, Window):
        EventHandler.__init__(self)
        self._repr = Square(Window)
        Window.add(self._repr)
        self._repr.add_handler(self)

    def highlight(self):
        self._repr.set_border_color(colorGen())
        self._repr.set_fill_color(colorGen())

    def handle_mouse_release(self):
        self.highlight()

def main(Window):
    button = Button(Window)


StartGraphicsSystem(main)
