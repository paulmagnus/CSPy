from cs110graphics import *

pressed = False

class Button(EventHandler):
    def __init__(self, win):
        EventHandler.__init__(self)
        self.pressed = False
        self.circ = Circle(win)
        self.circ.add_handler(self)
        win.add(self.circ)

        self.timer = Timer(win, 200, self.variable)

    def variable(self):
        if self.pressed:
            self.circ.set_radius(100)
            self.pressed = False
        else:
            self.circ.set_radius(40)
            self.pressed = True

    def handle_mouse_press(self, event):
        self.timer.start()

    def handle_mouse_release(self, event):
        self.timer.stop()

def fun(win):
    button = Button(win)

StartGraphicsSystem(fun)