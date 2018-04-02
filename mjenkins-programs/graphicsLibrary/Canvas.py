import Tkinter as tk

class Window(tk.Frame):
    def __init__(self, width = 500, height = 500, master = None):
        tk.Frame.__init__(self, master)
        self.Canvas = tk.Canvas(self, width = width, height = height, bg = '#FFFFFF')
        self.pack()
        self.Objects = {}

    def loadGraphicsLibrary(self):
        self.Canvas.pack()
        self.master.title('')
        self.mainloop()     

    def deleteMostRecent(self):
        self.Canvas.delete(self.Objects[-1])
        del self.Objects[-1]

    def addOval(self, topLeft, bottomRight):
        self.Objects.append(self.Canvas.create_oval(topLeft[0], topLeft[1], bottomRight[0], bottomRight[1]))   

    def addRectangle(self, topLeft, bottomRight):
        self.Objects.append(self.Canvas.create_rectangle(topLeft[0], topLeft[1], bottomRight[0], bottomRight[1]))

    def addText(self, center, text):
        self.Objects.append(self.Canvas.create_text(center[0], center[1], text = str(text)))

    def addLine(self, pointA, pointB):
        self.Objects.append(self.Canvas.create_line(pointA[0], pointA[1], pointB[0], pointB[1]))

    def addTriangle(self, pointA, pointB, pointC):
        self.Objects.append(self.Canvas.create_line(pointA[0], pointA[1], pointB[0], pointB[1], pointC[0], pointC[1], pointA[0], pointA[1]))

class Oval:
    def __init__(self, Board, topLeft, bottomRight):
        Board.addOval(topLeft, bottomRight)

class Rectangle:
    def __init__(self, Board, topLeft, bottomRight):
        Board.addRectangle(topLeft, bottomRight)

class Text:
    def __init__(self, Board, center, text):
        Board.addText(center, text)

class Line:
    def __init__(self, Board, pointA, pointB):
        Board.addLine(pointA, pointB)

class Triangle:
    def __init__(self, Board, pointA, pointB, pointC):
        Board.addTriangle(pointA, pointB, pointC)