from Tkinter import *
import Tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky = tk.N + tk.S + tk.E + tk.W)
        self.createWidgets()
    def createWidgets(self):
        #needs to be in its own window
        directory = tk.Canvas(self)
        directory.grid(row = 0, column = 0)

        #needs to be in its own window
        textentry = tk.Text(self)
        textentry.grid(row = 0, column = 2)

        #needs to be in its own window
        test = tk.Canvas(self)
        test.grid(row = 0, column = 4)

        #needs to be in its own window
        test = tk.Button(self, text = "Test")
        submit = tk.Button(self, text = "Submit")
        test.grid(row = 1, column = 0, sticky = tk.N + tk.S + tk.E + tk.W)
        submit.grid(row = 1, column = 1, sticky = tk.N + tk.S + tk.E + tk.W)

app = App()
app.master.title('CDE: CSPy Development Environment')
app.mainloop()
