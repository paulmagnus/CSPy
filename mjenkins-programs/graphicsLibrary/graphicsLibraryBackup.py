import Tkinter as tk
import heapq
import cmath
from PIL import Image as image
from PIL import ImageTk as itk

#TODO: implement currentObjects as a heap so that objects can be generated in a specific order - for depth
#TODO: Event Handling - HOW???

def StartGraphicsEngine(Window):
    """Running this with your frame as an input starts the main loop."""
    Window.master.title(Window.name)
    Window.mainloop()

class Window(tk.Frame):
    """A class which allows for the placing of Graphical Objects."""
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.width = 0
        self.height = 0
        self.background = ""
        self.name = ""
        self.currentObjects = {}
    
    def Window(self, width = 400, height = 400, background = "white", name = ""):
        """A window is created."""

        #OPTIONAL PARAMETERS: width(int), height(int), background (string), name(string)

        self.width = width
        self.height = height
        self.background = background
        self.name = name
        self.Canvas = tk.Canvas(self, bg=self.background, height=self.height, width=self.width)
        self.Canvas.pack()

    def add(self, graphic):
        """Adds an object to the Window, assuming it is of type Graphical Object."""
        assert isinstance(graphic, GraphicalObject) #primary exception handling
        if isinstance(graphic, Oval):
            self.currentObjects[graphic] = self.Canvas.create_oval(graphic.topLeft[0], graphic.topLeft[1], 
                                                                   graphic.bottomRight[0], graphic.bottomRight[1], width = 2)
            graphic.window = self
        elif isinstance(graphic, Circle): 
            self.currentObjects[graphic] = self.Canvas.create_oval(graphic.topLeft[0], graphic.topLeft[1], 
                                                                   graphic.bottomRight[0], graphic.bottomRight[1], width = 2)
            graphic.window = self
        elif isinstance(graphic, Rectangle): 
            self.currentObjects[graphic] = self.Canvas.create_rectangle(graphic.topLeft[0], graphic.topLeft[1], 
                                                                        graphic.bottomRight[0], graphic.bottomRight[1],
                                                                        width = 2)
            graphic.window = self
        elif isinstance(graphic, Square):
            self.currentObjects[graphic] = self.Canvas.create_rectangle(graphic.topLeft[0], graphic.topLeft[1], 
                                                                        graphic.bottomRight[0], graphic.bottomRight[1],
                                                                        width = 2)
            graphic.window = self
        elif isinstance(graphic, Polygon):
            self.currentObjects[graphic] = self.Canvas.create_polygon(*graphic.points, width = 2, 
                                                                       fill = "", outline = "Black") 
                                                                       #so it looks similar to the other objects
            
            graphic.window = self
        elif isinstance(graphic, Text):
            self.currentObjects[graphic] = self.Canvas.create_text(graphic.center[0], graphic.center[1], 
                                                                   text = str(graphic.text), 
                                                                   font = ("Helvetica", graphic.size))
            graphic.window = self
        elif isinstance(graphic, Image):
            self.currentObjects[graphic] = self.Canvas.create_image(graphic.center[0], graphic.center[1], 
                                                                    image = graphic.img)
            graphic.window = self
        else: 
            #secondary exception handling, mostly to catch if something isn't implemented yet
            raise ObjectNotDeclaredException("Your object is of type GraphicalObject, \
                                             but it isn't one of the types allowed by the graphics library.")

    def remove(self, graphic):
        """Removes an object, if it exists, from the Window."""
        assert isinstance(graphic, GraphicalObject) and graphic in self.currentObjects
        self.Canvas.delete(self.currentObjects[graphic])
        del self.currentObjects[graphic]

    def setBackgroundColor(self, color):
        """Sets the Window's background color."""
        self.Canvas.configure(bg = color)

    def setHeight(self, height):
        """Sets the Window's height."""
        self.Canvas.configure(height = height)

    def setTitle(self, name): 
        """Sets the name of the Window."""
        self.name = name
        self.master.title(name)

    def setWidth(self, width):
        """Sets the width of the Window."""
        self.Canvas.configure(width = width)

class GraphicalObject:
    """An abstract class. This handles all objects which are added to the Window."""
    def addHandler(self, handler):
        """Adds user input through the keyboard or mouse."""
        pass

    def getCenter(self):
        """Returns the center of the graphical object."""
        return self.center

    def getDepth(self):
        """Returns the depth of the graphical object."""
        return self.depth

    def move(self, dx, dy):
        """Moves the object dx pixels horizontally and dy pixels vertically."""
        assert isinstance(point, tuple) and len(point) == 2
        if isinstance(self, Image) or isinstance(self, Text):
            self.center = (self.center[0] + dx, self.center[1] + dy)
            self.window.Canvas.coords(self.window.currentObjects[self], self.center[0], self.center[1])
        elif isinstance(self, Polygon):
            for i in range(len(self.points)):
                if i % 2 == 0:
                    self.points[i] += dx
                else:
                    self.points[i] += dy
            self.window.Canvas.coords(self.window.currentObjects[self], *self.points)
        else:
            self.topLeft = (self.topLeft[0] + dx, self.topLeft[1] + dy)
            self.bottomRight = (self.bottomRight[0] + dx, self.bottomRight[1] + dy)
            self.center = (self.center[0] + dx, self.center[1] + dy)
            self.window.Canvas.coords(self.window.currentObjects[self], 
                                      self.topLeft[0], self.topLeft[1], 
                                      self.bottomRight[0], self.bottomRight[1])
 
    def moveTo(self, point):
        """Moves the object to a point."""
        assert isinstance(point, tuple) and len(point) == 2
        #regenerate topleft bottomright depending on object type
        if isinstance(self, Text) or isinstance(self, Image): 
            self.center = point
            self.window.Canvas.coords(self.window.currentObjects[self], self.center[0], self.center[1])
        elif isinstance(self, Polygon):
            difference = ((self.center[0] + point[0] / 2), (self.center[1] + point[1] / 2))
            for i in range(len(self.points)):
                if i % 2 == 0:
                    self.points[i] += difference[0]
                else:
                    self.points[i] += difference[1]
            self.window.Canvas.coords(self.window.currentObjects[self], *self.points)
        elif isinstance(self, Fillable) and self.width and self.height:
                self.center = point
                self.topLeft = (self.center[0] - self.width, self.center[1] - self.height) 
                self.bottomRight = (self.center[0] + self.width, self.center[1] + self.height)
                self.window.Canvas.coords(self.window.currentObjects[self], 
                                          self.topLeft[0], self.topLeft[1], 
                                          self.bottomRight[0], self.bottomRight[1]) 
        else:
            raise ObjectNotDeclaredException("Your object is of type GraphicalObject, \
                                             but it isn't one of the types allowed by the graphics library.")

    def setDepth(self, depth):
        """Sets the depth of the object."""
        pass

class Image(GraphicalObject):
    """A bitmap image."""
    def __init__(self):
        self.image_loc = ""
        self.center = ()
        self.width = 0
        self.height = 0

    def Image(self, image_loc = "", center = (0, 0), width = 25, height = 25):
        """An Image is created. Images must be located within the current working directory 
        (ex. If you're working in /foo/bar and your picture is called foobar.jpg, 
        the picture has to be in /foo/bar in order to work.)."""

        #REQUIRED PARAMETERS: image_loc (str)
        #OPTIONAL PARAMETERS: center (tuple of int * int), width (int), height (int)

        self.image_loc = "./" + image_loc
        self.center = center
        self.width = width
        self.height = height
        self.img = imageGen(image_loc, width, height)

def imageGen(image_loc, width, height):
    """This generates an ImageTk object with the ability to be resized."""
    imgTemp = image.open(image_loc)
    imgTemp = imgTemp.resize((width, height), image.ANTIALIAS)
    return itk.PhotoImage(imgTemp)

class Text(GraphicalObject):
    """A string of characters."""
    def __init__(self):
        self.text = ""
        self.center = ()
        self.size = 0

    def Text(self, text, center = (0, 0), size = 12):
        self.text = text
        self.center = center
        self.size = size

class Fillable(GraphicalObject):
    """An abstract class which contains all objects whose colors can be modified."""
    def getBorderColor(self):
        """Returns the string containing the border color."""
        return self.borderColor

    def getBorderWidth(self):
        """Returns the border width."""
        return self.borderWidth

    def getDepth(self):
        """Returns the depth of the object."""
        return self.depth

    def getFillColor(self):
        """Returns the fill color of the object."""
        return self.fillColor

    def getPivot(self):
        """Returns the pivot point."""
        return self.pivot

    #this is broken because of the way Square and Rectangle objects are currently implemented.
    #TODO: possibly reimplement everything as Polygon objects.
    def rotate(self, degrees):
        """Rotates an object."""
        radians = (cmath.pi / 180) * degrees
        self.topLeft = rotateHelper(self.topLeft, radians, self.center)
        self.bottomRight = rotateHelper(self.bottomRight, radians, self.center)
        self.window.Canvas.coords(self.window.currentObjects[self], 
                                  self.topLeft[0], self.topLeft[1], 
                                  self.bottomRight[0], self.bottomRight[1])

    def scale(self, factor):
        """Scales an object."""
        self.topLeft = (self.center[0] - (factor * self.width), self.center[1] - (self.height * factor))
        self.bottomRight = (self.center[0] + (factor * self.width), self.center[1] + (self.height * factor))
        self.window.Canvas.coords(self.window.currentObjects[self], 
                                  self.topLeft[0], self.topLeft[1], 
                                  self.bottomRight[0], self.bottomRight[1])

    def setBorderColor(self, color):
        """Sets the border color."""
        self.borderColor = color
        self.window.Canvas.itemconfigure(self.window.currentObjects[self], outline = color)

    def setBorderWidth(self, width):
        """Sets the border width."""
        self.borderWidth = width
        self.window.Canvas.itemconfigure(self.window.currentObjects[self], width = width)

    def setFillColor(self, color):
        """Sets the border width."""
        self.fillColor = color  
        self.window.Canvas.itemconfigure(self.window.currentObjects[self], fill = color)

    def setPivot(self, pivot):
        """Sets the pivot point."""
        self.pivot = pivot

def rotateHelper(point, angle, pivot):
    """Aids in rotation."""
    assert isinstance(point, tuple) and len(point) == 2, "Point must be an (x,y) pair"
    assert isinstance(pivot, tuple) and len(pivot) == 2, "Pivot must be an (x,y) pair"
    
    cplx_pt = point[0] + point[1] * 1j - pivot[0] - pivot[1] * 1j
    cplx_rotation = cmath.exp(angle * 1j)
    
    new_pt = cplx_pt * cplx_rotation
    return (new_pt.real + pivot[0], new_pt.imag + pivot[1])

class Circle(Fillable):
    """A circle."""
    def __init__(self):
        self.width = 0
        self.height = 0
        self.center = ()
        self.window = None

    def Circle(self, radius = 40, center = (0, 0)):

        #OPTIONAL PARAMETERS: radius (int), center (tuple of int * int)

        self.width = radius
        self.height = radius
        self.center = center
        self.topLeft = (self.center[0] - self.width, self.center[1] - self.height) #necessary for importing to canvas
        self.bottomRight = (self.center[0] + self.width, self.center[1] + self.height) #necessary for importing to canvas

class Oval(Fillable):
    """An oval."""
    def __init__(self):
        self.width = 0
        self.height = 0
        self.center = ()
        self.window = None

    def Oval(self, radiusX = 40, radiusY = 60, center = (0, 0)):

        #OPTIONAL PARAMETERS: radiusX (int), radiusY (int), center (tuple of int * int) 

        self.width = radiusX
        self.height = radiusY
        self.center = center
        self.topLeft = (self.center[0] - self.width, self.center[1] - self.height) #necessary for importing to canvas
        self.bottomRight = (self.center[0] + self.width, self.center[1] + self.height) #necessary for importing to canvas

class Square(Fillable):
    """A square."""
    def __init__(self):
        self.sideLength = 0
        self.center = ()
        self.window = None

    def Square(self, sideLength = 40, center = (0, 0)):
        
        #OPTIONAL PARAMETERS: sideLength (int), center (tuple of int * int)
        
        self.width = sideLength
        self.height = sideLength
        self.center = center
        self.topLeft = (self.center[0] - self.width, self.center[1] - self.height) #necessary for importing to canvas
        self.bottomRight = (self.center[0] + self.width, self.center[1] + self.height) #necessary for importing to canvas

class Rectangle(Fillable): 
    """A rectangle."""
    def __init__(self):
        self.width = 0
        self.height = 0
        self.center = ()
        self.window = None

    def Rectangle(self, width = 40, height = 60, center = (0, 0)):

        #OPTIONAL PARAMETERS: width (int), height (int), center (tuple of int * int)

        self.width = width
        self.height = height
        self.center = center
        self.topLeft = (self.center[0] - self.width, self.center[1] - self.height) #necessary for importing to canvas
        self.bottomRight = (self.center[0] + self.width, self.center[1] + self.height) #necessary for importing to canvas

class Polygon(Fillable):
    """A polygon"""
    def __init__(self):
        self.points = []
        self.window = None

    def Polygon(self, * points):

        #REQUIRED PARAMETERS: points (list of tuple of int * int)

        self.points = points
        self.points = [i[j] for i in self.points for j in range(len(i))]
        self.center = listAverage(self.points)

def listAverage(points):
    """Averages all the even and odd integers in a list of integers. Returns a tuple."""
    pointsX = points[0:len(points):2]
    pointsY = points[1:len(points):2]
    return (float(sum(pointsX)) / len(pointsX), float(sum(pointsY)) / len(pointsY))

class ObjectNotDeclaredException(Exception):
    pass
