import Tkinter as tk

class Label:
    def __init__(self, master = None):
        self.label = tk.Label(master)

    def setBackground(color):
        self.label.config(bg = color)

    def setBorderWidth(bw):
        self.label.config(bd = bw)

    def setWidth(w):
        self.label.config(width = w)
        
    def setHeight(h):
        self.label.config(height = h)

    def setText(txt):
        self.label.config(text = txt)

    def padX(x):
        self.label.config(padx = x)
    
    def padY(y):
        self.label.config(padY = y)
