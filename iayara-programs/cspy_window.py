from Tkinter import *
from ttk import *
from cspy_texteditor import *
from cspy_searchbox import *
from cspy_statusbar import *
from cspy_notebook import *
from cspy_menu import *
from cspy_window import *


class App:
    def __init__(self, title, h, w):
        self.root = Tk()
        self.root.geometry("655x450")
        self.root.title(title)
        self.width = w
        self.height = h
        self.root.minsize(width=1, height=self.height)
        self.root.maxsize(width=self.width, height=self.height*5)
        
        self.notebook = CustomNotebook()
        self.frame = Frame(self.notebook)
        self.statusbar = StatusBar(self.frame, self.notebook)
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)
        self.text = Text_editor(self.root, self.frame, 
                                self.notebook, self.statusbar)
        self.scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.notebook.add(child=self.frame, 
                          text= "Untitled   ")
        self.notebook.pack()
        self.menubar = Menubar(self.root, self.notebook)
        self.root.config(menu = self.menubar)
        self.root.mainloop()

    def get_root(self):
        return self.root

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width
    
    
