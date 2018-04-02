"""
A graphics library for CS 110

\defgroup Functions Global graphics functions

"""


## Current issues:

# Can use setPivot on Path (or other non-fillable?). Need to implement
# rotate, etc. for all of these, flip too.


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

# $Revision: 20 $
# $Date: 2011-11-14 21:11:16 -0500 (Mon, 14 Nov 2011) $

import sys

#if "cs110graphics" in sys.modules.keys():
#    raise StandardError ("""you have already imported the old graphics library.
#You can't import both the old and new libraries.""")

import math
#import mtTkinter as Tk
import Tkinter as Tk
import tkMessageBox
import tkFont
import copy
import types
from PIL import Image as PILimage
from PIL import ImageTk

GraphicsLibraryVersion = "Version $Revision: 20 $, last revised $Date: 2011-11-1p4 21:11:16 -0500 (Mon, 14 Nov 2011) $"

ALL_GRAPHIC_OBJECTS = {}

# Place all globals that other modules need to see here before imports so
# the submodules can do an import of this module

GS = None

from cs110exceptions import *
from cs110utils import *
from cs110locks import *
from cs110GraphicsSupport import *
from cs110Colors import *
from cs110events import *
from cs110transform import *
from cs110point import *

gen = None


# May need to do something with exiting...

#def exiting():
#    print "Exiting!"

#import atexit
#atexit.register(exiting)

class UserPressedQuit(Exception): 
    pass

QuitButtonPressed = False

class GraphicsSystem:
    # Keeper of window related information
    def __init__(self, first):
        global GS
        
        GS = self
        log("Creating graphics system")

        self._openWindowCount = 0
        self._windows = []
        self._firstWindow = True

        self._eventDriven  = True

        log("Starting graphics system")

        self.tkRoot = Tk.Tk()

        # Replace the standard exception handling messages

        self.tkRoot.report_exception = self.handleGraphicsException
        self.tkRoot.report_callback_exception = \
             self.handleUserGraphicsHandlerException

        # Add handlers for CTRL-C and CTRL-Z to the graphics window

        self.tkRoot.bind_all("<Control-c>", self.ctrlC)
        self.tkRoot.bind_all("<Control-C>", self.ctrlC)
        self.tkRoot.bind_all("<Control-z>", self.ctrlZ)
        self.tkRoot.bind_all("<Control-Z>", self.ctrlZ)

        # A wrapper function for the first user function that closes down
        # the system if no windows remain open

        def lastFunction():
#            console("Last function called")
            if GUIRaisedKeyboardInterrupt.get():
                raise GUIKeyboardInterrupt

            self.tkRoot.after(200, lastFunction)

        def firstWrapper():
            try:
                first()
            except UserPressedQuit:
                pass

#            if not QuitButtonPressed and not self.eventDriven() and self._openWindowCount > 0:
#                print >> sys.stderr, "First function returned without closing the window!"
##                self._windows[0].addQuitButton()

            self.shutdownIfNoWindows()
            lastFunction()
        
        # def oldfirstWrapper():
        #     global gen

        #     if gen == None:
        #         gen = first()
            
        #     # Check if this is a generator -- this needs to be more robust

        #     if gen != None:
        #         try:
        #             gen.next()
        #             self.tkRoot.after(0, firstWrapper)
        #             return

        #         except StopIteration:
        #             pass
        #     self.shutdownIfNoWindows()

        # Register the first function to be called after the graphics system
        # is up and running

        self.tkRoot.after(0, firstWrapper)

        log("Entering graphics main loop")
        try:
            try:
                self.tkRoot.mainloop()
            except GUIKeyboardInterrupt:
                log("Keyboard interrupt caught in mainloop. Shutting down.")
                print >> Console, "Shutting down graphics system"
                raise
            except KeyboardInterrupt:
                log("Keyboard interrupt caught in mainloop. Shutting down.")
                print >> Console, "Control-c pressed. Program aborted by user!"
                print >> Console, "Shutting down graphics system"
                raise
        finally:
            log("Exiting main loop")

#        self.tkRoot.stop()
#        raise SystemExit
#        self.tkRoot.destroy()

    def eventDriven(self):
        return self._eventDriven
    
    def setEventDriven(self, value):
        self._eventDriven = value


    # handler for control-z events on graphics windows

    def ctrlZ(self, _ = None):
        print "Don't use control-z to abort. Please use control-c"

    # handler for control-c events on graphics windows

    def ctrlC(self, _ = None):
        log("Control C pressed in graphics window. Aborting.")

        if not GUIRaisedKeyboardInterrupt.get():
            print >> Console, "Control-c pressed. Program aborted by user!"

            GUIRaisedKeyboardInterrupt.set(True)
        else:
            print >> Console, "Program aborting, please wait."

    # Exception reporter for non-callback exceptions

    def handleGraphicsException(self, _unused_ty, _unused_value, _unused_tb):

        # For now, pass raise the exception again, causing TkInter to pass
        # the exception back to the surrounding system

        log("Tkinter called graphics handler exception")

        raise

    # Exception reporter for callback exceptions

    def handleUserGraphicsHandlerException(self, _unused_ty, _unused_value,
                                           _unused_tb):

        # For now, pass raise the exception again, causing TkInter to pass
        # the exception back to the surrounding system

        log("Tkinter called callback handler exception")

        raise

    # Creates a graphics window

    def createWindow(self, windowObject, width, height, x, y, name = None, screen = None):
        self._openWindowCount += 1
        self._windows.append(windowObject)

        # If no name is given, use a reasonable name

        if name == None:
            if self._firstWindow:
                name = "Main Graphics Window"
            else:
                name = "Secondary Graphics Window"
        
        # If this is the first window, we can use the TK root. Otherwise
        # create a new one.

        if self._firstWindow:
            self._firstWindow = False
            toplevel = GS.tkRoot
            toplevel.config(height = height, width = width, bd = 0,
                            relief = Tk.FLAT)

            # What if the first window is a remote window?

        else:
            if screen is None:
                toplevel = Tk.Toplevel(height = height, width = width)
            else:
                toplevel = Tk.Toplevel(screen = screen, height = height,
                                       width = width)

        # Set the size of the window and its title.

        toplevel.geometry("+%d+%d" % (x, y))
        toplevel.title(name)
            
        # Add an icon

#        toplevel.iconbitmap("/home/mbailey/graphics/src/logo.xbm")

        return toplevel

    # Removes the window from the screen

    def destroyWindow(self, toplevel):
        self._openWindowCount -= 1
        toplevel.withdraw()

    # Shuts down the graphics system if no open windows remain.

    def shutdownIfNoWindows(self):
        if self.windowsOpen():
            return

        self.shutdown()

    def windowsOpen(self):
        return self._openWindowCount > 0

    # Shuts down the system

    def shutdown(self):
        log ("Signalling graphics system to close")
        self.tkRoot.quit()

def sleep(seconds):
    """
    Sleeps for the a period of time

    @param seconds float : the number of seconds for which to sleep
    @return None

    \ingroup Functions
    """
    import time
    autoUpdate()
    time.sleep(seconds)
    autoUpdate()

AutoUpdate = True
EventDriven = False

def SetEventDriven():
    """
    Sets the event driven flag
    @return None

    \ingroup Functions
    """
    global EventDriven
    global AutoUpdate

    EventDriven = True
    AutoUpdate = False

def SetAutoUpdate(value):
    """
    Sets the auto update flag

    @param value bool : if True, update the screen upon graphics changes. Otherwise, don't update.
    @return None

    \ingroup Functions
    """
    global AutoUpdate
    AutoUpdate = value

def autoUpdateManual():
    pass

def autoUpdate():
    if AutoUpdate:
        update()

# This function is called from inside either a user's first function or
# inside a user's callback. It gives control back to the graphics system
# to process all outstanding events.

def update():
    """
    Signals the graphics system to update the display. Use this function to
    show intermediate steps in an animation. 
    @return None
    \ingroup Functions
    """

#    log ("Updating graphics display")
    if GUIRaisedKeyboardInterrupt.get():
        raise GUIKeyboardInterrupt
    GS.tkRoot.update()
#    log ("Done updating")

firstFunctionOverride = False

# This function is used to disable the calling of the first function.
# Used by grading systems to bypass calls.

def overrideFirstFunction():
    global firstFunctionOverride
    firstFunctionOverride = False


def StartGraphicsSystem(func, overriding = False):
    """
    Labels the top-level function of a program. This will cause the graphics
    system to invoke the function indicated after the system has started.

    @param func function: the function to call to start the use program.
    @return None
    \ingroup Functions
    """
    
    # Put a type check here to make sure they don't do anything too funky

#    print "Starting up graphics library"

    if not firstFunctionOverride or overriding:
        try:
            GraphicsSystem(func)
            if EventDriven:
                update()
        except KeyboardInterrupt:
            raise
#    print >> Console, "First function has exited. Won't be able to catch exceptions"

def verifyGraphicalObject(obj):
    TypeCheck(obj, None, GraphicalObject)

def verifyPoint(obj):
    TypeCheck(obj, None, Point)

# This class is used to handle the auto update scheme. Each object that may
# cause an update to be needed extends this class. All methods calls are 
# tracked. The last method return in a stack calls autoupdate.

CanvasDirty = False
EnteredGraphicsLibrary = False
class AutoUpdaterObject(CS110Object):
    def __getattribute__(self, name):

        # Overrides the standard attribute lookup. When a method is called,
        # first the attribute is looked up. 

        objectAttribute = object.__getattribute__(self, name)

        # See if the attribute we get back is callable (is a method)
        # If not, just return it because we don't want to wrap it

        if not hasattr(objectAttribute, '__call__'):
            return objectAttribute

        # Don't mess with builtin stuff...

        if name[:2] == "__" and name != "__init__":
            return objectAttribute

        # So, we have a method. Wrap the method and return the result
        # that is being called...

        invokedMethod = objectAttribute

        def functionCallMonitor(*args, **kwargs):
            global EnteredGraphicsLibrary
            global CanvasDirty

            # If this call is not the one to enter the library, just invoke
            # it in the usual way.

            if EnteredGraphicsLibrary:
                return invokedMethod(*args, **kwargs)

            # If this call is the one to enter the library, mark it as so,
            # call the method, and when it returns, call autoupdate.

            EnteredGraphicsLibrary = True
            result = invokedMethod(*args, **kwargs)
            EnteredGraphicsLibrary = False
            if CanvasDirty:
                autoUpdate()
#            else:
#                print "Saving an update!"
            CanvasDirty = False

            return result
        
        # Make this function have the same docstring as the invoked
        # method (Used for EventHandler)

        functionCallMonitor.__doc__ = invokedMethod.__doc__

        return functionCallMonitor

class GraphicalObject(AutoUpdaterObject):
    """
    An abstract class for all objects can be drawn in a window.
    You don't create objects of this class, instead, other classes depend
    on this class to provide their funcationality.
    """
    # pylint: disable=W0231
    # (base class __init__ not called)
    def __init__(self, center):
        self._center = center
        self._depth = 50
        self._canvas = None
        self._tkGraphic = None
        self._eventHandlers = []
        self._container = None
        self._tkAttr = {}
    # pylint: enable=W0231
    # (base class __init__ not called)

    def __str__(self):
        return "cs110 %s(center = %s)" % (type(self).__name__, str(self._center))

#    def __str__(self):
#        return ("cs110 " + self.__class__.__name__ + " object" + " (" +
#                str(self.getTkGraphic())+ ")")

    def setContainer(self, container):
        self._container = container

    def getContainer(self):
        return self._container
    
    def setTkGraphic(self, graphic):
        self._tkGraphic = graphic

    def getTkGraphic(self):
        return self._tkGraphic

    def _getCanvas(self):
        return self._canvas

    def getCenter(self):
        """
        Returns the center point of the object.
        @return Point: the location of the center.
        """
        return self._center

    def move(self, dx, dy = None):
        """
        Moves the object dx (int) pixels along the x-axis and dy (int) units
        along the y-axis.

        @param dx int: the x distance. If dy is omitted, dx must be a Point
        containing (dx, dy).
        @param dy int: the y distance. If omitted, dx must be a Point
        containing (dx, dy).
        @return None
        """
        
  ## Also: move(self, point)

        CheckParms((dx, "dx", (int, float, Point)),
                   (dy, "dy", (int, float, types.NoneType)))

        if isinstance(dx, Point) and dy == None:
            dx, dy = dx.get()

        self._center += Point(dx, dy)

        if self.drawn():
            self._canvas.move(self._tkGraphic, dx, dy)

    def moveTo(self, point):
        """
        Moves the object to the specified location.

        @param point Point: the new location of the object.
        @return None
        """

        CheckParms((point, "point", Point))

        dx, dy = (point - self._center).get()
        self.move(dx, dy)

    def updateDepth(self):
        if self.drawn():
            self._canvas.setDepth(self._tkGraphic, self.getCanonicalDepth())

    def setDepth(self, depth):
        """
        Sets the depth of the object.

        @param depth int: the object's depth.
        @return None
        """
        CheckParms((depth, "depth", (int, float, str)))

        self._depth = depth
        self.updateDepth()

    def getDepth(self):
        """
        Gets the depth of the object.

        @return int: the object's depth.
        """
        return self._depth

    def getCanonicalDepth(self):
        if self._container == None:
            return (self._depth,)

        depth = list(self._container.getCanonicalDepth())
        depth.append(self._depth)
        return tuple(depth)

#    def clone(self):
#        """
#        Makes a copy of the object.
#
#        @return GraphicalObject: the copy.
#        """
#        cp = copy.copy(self)
#        cp._clone()
#        return cp

    def _clone(self):
        self._canvas = None
        self._tkGraphic = None

    def draw(self, canvas):

        # Draw the object on the canvas

        self._draw(canvas)

        # Bind any handlers that have already been added

        self._addBoundHandlers()

        # This may have caused a change in the window, so call update to
        # allow the graphics system to process all of the requests.

        autoUpdateManual()

    def _draw(self, canvas):
        self._canvas = canvas
        
    def _addBoundHandlers(self):

        # Setup all of the handlers that have already been added

        for handler in self._eventHandlers:
            self._addHandler(handler)

    def addHandler(self, handler):
        """
        Registers an object to handle events for the object.

        @param handler object: the event handler object.
        @return None
        """
        CheckParms((handler, "handler", EventHandler))

        # Check if this handler has already been added

        if handler in self._eventHandlers:
            print >> sys.stderr, "Event handler already added to Graphical Object:" + str(self)
            return

        self._eventHandlers.append(handler)

        # If there is no graphic, either the object hasn't been drawn yet, or
        # we have a Group object. Either way, we don't want to actually 
        # bind the handler
        
        if self._tkGraphic is None:
            return

        assert not isinstance(self, Group) and self.drawn()
        
        self._addHandler(handler)
        return

#        if self._tkGraphic is None:
#            print "No graphic to add handler to"
#            self._addHandler(handler, self._tkGraphic)
#        else:
#            print "Adding handler to graphic"
        self._addHandler(handler, [self._tkGraphic])

#    def _addHandler(self, handler, graphics):
    def _addHandler(self, handler, graphicalObject = None):
#        eventTypes = handlerEventTypes
        
        if graphicalObject is None:
            graphicalObject = self

        assert self._tkGraphic
        EventManager.bindEventHandler(self, graphicalObject, handler)
#        bindHandler(handler.getEventTypes(), self._canvas, handler, graphics)

    def removeHandler(self, handler):
        CheckParms((handler, "handler", EventHandler))

        if handler not in self._eventHandlers:
            print >> sys.stderr, "Event handler not attached to Graphical Object:" + str(self)
            return

        # May not have been bound. Need to check for that!

        EventManager.unbindEventHandler(self, self, handler)
#        raise GraphicsError("Method unimplemented: removeHandler")
#        raise NotImplementedError

    def drawn(self):
        return self._canvas != None

    def redraw(self):
        if self.drawn():
            # Preserve canvas since undraw will clobber it

            canvas = self._canvas

            self.undraw()
            self.draw(canvas)
        
    def undraw(self):
        if not isinstance(self, Group):
            self._canvas.delete(self._tkGraphic, self)
        self._canvas = None
#        self._tkGraphic = None

    def wait(self):
        """
        Waits for an event to arrive for the object.
        @return Event: an object describing the event.
        """

        # Set this as a non-event driven application (shouldn't use event
        # handlers, etc. Main should return after a window close)

        GS.setEventDriven(False)

        # Flush the standard output so we see any prompts that may have been
        # printed.
        
        sys.stdout.flush()

        if self._tkGraphic is None:
            return self._wait(self._tkGraphic)
        else:
            return self._wait([self._tkGraphic])

    def _wait(self, graphics):

        if not self.drawn():
            raise GraphicsError(
                "Cannot wait on graphical object not on a canvas")

        eventTypes = staticEventTypes

        # Temporary, just make left button work

        eventTypes = ["<ButtonRelease-1>"]

        waiter = WaitHandler()
        EventManager.bindEventHandler(self, self, waiter)
#        bindHandler(eventTypes, self._canvas, waiter, graphics)

        # If there are no graphics, wait on the canvas (this is for the top
        # level layer). Is this the semantics we want for empty layers?

        log("Waiting on an event to arrive", kind = "event")
        event = waiter.wait()
        log("Event arrived", kind = "event")

        EventManager.unbindEventHandler(self, self, waiter)
#        unbindEvents(eventTypes, self._canvas, graphics)

        return event



class Group(GraphicalObject):
    """
    A set of GraphicalObjects that are treated as a single GraphicalObject.
    """
    def __init__(self, center = Point(0, 0)):
        CheckParms((center, "center", Point))
        
        GraphicalObject.__init__(self, center)
        self._contents = []
        self._groupEventHandlers = []

    def updateDepth(self):
        for item in self._contents:
            item.updateDepth()
            
    def move(self, dx, dy = None):
        CheckParms((dx, "dx", (int, float, Point)),
                   (dy, "dy", (int, float, types.NoneType)))

        if isinstance(dx, Point) and dy == None:
            dx, dy = dx.get()

        self._center += Point(dx, dy)

        for graphic in self._contents:
            graphic.move(dx, dy)

    def _draw(self, canvas):

        GraphicalObject._draw(self, canvas)
        
        # Draw all the items in the layer

        for graphicalObject in self._contents:
            graphicalObject.draw(canvas)
            
        autoUpdateManual()

    def _addBoundHandlers(self):
 

        # Setup all of the handlers that have already been added

        for handler in self._groupEventHandlers:
            for graphicalObject in self._contents:
                self._addHandler(handler, graphicalObject)

    def addHandler(self, handler):
        CheckParms((handler, "handler", EventHandler))

        # Check if this handler has already been added

        if handler in self._groupEventHandlers:
            print >> sys.stderr, "Event handler already added to Graphical Object:" + str(self)
            return

        self._groupEventHandlers.append(handler)

        # If the group hasn't been drawn, we can't process the event
        # handlers.

        if not self.drawn():
            return

        # Add the handler to each object in the group

        for graphicalObject in self._contents:
            self._addHandler(handler, graphicalObject)

    def _addHandler(self, handler, graphicalObject):
        EventManager.bindEventHandler(self, graphicalObject, handler)

    def removeHandler(self, handler):
        GraphicalObject.removeHandler(self, handler)
        for graphic in self._contents:
            graphic.removeHandler(handler)

    def undraw(self):

        # Undraw all the items in the layer

        for graphic in self._contents:
            graphic.undraw()

        GraphicalObject.undraw(self)

    def add(self, graphic):
        """
        Adds graphic to the Group.
        @param graphic GraphicalObject: the object to add.
        @return None
        """
        
        CheckParms((graphic, "graphic", GraphicalObject))
        verifyGraphicalObject(graphic)

        graphic.setContainer(self)

        if graphic.drawn():
            raise GraphicsError(str(graphic) + 
                                " already added to a window, not adding again")
        
        # Draw the object if the group is drawn

        if self.drawn():
            graphic.draw(self._getCanvas())

            # Add any handlers already added to the group

            for handler in self._groupEventHandlers:
                self._addHandler(handler, graphic)

        # should this append happen after the draw? If so, we won't issue
        # draw command to the graphic...I think.

        self._contents.append(graphic)

    def remove(self, graphic):
        """
        Removes graphic from the Group.
        @param graphic GraphicalObject: the object to remove.
        @return None
        """        

        CheckParms((graphic, "graphic", GraphicalObject))
        verifyGraphicalObject(graphic)

        graphic.setContainer(None)

        for i in range(len(self._contents)):
            if graphic == self._contents[i]:
                self._contents.pop(i)
                break
            
        if self.drawn():
            graphic.undraw()

class _TrackingCanvas(Tk.Canvas):
    def __init__(self, master = None, **options):
        Tk.Canvas.__init__(self, master, **options)
        self._graphics = []
        self._depths = {}
#        print "Creating a tracking canvas"

    def create_text(self, *args, **kwargs):
        return self._createGraphic(Tk.Canvas.create_text,
                                   self, *args, **kwargs)

    def create_rectangle(self, *args, **kwargs):
        return self._createGraphic(Tk.Canvas.create_rectangle,
                                   self, *args, **kwargs)

    def create_polygon(self, *args, **kwargs):
        return self._createGraphic(Tk.Canvas.create_polygon,
                                   self, *args, **kwargs)

    def create_window(self, *args, **kwargs):
        return self._createGraphic(Tk.Canvas.create_window,
                                   self, *args, **kwargs)

    def create_line(self, *args, **kwargs):
        return self._createGraphic(Tk.Canvas.create_line,
                                   self, *args, **kwargs)

    def create_image(self, *args, **kwargs):
        return self._createGraphic(Tk.Canvas.create_image,
                                   self, *args, **kwargs)
    def delete(self, item, graphicalObject):

        # Set the owner's Tk graphic to None

        graphicalObject.setTkGraphic(None)

        # Delete the item from the list of graphics

        self._graphics.remove(item)

        # Delete the item's depth from the depth table

        del self._depths[item]

        # Remove the item from the canvas

        return Tk.Canvas.delete(self, item)

    def _createGraphic(self, function, *args, **kwargs):

#        print function
        
        # Extract and remove the depth keyword argument

        depth = None
        if "depth" in kwargs:
            depth = kwargs["depth"]
            del kwargs["depth"]

        # Extract and remove the graphicalObject keyword argument

        graphicalObject = None
        if "graphicalObject" in kwargs:
            graphicalObject = kwargs["graphicalObject"]
            del kwargs["graphicalObject"]

        if graphicalObject == None:
            raise GraphicsError("No graphical object for owner")

        # Create the graphic, causing it to be drawn on top

        graphic = function(*args, **kwargs)

        # Register the Tk graphic with the graphical object owner

        graphicalObject.setTkGraphic(graphic)

        # Find all graphics above this one

        loc = self._findDepthIndex(depth)

        # Raise all graphics above this one
        self._raiseAbove(self._graphics[:loc])

        # Record this graphic and its depth

        self._graphics.insert(loc, graphic)
        self._depths[graphic] = depth

        return graphic

    def printTable(self):
        print >> Console, "Drawing order"
        for item in self._graphics:
            print >> Console, "Item:", item, "depth =", self._depths[item]

    def _findDepthIndex(self, depth):

        # No graphics? Insert at position zero

        if len(self._graphics) == 0:
            return 0

        # Otherwise, find the index of the first item greater than this depth

        for i in range(len(self._graphics)):
            if self._depths[self._graphics[i]] > depth:
                return i

        # This item will be at the bottom of the drawing order

        return len(self._graphics)

    def _raiseAbove(self, items):

        # Tag each item

        for item in items:
            self.itemconfig(item, tag = "aboveMe")

        # Raise all tagged items in one operation (this is faster)

        self.tag_raise("aboveMe")

        # Remove the tag

        self.dtag("aboveMe")

    def setDepth(self, item, depth):

#        self.printTable()
        # Remove the graphic from the graphics list

        self._graphics.remove(item)
        
        # Find the new location for this graphic

        loc = self._findDepthIndex(depth)

        # Raise the graphics

        self.tag_raise(item)

        # Raise all graphics above this one

        self._raiseAbove(self._graphics[:loc])

        # Record this graphic and its depth

        self._graphics.insert(loc, item)
        self._depths[item] = depth
#        self.printTable()

def markCanvasDirty(invokedMethod):
    def wrappedCall(*args, **kwargs):
        global CanvasDirty
        result = invokedMethod(*args, **kwargs)
        CanvasDirty = True
        return result
    return wrappedCall

#TrackingCanvas = _TrackingCanvas
TrackingCanvas = classWrap(_TrackingCanvas, markCanvasDirty)

XWindowDisplays = {}

FrameMap = {}
class Window(AutoUpdaterObject):
    """
    Creates a window on the display in which to draw graphics
    """

    # Keep a class variable to keep track of all instances

#    _windows = set()

    # identify the first window so we know how to create it.

#    _firstWindow = True

    # pylint: disable=W0231
    # (base class __init__ not called)
    def __init__(self, width = 400, height = 400, background = 'white',
                 name = None, location = Point(0, 0), remote = False,
                 quitButton = True, displayMessageBox = True):
        """
        The constructor.

        @param width int:     width of the window in pixels.
        @param height int:    height of the window in pixels.
        @param background str: background color of the window.
        @param name str:       title of the window.
        @param location Point: location of window on computer display
        @param remote bool/str:     name of a computer display
        @param quitButton:     add a quit button to the window
        @param displayMessageBox bool:  add a message line to the window
        """

#        remote = False
        CheckParms((width, "width", number), (height, number), (background, (str, tuple)),
                   (name, "name", (str, types.NoneType)),
                   (remote, "remote", (bool, str)),
                   (location, "location", Point))

        if GS is None:
            raise GraphicsError(
                "Window cannot be created before first function is invoked")

        self._open = True
        self._group = Group()
        self._width = width
        self._height = height
        self._name = name
        self._backgroundColorName = background
        self._background = colorLookup(background)
        self._quitButton = quitButton

        screen = None

        if remote == True:
            remote = "true"
     
        if remote:
            if not remote in XWindowDisplays:

                print >> Console, "Attempting to setup remote display for " + remote + "."
                print >> Console, "Be sure to allow it by issuing the following command on the remote computer:"
                screen = XWindowDisplays[remote] = setupXDisplay(remote)
                print >> Console, "Remote display successfully configured!"
             
        self._screen = screen

        # Add the current instance to the list of instances

#        Window._windows.add(self)

        # If no window has been created, use the toplevel window provided.

        self._toplevel = GS.createWindow(self, self._width, self._height,
                                         location.getX(), location.getY(),
                                         self._name, self._screen)

        # Make a Tk Frame to hold the canvas

        self._frame = Tk.Frame(self._toplevel, width = self._width,
                                   height = self._height, bd = 0,
                                   relief = Tk.FLAT)
        self._frame.pack()

        # Make a Tk Canvas to hold all the graphics

        self._canvas = TrackingCanvas(self._frame, width = self._width,
                                      highlightthickness = 0,
                                      background = self._background,
                                      height = self._height, bd = 0,
                                      relief = Tk.FLAT)
        self._canvas.pack()

        if displayMessageBox:

            # Add a message window

            self._messageBox = Tk.Entry(self._frame, state = "readonly",
                                        relief = Tk.FLAT)
            self._messageBox.config(highlightcolor = 
                                    self._messageBox.cget("background"))

#            self._messageBox.pack(side=Tk.LEFT)
            self._messageBox.pack(side=Tk.LEFT, fill = Tk.X, expand = True)

            # Redirect print to the message box

            overrideStandardOutput(self)

            # Redirect raw_input to a dialog box

            overrideStandardInput()

        self.addQuitButton()

        overrideStandardError()

        # Make the canvas have the focus so we can get key events. If it
        # ever loses the focus, we'll have to reset this!
        
        self._canvas.focus_set()

        FrameMap[self._canvas] = self._frame

        # Add the background watermark

#        watermark = CreateWatermark(self._width, self._height)
#        watermark.setDepth(100000)
#        self.add(watermark)
        
        self._group.draw(self._canvas)
        
    def addQuitButton(self):

        # Add a quit button at the bottom of the window if necessary

        if self._quitButton:
            def quitCommand():
                global QuitButtonPressed
#                print >> Console, "Application closed by user"
                QuitButtonPressed = True
                self._canvas.event_generate('<ButtonRelease-1>', x=0, y=0)

                self._frame.quit()

            button = Tk.Button(self._frame, text = "Quit", background = "Red", 
                               command = quitCommand)
            button.pack(side = Tk.RIGHT)


    def setMessageBoxText(self, text):
        """
        Sets the text of the message in the message box.

        @param text string: the text to be displayed in the message box.
        @return None
        """

        # Enable the message box to be changed

        self._messageBox.config(state = Tk.NORMAL)

        # Clear it

        self._messageBox.delete(0, Tk.END)

        # Set the new text

        self._messageBox.insert(0, text)

        # Disable the box

        self._messageBox.config(state = "readonly")

        # Update the screen

        autoUpdate()

    # raiseException is used to raise an exception in the graphics system
    # for testing purposes (To test exception processing).

    def raiseException(self):
        raise Exception

    # pylint: enable=W0231
    # (base class __init__ not called)

    def close(self):
        """
        Removes the window from the display.
        @return None
        """

        if not self._open:
            print >> Console, "Window is not open"
            return

        self._open = False
        self._group.undraw()


        GS.destroyWindow(self._toplevel)

        # Needs to be done in the final window

        if not GS.windowsOpen():
            reinstateStandardOutput()
            reinstateStandardError()

        autoUpdateManual()

#        self._toplevel.withdraw()

#        Window._windows.remove(self)

#        if not Window.anyWindowsOpen():
#            log("No more windows are open")
#            GS.windowsOpen = False

#            GS.shutdown()
        
    def setBackgroundColor(self, color):
        """
        Sets the background color of the window to color (str).
        @param color str/None/rgb tuple: color
        @return None
        """

        CheckParms((color, "color", (str, tuple)))
        self._backgroundColorName = color
        self._background = colorLookup(color)
        self._canvas.config(bg = self._background)

    def setWidth(self, width):
        """
        Sets the width of the window.

        @param width int: the width of the window
        @return None
        """

        CheckParms((width, "width", number))

        self._width = width
        self._canvas.config(width = self._width)

    def setHeight(self, height):
        """
        Sets the height of the window.
        @param height int: the height of the window
        @return None
        """
        CheckParms((height, "height", number))

        self._height = height
        self._canvas.config(height = self._height)

    def setTitle(self, name):
        """
        Sets the title of the window.

        @param name str: the window title.
        @return None
        """
        CheckParms((name, "name", str))

        self._name = name
        self._toplevel.title(self._name)

    def add(self, graphic):
        """
        Adds a graphic to the Window.
        @param graphic GraphicalObject: the object to add.
        @return None
        """
        CheckParms((graphic, "graphic", GraphicalObject))
        self._group.add(graphic)

    def remove(self, graphic):
        """
        Removes graphic from the Window.
        @param graphic GraphicalObject: the object to add.
        @return None
        """        

        CheckParms((graphic, "graphic", GraphicalObject))
        self._group.remove(graphic)
        
    def wait(self, prompt = "Please click the mouse"):
        """
        Waits for an event to arrive for the window.
        @param prompt str: a string to be written to the text window
        @return Event: an object describing the event.
        """
        import os
        if "NOWAIT" in os.environ:
            
            if prompt != None:
                print prompt + "(sythetic wait)"
            else:
                print "(sythetic wait)"

            sleep(.1)
            print ""
            return Event("mouse release", None, Point(0, 0), Point(0, 0), None,
                         "left")

        if prompt != None:
            print prompt
        result = self._group.wait()

        # Used to clear the status line after we have printed the prompt

        if prompt != None:
            print ""

        if QuitButtonPressed:
            raise UserPressedQuit

        return result

    def addHandler(self, handler):
        """
        Registers an object to handle events for the window.

        @param handler object: the event handler object.
        @return None
        """
        CheckParms((handler, "handler", EventHandler))

        EventManager.bindEventHandler(self, self, handler)
        
#        bindHandler(handler.getEventTypes(), self._canvas, handler)
#        self._group.addHandler(handler)

    def drawn(self):

        # Hack: Used for event handling

        return self._open

    def getTkGraphic(self):

        # Hack: Used for event handling

        return None

    def _getCanvas(self):

        # Hack: Used for event handling

        return self._canvas

    def __str__(self):
        return "Window(%d x %d)" % (self._width, self._height)

class Line(GraphicalObject):
    """
    A line segment that can be drawn in a window.
    """

    def __init__(self, start, end):
        """
        The constructor.

        @param start Point: the starting point of the line segment.
        @param end Point: the ending point of the line segment.
        """
        
        CheckParms((start, Point), (end, Point))

        center = (start + end) / 2
        GraphicalObject.__init__(self, center)
        self._start = start
        self._end = end
        self._line = None

        # These get added on to the parameter list when creating the object

        self._tkAttr["width"] = 1
        self._tkAttr["fill"] = "black"


    def draw(self, canvas):
        self._line = canvas.create_line(self._start.getX(), self._start.getY(),
                                        self._end.getX(), self._end.getY(),
                                        self._tkAttr,
                                        graphicalObject = self,
                                        depth = self.getCanonicalDepth())
#        self.setTkGraphic(self._line)
        GraphicalObject.draw(self, canvas)

    def setLineColor(self, color):
        """
        Sets the color of the line.

        @param color str/rgb tuple: the color of the line.
        @return None
        """
        CheckParms((color, "color", (str, tuple)))

        self._tkAttr["fill"] = colorLookup(color)
        self.redraw()

    def setLineWidth(self, width):
        """
        Sets the width of the line.

        @param width float: the width of the line (in pixels).
        @return None
        """
        CheckParms((width, "width", number))

        self._tkAttr["width"] = width
        self.redraw()

class Path(GraphicalObject):   #AERC 8/14
#class Path(Morphable):
    """
    A multi-segment line that can drawn in a window.
    """
    def __init__(self, *points):
        """
        @param points list: a list of Points defining the path.
        """
        CheckParms((points, "points", sequence))

        self._lineColor = "black"
        self._lineWidth = 1
        self._points = points
        self._line = None
        center = Point(0, 0)
        for pt in self._points:
            CheckParms((pt, "pt", Point))
            center += pt
        center /= len(self._points)
        GraphicalObject.__init__(self, center)   #AERC 8/14
        #Morphable.__init__(self, *points)

    def draw(self, canvas):
        pts = []
        for pt in self._points:
            pts += [pt.getX(), pt.getY()]
        self._line = canvas.create_line(fill = self._lineColor,
                                        width = self._lineWidth,
                                        graphicalObject = self,
                                        depth = self.getCanonicalDepth(), *pts)

#        self.setTkGraphic(self._line)
        GraphicalObject.draw(self, canvas)

    def setLineColor(self, color):
        """
        Sets the color of the line.

        @param color str/rgb tuple: the color of the line.
        @return None
        """
        CheckParms((color, "color", (str, tuple)))

        self._lineColorName = color
        self._lineColor = colorLookup(color)
        self.redraw()

    def setLineWidth(self, width):
        """
        Sets the width of the line.

        @param width float: the width of the line (in pixels).
        @return None
        """
        CheckParms((width, "width", number))

        self._lineWidth = width
        self.redraw()

class Text(GraphicalObject):
    """
    A string of text that can be drawn in window.
    """
    
    def __init__(self, textString, center = Point(0, 0), fontSize = 12,
                 fontFamily = "Helvetica"):
        """
        The constructor.

        @param textString str: the string to be displayed
        @param center Point: the center of the text
        @param fontSize int: the size of the font in points.
        @param fontFamily str: the name of the font family
        """
        CheckParms((textString, "textString", str), (center, "center", Point),
                   (fontSize, "fontSize", int), 
                   (fontFamily, "fontFamily", str))

        GraphicalObject.__init__(self, center)
        self._textString = textString
        self._family = fontFamily
        self._size = fontSize
        self._weight = tkFont.BOLD
        self._color = "black"
        self._text = None

    def setTextString(self, textString):
        """
        Sets the text string that is displayed

        @param textString str: the text to display
        @return None
        """

        CheckParms((textString, "textString", str))

        self._textString = textString
        self.redraw()

    def setTextColor(self, color):
        """
        Sets the color of the text.

        @param color str/rgb tuple: the color of the text.
        @return None
        """
        CheckParms((color, "color", (str, tuple)))

        self._colorName = color
        self._color = colorLookup(color)
        self.redraw()

    def setFont(self, fontSize = 12, fontFamily = "Helvetica"):
        """
        Sets the font of the text.

        @param fontSize int: the size of the font in points.
        @param fontFamily str: the name of the font family.
        @return None
        """
        CheckParms((fontSize, "fontSize", int), (fontFamily, str))

        self._family = fontFamily
        self._size = fontSize
        self._weight = tkFont.BOLD
        self.redraw()

    def draw(self, canvas):
        x, y = self._center.get()

        # Font can't be created until we draw this because the X connection
        # has to be up (we have to have a window)

        self._font = tkFont.Font(family = self._family, size = self._size,
                                 weight = self._weight)

        self._text = canvas.create_text(x, y, text = self._textString,
                                        fill = self._color,
                                        font = self._font,
                                        graphicalObject = self,
                                        depth = self.getCanonicalDepth())

#        self.setTkGraphic(self._text)
        GraphicalObject.draw(self, canvas)

    def _clone(self):
        GraphicalObject._clone(self)
        self._text = None


class TextArea(GraphicalObject):
    def __init__(self, width = 80, height = 2, center = Point(0, 0)):
        GraphicalObject.__init__(self, center)
        self._textString = ""
        self._width = width
        self._height = height

    def setTextString(self, textString):
        self._textString = textString
        if self.drawn():
            self._text.delete(1.0, Tk.END)
            self._text.insert(Tk.END, self._textString)
        
        # No need to do this redraw because this widget will update itself
                        
        #self.redraw()

    def appendTextString(self, textString):
        self.setTextString(self._textString + textString)
        
    def draw(self, canvas):
        self._text = Tk.Text(width = self._width, height = self._height)

        self._text.delete(1.0, Tk.END)
        self._text.insert(Tk.END, self._textString)

        self._window = canvas.create_window(self._center.getX(),
                                            self._center.getY(),
                                            window = self._text,
                                            graphicalObject = self,
                                            depth = self.getCanonicalDepth())

        GraphicalObject.draw(self, canvas)
#        self.setTkGraphic(self._window)

# Other possible choices:

# Point
# Ellipse
# Line
# Image
# Bitmap?

class Fillable(GraphicalObject):
    """
    An abstract class providing fillable graphical objects.
    
    You don't create objects of this class, instead, other classes depend
    on this class to provide their funcationality.
    """
    def __init__(self, *points):
        CheckParms((points, "points", sequence))

        sumx = 0
        sumy = 0
        for point in points:
            CheckParms((point, "point", Point))
            verifyPoint(point)
            sumx += point.getX()
            sumy += point.getY()

        if len(points) != 0:
            center = Point(sumx / len(points), sumy / len(points))
        else:
            center = Point(0, 0)

        GraphicalObject.__init__(self, center)
        
        self._borderColorName = "black"
        self._borderColor = colorLookup("black")
        self._fillColor = ""
        self._fillColorName = None
#        print "Setting fill color to    ", self._fillColor
#        print "Setting fill color nameto", self._fillColorName

        self._borderWidth = 1
        self._points = tuple(points)
        self._polygon = None
        self._pivot = center
        
    def getBorderColor(self):
        """
        Returns the border color.
        
        @return str: the color of the border.
        """
        return self._borderColorName

    def getFillColor(self):
        """
        Returns the fill color.
        @return str: the fill color.
        """
        return self._fillColorName

    def getBorderWidth(self):
        """
        Returns the border width.
        @return int: the border width.
        """
        return self._borderWidth

    def setBorderColor(self, color):
        """
        Sets the border color.
        @param color str/rgb tuple: color
        @return None
        """
        CheckParms((color, "color", (str, tuple)))

        self._borderColorName = color
        self._borderColor = colorLookup(color)
        self._setGraphicAttribute(outline = self._borderColor)

    def setFillColor(self, color):
        """
        Sets the fill color.
        @param color str/None/rgb tuple: color
        @return None
        """
        CheckParms((color, "color", (str, tuple, type(None))))

        if color == None:
            self._fillColor = ""
        else:
            self._fillColorName = color
            self._fillColor = colorLookup(color)
#        print "Setting fill color to    ", self._fillColor
#        print "Setting fill color nameto", self._fillColorName
        self._setGraphicAttribute(fill = self._fillColor)

    def setBorderWidth(self, width):
        """
        Sets the border width.
        @param width int: the border width in pixels.
        @return None
        """
        CheckParms((width, "width", number))

        self._borderWidth = width
        self._setGraphicAttribute(width = self._borderWidth)

# Probably don't need this?
#    def drawn(self):
#        raise NotImplementedError

    def _setGraphicAttribute(self, **kwargs):
        if self.drawn():
            canvas = self._getCanvas()
            graphic = self.getTkGraphic()
            canvas.itemconfig(graphic, **kwargs)


    def draw(self, canvas):
        coords = []
        for point in self._points:
            coords.append(point.get())
            
        # You can't have a borderWidth of 0. Instead, you have to set
        # the border color (outline) to the empty string. Then, it won't
        # draw the border at all.

        width = self.getBorderWidth()
        if width == 0:
            outline = ""
        else:
            outline = self._borderColor

        self._polygon = canvas.create_polygon(coords,
                                              joinstyle = Tk.MITER,
                                              fill = self._fillColor,
                                              width = width,
                                              outline = outline,
                                              graphicalObject = self,
                                              depth = self.getCanonicalDepth())

#        self.setTkGraphic(self._polygon)
        GraphicalObject.draw(self, canvas)

    def _clone(self):
        GraphicalObject._clone(self)
        self._polygon = None

    def move(self, dx, dy = None):

        CheckParms((dx, "dx", (int, float, Point)),
                   (dy, "dy", (int, float, types.NoneType)))

        if isinstance(dx, Point) and dy == None:
            dx, dy = dx.get()

        # Create a translation transformation to compute the point movements

        center = self._center
        transform = Transformation()
        transform.translate(dx, dy)
        self._transform(transform, False)
        self._center = center

        GraphicalObject.move(self, dx, dy)

    def _transform(self, transform, redraw = True):
        # Create a new set of translated points

        newPoints = list(self._points)
        for i in range(len(self._points)):
            newPoints[i] = transform * self._points[i]
        self._points = tuple(newPoints)
        self._center = transform * self._center

        # Redraw the object with the new points

        if redraw:
            self.redraw()

    def getPivot(self):
        """
        Gets the pivot point of the object.

        @return Point: the object's pivot.
        """
        return self._pivot

    def setPivot(self, pivot):
        """
        Sets the pivot point of the object.

        @param pivot Point: the pivot point.
        @return None
        """
        CheckParms((pivot, "pivot", Point))

        self._pivot = pivot
    
    def rotate(self, degrees):
        """
        Rotates the object about its pivot point.

        @param degrees float: the number of degrees of clockwise rotation.
        @return None
        """
        
        CheckParms((degrees, "degrees", number))

        # Create a rotation transformation to compute the point movements

        transform = Transformation()
        transform.rotateDegrees(degrees, self.getPivot())
        self._transform(transform)

    def scale(self, factor):
        """
        Scales the object around its pivot point.

        @param factor float: the scaling factor (2 doubles the size)
        @return None
        """
        CheckParms((factor, "factor", number))

        transform = Transformation()
        transform.scale(factor, factor, self.getPivot())
        self._transform(transform)

    def flip(self, angle = 0):
        """
        Flips object about an angle.

        @param angle float: the angle of the axis of flip.
        @return None
        """
        CheckParms((angle, "angle", number))

        transform = Transformation()
        transform.rotateDegrees(-angle, self.getPivot())
        transform.scale(-1, 1, self.getPivot())
        transform.rotateDegrees(angle, self.getPivot())
        self._transform(transform)

class Morphable(Fillable):
    """
    An abstract class providing morphable (stretch and shear), fillable,
    graphical objects.
    
    You don't create objects of this class, instead, other classes depend
    on this class to provide their funcationality.
    """

    def __init__(self, *points):
        Fillable.__init__(self, *points)

    def stretch(self, xFactor, yFactor, angle = 0):
        """
        Stretches an object around its pivot point.

        @param xFactor float: the x scaling factor.
        @param yFactor float: the y scaling factor.
        @param angle float: the angle x-axis stretch.
        @return None
        """

        # These angles may be reversed. Determine correct direction

        CheckParms((xFactor, "xFactor", number), (yFactor, "yFactor", number),
                   (angle, "angle", number))

        transform = Transformation()
        transform.rotateDegrees(-angle, self.getPivot())
        transform.scale(xFactor, yFactor, self.getPivot())
        transform.rotateDegrees(angle, self.getPivot())
        self._transform(transform)

    def shear(self, shear, angle = 0):
        """
        Shears an object around its pivot point.

        @param shear float: pixels of shear per pixel above the pivot point
        @param angle float: the axis about which to shear.
        @return None
        """
        CheckParms((shear, "shear", number), (angle, "angle", number))

        transform = Transformation()
        transform.rotateDegrees(-angle, self.getPivot())
        transform.shear(-shear, self.getPivot())
        transform.rotateDegrees(angle, self.getPivot())
        self._transform(transform)

class Circle(Fillable):
    """
    A circle that can be drawn in a window.
    """
    def __init__(self, radius, center = Point(0, 0)):
        """
        @param radius int: the radius of the circle.
        @param center Point: the location of the center of the circle
        """
        CheckParms((radius, "radius", number), (center, "center", Point))

        self._center = center
        points = []
        precision = 1
        for angle in range(0, 360 * precision):
            rangle = angle / precision * math.pi / 180.0
            points.append(Point(radius * math.cos(rangle) +
                                self._center.getX(),
                                radius * math.sin(rangle) +
                                self._center.getY()))
        Fillable.__init__(self, *points)

    def setRadius(self, radius):
        """
        Sets the radius of the circle.
        @param radius int: the radius of the circle (in pixels).
        @return None
        """

        CheckParms((radius, "radius", number))
        points = []
        precision = 1
        for angle in range(0, 360 * precision):
            rangle = angle / precision * math.pi / 180.0
            points.append(Point(radius * math.cos(rangle) +
                                self._center.getX(),
                                radius * math.sin(rangle) +
                                self._center.getY()))
        self._points = tuple(points)
        self.redraw()

class Square(Fillable):
    """
    A square that can be drawn in a window.
    """
    def __init__(self, sideLength, center = Point(0, 0)):
        """
        @param sideLength int: the length of a side (in pixels).
        @param center Point: the location of the center.
        """
        CheckParms((sideLength, "sideLength", number),
                   (center, "center", Point))
        ul = center - Point(sideLength / 2, sideLength / 2)
        lr = ul + Point(sideLength, sideLength)
        ll = ul + Point(0, sideLength)
        ur = ul + Point(sideLength, 0)
        Fillable.__init__(self, ul, ur, lr, ll)

class Polygon(Morphable):
    """
    A polygon than can be drawn in a window.
    """

    def __init__(self, *points):
        """
        @param points list: a list of points defining the polygon
        """
        CheckParms((points, "points", sequence))
        for point in points:
            CheckParms((point, "point", Point))

        Morphable.__init__(self, *points)

    def clearPoints(self):
        """
        Erases all points from the polygon.
        @return None
        """
        self._points = tuple()
        self.redraw()

    def deletePoints(self, index = -1):
        """
        Deletes a point from the polygon.
        @param index int: the index of the point to delete.
        @return None
        """

        # assert index is in range

        CheckParms((index, "index", int))

        pts = list(self._points)
        pts.pop(index)
        self._points = tuple(pts)
        self.redraw()

    def getNumberOfPoints(self):
        return len(self._points)

    def getPoint(self, index):
        CheckParms((index, "index", int))

        return self._points[index]
    
    def getPoints(self):
        return copy.deepcopy(self._points)

    def setPoint(self, point, index = -1):
        CheckParms((point, "point", Point), (index, "index", int))

        # assert index is in range
        self._points[index] = point
        self.redraw()

    def addPoint(self, point, index = None):
        CheckParms((point, "point", Point),
                   (index, "index", (int, types.NoneType)))

        if index == None:
            index = len(self._points)
            
        points = list(self._points)
        points.insert(index - 1, point)
        self._points = tuple(points)
        self.redraw()


class Rectangle(Morphable):
    """
    A rectangle that can be drawn in a window.
    """
    def __init__(self, width, height, center = Point(0, 0)):
        """
        @param width int: width of the rectangle (in pixels).
        @param height int: height of the rectangle (in pixels).
        @param center Point: the center of the rectangle.
        """
        CheckParms((width, "width", number), (height, "height", number),
                   (center, "center", Point))

        ul = center - Point(width / 2, height / 2)
        lr = center + Point(width / 2, height / 2)

        # Need to be careful here that the corners have matching X's and Y's

        ll = Point(ul.getX(), lr.getY())
        ur = Point(lr.getX(), ul.getY())
#        ll = ul + Point(0, height)
#        ur = ul + Point(width, 0)
        Morphable.__init__(self, ul, ur, lr, ll)

class Ellipse1(Square):
    def __init__(self, xrad, yrad, point):
        Square.__init__(self, xrad, point)


class Button(GraphicalObject):
    def __init__(self, text = "", center = Point(0, 0), command = None):
        GraphicalObject.__init__(self, center)
        self._text = text
        self._command = command
        self._canvas = None
        self._button = None
        self._window = None

    def draw(self, canvas):
        frame = FrameMap[canvas]

        if self._command == None:
            self._button = Tk.Button(canvas, text = self._text,
                                     command = frame.quit)
            self._button.pack()
        else:
            self._button = Tk.Button(canvas, text = self._text,
                                     command = self._command)

        # Create a window on the canvas to hold the button.

#        print self._button
        self._window = canvas.create_window(self._center.getX(),
                                            self._center.getY(),
                                            window = self._button,
                                            graphicalObject = self,
                                            depth = self.getCanonicalDepth())
        GraphicalObject.draw(self, canvas)
#        self.setTkGraphic(self._window)

        # If we delete one of these, we may have to worry about the button?

    def _clone(self):
        GraphicalObject._clone(self)
        self._canvas = None
        self._button = None
        self._window = None

class Image(GraphicalObject):
    """
    A raster graphics image that can be drawn in a window
    """
    def __init__(self, filenameOrWidth = None, centerOrHeight = Point(0, 0)):
        """
        The constructor.

        Example uses:

        img = Image("balloons.jpg")  # An image loaded from a file, centered at (0, 0)

        img = Image(300, 400)        # An empty image 300x400 pixels in size

        @param filenameOrWidth str/int: the name of the file containing an
        image (typically a jpeg) or the width of a blank image
        @param centerOrHeight Point/int: the location of the center of the
        image or the height of a blank image
        """

        CheckParms((filenameOrWidth, "filenameOrWidth",
                    (str, int, types.NoneType)),
                   (centerOrHeight, "centerOrHeight", (int, Point)))

        # Check if this is the form: Image(width, height) for building
        # blank images

        if (isinstance(filenameOrWidth, int) and
            isinstance(centerOrHeight, int)):
            width = filenameOrWidth
            height = centerOrHeight
            center = Point(0, 0)
            filename = None
        else:
            filename = filenameOrWidth
            center = centerOrHeight
            
        GraphicalObject.__init__(self, center)

        # Check if this is a blank image

        if filename == None:
            self._pilImage = PILimage.new("RGBA",
                                          (width, height)).convert("RGBA")

        else:
            TypeCheck(filename, None, str)

            # PIL image documentation:
            # http://www.pythonware.com/library/pil/handbook/image.htm
            
            # PIL image open is lazy. This forces it so the student gets the
            # error message at the right time.
        
            #        self.pilImage = self._pilImage.rotate(45)

            self._filename = filename
            self._pilImage = PILimage.open(self._filename).convert("RGBA")
            self._pilImage.load()

        self._image = None

        # We must keep a reference to this image object, or the garbage
        # collector can collect it even if it is currently being displayed.
        # This may be an issue if the student doesn't keep a copy of this
        # object around! (maybe we do?)

        # Helpful documentation:
        # http://epydoc.sourceforge.net/stdlib/Tkinter.PhotoImage-class.html

#        self._photoImage = Tk.PhotoImage(file = self._filename)
        self._photoImage = None

    def draw(self, canvas):
        log("Creating a new PhotoImage (draw)")
        self._photoImage = ImageTk.PhotoImage(self._pilImage)
        self._image = canvas.create_image(self._center.getX(),
                                          self._center.getY(),
                                          image = self._photoImage,
                                          graphicalObject = self,
                                          depth = self.getCanonicalDepth())
        GraphicalObject.draw(self, canvas)
#        self.setTkGraphic(self._image)

    def undraw(self):
        GraphicalObject.undraw(self)
        self._photoImage = None

    def size(self):
        """
        Returns the size, in pixels, of the image.

        @return tuple: the width and height
        """
        return self._pilImage.size

    def rotate(self, degrees):
        """
        Mutate an image by rotating.


        @param degrees float: the angle to rotate the image.
        @return None
        """
        self._pilImage = self._pilImage.rotate(degrees)
        self.redraw()

    def getPixels(self):
        """
        Returns the pixels in the image.

        @return list: the pixels (4-tuples: (R, G, B, A))
        """
        return list(self._pilImage.getdata())

    def setPixels(self, pixels):
        """
        Mutate an image by changing all the pixels.

        @param pixels list: the pixels (4-tuples: (R, G, B, A))
        @return None
        """
        CheckParms((pixels, "pixels", list))
        self._pilImage.putdata(pixels)
        self._pilImage = self._pilImage.convert("RGBA")
        self.redraw()

    def crop(self, top, bottom, left, right):
        """
        Mutates an image by cropping.

        @param top int: number of pixels to trim off the top.
        @param bottom int: number of pixels to trim off the bottom.
        @param left int: number of pixels to trim off the left.
        @param right int: number of pixels to trim off the right.
        @return None
        """
        CheckParms((top, "top", int), (bottom, int), (left, "left", int),
                   (right, "right", int))

        width, height = self.size()
        self._pilImage = self._pilImage.crop((left, top, width - right,
                                              height - bottom))
        self.redraw()

    def save(self, filename):
        """
        Saves the image to a file.

        @param filename str: the name of the file.
        @return None
        """
        CheckParms((filename, "filename", str))
        self._pilImage.save(filename)

    def resize(self, width, height):
        """
        Mutates an image by resizing.

        @param width int: the desired width, in pixels
        @param height int: the desired height, in pixels
        @return None
        """

        CheckParms((width, "width", number), (height, "height", number))
        self._pilImage = self._pilImage.resize((width, height))
        self.redraw()

    def _clone(self):
        GraphicalObject._clone(self)
        self._pilImage = self._pilImage.copy()
        self._photoImage = None
        self._image = None

class Dot(Circle):
    def __init__(self, center, radius = 4):
        Circle.__init__(self, radius / 2, center)
        self.setFillColor("Black")

def snapPoint(location, gridXSize = 20, gridYSize = 20):
    x, y = location.get()

    if x % gridXSize > gridXSize / 2:
        x = x + gridXSize - x % gridXSize
    else:
        x -= x % gridXSize

    if y % gridYSize > gridYSize / 2:
        y = y + gridYSize - y % gridYSize
    else:
        y -= y % gridYSize

    if x < 40 or x > 220:
        return None

    if y < 40 or y > 220:
        return None

    return Point(x, y)

class Tile(Group, EventHandler):

    def __init__(self, width = 20, height = 20, center = Point(0, 0), mouseButton = "Left", alwaysSnap = False, content = Text("No Content"), window = None):
        EventHandler.__init__(self)
        Group.__init__(self)
        
        self._content = content

        # Create a group to hold everything so we can manage the depths

        self._group = Group()
        self.add(self._group)

        # Add all the items to the group

        self._border = Rectangle(width, height, center)
        self._group.add(self._border)
        self._border.setDepth(2)
        self._group.add(self._content)
        self._content.setDepth(1)

        self._disableCover = Image(1, 1)
#        self._disableCover.setPixels([(255, 255, 255, 125)])
        self._disableCover.setPixels([(0, 0, 0, 50)])
        self._disableCover.resize(width, height)
        self._group.add(self._disableCover)
        self._disableCover.setDepth(3)
        
        self._border.setFillColor("Yellow")
        self._disabled = False
        self._lastLocation = None
        self._dragCenterOffset = None
        self._alwaysSnap = alwaysSnap
        self._originalCenter = None
        self._button = mouseButton
        self.addHandler(self)

        self._window = window
        self._snappoint = Dot(Point(0, 0))
        self.add(self._snappoint)

    def handleMousePress(self, button, loc):

        # Check if this is the mouse button that activates dragging

        if button != self._button:
            return

        # Don't process event if button is disabled

        if self._disabled:
            return

        # Mark the clicked location

#        self._clickLocation = Dot(loc)
#        self.add(self._clickLocation)

        # Record the last location and its offset from the center

        self._originalCenter = self.getCenter()
        self._lastLocation = loc

        self._dragCenterOffset = loc - self.getCenter()
        print >> Console, self._dragCenterOffset
        self._snappoint.moveTo(Point(0, 0))

    def handleMouseRelease(self, button, loc):

        # Check if this is the mouse button that ends dragging

        if button != "Left":
            return

        # Don't process event if button is disabled

        if self._disabled:
            return

        # If the object is always snapped, figure the offset and move it

        if self._alwaysSnap:
            print >> Console, self._dragCenterOffset
            newCenter = snapPoint(loc - self._dragCenterOffset)
            if newCenter == None:
                self.moveTo(self._originalCenter)
                self._snappoint.moveTo(Point(0, 0))
            else:
                self.move(newCenter - self.getCenter())
                self._snappoint.moveTo(newCenter)
            
        # Otherwise, move from the last center

        else:

            newCenter = snapPoint(self.getCenter())
            if newCenter == None:
                self.moveTo(self._originalCenter)
                self._snappoint.moveTo(Point(0, 0))
            else:
                self.move(newCenter - self.getCenter())
                self._snappoint.moveTo(newCenter)

        self._lastLocation = None
        self._dragCenterOffset = None
#        self.remove(self._clickLocation)

    def handleMouseDrag(self, button, loc):

        # Check if this is the mouse button for dragging

        if button != self._button:
            return

        # Don't process event if button is disabled

        if self._disabled:
            return

        # If the object is always snapped, snap the center on each drag

        if self._alwaysSnap:
            newCenter = snapPoint(loc - self._dragCenterOffset)
            if newCenter == None:
                self.moveTo(self._originalCenter)
                self._snappoint.moveTo(Point(0, 0))
            else:
                self.move(newCenter - self.getCenter())
                self._snappoint.moveTo(newCenter)

        # Otherwise, just move the object in relation to the drag

        else:
            self.move(loc - self._lastLocation)
            self._lastLocation = loc
            newCenter = snapPoint(loc - self._dragCenterOffset)
            if newCenter != None:
                self._snappoint.moveTo(newCenter)
            else:
                self._snappoint.moveTo(Point(0, 0))

    def handleMouseEnter(self, loc):
        # Don't process event if button is disabled

        if self._disabled:
            return
        self._border.setBorderWidth(2)
        self._border.setBorderColor("Blue")

    def handleMouseLeave(self, loc):
        # Don't process event if button is disabled

        if self._disabled:
            return
        self._border.setBorderWidth(1)
        self._border.setBorderColor("Black")

    def disable(self):
        self._disableCover.setDepth(0)
        self._disabled = True
        print "disabled"

    def enable(self):
        self._disableCover.setDepth(3)
        self._disabled = False
        print "enabled"

def CreateWatermark(winWidth, winHeight):

    # Load the watermark image

    watermark = Image("/home/mbailey/graphics/src/background.gif", 
                 Point(winWidth, winHeight) / 2)

    width, height = watermark.size()

    # Resize it to fit in the window--if it is too large

    if winWidth < width or winHeight < height:
        widthRatio = winWidth / float(width)
        heightRatio = winHeight / float(height)

        # Figure out which aspect is too small

        if widthRatio < heightRatio:
            ratio = widthRatio
        else:
            ratio = heightRatio

        # Resize while maintaining aspect ratio

        watermark.resize(int(width * ratio), int(height * ratio))

    # lighten the image so it is a watermark

    pix = watermark.getPixels()

    for i in range(len(pix)):
        pix[i] = (pix[i][0], pix[i][1], pix[i][2], pix[i][3]/2)
    watermark.setPixels(pix)

    return watermark

def WarningDialog(msg):
    """
    Displays a warning dialog box

    @param msg str : the message to display
    @return None

    \ingroup Functions
    """
    return tkMessageBox.showwarning("Warning", msg)

def MessageDialog(msg):
    """
    Displays a message dialog box

    @param msg str : the message to display
    @return None

    \ingroup Functions
    """
    return tkMessageBox.showinfo("Message", msg)

def YesNoDialog(msg, title = "Question"):
    """
    Displays a yes/no dialog box

    @param msg str : the text of the question to ask
    @param title str : title of the dialog box

    \ingroup Functions
    """
    return tkMessageBox.askyesno(title, msg)

import tkFileDialog

def OpenFileDialog(title = "Select File to Open"):
    """
    Prompts the user to specify a file for opening

    @param title str : title of the dialog box
    @return str : the file name to open

    \ingroup Functions
    """

    filetypes = [("allfiles", "*")]
    result = tkFileDialog.askopenfilename(multiple = False, title = title,
                                        filetypes=filetypes)
    if result == "":
        raise GraphicsError("Dialog box cancelled")

    return result

def SaveFileDialog(title = "Select File to Save As"):
    """
    Prompts the user to specify a file for saving

    @param title str : title of the dialog box
    @return str : the file name to use for saving

    \ingroup Functions
    """

    filetypes = [("allfiles", "*")]
    result = tkFileDialog.asksaveasfilename(title = title, filetypes=filetypes)
    if result == "":
        raise GraphicsError("Dialog box cancelled")

    return result

def console(*strings):
    """
    Prints strings to the console window.

    @param strings : any number of strings to print (the strings are output separated by spaces)
    @return None

    \ingroup Functions
    """
    for string in strings:
        print >> Console, string,

    print >> Console

