"""
********************************************************************************
FILE:       Game.py

AUTHOR:     Sarah Stigberg

PARTNER:    -

ASSIGNMENT: Project 6

DATE:       May 1, 2017

DESCRIPTION: This program creates a graphical game of Backgammon and allows for
             two dice to be rolled and the pawns to be moved equal to the 
             rolls of the seperate dies. This game is designed for two players
             and had I had more time I would have added more significant rules 
             such as bumping to the center when a single pawn was landed on and
             made the game more graphically pleasing to look at. Major thank you
             to all TA's for their many hours of assistance, specifically Kat, 
             Ben, Kelsey, Linnea, and Alex. All of the TA's helped me to 
             understand the fundamentals of the organization of my game and to
             write the code needed to create the movement and changes in the
             graphical window that make my game what it is.
********************************************************************************
"""

import random
from cs110graphics import *

#Global variables to set up the initial points of each piece
PLAYER_1 = [(30, 230), (30, 250), (30, 270), (30, 290), (30, 310),
            (126, 90), (126, 110), (126, 130), (198, 90), (198, 110), 
            (198, 130), (198, 150), (198, 170), (318, 310), (318, 290)]
                         
PLAYER_2 = [(30, 90), (30, 110), (30, 130), (30, 150), (30, 170), (126, 310),
            (126, 290), (126, 270), (198, 310), (198, 290), (198, 270), 
            (198, 250), (198, 230), (318, 90), (318, 110)]

class Board1:
    """Sets up the graphical image of the board with all colors and shapes"""
    def __init__(self):
        self._value = 24
        self._outline = Rectangle(312, 240, (174, 200))
        self._outline.setDepth(20)
        self._outline.setFillColor('white')
        self._side1 = Rectangle(144, 240, (90, 200))
        self._side1.setDepth(20)
        self._side2 = Rectangle(144, 240, (258, 200))
        self._side2.setDepth(20)
        self._top1 = Polygon([(18, 80), (30, 180), (42, 80)])
        self._top2 = Polygon([(42, 80), (54, 180), (66, 80)])
        self._top3 = Polygon([(66, 80), (78, 180), (90, 80)])
        self._top4 = Polygon([(90, 80), (102, 180), (114, 80)])
        self._top5 = Polygon([(114, 80), (126, 180), (138, 80)])
        self._top6 = Polygon([(138, 80), (150, 180), (162, 80)])
        self._top7 = Polygon([(186, 80), (198, 180), (210, 80)])
        self._top8 = Polygon([(210, 80), (222, 180), (234, 80)])
        self._top9 = Polygon([(234, 80), (246, 180), (258, 80)])
        self._top10 = Polygon([(258, 80), (270, 180), (282, 80)])
        self._top11 = Polygon([(282, 80), (294, 180), (306, 80)])
        self._top12 = Polygon([(306, 80), (318, 180), (330, 80)])
        self._bottom1 = Polygon([(18, 320), (30, 220), (42, 320)])
        self._bottom2 = Polygon([(42, 320), (54, 220), (66, 320)])
        self._bottom3 = Polygon([(66, 320), (78, 220), (90, 320)])
        self._bottom4 = Polygon([(90, 320), (102, 220), (114, 320)])
        self._bottom5 = Polygon([(114, 320), (126, 220), (138, 320)])
        self._bottom6 = Polygon([(138, 320), (150, 220), (162, 320)])
        self._bottom7 = Polygon([(186, 320), (198, 220), (210, 320)])
        self._bottom8 = Polygon([(210, 320), (222, 220), (234, 320)])
        self._bottom9 = Polygon([(234, 320), (246, 220), (258, 320)])
        self._bottom10 = Polygon([(258, 320), (270, 220), (282, 320)])
        self._bottom11 = Polygon([(282, 320), (294, 220), (306, 320)])
        self._bottom12 = Polygon([(306, 320), (318, 220), (330, 320)])
        
        self._odds = [self._top1, self._bottom2, self._top3, self._bottom4, 
                      self._top5, self._bottom6, self._top7, self._bottom8, 
                      self._top9, self._bottom10, self._top11, self._bottom12]
                       
        self._evens = [self._bottom1, self._top2, self._bottom3, 
                       self._top4, self._bottom5, self._top6, 
                       self._bottom7, self._top8, self._bottom9, 
                       self._top10, self._bottom11, self._top12]

    def addTo(self, win):
        """ Adds the board to the window with correct colors and depths"""
        win.add(self._outline)
        win.add(self._side1)
        win.add(self._side2)
        for obj in self._odds:
            obj.setFillColor('DarkBlue')
            obj.setDepth(20)
            win.add(obj)
        for obj in self._evens:
            obj.setFillColor('khaki')
            obj.setDepth(20)
            win.add(obj)
        
    
class Die(EventHandler):
    """Creates a die that can be created more than once with correct locations
    for pips and graphical objects"""
    SIDES = 6
    POSITIONS = [None, 
                 [(0, 0), None, None, None, None, None], 
                 [(-.25, .25), (.25, -.25), None, None, None, None], 
                 [(-.25, .25), (0, 0), (.25, -.25), None, None, None], 
                 [(-.25, .25), (.25, .25), (-.25, -.25), (.25, -.25), None,
                  None],
                 [(-.25, .25), (.25, .25), (-.25, -.25), (.25, -.25), (0, 0), 
                  None], 
                 [(-.25, .25), (.25, .25), (-.25, -.25), (.25, -.25), (-.25, 0),
                  (.25, 0)]]
    
    def __init__(self, board, width=35, center=(20, 370), bgcolor='white', 
                 fgcolor='black'):
        """Creates the correct graphical image for each die instance """
        EventHandler.__init__(self)
        self._board = board
        self._value = 6
        self._die = Rectangle(30, 30, center)
        self._die.setFillColor(bgcolor)
        self._die.setBorderColor(fgcolor)
        self._die.setDepth(20)
        self._width = width
        self._center = center
        self._active = False
        self._pips = []
        #Adds all possible pips to the rectangular image of the die
        for _ in range(Die.SIDES):
            pip = Circle(2, center)
            pip.setFillColor(fgcolor)
            pip.setDepth(20)
            self._pips.append(pip)
        #Allows the die to respond to a click within the rectangle of its face
        self._die.addHandler(self)
        self._update()
                        
    def addTo(self, win):
        """Adds the die image and the correct number of pips to the window """
        win.add(self._die)
        for pip in self._pips:
            win.add(pip)
            
    def roll(self):
        """Gives a random die roll and updates the graphical die image"""
        self._value = random.randrange(Die.SIDES) + 1
        self._update()
        
    def getValue(self):
        """Returns the integer of the die roll"""
        return self._value
        
    def _update(self):
        """Changes the locations images of the pips on the die face based on the
        random roll of the die"""
        positions = Die.POSITIONS[self._value]
        for i in range(len(positions)):
            if positions[i] is None:
                self._pips[i].setDepth(25)
            else:
                self._pips[i].setDepth(5)
                cx, cy = self._center
                dx = positions[i][0] * 35
                dy = positions[i][1] * 35
                self._pips[i].moveTo((cx + dx, cy + dy))
                
    def activate(self):
        """Activates the dies identifiable by a green
        outline"""
        self._active = True
        self._die.setBorderColor('green')
        
    def deactivate(self):
        """Deactivates the dies identifiable by a red
        outline"""
        self._active = False
        self._die.setBorderColor('red')
                
    def handleMouseRelease(self, event):
        """When the die face is clicked the die will be rolled to a random
        number 1-6"""
        self.roll()
        self.deactivate()
        
class BoardSpace(EventHandler):
    """Sets up cells that will be used to hold and pass pieces but will not
    appear on the screen"""
    def __init__(self, center):
        """Creates the graphical cell"""
        EventHandler.__init__(self)
        self._center = center
        self._rect = Rectangle(24, 20, center)
        self._rect.setBorderColor('white')
        self._rect.setDepth(50)
        self._piece = None
        
    def addTo(self, win):
        """Adds the cell to the window"""
        win.add(self._rect)
        
    def getCenter(self):
        """Returns the center of the cell"""
        return self._center
        
    def getPiece(self):
        """Returns the piece inside of the cell"""
        return self._piece
        
    def addPiece(self, piece):
        """Adds a piece to the cell when inside of the cell"""
        self._piece = piece
        
class Pawn(EventHandler):
    """Creates the graphical pawns as well as methods to move and identify"""
    def __init__(self, board, color, ident, position):
        """Designs the individual pawns"""
        EventHandler.__init__(self)
        self._board = board
        self._ident = ident
        self._position = position
        self._piece = Circle(10, (0, 0))
        self._piece.setDepth(5)
        self._piece.setFillColor(color)
        self._piece.addHandler(self)
        self._location = (0, 0)
        self._active = False
        
    def addTo(self, win):
        """Adds the pawns to the window"""
        win.add(self._piece)
        
    def handleMouseRelease(self, event):
        """Allows the pawn to react, if active, to the mouse release"""
        if self._active:
            self._board.reportPawnClick(self)
        
    def getPosition(self):
        """Returns the position of the pawn"""
        return self._position
        
    def setPosition(self, pos):
        """Changes the position of the pawn"""
        self._position = pos
            
    def moveTo(self, location):
        """Moves the center of the pawn to a new location and identifies the
        cell that it has landed in in order to alert the board"""
        self._piece.moveTo(location)
        self._board.find(self)
        
    def move(self, dx, dy):
        """Moves the piece to a new coordinate"""
        self._piece.move(dx, dy)
        
    def getCenter(self):
        """Returns the center of the pawn"""
        return self._piece.getCenter()
        
    def activate(self):
        """Activates the current players pieces identifiable by a green
        outline"""
        self._active = True
        self._piece.setBorderColor('green')
        
    def deactivate(self):
        """Deactivates the current players pieces identifiable by a red
        outline"""
        self._active = False
        self._piece.setBorderColor('red')

class Board:
    """Sets up all objects in the screen including, two dice, all pawns in their
    starting locations, the graphical image of the board, all underground cells
    and creates the ability for the pawn clicked to be moved the number of 
    spaces designated by the die roll"""
    
    def __init__(self, win):
        """Initializes both dice, creates the board of cells, creates two lists
        of pawns, one for each player"""
        #Creates two dice that roll when clicked
        self._die1 = Die(self, center=(20, 370))
        self._die2 = Die(self, center=(60, 370))
        self._die1.addTo(win)
        self._die1.activate()
        self._die2.addTo(win)
        self._die2.activate()
        self._die1.roll()
        self._die2.roll()
        
        #adds the graphical image of the board to the window
        self._boardimage = Board1()
        self._boardimage.addTo(win)
        
        self._dieUsed = False
        self._cells = []
        
        #Builds a grid of cells underneath the board with 6 rectangles per
        #triangle starting in the bottom right corner and wrapping around to the
        #top right corner
        
        xpos = 486
        ypos = 310
        for triangle in range(12):
            xpos -= 24
            for spot in range(6):
                newCell = BoardSpace((xpos, ypos))
                newCell.addTo(win)
                self._cells.append(newCell)
                ypos -= 20
            ypos = 310
            
        xpos = 174
        ypos = 310
        for triangle in range(6):
            xpos -= 24
            for spot in range(6):
                newCell = BoardSpace((xpos, ypos))
                newCell.addTo(win)
                self._cells.append(newCell)
                ypos -= 20
            ypos = 310
            
        xpos = 6
        ypos = 90
        for triangle in range(6):
            xpos += 24
            for spot in range(6):
                newCell = BoardSpace((xpos, ypos))
                newCell.addTo(win)
                self._cells.append(newCell)
                ypos += 20
            ypos = 90
        
        xpos = 174
        ypos = 90
        for triangle in range(12):
            xpos += 24
            for spot in range(6):
                newCell = BoardSpace((xpos, ypos))
                newCell.addTo(win)
                self._cells.append(newCell)
                ypos += 20
            ypos = 90
        
        #adds 15 pawns to their starting location based on their given identity 
        self._pawns = [[], []]
        for color, which in [('white', 0), ('purple', 1)]:
            if color == 'white':
                for i in range(len(PLAYER_1)):
                    thisPawn = Pawn(self, color, which, 0)
                    thisPawn.addTo(win)
                    self._pawns[0].append(thisPawn)
                    thisPawn.moveTo(PLAYER_1[i])
                    thisPawn.activate()
            if color == 'purple':
                for i in range(len(PLAYER_2)):
                    thisPawn = Pawn(self, color, which, 0)
                    thisPawn.addTo(win)
                    self._pawns[1].append(thisPawn)
                    thisPawn.moveTo(PLAYER_2[i])
                    thisPawn.deactivate()
        self._updatePawnLocations()
        
        #The first player to move is set to white    
        self._current = 0
    
    def find(self, pawn):
        """Matches pawns in their graphical locations on the window to the cell
        they occupy"""
        for i in range(len(self._cells)):
            if self._cells[i].getCenter() == pawn.getCenter():
                self._cells[i].addPiece(pawn)
                pawn.setPosition(i)
        
    def reportPawnClick(self, pawn):
        """Moves the pawn that has been clicked on equal to the number of spaces
        designated by the first die and then moves the second pawn clicked on
        the number of spaces told by the second die and finishes by changing
        the turn"""
        if not self._dieUsed:
            pos = pawn.getPosition()
            if self._current == 0:
                pos = pos + self._die1.getValue() * 6
            else:
                pos = pos - self._die1.getValue() * 6
            pos -= pos % 6
            pawn.setPosition(pos)
            self._updatePawnLocations()
            self._dieUsed = True
            
        else: 
            pos = pawn.getPosition()
            if self._current == 0:
                pos = pos + self._die2.getValue() * 6
            else:
                pos = pos - self._die2.getValue() * 6
            pos -= pos % 6
            pawn.setPosition(pos)
            self._updatePawnLocations()
            self.changeTurn()
            if self._die1.getValue() == self._die2.getValue():
                self.changeTurn()
            self._dieUsed = False
            
    def changeTurn(self):
        """Activates the pawns of the player whos turn it is to move and
        deactivates the other pawns"""
        #Changes the current player to the other player
        self._current = (self._current + 1) % len(self._pawns)
        self.deactivateAll()
        self.activateAll()
        self._die1.activate()
        self._die2.activate()
        
    def activateAll(self):
        """Activates the correct pawns"""
        for piece in self._pawns[self._current]:
            piece.activate()
            
    def deactivateAll(self):
        """Deactivates the correct pawns"""
        for piece in self._pawns[self._current - 1]:
            piece.deactivate()
        
    def _updatePawnLocations(self):
        """Changes the list of the locations where the pawns sit"""
        for player in self._pawns:
            for i in range(len(player)):
                pos = player[i].getPosition()
                theSpace = self._cells[pos]
                player[i].moveTo(theSpace.getCenter())
                
                

def play(win):
    """Calls board in order to run the game in the window"""
    win.setHeight(400)
    win.setWidth(600)
    Board(win)
    
StartGraphicsSystem(play)
