import Tkinter as tk


class Frame:
    def __init__(self, master = None):
        self.frame = tk.Frame(master)

    def setBackground(self, color):
        self.frame.config(bg = color)
    
    def setBorderWidth(self, bw):
        self.frame.config(borderwidth = bw)

    def setHeight(self, h):
        self.frame.config(height = h)
    
    def setWidth(self, w):
        self.frame.config(width = w)

    def highlightBackground(self, color):
        self.frame.config(hightlightcolor = color)

    def setPadx(self, x):
        self.frame.config(padx = x)
        

    def setPady(self, y):
        self.frame.config(pady = y)

    
    def pack(self):
        self.frame.pack()
