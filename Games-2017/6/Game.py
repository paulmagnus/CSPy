"""
________________________________________________________________________________
|
|   Assignment: Project 6: Board Game
|   Name: Andrew Wheeler
|   Date: 
|   
|
|                                                                              |
|______________________________________________________________________________|

"""
import random
from cs110graphics import *

WIN_HEIGHT = 500
WIN_WIDTH = 800

PLAYER2COLOR_DICT = {1: 'Red', 2: 'Green', 3: 'Blue', 
                     4: 'Yellow', 5: 'Purple', 6: 'Orange'}
STARTINGSTRENGTH_DICT = {1: 40, 2: 40, 3: 35,
                         4: 30, 5: 25, 6: 20}
PLAYERS = int(input("How many people will be playing? "))

class Player:
    """ Class to set up the player and all its respective units """
    def __init__(self, win, player, board):
        self._win = win
        self._player = player
        self._board = board
        
        unitNumStart = STARTINGSTRENGTH_DICT[PLAYERS]
            
        self._units = []
        for i in range(unitNumStart):
            unit = Unit(player, (15 + 7 * i, 400 + player * 15), board)
            unit.addTo(win)
            self._units.append(unit)
            
    def activateAll(self):
        """ Turns all units 'on' """
        for unit in self._units:
            unit.activate()
    
    def deactivateAll(self):
        """ Turns all units 'off' """
        for unit in self._units:
            unit.deactivate()
            
    def report(self, piece, event):
        """ Reports event to the board """
        self._board.report(piece, event)

class Die(EventHandler):
    """ A class to simulate a fair, 6 sided die. """
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
                 
    def __init__(self, board, width=25, center=(200,200), bgcolor='white',
                 fgcolor='black'):
        EventHandler.__init__(self)
        self._board = board
        self._value = 6
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgcolor)
        self._square.setDepth(20)
        self._width = width
        self._center = center
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgcolor)
            pip.setDepth(20)
            self._pips.append(pip)
        for pip in self._pips:
            pip.addHandler(self)
        self._square.addHandler(self)
        self._update()

    def addTo(self, win):
        """ Adds pips and square to window """
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
        positions = Die.POSITIONS[self._value]
        for i in range(len(positions)):
            if positions[i] is None:
                self._pips[i].setDepth(25)
            else:
                self._pips[i].setDepth(15)
                cx, cy = self._center  # center of the die.
                dx = positions[i][0] * self._width
                dy = positions[i][1] * self._width  
                self._pips[i].moveTo((cx + dx, cy + dy))

    def move(self, dx, dy):
        """ moves the graphical elements of the die """
        self._square.move(dx, dy)
        for pip in self._pips:
            pip.move(dx, dy)
    
    def handleMouseRelease(self, event):
        """ Tells the die what to do upon being clicked """
        self.roll()

class Unit(EventHandler):
    """ Class to create an individual unit of the game"""
    def __init__(self, player, position, board):
        EventHandler.__init__(self)
        self._board = board
        #self._ident = ident         # identifying number for this pawn
        self._position = position   # current logical position on the board
        self._player = player
        self._startLoc = None       # Where the mouse was when we started moving
        self._location = (0, 0)     # Where the piece is
        self._active = True
        self._moving = False
        self._color = PLAYER2COLOR_DICT[player]
        self._unitTerOwner = None
        self._square = Rectangle(15, 15, position)
        self._square.setFillColor(self._color)
        self._square.moveTo(position)
        self._location = position
        self._square.addHandler(self)
        
    def activate(self):
        """ Turns unit 'on' """
        self._active = True
        self._square.setBorderColor('green')
        
    def deactivate(self):
        """ Turns unit 'off' """
        self._active = False
        self._square.setBorderColor('black')
    
    def addTo(self, win):
        """ Adds visuals to window """
        win.add(self._square)
    
    def handleMouseRelease(self, event):
        """ Tells the unit what to do upon mouse release if active """
        if not self._active:
            return
        if self._moving:
            self._moving = False
            self._player.report(self, event)
        else:
            self._moving = True
            self._startLoc = event.getMouseLocation()

    def handleMouseMove(self, event):
        """ Tells unit what to do upon mouse movement """
        if not self._active:
            return
        if self._moving:
            oldx, oldy = self._startLoc
            newx, newy = event.getMouseLocation()
            self.move(newx - oldx, newy - oldy)
            self._startLoc = self._location
    
    def getPosition(self):
        """ Returns position of unit """
        return self._position
    
    def setPosition(self, pos):
        """ Updates position of unit """
        self._position = pos
        
    def moveTo(self, location):
        """ Moves both the unit's logical and graphical position """
        self._square.moveTo(location)
        self._location = location
    
    def move(self, dx, dy):
        oldx, oldy = self._location
        newx = oldx + dx
        newy = oldy + dy
        self.moveTo((newx, newy))

class Board:
    def __init__(self, win):
        """ Sets up all the necessary parts of the game on the board """
        
        self._board = Image(
            "https://cs.hamilton.edu/~axwheele/images/board_risk.png",
            (500, 256), 1000, 516)
        win.add(self._board)

        for i in range(3):
            self._die = Die(board=self, center=(350 + i * 50, 475), 
                            bgcolor='red')
            self._die.addTo(win)
        self._attackerDieText = Text("Dice for attackers", (390, 500), 14)
        win.add(self._attackerDieText)
        
        for i in range(2):
            self._die = Die(board=self, center=(350 + i * 50, 425), 
                            bgcolor='white')
            self._die.addTo(win)
        self._defenderDieText = Text("Dice for the defenders", (405, 450), 14)
        win.add(self._defenderDieText)
            
        self._current = 1
        self._players = []
        for num in range(PLAYERS):
            self._players.append(Player(win, num + 1, self))
        #self.changeTurn()
        
    def changeTurn(self):
        self._players[self._current].deactivateAll()
        self._current += 1
        self._current %= PLAYERS
        self._players[self._current].activateAll()

def main(win):
    """ Starts the board with the correct number of units per player """    
    Board(win)

StartGraphicsSystem(main, 1000, 516)
