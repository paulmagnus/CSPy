from Tkinter import *
from ttk import *
from cspy_line_numbers import *
from cspy_statusbar import *
from cspy_texteditor import *


class CustomFrame(Frame):

    def __init__(self, root, notebook):
        Frame.__init__(self, notebook)
        self.root = root
        self.notebook = notebook
        self.statusbar = StatusBar(self, self.notebook)
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)
        self.text = Text_editor(self.root, self,
                                self.notebook,
                                self.statusbar)
        self.linenumbers = TextLineNumbers(self, width=40)
        self.linenumbers.attach(self.text)
        self.linenumbers.pack(side=LEFT, fill=Y)
        self.text.pack(side=RIGHT, fill=BOTH, expand=True)
        self.scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)

    def get_text_widget(self):
        return self.text
