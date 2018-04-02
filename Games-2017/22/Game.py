"""
 *****************************************************************************
FILE: Deck.py
AUTHOR: Justin
ASSIGNMENT: Game
DATE: 4/14/17
DESCRIPTION: A  program that creates the  board game Risk.
*****************************************************************************
""" 

import random
from cs110graphics import *


class Game: 
    """Creates base for boardgame """
    def __init__(self):
        """ Create graphical objects necessary for board game"""
        self._window = None
        
        self._circle1 = Circle(25, (145, 50))
        self._circle1.setFillColor('orange')
        self._circ1 = Text('5', (145, 50))
        
        self._circle2 = Circle(25, (290, 50))
        self._circle2.setFillColor('purple')
        self._circ2 = Text('2', (290, 50))
        
        self._circle3 = Circle(25, (435, 50))
        self._circle3.setFillColor('red')
        self._circ3 = Text('3', (435, 50))
        
        self._circle4 = Circle(25, (580, 50))
        self._circle4.setFillColor('teal')
        self._circ4 = Text('7', (580, 50))
        
        self._circle5 = Circle(25, (725, 50))
        self._circle5.setFillColor('green')
        self._circ5 = Text('2', (725, 50))
        
        self._circle6 = Circle(25, (870, 50))
        self._circle6.setFillColor('blue')
        self._circ6 = Text('5', (870, 50))
        
        self._circle7 = Circle(25, (145, 950))
        self._circle7.setFillColor('blue')
        self._circ7 = Text('5', (145, 950))
        
        self._circle8 = Circle(25, (290, 950))
        self._circle8.setFillColor('green')
        self._circ8 = Text('2', (290, 950))
        
        self._circle9 = Circle(25, (435, 950))
        self._circle9.setFillColor('teal')
        self._circ9 = Text('7', (435, 950))
        
        self._circle10 = Circle(25, (580, 950))
        self._circle10.setFillColor('red')
        self._circ10 = Text('3', (580, 950))
        
        self._circle11 = Circle(25, (725, 950))
        self._circle11.setFillColor('purple')
        self._circ11 = Text('2', (725, 950))
        
        self._circle12 = Circle(25, (870, 950))
        self._circle12.setFillColor('orange')
        self._circ12 = Text('5', (870, 950))
        
        
        self._square = Square(1000, (500, 500))
        self._square.setFillColor('azure')
        self._square.setBorderWidth(10)
        self._square.setBorderColor('black')
        #self._square.setDepth(100)
    
    def addTo(self, win):
        """Adds board basics to window"""
        win.add(self._square)
        
        win.add(self._circle1)
        win.add(self._circle2)
        win.add(self._circle3)
        win.add(self._circle4)
        win.add(self._circle5)
        win.add(self._circle6)
        win.add(self._circle7)
        win.add(self._circle8)
        win.add(self._circle9)
        win.add(self._circle10)
        win.add(self._circle11)
        win.add(self._circle12)
        
        win.add(self._circ1)
        win.add(self._circ2)
        win.add(self._circ3)
        win.add(self._circ4)
        win.add(self._circ5)
        win.add(self._circ6)
        win.add(self._circ7)
        win.add(self._circ8)
        win.add(self._circ9)
        win.add(self._circ10)
        win.add(self._circ11)
        win.add(self._circ12)
        

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
                 
    def __init__(self, board, width=25, center=(600, 875), bgcolor='white',
                 fgcolor='black'):
        """" Creates two dies for the defender to roll and records the number on
        the dice"""            
        EventHandler.__init__(self)
        self._board = board
        self._value = 1
        self._value1 = 2
        self._width = width
        self._center = center
        self._pips = []
        self._pips1 = []
        
        # Creates the first die
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgcolor)
        self._square.setDepth(20)
        
        #Creates the second die
        self._square1 = Rectangle(width, width, (600, 850))
        self._square1.setFillColor(bgcolor)
        self._square1.setDepth(20)
        
        # Creates button to roll die
        self._button = Rectangle(50, 30, (700, 850))
        self._button.setFillColor('white')
        self._button.setDepth(20)
        self._front = Text('Defender', (700, 850))
        self._front.setDepth(19)
        
        # Creates pips for first die
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgcolor)
            pip.setDepth(20)
            self._pips.append(pip)
        
        # Creates pips for the second die
        for _ in range(Die.SIDES):
            pip1 = Circle(width / 15, (600, 850))
            pip1.setFillColor(fgcolor)
            pip1.setDepth(20)
            self._pips1.append(pip1)    
        
        # Event Handler for the button
        self._button.addHandler(self)
        self._update()   ### BUG IN DIE!!!
        
    def addTo(self, win):
        """Adds the graphical objects (dies, pips, button) to window"""
        win.add(self._square)
        win.add(self._square1)
        win.add(self._button)
        win.add(self._front)
        for pip in self._pips:
            win.add(pip)
        for pip1 in self._pips1:
            win.add(pip1)
    
    def roll(self):
        """ changes the value of the dice to random numbers between 1 and 
            the number of sides of the dice """
        self._value = random.randrange(Die.SIDES) + 1
        self._value1 = random.randrange(Die.SIDES) + 1
        self._update()
    
    def getValue(self):
        """ return the current value of this die """
        return self._value
    
    def getValue1(self):
        """ return the current value of this die """
        return self._value1    
    
    def descending(self):
        """ Creates a list of the values of the die from greatest to least"""
        greatest = [] 
        if self._value >= self._value1:
            greatest.append(self._value)
            greatest.append(self._value1)
        else:
            greatest.append(self._value1)
            greatest.append(self._value)
        return greatest
    
    def _update(self):
        """ private method: make the dice appearances match their value """
        #self._text.setTextString(str(self._value))
        positions = Die.POSITIONS[self._value]
        positions1 = Die.POSITIONS[self._value1]
        
        # Changes pips for pips on the first die
        for i in range(len(positions)):
            if positions[i] is None:
                self._pips[i].setDepth(25)
            else:
                self._pips[i].setDepth(15)
                cx, cy = self._center  # center of the die.
                dx = positions[i][0] * self._width
                dy = positions[i][1] * self._width  
                self._pips[i].moveTo((cx + dx, cy + dy))
        
        # Changes apperance for pips on the second die
        for i in range(len(positions1)):
            if positions1[i] is None:
                self._pips1[i].setDepth(25)
            else:
                self._pips1[i].setDepth(15)
                cx, cy = (600, 850)  # center of the die.
                dx = positions1[i][0] * self._width
                dy = positions1[i][1] * self._width  
                self._pips1[i].moveTo((cx + dx, cy + dy))
                
    def handleMouseRelease(self, event):
        """ Change values on die when button is clicked and released"""
        self.roll()
        print(self.descending())
        
class Die2(EventHandler):
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
                 
    def __init__(self, board, width=25, center=(400, 875), bgcolor='red', 
                 fgcolor='white'):
        """" Creates three dies for the attacker to roll and records the number
        on the dice"""  
        EventHandler.__init__(self)
        self._board = board
        self._value = 1
        self._value1 = 2
        self._value2 = 3
        self._width = width
        self._center = center
        self._pips = []
        self._pips1 = []
        self._pips2 = []
        
        # Creates the first die
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgcolor)
        self._square.setDepth(20)
        
        # Creates the second die
        self._square1 = Rectangle(width, width, (400, 850))
        self._square1.setFillColor(bgcolor)
        self._square1.setDepth(20)
        
        # Creates the third die
        self._square2 = Rectangle(width, width, (400, 825))
        self._square2.setFillColor(bgcolor)
        self._square2.setDepth(20) 
        
        # Creates button to roll dice
        self._button = Rectangle(50, 30, (300, 850))
        self._button.setFillColor('red')
        self._button.setDepth(20)
        self._front = Text('Attacker', (300, 850))
        self._front.setDepth(19)
        
        # Creates the pips for the first die
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgcolor)
            pip.setBorderColor(fgcolor)
            pip.setDepth(20)
            self._pips.append(pip)
        
        # Creates the pips for the second die
        for _ in range(Die.SIDES):
            pip1 = Circle(width / 15, (400, 850))
            pip1.setFillColor(fgcolor)
            pip1.setBorderColor(fgcolor)
            pip1.setDepth(20)
            self._pips1.append(pip1)    
        
        # Creates the pips for the third die
        for _ in range(Die.SIDES):
            pip2 = Circle(width / 15, (400, 825))
            pip2.setFillColor(fgcolor)
            pip2.setBorderColor(fgcolor)
            pip2.setDepth(20)
            self._pips2.append(pip2)    
        
        # Makes the button an event handler
        self._button.addHandler(self)
        self._update()   ### BUG IN DIE!!!
        
    def addTo(self, win):
        """ Adds the graphical objects (dies, pips, button) to window """
        win.add(self._square)
        win.add(self._square1)
        win.add(self._square2)
        win.add(self._button)
        win.add(self._front)
        for pip in self._pips:
            win.add(pip)
        for pip1 in self._pips1:
            win.add(pip1)
        for pip2 in self._pips2:
            win.add(pip2)
    
    def roll(self):
        """ changes the value of this dice random numbers between 1 and 
            the number of sides of the dice """
        self._value = random.randrange(Die.SIDES) + 1
        self._value1 = random.randrange(Die.SIDES) + 1
        self._value2 = random.randrange(Die.SIDES) + 1
        self._update()
    
    def getValue(self):
        """ return the current value of this dice """
        return self._value 
    
    def getValue1(self):
        """ return the current value of this die """
        return self._value1    
    
    def getValue2(self):
        """ return the current value of this die """
        return self._value2    
    
    def descending(self):
        """ Creates list of values of die from greatest to least"""
        greatest = [] 
        if self._value >= self._value1 and self._value >= self._value2:
            greatest.append(self._value)
            if self._value1 >= self._value2:
                greatest.append(self._value1)
                greatest.append(self._value2)
            else:
                greatest.append(self._value2)
                greatest.append(self._value1)
        elif self._value1 >= self._value and self._value1 >= self._value2:
            greatest.append(self._value1)
            if self._value >= self._value2:
                greatest.append(self._value)
                greatest.append(self._value2)
            else:
                greatest.append(self._value2)
                greatest.append(self._value)
        else:
            greatest.append(self._value2)
            if self._value >= self._value1:
                greatest.append(self._value)
                greatest.append(self._value1)
            else:
                greatest.append(self._value1)
                greatest.append(self._value)
        return greatest
    
    def _update(self):
        """ private method: make this dice appearance match their value """
        #self._text.setTextString(str(self._value))
        positions = Die.POSITIONS[self._value]
        positions1 = Die.POSITIONS[self._value1]
        positions2 = Die.POSITIONS[self._value2]
        
        # Changes appearance of first die
        for i in range(len(positions)):
            if positions[i] is None:
                self._pips[i].setDepth(25)
            else:
                self._pips[i].setDepth(15)
                cx, cy = self._center  # center of the die.
                dx = positions[i][0] * self._width
                dy = positions[i][1] * self._width  
                self._pips[i].moveTo((cx + dx, cy + dy))
        
        # Changes appearance of second die
        for i in range(len(positions1)):
            if positions1[i] is None:
                self._pips1[i].setDepth(25)
            else:
                self._pips1[i].setDepth(15)
                cx, cy = (400, 850)  # center of the die.
                dx = positions1[i][0] * self._width
                dy = positions1[i][1] * self._width  
                self._pips1[i].moveTo((cx + dx, cy + dy))
        
        # Changes appearance of third die
        for i in range(len(positions2)):
            if positions2[i] is None:
                self._pips2[i].setDepth(25)
            else:
                self._pips2[i].setDepth(15)
                cx, cy = (400, 825)  # center of the die.
                dx = positions2[i][0] * self._width
                dy = positions2[i][1] * self._width  
                self._pips2[i].moveTo((cx + dx, cy + dy))        
    
    def handleMouseRelease(self, event):
        """ Change values on die when button is clicked and released"""
        self.roll()
        print(self.descending())

class Card(EventHandler):
    """ Card class"""
    def __init__(self):
        """initializes"""
        EventHandler.__init__(self)
        boardurl = "https://cs.hamilton.edu/~jmadison/images/risk_card.gif"
        self._card = Image(boardurl, center=(500, 850), width=71, height=96)
        self._card.setDepth(10)
        self._card.addHandler(self)
    
    def addTo(self, win):
        """adds"""
        win.add(self._card)

class Piece(EventHandler):
    """piece class"""
    def __init__(self, kind, player):
        """initilizes"""
        EventHandler.__init__(self)
        self._kind = kind
        self._player = player
        self._num = [1] # the length of list determines the number on square
        self._back = Rectangle(25, 25)
        self._back.setDepth(20)
        self._front = Text(len(self._num))
        self._front.setDepth(15)
        self._back.setFillColor(kind)
        self._back.addHandler(self)
        self._front.addHandler(self)
        self._moving = False
        self._location = (0, 0)  # window location of the piece
        self._startPos = None    # mouse position where movement started
        self._active = False
    
    def activate(self):
        """Changes color of border of active square to green"""
        self._active = True
        self._back.setBorderColor('green')
        
    def deactivate(self):
        """Changes color of border of deactive square to black"""
        self._active = False
        self._back.setBorderColor('black')
    
    def addTo(self, win):
        """Adds both the front and back of player's square to window"""
        win.add(self._back)
        win.add(self._front)
    
    def remove(self, win):
        """Removes both the front and back of player's square to window"""
        win.remove(self._back)
        win.remove(self._front)
    
    
    def moveTo(self, pos):
        """Moves both the front and back of player's square to pos"""
        self._back.moveTo(pos)
        self._front.moveTo(pos)
        self._location = pos
    
    def move(self, dx, dy):
        """ Makes the player's piece draggable"""
        oldx, oldy = self._location
        newx = oldx + dx
        newy = oldy + dy
        self.moveTo((newx, newy))
    
    def frontChange(self):
        """Changes the number on the player's square by one"""
        self._num.append(1) 
        self._front.setText(len(self._num))
       
    def change(self, num):
        """changes appearance"""
        self._front.setText(num + 1)
        self._front.setDepth(5)
        self._back.setDepth(10)
        
    def getLocation(self):
        """Returns the location of a piece"""
        return self._location
        
    def getKind(self):
        """ Returns kind of a piece """
        return self._kind
    
    def armies(self):
        """ Returns the length of self._num"""
        return len(self._num)
    
    def handleMouseRelease(self, event):
        """ When clicked, allows the piece to be dragged """
        if not self._active:
            return 
        if self._moving:
            self._moving = False
            self._player.report(self, event)
        else:
            self._moving = True
            self._startPos = event.getMouseLocation()
    
    def handleMouseMove(self, event):
        """ Dragging motion of the piece """
        if not self._active:
            return
        if self._moving:
            oldx, oldy = self._startPos
            newx, newy = event.getMouseLocation()
            self.move(newx - oldx, newy - oldy)
            self._startPos = newx, newy
    
class Cell(EventHandler):
    """ Class for cells of the countries """
    def __init__(self, win, pos, color):
        """ Initializes the cell """
        EventHandler.__init__(self)
        self._location = pos
        self._rect = Rectangle(50, 50, pos)
        self._rect.setFillColor(color)
        self._rect.setDepth(50)
        win.add(self._rect)
        self._tracker = []
        self._count = [1]
        self._piece = None
        self._defending = None
        self._rect.addHandler(self)
    
    def getLocation(self):
        """ Returns the center of a cell """
        return self._location
    
    def numTracker(self):
        """ Tracks and returns the number of times a cell has been clicked"""
        self._tracker.append(1)
        return self._tracker
        
    def getPiece(self):
        """ Returns a single piece in a cell """
        return self._piece
    
    def getPieces(self):
        """ Returns two pieces that are in a cell """
        return (self._piece, self._defending)
        
    def getKind(self):
        """ Returns the kind of a piece """
        return self._piece.getKind()
    
    def depth(self):
        """ a """
        self.getPiece().depth()
    
    def addPiece(self, piece):
        """ Assigns a piece to a cell """
        self._piece = piece
    
    def defend(self, piece):
        """ Assigns a defending pieces to a cell"""
        self._piece = piece
    
    def count(self):
        """ Counts"""
        self._count.append(1)
        return len(self._count)
    
    def change(self):
        """ Adds one two the piece in a cell"""
        self.getPiece().frontChange()
    
    def handleMousePress(self, event):
        """ Calls change when a cell is clicked """
        self.change()    
        
class Player1:
    """"Class to hold the pieces of player 1 """
    def __init__(self, win, kind, board):
        self._pieces = []
        self._board = board
        self._moves = []
        count = 100
        
        for _ in range(count):
            piece = Piece(kind, self)
            piece.addTo(win)
            piece.moveTo((40, 40 + (count - 99) * 200))
            self._pieces.append(piece)        
    
    def report(self, piece, event):
        """ Reports if a piece in placed in any country (group of cells) """
        self._board.report(piece, event)
        self._board.report1(piece, event)
        self._board.report2(piece, event)
        self._board.report3(piece, event)
        self._board.report4(piece, event)
        self._board.report5(piece, event)
    
    def activateAll(self):
        """ Activates all pieces in Player 1 """
        for piece in self._pieces:
            piece.activate()
    
    def removePiece(self, piece):
        """ Removes a piece from the lsit of Player 1 pieces """
        pos = None        
        for i in range(len(self._pieces)):
            if self._pieces[i] == piece:
                pos = i
        if pos != None:
            self._pieces.pop(pos)
                
    def deactivateAll(self):
        """ Deactivates all pieces in Player 1  """
        for piece in self._pieces:
            piece.deactivate() 
    
    def move(self):
        """ Adds one to the number of moves performed """
        self._moves.append(1)

    def moveTrack(self):
        """ Returns the number of moves performed"""
        return self._moves

class Player2:
    """"Class to hold the pieces of player 2 """
    def __init__(self, win, kind, board):
        self._pieces = []
        self._board = board
        self._moves = []
        count = 100
        for _ in range(count):
            piece = Piece(kind, self)
            piece.addTo(win)
            piece.moveTo((40, 40 + (count - 100) * 200))
            self._pieces.append(piece)        
    
    def report(self, piece, event):
        """ Reports if a piece in placed in any country (group of cells) """
        self._board.report(piece, event)
        self._board.report1(piece, event)
        self._board.report2(piece, event)
        self._board.report3(piece, event)
        self._board.report4(piece, event)
        self._board.report5(piece, event)
    
    def activateAll(self):
        """ Activates all pieces in Player 2 """
        for piece in self._pieces:
            piece.activate()
    
    def removePiece(self, piece):
        """ Removes a piece from the lsit of Player 2 pieces """
        pos = None        
        for i in range(len(self._pieces)):
            if self._pieces[i] == piece:
                pos = i
        if pos != None:
            self._pieces.pop(pos)
                
    def deactivateAll(self):
        """ Deactivates all pieces in Player 2  """
        for piece in self._pieces:
            piece.deactivate()
    
    def move(self):
        """ Adds one to the number of moves performed """
        self._moves.append(1)
    
    def moveTrack(self):
        """ Returns the number of moves performed"""
        return self._moves

class Board(EventHandler):
    """ Combines all graphical objects to create game """
    def __init__(self, win):
        """ Initializes the graphical objects, and creates a battle button """
        EventHandler.__init__(self)
        self._endTurn = Rectangle(70, 50, (50, 900))
        self._endTurn.setDepth(20)
        self._endTurn.setFillColor('white')
        self._front = Text('Attack', (50, 900))
        self._front.setDepth(19)
        win.add(self._endTurn)
        win.add(self._front)
        self._win = win
        self._die = Die(self)
        self._die.addTo(win)
        self._die2 = Die2(self)
        self._die2.addTo(win)
        self._game = Game()
        self._game.addTo(win)
        self._card = Card()
        self._card.addTo(win)
        self._players = []
        self._players.append(Player1(win, 'red', self))
        self._players.append(Player2(win, 'blue', self))
        
        # America's Territories
        x, y = 225, 200  # center of the upperleft cell
        self._cells = []
        for row in range(4):
            self._cells.append([])
            for col in range(3):
                newCell = Cell(win, (x + 50 * row, y + 50 * col), 'orange')
                self._cells[-1].append(newCell)
         
        # South America's Terrirtories        
        x1, y1 = 250, 350  # center of the upperleft cell
        self._cells1 = []
        for row in range(3):
            self._cells1.append([])
            for col in range(6):
                newCell1 = Cell(win, (x1 + 50 * row, y1 + 50 * col), 'green')
                self._cells1[-1].append(newCell1)
        
        # Africa's Territories
        x2, y2 = 525, 400  # center of the upperleft cell
        self._cells2 = []
        for row in range(3):
            self._cells2.append([])
            for col in range(4):
                newCell2 = Cell(win, (x2 + 50 * row, y2 + 50 * col), 'red')
                self._cells2[-1].append(newCell2)
        
        # Europe's Territories
        x3, y3 = 475, 250  # center of the upperleft cell
        self._cells3 = []
        for row in range(2):
            self._cells3.append([])
            for col in range(3):
                newCell3 = Cell(win, (x3 + 50 * row, y3 + 50 * col), 'blue')
                self._cells3[-1].append(newCell3)
        
        # Asia's Territories
        x4, y4 = 575, 150  # center of the upperleft cell
        self._cells4 = []
        for row in range(5):
            self._cells4.append([])
            for col in range(5):
                newCell4 = Cell(win, (x4 + 50 * row, y4 + 50 * col), 'yellow')
                self._cells4[-1].append(newCell4)        
        
        # Austrailia's Territories 
        x5, y5 = 750, 500  # center of the upperleft cell
        self._cells5 = []
        for row in range(3):
            self._cells5.append([])
            for col in range(3):
                newCell5 = Cell(win, (x5 + 50 * row, y5 + 50 * col), 'purple')
                self._cells5[-1].append(newCell5)
                
        self._current = 1
        self.changeTurn()        
        self._endTurn.addHandler(self)
    
    def changeTurn(self):
        """ Changes turns of active players """
        self._players[self._current].deactivateAll()
        self._current += 1
        self._current %= 2
        self._players[self._current].activateAll()
    
    def handleMouseRelease(self, event):
        """ When button is clciked the highest of two die are compared"""
        self.battle(self._die, self._die2)
    
    def battle(self, die, die2):
        """ Compares two sets of die to see which have higher values"""
        wins = 0
        rolls = die2.descending()
        rolls1 = die.descending()
        
        for i in range(2):
            if rolls[i] > rolls1[i]:
                wins += 1
        print(wins)
        return wins
    
    def computeLanding(self, piece):
        """ Determine the cell where a piece was placed,
            as long as that cell is legal.
            Otherwise, None """
        x0, y0 = self._cells[0][0].getLocation()
        x0 -= 25
        y0 -= 25
        x1, y1 = piece.getLocation()
        row = (x1 - x0) // 50
        col = (y1 - y0) // 50
        if row < 0 or col < 0 or row > 3 or col > 2:
            return None
        if self._cells[row][col].getPiece() != None:
            if self._cells[row][col].getKind() == piece.getKind():
                self._players[self._current].move()
                if len(self._players[self._current].moveTrack()) == 5:
                    self.changeTurn()
                    self._players[self._current].movereset()
                return (self._cells[row][col], 1)
            else:
                self._players[self._current].move()
                if len(self._players[self._current].moveTrack()) == 5:
                    self.changeTurn()
                    self._players[self._current].movereset()
                return (self._cells[row][col], 2)
        self._players[self._current].move()
        if len(self._players[self._current].moveTrack()) == 5:
            self.changeTurn()
            self._players[self._current].movereset()
        return (self._cells[row][col], 0)
    
    def computeLanding1(self, piece):
        """ Determine the cell where a piece was placed,
            as long as that cell is legal.
            Otherwise, None """
        x0, y0 = self._cells1[0][0].getLocation()
        x0 -= 25
        y0 -= 25
        x1, y1 = piece.getLocation()
        row = (x1 - x0) // 50
        col = (y1 - y0) // 50
        if row < 0 or col < 0 or row > 2 or col > 5:
            return None
        if self._cells1[row][col].getPiece() != None:
            if self._cells1[row][col].getKind() == piece.getKind():
                self._players[self._current].move()
                if len(self._players[self._current].moveTrack()) == 5:
                    self.changeTurn()
                return (self._cells1[row][col], 1)
            else:
                self._players[self._current].move()
                if len(self._players[self._current].moveTrack()) == 5:
                    self.changeTurn()
                return (self._cells1[row][col], 2)
        self._players[self._current].move()
        if len(self._players[self._current].moveTrack()) == 5:
            self.changeTurn()
            
        return (self._cells1[row][col], 0)
    
    def computeLanding2(self, piece):
        """ Determine the cell where a piece was placed,
            as long as that cell is legal.
            Otherwise, None """
        x0, y0 = self._cells2[0][0].getLocation()
        x0 -= 25
        y0 -= 25
        x1, y1 = piece.getLocation()
        row = (x1 - x0) // 50
        col = (y1 - y0) // 50
        if row < 0 or col < 0 or row > 2 or col > 3:
            return None
        if self._cells2[row][col].getPiece() != None:
            if self._cells2[row][col].getKind() == piece.getKind():
                self._players[self._current].move()
                if len(self._players[self._current].moveTrack()) == 5:
                    self.changeTurn()
                return (self._cells2[row][col], 1)
            else:
                self._players[self._current].move()
                if len(self._players[self._current].moveTrack()) == 5:
                    self.changeTurn()
                return (self._cells2[row][col], 2)
        self._players[self._current].move()
        if len(self._players[self._current].moveTrack()) == 5:
            self.changeTurn()
        return (self._cells2[row][col], 0)
    
    def computeLanding3(self, piece):
        """ Determine the cell where a piece was placed,
            as long as that cell is legal.
            Otherwise, None """
        x0, y0 = self._cells3[0][0].getLocation()
        x0 -= 25
        y0 -= 25
        x1, y1 = piece.getLocation()
        row = (x1 - x0) // 50
        col = (y1 - y0) // 50
        if row < 0 or col < 0 or row > 1 or col > 2:
            return None
        if self._cells3[row][col].getPiece() != None:
            if self._cells3[row][col].getKind() == piece.getKind():
                self._players[self._current].move()
                if len(self._players[self._current].moveTrack()) == 5:
                    self.changeTurn()
                return (self._cells3[row][col], 1)
            else:
                self._players[self._current].move()
                if len(self._players[self._current].moveTrack()) == 5:
                    self.changeTurn()
                return (self._cells3[row][col], 2)
        self._players[self._current].move()
        if len(self._players[self._current].moveTrack()) == 5:
            self.changeTurn()
        return (self._cells3[row][col], 0)
        
    def computeLanding4(self, piece):
        """ Determine the cell where a piece was placed,
            as long as that cell is legal.
            Otherwise, None """
        x0, y0 = self._cells4[0][0].getLocation()
        x0 -= 25
        y0 -= 25
        x1, y1 = piece.getLocation()
        row = (x1 - x0) // 50
        col = (y1 - y0) // 50
        if row < 0 or col < 0 or row > 4 or col > 4:
            return None
        if self._cells4[row][col].getPiece() != None:
            if self._cells4[row][col].getKind() == piece.getKind():
                self._players[self._current].move()
                if len(self._players[self._current].moveTrack()) == 5:
                    self.changeTurn()
                return (self._cells4[row][col], 1)
            else:
                self._players[self._current].move()
                if len(self._players[self._current].moveTrack()) == 5:
                    self.changeTurn()
                return (self._cells4[row][col], 2)
        self._players[self._current].move()
        if len(self._players[self._current].moveTrack()) == 5:
            self.changeTurn()
        return (self._cells4[row][col], 0)
    
    def computeLanding5(self, piece):
        """ Determine the cell where a piece was placed,
            as long as that cell is legal.
            Otherwise, None """
        x0, y0 = self._cells5[0][0].getLocation()
        x0 -= 25
        y0 -= 25
        x1, y1 = piece.getLocation()
        row = (x1 - x0) // 50
        col = (y1 - y0) // 50
        if row < 0 or col < 0 or row > 2 or col > 2:
            return None
        if self._cells5[row][col].getPiece() != None:
            if self._cells5[row][col].getKind() == piece.getKind():
                self._players[self._current].move()
                if len(self._players[self._current].moveTrack()) == 5:
                    self.changeTurn()
                return (self._cells5[row][col], 1)
            else:
                self._players[self._current].move()
                if len(self._players[self._current].moveTrack()) == 5:
                    self.changeTurn()
                return (self._cells5[row][col], 2)
        self._players[self._current].move()
        if len(self._players[self._current].moveTrack()) == 5:
            self.changeTurn()
        return (self._cells5[row][col], 0)
    
    def report(self, piece, event):
        """ Places the piece in the appropriate cell in the America """
        landing = self.computeLanding(piece) #Orange Cells
        if landing != None: #Checks first for a piece
            loc = landing[0].getLocation()
            if landing[1] == 1: # if a piece of same kind occupies cell
                loc = landing[0].getLocation()
                landing[0].getPiece().remove(self._win)
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0], loc[1]))
                piece.change(len(landing[0].numTracker()))
                
            elif landing[1] == 2: # if a piece of another kind is in cell
                landing[0].defend(landing[0].getPiece())
                landing[0].getPiece().moveTo((loc[0] - 12.5, loc[1]))
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                result = self.battle(self._die, self._die2)
                piece.moveTo((loc[0] + 12.5, loc[1]))
                if result == 0:
                    landing[0].getPieces()[0].remove(self._win)
            
            else: # if no piece of any kind occupie cell
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0], loc[1]))
    
    def report1(self, piece, event):
        """ Places the piece in the appropriate cell, if any """
        landing = self.computeLanding1(piece) #Green cells
        if landing != None: #Checks first for a piece
            loc = landing[0].getLocation()
            if landing[1] == 1: # if a piece of same kind occupies cell
                loc = landing[0].getLocation()
                landing[0].getPiece().remove(self._win)
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0], loc[1]))
                piece.change(len(landing[0].numTracker()))
                
            elif landing[1] == 2: # if a piece of another kind is in cell
                landing[0].getPiece().moveTo((loc[0] - 12.5, loc[1]))
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0] + 12.5, loc[1]))
                
            else: # if no piece of any kind occupie cell
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0], loc[1]))

    def report2(self, piece, event):
        """ Places the piece in the appropriate cell, if any """
        landing = self.computeLanding2(piece) # Red cells
        if landing != None: #Checks first for a piece
            loc = landing[0].getLocation()
            if landing[1] == 1: # if a piece of same kind occupies cell
                loc = landing[0].getLocation()
                landing[0].getPiece().remove(self._win)
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0], loc[1]))
                piece.change(len(landing[0].numTracker()))
                
            elif landing[1] == 2: # if a piece of another kind is in cell
                landing[0].getPiece().moveTo((loc[0] - 12.5, loc[1]))
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0] + 12.5, loc[1]))
            
            else: # if no piece of any kind occupie cell
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0], loc[1]))
                
    def report3(self, piece, event):
        """ Places the piece in the appropriate cell, if any """
        landing = self.computeLanding3(piece) # Blue Cells
        if landing != None: #Checks first for a piece
            loc = landing[0].getLocation()
            if landing[1] == 1: # if a piece of same kind occupies cell
                loc = landing[0].getLocation()
                landing[0].getPiece().remove(self._win)
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0], loc[1]))
                piece.change(len(landing[0].numTracker()))
                
            elif landing[1] == 2: # if a piece of another kind is in cell
                landing[0].getPiece().moveTo((loc[0] - 12.5, loc[1]))
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0] + 12.5, loc[1]))
            
            else: # if no piece of any kind occupie cell
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0], loc[1]))

    def report4(self, piece, event):
        """ Places the piece in the appropriate cell, if any """
        landing = self.computeLanding4(piece) # Yellow cells
        if landing != None: #Checks first for a piece
            loc = landing[0].getLocation()
            if landing[1] == 1: # if a piece of same kind occupies cell
                loc = landing[0].getLocation()
                landing[0].getPiece().remove(self._win)
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0], loc[1]))
                piece.change(len(landing[0].numTracker()))
                
            elif landing[1] == 2: # if a piece of another kind is in cell
                landing[0].getPiece().moveTo((loc[0] - 12.5, loc[1]))
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0] + 12.5, loc[1]))

            else: # if no piece of any kind occupie cell
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0], loc[1]))
                
    def report5(self, piece, event):
        """ Places the piece in the appropriate cell, if any """
        landing = self.computeLanding5(piece) #purple cells
        if landing != None: #Checks first for a piece
            loc = landing[0].getLocation()
            if landing[1] == 1: # if a piece of same kind occupies cell
                loc = landing[0].getLocation()
                landing[0].getPiece().remove(self._win)
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0], loc[1]))
                piece.change(len(landing[0].numTracker()))
                
            elif landing[1] == 2: # if a piece of another kind is in cell
                landing[0].getPiece().moveTo((loc[0] - 12.5, loc[1]))
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0] + 12.5, loc[1]))

            else: # if no piece of any kind occupie cell
                piece.deactivate()
                self._players[self._current].removePiece(piece)
                landing[0].addPiece(piece)
                piece.moveTo((loc[0], loc[1]))

def play(win):
    """ Calls board to a win """
    Board(win)
    
StartGraphicsSystem(play, 1000, 1000)
