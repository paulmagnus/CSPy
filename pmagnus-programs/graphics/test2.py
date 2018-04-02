from Tkinter import *
from ttk import *

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        notebook = Notebook(self)
        frame1 = Frame(notebook)
        Text(frame1).pack()
        Label(frame1, text="1").pack()
        notebook.add(child=frame1, text='tab1')
        notebook.add(child=Frame(notebook), text='tab2')
        notebook.add(child=Frame(notebook), text='tab3')
        notebook.pack()

        print notebook.children
        print('Tabs are:', notebook.children.keys())
        print('Active tab:', notebook.select())
        print(notebook.children[notebook.select().split('.')[2]].children)
        print(notebook.select().split('.')[2])
App().mainloop()
