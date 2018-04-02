from Tkinter import *
from ttk import *


class TextLineNumbers(Canvas):

    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.config(background="#002b36",
                    bd=0,
                    highlightthickness=0,
                    relief='ridge')

        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(30, y,
                             anchor="ne",
                             text=linenum,
                             font=("Monospace", 13),
                             fill="#A9A9A9")
            i = self.textwidget.index("%s+1line" % i)
