import random
from cs110graphics import *


class Die:
    SIDES = 6
    POSITIONS = [None,
                 [(0, 0), None, None, None, None, None],
                 [(-.25, .25), (.25, -.25), None, None, None, None],
                 [(-.25, .25), (0, 0), (.25, -.25), None, None, None],
                 [(-.25, -.25), (-.25, .25), (.25, -.25),
                  (.25, .25), None, None],
                 [(-.25, -.25), (-.25, .25), (.25, -.25),
                  (.25, .25), (0, 0), None],
                 [(-.25, -.25), (-.25, .25), (.25, -.25),
                  (.25, .25), (-.25, 0), (.25, 0)]]

    def __init__(self, window, width=25, center=(200, 200), bgcolor='white',
                 fgcolor='black'):
        self._value = 1
        self._square = Rectangle(window, width, width, center)
        self._square.set_fill_color(bgcolor)
        self._square.set_depth(20)
        self._center = center
        self._width = width
        # self._text = Text("1", center, 18)
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(window, width / 15, center)
            pip.set_fill_color(fgcolor)
            pip.set_depth(20)
            self._pips.append(pip)

    def addTo(self, win):
        win.add(self._square)
        # win.add(self._text)
        for pip in self._pips:
            win.add(pip)

    def roll(self):
        """ change this die's current value to a random number between 1
            and the number of sides this die has"""
        self._value = random.randrange(Die.SIDES) + 1
        self._update()

    def getValue(self):
        """ return this die's current value """
        return self._value

    def _update(self):
        """ private method.  make the appearance of the die match
            the die's value"""
        # self._text.setTextString(str(self._value))
        positions = Die.POSITIONS[self._value]
        cx, cy = self._center
        for i in range(len(positions)):
            if positions[i] is None:
                self._pips[i].set_depth(25)
            else:
                self._pips[i].set_depth(15)
                dx, dy = positions[i]
                self._pips[i].move_to((cx + dx * self._width,
                                      cy + dy * self._width))


class Controller(EventHandler):
    def __init__(self, win):
        """ set up objects with events on a window """
        EventHandler.__init__(self)   # set up the EventHandler properly
        self._die = Die(win, bgcolor='red')
        self._die.addTo(win)
        self._button = Rectangle(win, 100, 50, (75, 75))
        self._button.set_fill_color('orange')
        win.add(self._button)
        self._button.add_handler(self)
        # register the controller as the handler
        # for button's events

    def handle_mouse_release(self, event):
        self._die.roll()


def main(win):
    _ = Controller(win)


StartGraphicsSystem(main)
