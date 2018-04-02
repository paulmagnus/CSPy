""" A simple interactive game """

import random
from cs110graphics import *

class Die(EventHandler):
    """ A six-sided die """
    SIDES = 6
    POSITIONS = [None,
                 [(0, 0), None, None, None, None, None],
                 [(-.25, .25), (.25, -.25), None, None, None, None],
                 [(-.25, .25), (0, 0), (.25, -.25), None, None, None],
                 [(-.25, -.25), (-.25, .25), (.25, -.25), 
                  (.25, .25), None, None],
                 [(-.25, -.25), (-.25, .25), (.25, -.25), 
                  (.25, .25), (0, 0), None],                  
                 [(-.25, -.25), (-.25, .25), (.25, -.25), 
                  (.25, .25), (-.25, 0), (.25, 0)]]
                 
    def __init__(self, win, board, width=25, center=(200,200), bgcolor='white', 
                 fgcolor='black'):
        EventHandler.__init__(self)
        self._board = board
        self._value = 6
        self._square = Rectangle(win, width, width, center)
        self._square.set_fill_color(bgcolor)
        self._square.set_depth(20)
        self._width = width
        self._center = center
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(win, width / 15, center)
            pip.set_fill_color(fgcolor)
            pip.set_depth(20)
            self._pips.append(pip)
        self._square.add_handler(self)
        self._update()   ### BUG IN DIE!!!
        
    def addTo(self, win):
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)

    def roll(self):
        """ changes the value of this die to a random number between 1 and 
            the number of sides of a die """
        self._value = random.randrange(Die.SIDES) + 1
        self._update()
    
    def getValue(self):
        """ return the current value of this die """
        return self._value
        
    def _update(self):
        """ private method: make this die's appearance match its value """
        #self._text.setTextString(str(self._value))
        positions = Die.POSITIONS[self._value]
        for i in range(len(positions)):
            if positions[i] is None:
                self._pips[i].set_depth(25)
            else:
                self._pips[i].set_depth(15)
                cx, cy = self._center  # center of the die.
                dx = int(positions[i][0] * self._width)
                dy = int(positions[i][1] * self._width)  
                self._pips[i].move_to((cx + dx, cy + dy))
                
    def handle_mouse_release(self, event):
        self.roll()
   
class Pawn(EventHandler):
    def __init__(self, win, board, color, ident, position):
        EventHandler.__init__(self)
        self._color = color
        self._board = board
        self._ident = ident   # identifying number for this pawn
        self._position = position # current logical position on the board
        self._square = Rectangle(win, 15, 15, (0, 0))
        self._square.set_fill_color(color)
        self._square.add_handler(self)
    
    def addTo(self, win):
        win.add(self._square)
    
    def handle_mouse_release(self, event):
        self._board.reportPawnClick(self._ident)  # tell the board I was clicked
    
    def getPosition(self):
        return self._position
    
    def setPosition(self, pos):
        self._position = pos
        
    def move_to(self, location):
        self._square.move_to(location)
        
    def move(self, dx, dy):
        self._square.move(dx, dy)
        

class BoardSpace(EventHandler):
    def __init__(self, win, board, center, color):
        EventHandler.__init__(self)
        self._board = board
        self._center = center
        self._square = Rectangle(win, 50, 50, center)
        self._square.set_fill_color(color)
    
    def addTo(self, win):
        win.add(self._square)

    def handle_mouse_release(self, event):
        pass
    
    def getCenter(self):
        return self._center

 
class Board:
    def __init__(self, win):
        self._die = Die(win, self)
        self._die.addTo(win)
        
        # set up some spaces
        self._spaces = []
        xpos = 55
        ypos = 75
        for color in ['red', 'orange', 'yellow', 'green', 
                      'blue', 'indigo', 'violet']:
            thisSpace = BoardSpace(win, self, (xpos, ypos), color)
            thisSpace.addTo(win)
            self._spaces.append(thisSpace)
            xpos += 50
            
        # set up two pawns
        self._pawns = []
        for color, which in [('black', 0), ('white', 1)]:
            thisPawn = Pawn(win, self, color, which, 0)
            thisPawn.addTo(win)
            self._pawns.append(thisPawn)
        self._updatePawnLocations()
    
        # current player
        self._current = 0
        
    def reportPawnClick(self, ident):
        if ident == self._current:
            thePawn = self._pawns[ident]
            pos = thePawn.getPosition()
            pos = pos + self._die.getValue()
            pos = pos % len(self._spaces)
            thePawn.setPosition(pos)
            self._updatePawnLocations()
            self.changeTurn()
    
    def changeTurn(self):
        self._current = (self._current + 1) % len(self._pawns)
    
    def _updatePawnLocations(self):
        """ Move the two pawns to their correct locations on the window """
        offsets = [-1, 1]
        for i in [0, 1]:
            pos = self._pawns[i].getPosition()
            theSpace = self._spaces[pos]
            self._pawns[i].move_to(theSpace.getCenter())
            self._pawns[i].move(0, offsets[i] * 10)
        
def main(win):
    Board(win)
    
StartGraphicsSystem(main)
