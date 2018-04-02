"""
A graphics library for CS 110

\defgroup Functions Global graphics functions

"""

"""
\mainpage Documentation for PYNT cs110graphics module

This is the documentation for the cs110graphics module.

\section Navigation basics

- Click on the modules tab to get to documentation about the global functions that
are available (currently only StartGraphicsSystem).

- Click on the classes tab to get the list of supported classes.

- Within the classes tab, you can get a class method index by clicking on the Class Members tab.

"""

# pylint: disable=C0301
# (Line too long)

# pylint: disable=C0103
# (Invalid name)

# pylint: disable=W0142
# (Used * or ** magic)

# pylint: disable=R0921
# (Abstract class not referenced)

# Enable these eventually

# pylint: disable=W0622
# (Redefining built-in type)

# pylint: disable=W0621
# (Redefining name from outer scope)

# pylint: disable=W0212
# (Access to protected member)


# PYDE summer research 2015 
# Emily and Kat
# Graphics Library

#import inspect

from browser import window, svg, html
from browser import document as doc
from javascript import JSObject
from jqueryui import jq

from utils import *
import shared
from config import *

import graphicsExceptions

jq = window.jQuery.noConflict(True)

# to determine if running in deployed or in editor
APP_DEPLOYED = window.location.href[:len(rootURL + "src/editor")] != rootURL + "src/editor"

# This gets defined the first time this library is loaded

LIBRARY_MODIFICATION_TIME = shared.getServerLibraryModificationTime()

class Window(object):
    """
    Creates a window on the display in which to draw graphics
    """
    def __init__(self, width=400, height=400, background="white",
                 name=None, quitButton=True, displayMessageBox=True,
                 firstFunction=None):
        self._width = width
        self._height = height
        self._quit_button = quitButton
        self._message_box = displayMessageBox
        self._contents = []

        if APP_DEPLOYED:
            self._dialog = doc["graphic-output"]
            self._content = doc["graphic-output"]
            self._window = doc["graphic-body"]
            self._canvas = doc["svg"]
            self._title = doc["title"]

        else:
            self._dialog = doc["graphics-modal-dialog"]
            self._content = doc["graphics-modal-content"]
            self._window = doc["graphics-modal-body"]
            self._canvas = doc["svg"]
            self._title = doc["graphics-title"]

            
            # show graphics modal -- requires jQuery
            jq('#graphics-popup').modal('show')
            jq('#graphics-popup').draggable()
        
            self._reset_modal()

        self.setHeight(height)
        self.setWidth(width)
        self.setBackgroundColor(background)
        
        if displayMessageBox:
            message = html.P(Id="graphics-message")
            box = html.DIV(message, Class="modal-footer", 
                           Id="graphics-modal-footer")

            if APP_DEPLOYED:
                box.style.height = "35px"
            else:
                box.style.height = "25px"

            self._content <= box
            self._message_box = document["graphics-message"]
        else:
            box = html.DIV(Class="modal-footer", 
                           Id="graphics-modal-footer")
            self._content <= box

        # new code

        firstFunction = graphicsExceptions.handleUserCodeException(firstFunction)
        self._firstFunction = firstFunction

#        self._firstFunction(self)

        self._rect = Rectangle(width, height, (width // 2, height // 2))
        self._rect.setFillColor("black")
        self._rect.setDepth(1000)
        self.add(self._rect)
        self.setMessageText("Click window to start your app")

        def startSystem():
            self._rect.move(-width, -height)
            self.setMessageText("Starting App...")
            clog("Calling first function...")
            self._firstFunction(self)
            self.setMessageText("First function complete...")

        self._rect.addHandler(clickHandlerFromFunction(startSystem)())

    def _reset_modal(self):
        try:
            self._content.remove(doc["graphics-modal-footer"])
        except:
            pass

        self._window.remove(self._canvas)
        _svg = document.createElementNS("http://www.w3.org/2000/svg", "svg")
        JSObject(_svg).setAttribute("width", self._width)
        JSObject(_svg).setAttribute("height", self._height)
        JSObject(_svg).setAttribute("id", "svg")
        self._window <= _svg
        self._canvas = doc["svg"]
        try:
            clog("X:" + str(JSObject(self._canvas).getAttribute("width")))
        except Exception as e:
            clog("Exception: " + str(e))

    def setHeight(self, height):
        """
        Sets the height of the window.
        @param height int: the height of the window
        @return None
        """
        # set svg container height
        JSObject(self._canvas).setAttribute("height", height)

        # set window height
        if APP_DEPLOYED:
            self._window.style.height = height+15
        else:
            self._window.style.height = height+2
        
    def setWidth(self, width):
        """
        Sets the width of the window.

        @param width int: the width of the window
        @return None
        """
        # set content width
        self._dialog.style.width = width+34

        # set svg container width
        JSObject(self._canvas).setAttribute("width", width)

        # set body width
        self._window.style.width = width+2

    def setBackgroundColor(self, color):
        """
        Sets the background color of the window to color (str).
        @param color str/None: color
        @return None
        """
        self._window.style = {"background-color": color}

    def setMessageText(self, text):
        """
        Sets the text of the message in the message box.

        @param text string: the text to be displayed in the message box.
        @return None
        """
        try:         
            self._message_box.text = text
        except:
            raise Exception("cannot set message box text")

    def setTitle(self, name):
        """
        Sets the title of the window.

        @param name str: the window title.
        @return None
        """
        self._title.text = name
    
    def close(self):
        """
        Removes the window from the display.
        @return None
        """
        jq("#graphics-popup").modal('hide')

    def add(self, graphic):
        """
        Adds a graphic to the Window.
        @param graphic GraphicalObject: the object to add.
        @return None
        """
        graphic._container = self
        graphic._draw(self)
        i = 0
        while i < len(self._contents) and self._contents[i]._depth >= graphic._depth:
            i += 1
        self._contents.insert(i, graphic)
        self._updateDepth(graphic)
        graphic._window = self._window

    def remove(self, graphic):
        """
        Removes graphic from the Window.
        @param graphic GraphicalObject: the object to remove.
        @return None
        """        
        graphic._undraw(self)
        graphic._container = None
        self._group.remove(graphic)

    def _updateDepth(self, graphic):
        redraw = [graphic]
        for member in self._contents:
            if member._depth < graphic._depth:
                redraw.append(member)

        for member in redraw:
            member._redraw(self)

class Event(object):
    """
    An object that represents graphical user interface events such as mouse
    clicks.
    """
    def __init__(self, ev):
        self._type = ev.type
        self._ev = ev

    def getButton(self):
        button = self._ev.button
        if button == 1:
            return "left"
        if button == 2:
            return "right"
        if button == 4:
            return "wheel"

    def getDescription(self):
        return "Type: " + self._type

    def getKey(self):
        return char(self._ev.which) # change

    def getMouseLocation(self):
        return (self._ev.x, self._ev.y)

class EventHandler(object):
    """
    An object that handles events reported by the graphical user interface
    """
    def __init__(self):
        """
        The constructor.
        """
        pass

    def handleKeyPress(self):
        """Not Implemented"""
        pass
    
    def handleKeyRelease(self):
        """Not Implemented"""
        pass
    
    def handleMouseDrag(self):
        """Not Implemented"""
        pass

    def handleMouseEnter(self):
        """Not Implemented"""
        pass

    def handleMouseLeave(self):
        """Not Implemented"""
        pass

    def handleMouseMove(self):
        """Not Implemented"""
        pass
    
    def handleMousePress(self):
        """
        Called by the graphical user interface when the mouse is clicked
        inside the registered graphical object
        """
        pass

    def handleMouseRelease(self):
        """Not Implemented"""
        pass

import inspect

def callHandlerWithOrWithoutEvent(handler, event):


    # Get the number of arguments for the handler. If the handler
    # has an argument (other than self), pass the event. Otherwise,
    # don't.

    argCount = len(inspect.getargs(handler.__code__)[0])

    # Wrap the function in an code exception handler

    handler = graphicsExceptions.handleUserCodeException(handler)

    if argCount == 1:
        handler()
    else:
        handler(event)

class GraphicalObject(object):
    """
    An abstract class for all objects can be drawn in a window.
    You don't create objects of this class, instead, other classes depend
    on this class to provide their funcationality.
    """
    def __init__(self):
        self._svgGraphic = None
        self._center = (0, 0)
        self._depth = 50
        self._container = None
        self._drawn = False
        self._window = None

    def addHandler(self, handler):
        """
        Registers an object to handle events for the object.

        @param handler EventHandler: the event handler object.
        @return None
        """
        def keyPress(ev):
            callHandlerWithOrWithoutEvent(handler.handleKeyPress, Event(ev))

        def keyRelease(ev):
            callHandlerWithOrWithoutEvent(handler.handleKeyRelease, Event(ev))

        def mouseDrag(ev):
            callHandlerWithOrWithoutEvent(handler.handleMouseDrag, Event(ev))

        def mouseEnter(ev):
            callHandlerWithOrWithoutEvent(handler.handleMouseEnter, Event(ev))
            
        def mouseLeave(ev):
            callHandlerWithOrWithoutEvent(handler.handleMouseLeave, Event(ev))

        def mouseMove(ev):
            callHandlerWithOrWithoutEvent(handler.handleMouseMove, Event(ev))

        def mousePress(ev):
            callHandlerWithOrWithoutEvent(handler.handleMousePress, Event(ev))

        def mouseRelease(ev):
            callHandlerWithOrWithoutEvent(handler.handleMouseRelease, Event(ev))

        types = ['keydown', 'keyup', 'mouseenter', 'mouseleave', 'mousemove', 
                 'mousedown', 'mouseup']
        funcs = [keyPress, keyRelease, mouseEnter, mouseLeave, mouseMove, 
                 mousePress, mouseRelease]
        handler_methods = ['handleKeyPress', 'handleKeyRelease', 
                           'handleMouseEnter', 'handleMouseLeave', 
                           'handleMouseMove', 'handleMousePress', 
                           'handleMouseRelease']

        for i in range(len(handler_methods)):
            if getattr(handler, handler_methods[i]).__doc__ != 'Not Implemented':
                if 'Key' in handler_methods[i]:
                    window.bind(types[i], funcs[i])
                else:
                    self._svgGraphic.bind(types[i], funcs[i])
            
    def getCenter(self):
        """
        Returns the center point of the object.
        @return tuple(int, int): the location of the center.
        """
        return self._center

    def move(self, dx, dy):
        """
        Moves the object dx (int) pixels along the x-axis and dy (int) units
        along the y-axis.

        @param dx int: the x distance.
        @param dy int: the y distance.
        @return None
        """
        self._center = (self._center[0]+dx, self._center[1]+dy)
        self._svgGraphic.x = float(self._svgGraphic.x) + dx
        self._svgGraphic.y = float(self._svgGraphic.y) + dy
            
    def moveTo(self, point):
        """
        Moves the object to the specified location.

        @param point tuple(int, int): the new location of the object.
        @return None
        """
        dx = point[0] - self._center[0]
        dy = point[1] - self._center[1]
        self.move(dx, dy)

    def getDepth(self):
        """
        Gets the depth of the object.

        @return int: the object's depth.
        """
        return self._depth

    def setDepth(self, depth):
        """
        Sets the depth of the object.

        @param depth int: the object's depth.
        @return None
        """
        self._depth = depth
        if self._drawn:
            self._container._updateDepth(self)
       
    def _draw(self, window):
        window._canvas.appendChild(self._svgGraphic)
        self._drawn = True

    def _undraw(self, window):
        window._canvas.removeChild(self._svgGraphic)
        self._drawn = False
  
    def _redraw(self, window):
        self._undraw(window)
        self._draw(window)

class Group(GraphicalObject):
    def __init__(self):
        GraphicalObject.__init__(self)
        self._contents = []

    def add(self, graphic):
        i = 0
        while i < len(self._contents) and self._contents[i]._depth >= graphic._depth:
            i += 1
        self._contents.insert(i, graphic)

        self._setCenter()

    def remove(self, graphic):
        self._contents.remove(graphic)
        self._setCenter()

    def _setCenter(self):
        x = 0
        y = 0
        for member in self._contents:
            x += member._center[0]
            y += member._center[1]
        self._center = (x/len(self._contents), y/len(self._contents))

    def move(self, dx, dy):
        for member in self._contents:
            member.move(dx, dy)

    def _draw(self, window):
        for member in self._contents:
            member._draw(window)
            member._container = self
        self._drawn = True

    def _undraw(self, window):
        for member in self._contents:
            member._undraw(window)
            member._container = None
        self._drawn = False

    def _redraw(self, window):
        self._undraw(window)
        self._draw(window)

    def _updateDepth(self, graphic):
        self._contents.remove(graphic)
        i = 0
        while self._contents[i]._depth >= graphic._depth:
            i += 1
        self._contents.insert(i, graphic)
        self._container._updateDepth()
             
class Fillable(GraphicalObject):
    """
    An abstract class providing fillable graphical objects.
    
    You don't create objects of this class, instead, other classes depend
    on this class to provide their funcationality.
    """
    def __init__(self):
        GraphicalObject.__init__(self)

        self._fill = None
        self._stroke = "black"
        self._stroke_width = 1
        self._transform_matrix = [1, 0, 0, 1, 0, 0]
        self._pivot = None
        self._rotate = 0

    def setFillColor(self, color):
        """
        Sets the fill color.
        @param color str/None: color
        @return None
        """
        self._svgGraphic.fill = color
        self._fill = color

    def getFillColor(self):
        """
        Returns the fill color.
        @return str: the fill color.
        """
        return self._fill
    
    def setBorderColor(self, color):
        """
        Sets the border color.
        @param color str/rgb tuple: color
        @return None
        """
        self._svgGraphic.stroke = color
        self._stroke = color

    def getBorderColor(self):
        """
        Returns the border color.
        
        @return str: the color of the border.
        """
        return self._stroke

    def setBorderWidth(self, width):
        """
        Sets the border width.
        @param width int: the border width in pixels.
        @return None
        """
        self._svgGraphic.stroke_width = width
        self._stroke_width = width
    
    def getBorderWidth(self):
        """
        Returns the border width.
        @return int: the border width.
        """
        return self._stroke_width

    def scale(self, factor):
        """
        Scales the object about its pivot point.

        @param factor float: the scaling factor (2 doubles the size)
        @return None
        """
        self._svgGraphic.height = float(self._svgGraphic.height)*factor
        self._svgGraphic.width = float(self._svgGraphic.width)*factor
        self._reset_center

    def _reset_center(self):
        self._svgGraphic.x = self._center[0]-float(self._svgGraphic.width)/2 
        self._svgGraphic.y = self._center[1]-float(self._svgGraphic.height)/2

    def _transform(self):
        matrix = []
        for i in self._transform_matrix:
            matrix.append(str(i))
        matrix = " ".join(matrix)
        new_matrix = "matrix("+ matrix + ")"
        self._svgGraphic.transform = new_matrix

    def getPivot(self):
        """
        Gets the pivot point of the object.

        @return tuple(int, int): the object's pivot.
        """
        return self._pivot

    def setPivot(self, pivot):
        """
        Sets the pivot point of the object.

        @param pivot tuple(int, int): the pivot point.
        @return None
        """
        self._pivot = pivot
        self.rotate(self._rotate)

    def rotate(self, degrees):
        """
        Rotates the object about its pivot point.

        @param degrees float: the number of degrees of clockwise rotation.
        @return None
        """
        rotate = [str(degrees), str(self._pivot[0]), str(self._pivot[1])]
        rotate = " ".join(rotate)
        self._rotate = degrees
        self._svgGraphic.transform = "rotate("+rotate+")"

    def flip(self, angle):
        # not sure how to do this one.. or what it should do
        pass

class Circle(Fillable):
    """
    A circle that can be drawn in a window.
    """
    def __init__(self, radius=40, center=(0, 0)):
        """
        @param radius int: the radius of the circle.
        @param center tuple(int, int): the location of the center of the circle
        """
        Fillable.__init__(self)
        self._center = center
        self._svgGraphic = svg.circle(r=radius, cx=center[0], cy=center[1], 
                                      stroke="black", stroke_width=1, fill=None,
                                      transform="rotate(0, 100, 100)")

    def move(self, dx, dy):
        """
        Moves the object dx (int) pixels along the x-axis and dy (int) units
        along the y-axis.

        @param dx int: the x distance.
        @param dy int: the y distance.
        @return None
        """
        self._center = (self._center[0]+dx, self._center[1]+dy)
        self._svgGraphic.cx = float(self._svgGraphic.cx) + dx
        self._svgGraphic.cy = float(self._svgGraphic.cy) + dy

    def setRadius(self, radius):
        """
        Sets the radius of the circle.
        @param radius int: the radius of the circle (in pixels).
        @return None
        """
        self._svgGraphic.r = radius

    def scale(self, factor):
        """
        Scales the object

        @param factor float: the scaling factor (2 doubles the size)
        @return None
        """

        self._svgGraphic.r = int(self._svgGraphic.r)*factor


class Square(Fillable):
    """
    A square that can be drawn in a window.
    """
    def __init__(self, sideLength=40, center=(0, 0)):
        """
        @param sideLength int: the length of a side (in pixels).
        @param center tuple(int, int): the location of the center.
        """
        Fillable.__init__(self)

        x = center[0]-sideLength/2
        y = center[1]-sideLength/2
        self._center = center
        self._pivot = center
        self._svgGraphic = svg.rect(height=sideLength, width=sideLength, x=x, 
                                    y=y, stroke="black", stroke_width=1, 
                                    fill=None, transform="rotate(0)")


class Text(GraphicalObject):
    """
    A string of text that can be drawn in window.
    """
    def __init__(self, text, center=(0, 0), size=12):
        GraphicalObject.__init__(self)
        self._center = center
        x = center[0]
        y = center[1]
        self._svgGraphic = svg.text(text, x=x, y=y, text_anchor="middle", font_size=size)

    def setText(self, text):
        """
        Sets the text string that is displayed
        This method is deprecated version of setTextString

        @param text str: the text to display
        @return None
        """
        self._svgGraphic.text = text

    def setTextString(self, textString):
        """
        Sets the text string that is displayed
        This method is identical to setText (deprecated)

        @param textString str: the text to display
        @return None
        """
        self._svgGraphic.text = textString

#    def setRotate(self, angle):
#        self._svgGraphic.transform="rotate("+str(angle)+")"

class Polygon(Fillable):
    """
    A polygon than can be drawn in a window.
    """
    def __init__(self, points):
        """
        @param points list: a list of points defining the polygon
        """

        Fillable.__init__(self)
        self._points = points
        self._center = points[0]
        pointstr = " ".join([+str(x)+","+str(y) for (x, y) in self._points])
        self._svgGraphic = svg.polygon(points=pointstr, fill=None, stroke="black")

    def move(self, dx, dy):
        """
        Moves the object dx (int) pixels along the x-axis and dy (int) units
        along the y-axis.

        @param dx int: the x distance.
        @param dy int: the y distance.
        @return None
        """
        for i in range(len(self._points)):
            x, y = self._points[i]
            x += dx
            y += dy
            self._points[i] = (x, y)
        self._center = self._points[0] 
        pointstr = " ".join([+str(x)+","+str(y) for (x, y) in self._points])
        self._svgGraphic.points = pointstr

class Image(GraphicalObject):
    """
    A raster graphics image that can be drawn in a window
    """

    def __init__(self, image_url=None, center=(0, 0), width=25, height=25):
        """
        The constructor.

        @param image_url str: the URL of the image on the web
        @param center tuple(int, int): the location of the center.
        @param width: the display width of the image (image will be scaled to this value)
        @param height: the display height of the image (image will be scaled to this value)
        """

        GraphicalObject.__init__(self)
# mwb - disable the width and height stuff for now
#          width, height = shared.get_image_size(image_url)
        x = center[0]-width/2
        y = center[1]-height/2
        self._center = center
        self._pivot = center
        
        self._clip_square = svg.rect(width=width, height=height, x=x, y=y, 
                                     transform="rotate(0)")
        self._clip_path = svg.clipPath(self._clip_square, Id="clip-path")

        self._svgGraphic = svg.image(width=width, height=height, x=x, y=y, 
                                     href=image_url, transform="rotate(0)")
        self._svgGraphic.setAttribute("preserveAspectRatio", "none")

        self._svgGraphic.setAttribute("clip-path", "url(#clip-path)")
          
      
    def size(self):
        """
        Returns the size, in pixels, of the image.

        @return tuple(int, int): the width and height
        """
        return (float(self._svgGraphic.width), float(self._svgGraphic.height))

    def resize(self, width, height):
        """
        Mutates an image by resizing.

        @param width int: the desired width, in pixels
        @param height int: the desired height, in pixels
        @return None
        """
        self._svgGraphic.width = width
        self._svgGraphic.height = height
        
        self._clip_square.width = width
        self._clip_square.height = height
        
        self._reset_center()

    def scale(self, factor):
        """
        Scales the image by the specified factor

        @param factor float: the scaling factor (2 doubles the size)
        @return None
        """

        self.resize(float(self._svgGraphic.width)*factor,
                    float(self._svgGraphic.height)*factor)

        self._reset_center()

    def _reset_center(self):
        self._svgGraphic.x = self._center[0]-float(self._svgGraphic.width)/2 
        self._svgGraphic.y = self._center[1]-float(self._svgGraphic.height)/2
        
        self._clip_square.x = self._center[0]-float(self._clip_square.width)/2
        self._clip_square.y = self._center[1]-float(self._clip_square.height)/2

    def rotate(self, degrees):
        """
        Rotates the image

        @param degrees float: the number of degrees of clockwise rotation.
        @return None
        """
        rotate = [str(degrees), str(self._pivot[0]), str(self._pivot[1])]
        rotate = " ".join(rotate)
        self._svgGraphic.transform = "rotate("+rotate+")"
        #self._clip_square.transform = "rotate("+rotate+")"

    def crop(self, top=0, bottom=0, left=0, right=0):
        """
        Crops the image

        @param top int: the row of pixels that will be the new top row
        @param bottom int: the row of pixels that will be the new bottom row
        @param left int: the column of pixels that will be the new left column
        @param right int: the column of pixels that will be the new right column
        @return None
        """
        square = self._clip_path
        self._clip_square.x = float(self._svgGraphic.x) + left
        self._clip_square.y = float(self._svgGraphic.y) + top
        self._clip_square.width = float(self._svgGraphic.width)-left-right
        self._clip_square.height = float(self._svgGraphic.height)-top-bottom
          
    def _draw(self, window):
        GraphicalObject._draw(self, window)
        window._canvas.appendChild(self._clip_path)


# new code

class Rectangle(Fillable):
    """
    A rectangle that can be drawn in a window.
    """
    def __init__(self, width=40, height=40, center=(0, 0)):
        """
        @param width int: width of the rectangle (in pixels).
        @param height int: height of the rectangle (in pixels).
        @param center tuple(int, int): the center of the rectangle.
        """
        Fillable.__init__(self)

        x = center[0]-width/2
        y = center[1]-height/2
        self._center = center
        self._pivot = center
        self._svgGraphic = svg.rect(height=height, width=width, x=x, 
                                    y=y, stroke="black", stroke_width=1, 
                                    fill=None, transform="rotate(0)")


class _ClickHandlerTemplateClass(EventHandler):
    def __init__(self, func, *args, **kwargs):
        EventHandler.__init__(self)
        self._func = func
        self._args = args
        self._kwargs = kwargs
    
    def handleMousePress(self):
        self._func(*self._args, **self._kwargs)

def clickHandlerFromFunction(func):
    def clickHandlerBuilder(*args, **kwargs):
        return _ClickHandlerTemplateClass(func, *args, **kwargs)
    return clickHandlerBuilder

GraphicsSystemEnabled = True

def disableGraphicsSystem():
    global GraphicsSystemEnabled
    GraphicsSystemEnabled = False

def enableGraphicsSystem():
    global GraphicsSystemEnabled
    GraphicsSystemEnabled = True

def StartGraphicsSystem(firstFunction, width=400, height=400, background="white", name=""):
    """
    Labels the top-level function of a program. This will cause the graphics
    system to invoke the function indicated after the system has started.

    @param firstFunction function(Window): the function to call to start the use program. The window is passed to this function.
    @param width int:     width of the window in pixels.
    @param height int:    height of the window in pixels.
    @param background str: background color of the window.
    @param name str:       title of the window.
    @return None
    \ingroup Functions
    """
    if GraphicsSystemEnabled:
        win = Window(width, height, background, name, firstFunction = firstFunction)

#    else:
#        print("Graphics system is disabled")

import browser.timer

request_animation_frame = browser.timer.request_animation_frame
cancel_animation_frame = browser.timer.cancel_animation_frame
set_timeout = browser.timer.set_timeout
clear_timeout = browser.timer.clear_timeout
set_interval = browser.timer.set_interval
clear_interval = browser.timer.clear_interval

class RunWithYieldDelay:
    """
    Registers a function to be called at various intervals.
    """
    def __init__(self, functionCall):
        """
        Register a function to be called at various intervals.

        @param: functionCall function call: A function to be called on intervals. The parameter should include parentheses and parameters for the function. The function *must* include a yield expression.

        Example use:

            def moveRect(rect):
                for _ in range(10):
                    rect.move(10, 10)
                    yield 100   # Yields control for 100 milliseconds
            ...
                RunWithYieldDelay(moveRect(the_rectangle_to_move))

        """
        gen = graphicsExceptions.handleUserCodeExceptionGen(functionCall)
        self._generator = gen
        self.run()

    def run(self):
        try:
            delay = self._generator.__next__()
            if delay is None:
                delay = 1000
        except StopIteration:
            delay = 0
        
        if delay > 0:
            set_timeout(self.run, delay)

class Timer:
    def __init__(self, function, interval):
        self._function = function
        self._interval = interval
        self._timer = None
        
    def start(self):
        if self._timer is not None:
            clear_interval(self._timer)
            
        self._timer = set_interval(self._function, self._interval)
        
    def stop(self):
        if self._timer is not None:
            clear_interval(self._timer)
        self._timer = None

    def setInterval(self, interval):
        self._interval = interval
        if self._timer is not None:
            self.stop()
            self.start()
            
    def setFunction(self, function):
        self._function = function
        if self._timer is not None:
            self.stop()
            self.start()
