from Tkinter import *
import Tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky = tk.N + tk.S + tk.E + tk.W)
        self.createWidgets()

    def createWidgets(self):
        #needs to be in its own window
        self.textentry = tk.Text(self, font = ('Courier New', 13))
        self.textentry.grid(row = 0, column = 2)

app = App()
app.master.title('CSPy Development Environment')
app.mainloop()
