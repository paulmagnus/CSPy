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

class Label:
    def __init__(self, master = None):
        self.label = tk.Label(master)

    def setBackground(self, color):
        self.label.config(bg = color)

    def setBorderWidth(self, bw):
        self.label.config(bd = bw)

    def setWidth(self, w):
        self.label.config(width = w)
        
    def setHeight(self, h):
        self.label.config(height = h)

    def setText(self, txt):
        self.label.config(text = txt)

    def padX(self, x):
        self.label.config(padx = x)
    
    def padY(self, y):
        self.label.config(padY = y)

    def pack(self):
        self.label.pack()


class Text:
    def __init__(self, master = None):
        self.text = tk.Text(master)

    def setBackground(self, color):
        self.text.config(bg = color)

    def borderWidth(self, bw):
        self.text.config(bd = bw)

    def setHeight(self, h):
        self.text.config(height = h)

    def setWidth(self, w):
        self.text.config(width = w)        
    
    def padX(self, x):
        self.text.config(padx = x)

    def padY(self, y):
        self.text.config(pady = y)
        
    def pack(self):
        self.text.pack()

class Button:
    def __init__(self, master = None):
        self.button = tk.Button(master)

    def setBackground(self, color):
        self.button.config(bg = color)

    def setBorderWidth(self, bw):
        self.button.config(bd = bw)

    def setWidth(self, w):
        self.button.config(width = w)
        
    def setHeight(self, h):
        self.button.config(height = h)

    def setText(self, txt):
        self.button.config(text = txt)

    def padX(self, x):
        self.button.config(padx = x)
    
    def padY(self, y):
        self.button.config(padY = y)

    def pack(self):
        self.button.pack()


class CheckButton:
    def __init__(self, master = None):
        self.checkButton = tk.Checkbutton(master)

    def setBackground(self, color):
        self.checkButton.config(bg = color)

    def setBorderWidth(self, bw):
        self.checkButton.config(bd = bw)

    def setWidth(self, w):
        self.checkButton.config(width = w)
        
    def setHeight(self, h):
        self.checkButton.config(height = h)

    def setText(self, txt):
        self.checkButton.config(text = txt)

    def padX(self, x):
        self.checkButton.config(padx = x)
    
    def padY(self, y):
        self.checkButton.config(padY = y)

    def pack(self):
        self.checkButton.pack()


class ListBox:
    def __init__(self, master = None):
        self.label = tk.Label(master)

    def setBackground(self, color):
        self.label.config(bg = color)

    def setWidth(self, w):
        self.label.config(width = w)
        
    def setHeight(self, h):
        self.label.config(height = h)

    def setText(self, txt):
        self.label.config(text = txt)

    def pack(self):
        self.label.pack()



#class Menu:

#class Msg:

#class Entry:

#class MenuButton:

#class Scrollbar:

class Image:
    def __init__(self, fileName):
        self.image = tk.PhotoImage(file = fileName)