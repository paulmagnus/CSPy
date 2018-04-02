from Tkinter import *
from ttk import *
from cspy_texteditor import *
from cspy_statusbar import *
from cspy_notebook import *
from cspy_menu import *


class App:

    def __init__(self):
        self.root = Tk()
        self.root.geometry("685x450")           # Width corresponds to 97 chars
        self.root.title("CSPy Text Editor")
        self.root.minsize(width=1, height=450)
        self.root.maxsize(width=685, height=2000)
        
        self.notebook = CustomNotebook()
        self.frame = CustomFrame(self.root, self.notebook)
        self.frame.linenumbers.redraw()
        self.notebook.add(child=self.frame,
                          text="Untitled")
        self.notebook.pack()
        self.menubar = Menubar(self.root, self.notebook)
        self.root.config(menu=self.menubar)
        self.root.mainloop()
        
    def get_root(self):
        return self.root
 