"""
*****************************************************************************
       FILE: Deck.py
     AUTHOR: Aidan Costello
 ASSIGNMENT: Project 6
   DUE DATE: May 1, 2017
DESCRIPTION: A program for a backgammon board game.
*****************************************************************************
"""
import random
from cs110graphics import *

class Die():
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
                 
    def __init__(self, board, width=25, center=(250, 35), bgcolor="white", 
                 fgcolor="black"):
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
        self._update()   
        
    def addTo(self, win):
        """ Adds die to window """
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
                cx, cy = self._center
                dx = positions[i][0] * self._width
                dy = positions[i][1] * self._width  
                self._pips[i].moveTo((cx + dx, cy + dy))
                

class Roller(EventHandler):
    """ A roller box for rolling both dice at the same time """
    def __init__(self, board, die1, die2, side=70, center=(250, 107), bgcolor  
                 ="#65a6ce"):
        EventHandler.__init__(self)
        self._die1 = die1
        self._die2 = die2
        self._board = board
        self._side = side
        self._centerx, self._centery = center
        self._box = Rectangle(side, side/2, center)
        self._box.setFillColor(bgcolor)
        self._box.addHandler(self)
    
    def addTo(self, win):
        """ Adds roller to window """
        win.add(self._box)
    
    def handleMouseRelease(self, event):
        """ When mouse is released on box, the dice are rolled """
        self._die1.roll()
        self._die2.roll()

class Pawn(EventHandler):
    """ A class for pawns on the board """
    def __init__(self, board, color, ident, position):
        EventHandler.__init__(self)
        self._color = color
        self._board = board
        self._ident = ident 
        self._position = position  
        self._circle = Circle(12, (position))
        self._circle.setFillColor(color)
        self._circle.addHandler(self)
    
    def addTo(self, win):
        """ Add pawn to window """
        win.add(self._circle)
    
    def handleMouseRelease(self, event):
        """ When mouse is released, """
        print("Clicking pawns is not allowed!")
    
    def getPosition(self):
        """ Returns pawn's position """
        return self._position
    
    def setPosition(self, pos):
        """ Sets pawn's position """
        self._position = pos
        
    def moveTo(self, location):
        """ Moves pawn to a location """
        self._circle.moveTo(location)
        
    def move(self, dx, dy):
        """ Moves pawn to a specific point """
        self._circle.move(dx, dy)
        

class Triangles(EventHandler):
    """ A class for the triangles on the board """
    def __init__(self, board, center, color, side):
        EventHandler.__init__(self)
        self._board = board
        self._center = center
        self._x = center[0]
        self._y = center[1]
        location = side % 2
        if location == 0:
            self._triangle = Polygon([(self._x, self._y), 
                                      (self._x + 30, self._y),
                                      (self._x + 15, 
                                       self._y + 120)])
            self._triangle.setFillColor(color)
        else:
            self._triangle = Polygon([(self._x, 600 - self._y), 
                                      (self._x + 30, 
                                       600 - self._y), 
                                      (self._x + 15, 
                                       600 - self._y - 120)])
            self._triangle.setFillColor(color)
        
    def addTo(self, win):
        """ Adds triangle to the window """
        win.add(self._triangle)
    
    def getCenter(self):
        """ Returns center of triangle """
        return (self._x + 15, self._y)

        
class BoardSpace():
    """ A class for the board space """
    def __init__(self, board, center, width=380, height=280):
        self._x = center[0]
        self._y = center[1]
        self._width = width
        self._height = height
        self._board = board
        self._center = center
        self._border = Rectangle(width+20, height+20, center)
        self._border.setFillColor("#30281f")
        self._middleBoard = Rectangle(width, height, center)
        self._middleBoard.setFillColor("beige")
        self._middleBorder = Rectangle(16, height, center)
        self._middleBorder.setFillColor("#30281f")
        
    def addTo(self, win):
        """ Adds board components to window """
        win.add(self._border)
        win.add(self._middleBoard)
        win.add(self._middleBorder)
        
class Board():
    """ A class for the board and its components """
    def __init__(self, win):
        self._die1 = Die(self, center=(230, 65))
        self._die1.addTo(win)
        self._die2 = Die(self, center=(270, 65))
        self._die2.addTo(win)
        self._roller = Roller(self, self._die1, self._die2)
        self._roller.addTo(win)
        self._text = Text("ROLL", (250, 113), 20)
        win.add(self._text)
        
        self._current = 0           
        currentTriangle = 1
        x, y = 61, 160                  # positions for the triangles
        centerX, centerY = 250, 300
        self._startingPositions = []
        self._spaces = []
        fullboard = BoardSpace(self, (centerX, centerY))
        fullboard.addTo(win)
        colorList = ["#5b4b3b", "#d8bfa6"]
        for _ in range(6):
            for color in colorList:
                currentSpace = Triangles(self, (x, y), color, currentTriangle)
                currentSpace.addTo(win)
                self._spaces.append(currentSpace)
                currentTriangle += 1
            x += 30
            colorList = [colorList[1], colorList[0]]
        for _ in range(6):
            for color in colorList:
                currentSpace = Triangles(self, (x+18, y), color, 
                                         currentTriangle)
                currentSpace.addTo(win)
                self._spaces.append(currentSpace)
                currentTriangle += 1
            x += 30
            colorList = [colorList[1], colorList[0]]    
        
        xPos, yPos = 76, 172
        xPos1, yPos1 = 424, 172
        xPos2, yPos2 = 196, 427
        xPos3, yPos3 = 274, 427
        for color, which in [("#8e301b", 0), ("#fff4f2", 1)]:
            if which == 0:
                for _ in range(5):
                    currentPawn = Pawn(self, color, which, (xPos, yPos))
                    currentPawn.addTo(win)
                    yPos += 24
                for _ in range(2):
                    currentPawn = Pawn(self, color, which, (xPos1, yPos1))
                    currentPawn.addTo(win)
                    yPos1 += 24
                for _ in range(3):
                    currentPawn = Pawn(self, color, which, (xPos2, yPos2))
                    currentPawn.addTo(win)
                    yPos2 -= 24
                for _ in range(5):
                    currentPawn = Pawn(self, color, which, (xPos3, yPos3))
                    currentPawn.addTo(win)
                    yPos3 -= 24
            else:
                for _ in range(5):
                    currentPawn = Pawn(self, color, which, (xPos, yPos+135))
                    currentPawn.addTo(win)
                    yPos -= 24
                for _ in range(2):
                    currentPawn = Pawn(self, color, which, (xPos1, yPos1+207))
                    currentPawn.addTo(win)
                    yPos1 -= 24
                for _ in range(3):
                    currentPawn = Pawn(self, color, which, (xPos2, yPos2-183))
                    currentPawn.addTo(win)
                    yPos2 += 24
                for _ in range(5):
                    currentPawn = Pawn(self, color, which, (xPos3, yPos3-135))
                    currentPawn.addTo(win)
                    yPos3 += 24
                    
        
def main(win):
    """ Starts the program """
    Board(win)
    
StartGraphicsSystem(main, width=500, height=500)
