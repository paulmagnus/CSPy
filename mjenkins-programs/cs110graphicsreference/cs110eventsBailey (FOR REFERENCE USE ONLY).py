# Load the global definitions from cs110graphics

import cs110graphics

from cs110point import *
from cs110locks import *
from cs110utils import *
from cs110GraphicsSupport import *

# These events are reported to eventHandlers

handlerEventTypes = (
	"<Key>",
	"<KeyRelease>",
	"<ButtonPress-1>",
	"<ButtonPress-2>",
	"<ButtonPress-3>",
	"<ButtonPress-4>",
	"<ButtonPress-5>",
	"<ButtonRelease-1>",
	"<ButtonRelease-2>",
	"<ButtonRelease-3>",
	"<ButtonRelease-4>",
	"<ButtonRelease-5>",
	"<Motion>",
	"<B1-Motion>",
	"<B2-Motion>",
	"<B3-Motion>",
	"<B4-Motion>",
	"<B5-Motion>",
#    "<Double-ButtonPress-1>",
#    "<Double-ButtonPress-2>",
#    "<Double-ButtonPress-3>",
#    "<Double-ButtonPress-4>",
#    "<Double-ButtonPress-5>",
#    "<Triple-ButtonPress-1>",
#    "<Triple-ButtonPress-2>",
#    "<Triple-ButtonPress-3>",
#    "<Triple-ButtonPress-4>",
#    "<Triple-ButtonPress-5>",
	"<Enter>",
	"<Leave>"
	)

# These events are reported when using the wait method

staticEventTypes = (
	"<Key>",
	"<ButtonRelease-1>", 
	"<ButtonRelease-2>", 
	"<ButtonRelease-3>", 
	"<ButtonRelease-4>", 
	"<ButtonRelease-5>"
	)

def buttonName(num):
	buttonMap = {
		"??" : "None", # used for mouse drag events without mouse down
		1 : "left",
		2 : "middle",
		3 : "right",
		4 : "scroll wheel up",
		5 : "scroll wheel down"
		}

	if num in buttonMap:
		return buttonMap[num]
	else:
		return "unknown mouse button number: " + str(num)

def eventName(tkEventType):
	eventMap = {
		"<Key>"       : "key press",
		"<KeyRelease>"      : "key release",
		"<ButtonPress-1>"   : "mouse press",
		"<ButtonPress-2>"   : "mouse press",
		"<ButtonPress-3>"   : "mouse press",
		"<ButtonPress-4>"   : "mouse press",
		"<ButtonPress-5>"   : "mouse press",
		"<ButtonRelease-1>"   : "mouse release",
		"<ButtonRelease-2>"   : "mouse release",
		"<ButtonRelease-3>"   : "mouse release",
		"<ButtonRelease-4>"   : "mouse release",
		"<ButtonRelease-5>"   : "mouse release",
		"<Motion>"      : "mouse move",
		"<B1-Motion>"     : "mouse drag",
		"<B2-Motion>"     : "mouse drag",
		"<B3-Motion>"     : "mouse drag",
		"<B4-Motion>"     : "mouse drag",
		"<B5-Motion>"     : "mouse drag",
		"<Double-ButtonPress-1>"  : "mouse double click",
		"<Double-ButtonPress-2>"  : "mouse double click",
		"<Double-ButtonPress-3>"  : "mouse double click",
		"<Double-ButtonPress-4>"  : "mouse double click",
		"<Double-ButtonPress-5>"  : "mouse double click",
		"<Triple-ButtonPress-1>"  : "mouse triple click",
		"<Triple-ButtonPress-2>"  : "mouse triple click",
		"<Triple-ButtonPress-3>"  : "mouse triple click",
		"<Triple-ButtonPress-4>"  : "mouse triple click",
		"<Triple-ButtonPress-5>"  : "mouse triple click",
		"<Enter>"     : "mouse enter",
		"<Leave>"     : "mouse leave",
		}

	if tkEventType in eventMap:
		return eventMap[tkEventType]
	else:
		return "unknown event type: " + str(tkEventType)

def makeEvent(tkEvent, tkEventType):

	# This function constructs an Event from a tkEvent and parses all the
	# fields to determine all the event information.

	evType = eventName(tkEventType)
	widget = tkEvent.widget
	location = Point(tkEvent.x, tkEvent.y)
	rootLocation = Point(tkEvent.x_root, tkEvent.y_root)

	# If this was a key press/release, set the keysym

	if "key" in evType:
		key = tkEvent.keysym
	else:
		key = None
		
	# If this was a mouse event, it will have the button number in the
	# event name. Extract it.

	button = None
	for buttonNum in range(1, 6):
		if str(buttonNum) in tkEventType:
			button = buttonName(buttonNum)
			break
		
	return Event(evType, widget, location, rootLocation, key, button)


# pylint: disable=R0921
# (Abstract class not referenced)

_eventCount = 0
class Event(CS110Object):
	"""
	An object that represents graphical user interface events such as mouse
	clicks.
	"""
	# pylint: disable=W0231
	# (base class __init__ not called)

	def __init__(self, evType, widget, location, rootLocation, key, button):
		global _eventCount
		self._type = evType
		self._widget = widget
		self._location = location
		self._rootLocation = rootLocation
		self._key = key
		self._button = button
		self._serial = _eventCount
		_eventCount = _eventCount + 1

	# pylint: enable=W0231
	# (base class __init__ not called)
		
	def __repr__(self):
		return ("Event(%s, %s, %s, %s, %s, %s)" % 
				(repr(self._type), repr(self._widget), repr(self._location),
				 repr(self._rootLocation), repr(self._key), repr(self._button)))

	def __str__(self):
		if "key" in self._type:
			descript = "key = " + self._key
		elif "mouse" in self._type:
			descript = "button = " + str(self._button)
		else:
			descript = "unknown (%s), " % self._type

		return ("Event: id = %s, type = %s, %s, loc = %s" %
				(self._serial, self._type, descript, str(self._location.get())))

	def getDescription(self):
		"""
		Returns a description of the event. It will be one of the following:

		"key press" - generated a keyboard key is pressed (generated by wait)

		"key release" - generated when a keyboard key is released
		
		"mouse press" - generated when the mouse button is pressed
		
		"mouse release" - generated when the mouse button is released
		(generated by wait)
		
		"mouse drag" - generated when the mouse is "dragged" with the mouse
		button pressed

		"mouse move" - generated when the mouse is moved without the mouse
		button pressed
						  
		"mouse enter" - generated when the mouse enters a region
		
		"mouse leave" - generated when the mouse leavea a region
		

		@return str: the string describing the event.
		"""
		
		return self._type

	def getKey(self):
		"""
		Returns the name of the keyboard key that generated the event.

		@return str: the name of the key
		"""
		if self._key == None:
			print >> stderr, "getKey called on a non-keyboard event"
		return self._key

	def getButton(self):
		"""
		Returns the name of the mouse button that generated the event.

		@return str: the name of the button
		"""
		if self._button == None:
			print >> stderr, "getButton called on a non-mouse event"
		return self._button

	def getMouseLocation(self):
		"""
		Returns the mouse's location when the event occurred (as a Point)
		@return Point: a Point specifying the location of the mouse.
		"""

		return self._location
	
	def getOldMouseLocation(self):
		raise NotImplementedError

	def getTrigger(self):
		raise NotImplementedError


class EventHandler(CS110Object):
	"""
	An object that handles events reported by the graphical user interface
	"""
	# pylint: disable=W0231
	# (base class __init__ not called)
	def __init__(self):
		"""
		The constructor.
		"""
		# map of method names to event types
		eventTypeMap = (
			(self.handleKeyPress  , ["<Key>"]),
			(self.handleKeyRelease  , ["<KeyRelease>"]),
			(self.handleMousePress  , ["<ButtonPress-1>",
										   "<ButtonPress-2>",
										   "<ButtonPress-3>", 
										   "<ButtonPress-4>",
										   "<ButtonPress-5>"]),
			(self.handleMouseRelease  , ["<ButtonRelease-1>", 
										   "<ButtonRelease-2>", 
										   "<ButtonRelease-3>", 
										   "<ButtonRelease-4>",
										   "<ButtonRelease-5>"]),
			(self.handleMouseMove , ["<Motion>"]),
			(self.handleMouseDrag , ["<B1-Motion>", 
										   "<B2-Motion>",
										   "<B3-Motion>",
										   "<B4-Motion>",
										   "<B5-Motion>"]),
			(self.handleMouseEnter  , ["<Enter>"]),
			(self.handleMouseLeave  , ["<Leave>"]),
			(self.handle    , handlerEventTypes)
		   )

		self._eventTypes = []

		# for each method in the map, check if it has been defined
		# if so, add its types to the list of event types to register

		for (method, evTypes) in eventTypeMap:

			# Check if this has the default docstring. If so, it hasn't
			# been overridden.

			if isinstance(method.__doc__, str) and "@param" in method.__doc__:
				continue

			# Otherwise, add the types (if it isn't handle, or all others
			# are not defined (order dependent)

			if not (method == self.handle and len(self._eventTypes) > 0):
				self._eventTypes += evTypes

#        print self._eventTypes
#        self._eventTypes = evTypes

		self._tkEventHandlers = {}
		for kind in self._eventTypes:

			# Create a custom event reporting function for each of the event
			# types. The eventType=eventType causes Python to capture the
			# value at function definition time instead of at function
			# execution time.

			def captureEvent(tkEvent, eventType = kind):
				log("Delivering event: ", eventType, kind = "event")
				print tkEvent
				self.handleEvent(makeEvent(tkEvent, eventType))
				if EventDriven:
					update()
#                cs110graphics.GS.shutdownIfNoWindows()

			self._tkEventHandlers[kind] = captureEvent

#                cs110graphics.GS.shutdownIfNoWindows()


	def getTkEventHandler(self, kind):
		return self._tkEventHandlers[kind]

	def getEventTypes(self):
		return self._eventTypes

	# pylint: enable=W0231
	# (base class __init__ not called)

	# pylint: disable=R0201
	# (Method could be a function)

	# pylint: disable=W0613
	# (Unused argument)

	def handle(self, event):
		"""
		Called by the graphical user interface when an event arrives on the
		registered graphical object.

		This method is called only in the absence of any other, more
		specialized handler (such as handleMouseEnter)
		@param event Event: the event that has arrived
		@return None
		"""
		
		print >> Console, (
			"WARNING: default EventHandler handle method called.\n" +
			"You haven't properly overridden the handle method.\n" +
			"Event info:"), event
				 
		raise NotImplementedError

	def handleMouseEnter(self, loc):
		"""
		Called by the graphical user interface when the mouse enters
		the registered graphical object
		@param loc Point: the mouse location
		@return None
		"""
		if True:
			raise NotImplementedError

	def handleMouseLeave(self, loc):
		"""
		Called by the graphical user interface when the mouse leaves
		the registered graphical object
		@param loc Point: the mouse location
		@return None
		"""
		if True:
			raise NotImplementedError

	def handleMouseMove(self, loc):
		"""
		Called by the graphical user interface when the mouse moves inside
		the registered graphical object
		@param loc Point: the mouse location
		@return None
		"""
		if True:
			raise NotImplementedError

	def handleMouseDrag(self, button, loc):
		"""
		Called by the graphical user interface when the mouse is dragged inside
		the registered graphical object
		@param button str: the name of the mouse button pressed
		@param loc Point: the mouse location
		@return None
		"""
		if True:
			raise NotImplementedError


	def handleMouseRelease(self, button, loc):
		"""
		Called by the graphical user interface when the mouse is released
		inside the registered graphical object
		@param button str: the name of the mouse button released
		@param loc Point: the mouse location
		@return None
		"""
		if True:
			raise NotImplementedError

	def handleMousePress(self, button, loc):
		"""
		Called by the graphical user interface when the mouse is clicked
		inside the registered graphical object
		@param button str: the name of the mouse button pressed
		@param loc Point: the mouse location
		@return None
		"""
		if True:
			raise NotImplementedError

# use when pylinting
#    def XhandleKeyPress(self, key, loc):
	def handleKeyPress(self, key, loc):
		"""
		Called by the graphical user interface when a key on the keyboard is
		pressed
		@param key str: the name of the key
		@param loc Point: the mouse location
		@return None
		"""
		if True:
			raise NotImplementedError

	def handleKeyRelease(self, key, loc):
		"""
		Called by the graphical user interface when a key on the keyboard is
		released
		@param key str: the name of the key
		@param loc Point: the mouse location
		@return None
		"""
		if True:
			raise NotImplementedError

	# pylint: enable=R0201
	# (Method could be a function)

	# pylint: enable=W0613
	# (Unused argument)

	def dispatchToHandler(self, event):
		dispatchMap = {
			"mouse enter" : self.handleMouseEnter,
			"mouse leave" : self.handleMouseLeave,
			"mouse press" : self.handleMousePress,
			"mouse release" : self.handleMouseRelease,
			"mouse drag" : self.handleMouseDrag,
			"mouse move" : self.handleMouseMove,
			"key press" : self.handleKeyPress,
			"key release" : self.handleKeyRelease
			}

#        print event
		eventType = event.getDescription()

		# Check if the event type is in the map. If it isn't
		# this is an event we don't expect to get.

		if not eventType in dispatchMap:
			print >> sys.stderr,  "Not handling event (no key)", event
			return

		# Get the event-specific method

		method = dispatchMap[eventType]

		# Check if the method is defined by the user. If it has @param
		# as the docstring, we will assume it is the original method.

		if isinstance(method.__doc__, str) and "@param" in method.__doc__:
#            print "Warning, method is not overridden!"
 
#            if isinstance(self.handle.__doc__, str) and "@param" in
# self.handle.__doc__:
#                print "Warning, handle is not overridden!"
			
			self.handle(event)
			
		elif eventType in ("mouse enter", "mouse leave", "mouse move"):
			method(event.getMouseLocation())
			
		elif eventType in ("mouse release", "mouse press", "mouse drag"):
			method(event.getButton(), event.getMouseLocation())

		elif eventType in ("keyboard", "key release"):
			method(event.getKey(), event.getMouseLocation())

	def handleEvent(self, evnt):

		# This is the method that gets called by the graphics system.
		# Its purpose is to wrap the handler in an exception handler to
		# abort the graphics system should an exception occur

		return self.dispatchToHandler(evnt)

##         try:
##             return self.dispatchToHandler(evnt)
##         except:
##             getGraphicsSystem().graphicsThreadAbort()
##             raise

	def __repr__(self):
		return str(type(self)) + "()"

	def __str__(self):
		return str(type(self))

# This class is used to build event handlers for the synchronized wait command
# on GraphicalObjects

class WaitHandler(EventHandler):

	# This event handler keeps an EventLock for syncronizing the GUI and the
	# main thread and an instance variable to capture the event.

	def __init__(self):
		EventHandler.__init__(self)
		self._capturedEvent = None
		self._eventStatus = NonblockingVar(cs110graphics.GS.tkRoot)

	# handle is called by the GUI. It captures the event and signals the
	# main thread that it is ready.

	def handle(self, event):
		if event.getDescription() != "mouse release" and event.getDescription() != "key release":
			return
		self._capturedEvent = event
		self._eventStatus.set("arrived")
				
	# wait is called by the main thread. It waits for the GUI to signal that
	# an event has arrived and returns the event.

	def wait(self):
		self._eventStatus.wait()
		return self._capturedEvent

class EventBindings(object):
	def __init__(self):
		self._handlerBindings = []
		self._handlerTable = {}


	def printBindingList(self):
		for (graphicalObject, graphic, handler, eventType) in self._handlerBindings:
			print graphicalObject, graphic, handler, eventType

	def inBindingList2(self, graphic, handler, eventType):
		for i in range(len(self._handlerBindings)):
			if self._handlerBindings[i][1:] == (graphic, handler, eventType):
				return True

		return False

	def inBindingList(self, graphicalObject, graphic, handler, eventType):
		for i in range(len(self._handlerBindings)):
			if self._handlerBindings[i] == (graphicalObject, graphic, handler, eventType):
				return i

		return None

	def addToBindingList(self, graphicalObject, graphic, handler, eventType):
		if self.inBindingList(graphicalObject, graphic, handler, eventType) != None:
			print >> ErrorConsole, "Binding already in list: ", graphic

		self._handlerBindings.append((graphicalObject, graphic, handler, eventType))

	def removeFromBindingList(self, graphicalObject, graphic, handler, eventType):
		i = self.inBindingList(graphicalObject, graphic, handler, eventType)

		if i == None:
			print >> ErrorConsole, "Can't find binding in list to remove"
		
		self._handlerBindings.pop(i)
									 
	def bindWaitHandler(self, graphicalObject, handler):
		eventTypes = ["<ButtonRelease-1>"]

		canvas = graphicalObject.getCanvas()

		# What if no graphics? Bind to the canvas, or what?

		if graphicalObject.drawn():
			graphics = graphicalObject.getGraphics()
		
	def unbindWaitHandler(self, graphicalObject):
		pass

	def bindEventHandler(self, owner, graphicalObject, handler):

#        print >> Console, "Bind event handler called on ", owner, " (", graphicalObject, ")"

		# If this graphical object is not visible, there are no graphics
		# to register the handler with

		if not owner.drawn():
			return

		graphic = graphicalObject.getTkGraphic()

		assert graphicalObject.drawn()

		# Get the canvas on which the graphic is drawn

		canvas = owner._getCanvas()

		# Find out what events the handler handles

		eventTypes = handler.getEventTypes()

		# For each of these events, register the handler with the object

		keyPressHandlerBound = False
		keyReleaseHandlerBound = False

#        print >> Console, "Binding: ", eventTypes
		for eventType in eventTypes:
			

			# Create a custom event reporting function for each of the event
			# types. This additional wrapper is necessary to carry along the
			# tkEventType since it is lost by the Tk event handling system

			# The eventType=eventType causes Python to capture the
			# value at function definition time instead of at function
			# execution time.

			def captureEvent(tkEvent, eventType = eventType, handler = handler):
				log("Delivering event: ", eventType, kind = "event")
#                print tkEvent
				handler.handleEvent(makeEvent(tkEvent, eventType))
#                cs110graphics.GS.shutdownIfNoWindows()

			# Keyboard events must be attached to the appropriate canvas. This
			# is what the focus is set to. If there are no graphics, we also
			# attach to the canvas. Otherwise, bind to the graphic.

#            canvas.focus_set()

			if "Key" in eventType or graphic is None:
				if eventType == "<Key>":
					if keyPressHandlerBound:
						continue
					keyPressHandlerBound = True
				if eventType == "<KeyRelease>":
					if keyReleaseHandlerBound:
						continue
					keyReleaseHandlerBound = True

				if self.inBindingList2(canvas, handler, eventType):
#                    print "Double key binding"
					continue
				log("Binding event on canvas: ", eventType, kind = "binding")
				canvas.bind(eventType, captureEvent, "+")
				self.addToBindingList(owner, canvas, handler, eventType)
				continue

			else:
				log("Binding event on graphic: ", eventType, kind = "binding")
#                print canvas
#                print graphic
#                print eventType
#                print captureEvent
				
				canvas.tag_bind(graphic, eventType, captureEvent, "+")
				self.addToBindingList(owner, graphic, handler, eventType)

#        self.printBindingList()
		return
			
	def unbindEventHandler(self, owner, graphicalObject, handler):
#        print "Unbind event handler called!"
		
		# If this graphical object is not visible, there are no graphics
		# to register the handler with

		if not graphicalObject.drawn():
			return

		graphic = graphicalObject.getTkGraphic()

		# Get the canvas on which the graphic is drawn

		canvas = graphicalObject._getCanvas()

		# Find out what events the handler handles

		eventTypes = handler.getEventTypes()

		# For each of these events, unregister the handler with the object

		keyHandlerUnbound = False

#        print >> Console, "Unbinding: ", eventTypes

		for eventType in eventTypes:
			if "Key" in eventType or graphic is None:
				if keyHandlerUnbound:
					continue
				keyHandlerUnbound = True
				log("UnBinding event on canvas: ", eventType, kind = "binding")
				canvas.unbind(eventType)
				self.removeFromBindingList(owner, canvas, handler, eventType)
#                self.removeFromBindingList(graphicalObject, graphic, handler, eventType)
				continue

			else:
				log("UnBinding event on graphic: ", eventType, kind = "binding")
				canvas.tag_unbind(graphic, eventType)
				self.removeFromBindingList(owner, graphic, handler, eventType)
#                self.removeFromBindingList(graphicalObject, graphic, handler, eventType)
#        self.printBindingList()
		return

EventManager = EventBindings()





# bindHandler a handler to one or more events for one or more graphics

def XbindHandler(eventTypes, canvas, handler, graphics = None):

	log("Binding handler for", graphics, kind = "binding")

	# If graphics is none, we are going to bind to the canvas.

	if graphics == None:
		graphics = [None]

	# For each graphic and event type, build a handler and register it.

	for eventType in eventTypes:

#        print eventType

		keyHandlerBound = False
		for graphic in graphics:

#            print "  ", graphic
			# Create a custom event reporting function for each of the event
			# types. The eventType=eventType causes Python to capture the
			# value at function definition time instead of at function
			# execution time.

			def captureEvent(tkEvent, eventType = eventType):
				handler.handleEvent(makeEvent(tkEvent, eventType))
				cs110graphics.GS.shutdownIfNoWindows()

			# Keyboard events must be attached to the appropriate canvas. This
			# is what the focus is set to. If there are no graphics, we also
			# attach to the canvas. Otherwise, bind to the graphic.

			canvas.focus_set()

			if "Key" in eventType or graphic is None:
				if keyHandlerBound:
					break
				keyHandlerBound = True
				log("Binding event on canvas: ", eventType, kind = "binding")
#                print "Before:", canvas.bind(eventType)
				canvas.bind(eventType, captureEvent, "+")
#                print "After:", canvas.bind(eventType)
				break
			else:
				log("Binding event on graphic: ", eventType, kind = "binding")
#                print "Before:", canvas.tag_bind(graphic, eventType)
				canvas.tag_bind(graphic, eventType, captureEvent, "+")
#                print "After:", canvas.tag_bind(graphic, eventType)

def unbindEvents(eventTypes, canvas, graphics = None):
	if graphics == None:
		graphics = [None]

	for graphic in graphics:
		for eventType in eventTypes:
			if "Key" in eventType or graphic is None:
				log("UnBinding event on canvas: ", eventType, kind = "binding")
				canvas.unbind(eventType)
			else:
				log("UnBinding event on graphic: ", eventType, kind = "binding")
				canvas.tag_unbind(graphic, eventType)

