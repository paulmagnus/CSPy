"""
*******************************************************************************
Title: Game.py
Author: Kyle Gately
Partner: Owen McCarthy
Date: 5/2/17
Description: The game that ruins friendships: SORRY! Draw cards to move 
pieces around the board. First player to get all four of their pieces into their home-space wins. Happy playing!
*******************************************************************************
"""
import random
from cs110graphics import *

class BoardSpace:
    """A class for initializing the playable parts of the board"""
    def __init__(self, board, center, color, win):
        self._color = color
        self._board = board
        self._win = win
        self._center = center
        self._square = Rectangle(20, 20, center)

    def addTo(self, win):
        """Adds object to window"""
        win.add(self._square)
    
    def getCenter(self):
        """Returns center"""
        return self._center

class Piece(EventHandler):
    def __init__(self, color, board, position, win):
        """Creates and adds the 16 Sorry pieces to the window"""
        EventHandler.__init__(self)
        self._color = color
        self._position = position
        self._board = board
        self._position = position
        self._rpawn1 = Circle(5, (329, 123))
        self._rpawn2 = Circle(5, (324, 127))
        self._rpawn3 = Circle(5, (318, 123))
        self._rpawn4 = Circle(5, (322, 127))
        self._bpawn1 = Circle(5, (274, 317))
        self._bpawn2 = Circle(5, (270, 322))
        self._bpawn3 = Circle(5, (267, 324))
        self._bpawn4 = Circle(5, (262, 319))
        self._ypawn1 = Circle(5, (85, 269))
        self._ypawn2 = Circle(5, (80, 274))
        self._ypawn3 = Circle(5, (77, 270))
        self._ypawn4 = Circle(5, (72, 276))
        self._gpawn1 = Circle(5, (135, 80))
        self._gpawn2 = Circle(5, (130, 87))
        self._gpawn3 = Circle(5, (126, 80))
        self._gpawn4 = Circle(5, (122, 86))
        
        self._rpawn1.setFillColor('red')
        self._rpawn2.setFillColor('red')
        self._rpawn3.setFillColor('red')
        self._rpawn4.setFillColor('red')
        self._bpawn1.setFillColor('blue')
        self._bpawn2.setFillColor('blue')
        self._bpawn3.setFillColor('blue')
        self._bpawn4.setFillColor('blue')
        self._ypawn1.setFillColor('yellow')
        self._ypawn2.setFillColor('yellow')
        self._ypawn3.setFillColor('yellow')
        self._ypawn4.setFillColor('yellow')
        self._gpawn1.setFillColor('green')
        self._gpawn2.setFillColor('green')
        self._gpawn3.setFillColor('green')
        self._gpawn4.setFillColor('green')
        
    def addTo(self, win):
        """Adds objects to the window"""
        win.add(self._rpawn1)
        win.add(self._rpawn2)
        win.add(self._rpawn3)
        win.add(self._rpawn4)
        win.add(self._bpawn1)
        win.add(self._bpawn2)
        win.add(self._bpawn3)
        win.add(self._bpawn4)
        win.add(self._ypawn1)
        win.add(self._ypawn2)
        win.add(self._ypawn3)
        win.add(self._ypawn4)
        win.add(self._gpawn1)
        win.add(self._gpawn2)
        win.add(self._gpawn3)
        win.add(self._gpawn4)
        
    def setPosition(self, pos):
        """Initializes a value for self._position"""
        self._position = pos

    def getPosition(self):
        """Returns the center of an object"""
        return self._position
        
    def moveTo(self, location):
        """Implements the moving of pieces on the 2D array"""
        self._position = location
        location = self._board._board[location[0]][location[1]]._center
        
    def handleMouseRelease(self):
        """Handles the physical action of the user"""
        self.calcNewSpot(self._board._deck.getValues())
        self.moveTo(self._board.calcNewSpot(self))
    
    def calcNewSpot(self, numMoves):
        """Calculates the new spot that a piece will land given the card that
            was flipped"""
        if numMoves == 'S':
            numMoves = 1
            
        for i in range(int(numMoves)):
            if self._position[0] == 0 and self._position[1] < 15:
                self._position = (self._position[0], self._position[1] + 1)
            elif self._position[0] < 15 and self._position[1] == 15:
                self._position = (self._position[0] + 1, self._position[1])
            elif self._position[0] == 15 and self._position[1] > 0:
                self._position = (self._position[0], self._position[1] - 1)
            elif self._position[0] > 0 and self._position[1] == 0:
                self._position = (self._position[0] - 1, self._position[1])

def print_board(board):
    for spot in board:
        for spot2 in spot:
            if spot2 != None:
                print('X ', end='')
            else:
                print('_ ', end='')
        print('')
    
    
class Board:
    """A class for designing the outline of the Sorry board spaces"""
    def __init__(self, win):
        """Sets up the playable parts of the board"""
        self._board = [[None for i in range(16)] for j in range(16)]
        self._spaces = []
        position = (0,0)
        xpos = 50
        ypos = 50
        self._circle = Circle(40, (200, 200))
        self._lastPlayerNum = 0
        self._currentPlayerNum = 0
        
        self._bstartCirc = Circle(20, (270, 319))
        self._board[14][11] = self._bstartCirc
        self._bhomeCirc = Circle(25, (310, 215))
        self._board[10][13] = self._bhomeCirc
        
        self._ystartCirc = Circle(20, (80, 270))
        self._board[11][1] = self._ystartCirc
        self._yhomeCirc = Circle(25, (185, 309))
        self._board[13][5] = self._yhomeCirc
        
        self._gstartCirc = Circle(20, (130, 80))
        self._board[1][4] = self._gstartCirc
        self._ghomeCirc = Circle(25, (91, 185))
        self._board[5][2] = self._ghomeCirc
        
        self._rstartCirc = Circle(20, (320, 130))
        self._board[4][14] = self._rstartCirc
        self._rhomeCirc = Circle(25, (215, 90))
        self._board[2][7] = self._rhomeCirc

        win.add(self._bstartCirc)
        win.add(self._bhomeCirc)
        win.add(self._ystartCirc)
        win.add(self._yhomeCirc)
        win.add(self._rhomeCirc)
        win.add(self._rstartCirc)
        win.add(self._ghomeCirc)
        win.add(self._gstartCirc)

        for i in range(15):
            color = 'white'
            thisSpace = BoardSpace(self, (xpos, ypos), color, win)
            thisSpace.addTo(win)
            self._spaces.append(thisSpace)
            self._board[position[0]][position[1]] = thisSpace
            xpos += 20
            
            if i == 1:
                for j in range(5):
                    ypos += 20
                    color = 'green'
                    thisSpaceHome1 = BoardSpace(self, (xpos, ypos), color, win)
                    thisSpaceHome1.addTo(win)
                    self._spaces.append(thisSpaceHome1)
                    self._board[j][2] = thisSpaceHome1
                ypos -= 100
            position = (position[0], position[1] + 1)

        for i in range(15):
            color = 'white'
            thisSpace1 = BoardSpace(self, (xpos, ypos), color, win)
            thisSpace1.addTo(win)
            self._spaces.append(thisSpace1)
            ypos += 20
            self._board[position[0]][position[1]] = thisSpace1
            
            if i == 1:
                z = 14
                for j in range(5):
                    xpos -= 20
                    color = 'red'
                    thisSpaceHome1 = BoardSpace(self, (xpos, ypos), color, win)
                    thisSpaceHome1.addTo(win)
                    self._spaces.append(thisSpaceHome1)
                    self._board[2][z] = thisSpaceHome1
                    z -= 1
                xpos += 100
            position = (position[0] + 1, position[1])

        for i in range(15):
            color = 'white'
            thisSpace2 = BoardSpace(self, (xpos, ypos), color, win)
            thisSpace2.addTo(win)
            self._spaces.append(thisSpace2)
            xpos -= 20
            self._board[position[0]][position[1]] = thisSpace2

            if i == 1:
                z = 15
                for _ in range(5):
                    ypos -= 20
                    color = 'blue'
                    thisSpaceHome1 = BoardSpace(self, (xpos, ypos), color, win)
                    thisSpaceHome1.addTo(win)
                    self._spaces.append(thisSpaceHome1)
                    self._board[z][13] = thisSpaceHome1
                    z -= 1
                ypos += 100
            position = (position[0], position[1] - 1)

        for i in range(15):
            color = 'white'
            thisSpace3 = BoardSpace(self, (xpos, ypos), color, win)
            thisSpace3.addTo(win)
            self._spaces.append(thisSpace3)
            ypos -= 20
            self._board[position[0]][position[1]] = thisSpace3

            if i == 1:
                for j in range(5):
                    xpos += 20
                    color = 'yellow'
                    thisSpaceHome1 = BoardSpace(self, (xpos, ypos), color, win)
                    thisSpaceHome1.addTo(win)
                    self._spaces.append(thisSpaceHome1)
                    self._board[13][j] = thisSpaceHome1
                xpos -= 100
            position = (position[0] - 1, position[1])

        self._pieces = []
        self._players = []
        for color, which in [('yellow', 0), ('blue', 1), ('red', 2), \
                             ('green', 3)]:
            player = Player(color, which)
            for _ in range(4):
                thisPiece = Piece(self, color, which, (0, 0))
                player.addPiece(thisPiece)
                thisPiece.addTo(win)
                self._pieces.append(player)
            self._players.append(player)
        
    def changeTurn(self):
        """Switches turns based on the sequential order of players"""
        self._lastPlayerNum = self._currentPlayerNum
        self._lastPlayer = self._players[self._lastPlayerNum]
        self._lastPlayer.deactivate()
        self._currentPlayerNum = (self._currentPlayerNum + 1) % 4
        self._currentPlayer = self._players[self._currentPlayerNum]
        self._currentPlayer.activate()

#CITE: SAM KNOLLMEYER
#NOTE: Suggested that another class be made to code the colors of the Sorry
#board.

class Space:
    """A class for adding pieces to their start positions and color coding the
        board"""
    def __init__(self, win, pos, color):
        self._location = pos
        self._color = color
        self._square = Rectangle(20, 20, pos)
        win.add(self._square)
        
    def getLocation(self):
        """Returns the center coordinates of the piece"""
        return self._location
        
    def getPiece(self):
        """Returns a piece in self._pieces"""
        return self._piece
        
    def addPiece(self, piece):
        """Initializes a value for piece"""
        self._piece = piece
        
    def addTo(self, win):
        """Adds object to the window"""
        win.add(self._square)
        
    def colorIt(self, color):
        """Changes the color of the squares in the board"""
        self._square.setFillColor(color)
        
class Player:
    """A class for changing player turns and activating/deactivating pieces"""
    def __init__(self, color, win):
        self._pieces = []
        
    def addPiece(self, piece):
        self._pieces.append(piece)
        
    def activate(self):
        """Activates the player's pieces if it is that player's turn"""
        for piece in self._pieces:
            piece.activate()
    
    def deactivate(self):
        """Deactivates the player's pieces if it's not that player's turn"""
        for piece in self._pieces:
            piece.deactivate()
    
class Deck:
    """A class for building a deck of cards. This class is not graphical"""
    def __init__(self):
        """Creates a complete deck of 52 playing cards."""
        self._deck = []
        self._shuffled = []
    
        for values in ['S', 'S', 'S', 'S', '1', '1', '1', '1', '1', '2', \
        '2', '2', '2', '3', '3','3', '3', '4', '4', '4', '4', '5', '5', '5',\
        '5', '7', '7', '7', '7','8', '8', '8', '8', '10', '10', '10', '10',\
        '11', '11', '11', '11', '12', '12', '12', '12']:
            self._deck.append(Card(values))
    
    def empty(self):
        """Returns True if the deck no longer contains any cards. Otherwise
        false is returned."""
        return self._deck == []
        
        
    def shuffle(self):
        """All cards currently in the deck are randomly ordered. You will want
        to use Python's randrange function in the random module. You may not
        use any other functions from this module."""
        for _ in range(45):
            positioncard = random.randrange(45 - _)
            self._shuffled.append(self._deck[positioncard])
            self._deck.remove(self._deck[positioncard])
        self._deck = self._shuffled
        return self._deck
    
    def deal(self):
        """Deals a card. A card is removed from the top of the deck and
        returned."""
    
        top = self._deck[0]
        self._deck.remove(top)
        return top
        
class Card:
    """A class used for building graphical playing cards"""
    def __init__ (self, values):
        """Creates a playing card with the given suit and name. suit is one of
        the names: "clubs," "diamonds", "hearts", or "spades". The name is
        one of the names: "ace", "2", "3", ..., "10", "jack", "queen", "king".
        The card is face down."""
        self._width = 71
        self._height = 96
        self._center = 600,  200
        self._values = values
        
        self._faceFileName = values
        
        self._faceup = False
        self._inWind = False
        faceurl = "https://cs.hamilton.edu/~omccarth/images/sorry" \
        + self._faceFileName
        self._face = Image(faceurl, self._center, self._width, self._height)
        backurl = "https://cs.hamilton.edu/~omccarth/images/sorryB"
        self._back = Image(backurl, self._center, self._width,self._height)
        self._depth = 10
        self._face.setDepth(self._depth+ 1 )
        self._back.setDepth(self._depth)
    
    def getValues(self):
        """Returns the value of the card."""
        return self._values
    
    def addTo(self, win):
        """Adds the card to the given graphics window."""
        win.add(self._face)
        win.add(self._back)
        self._inWind = True
    
    def removeFrom(self, win):
        """Removes the card from the given graphics window. You cannot remove
        a card that hasn't been added previously."""
        win.remove(self._face)
        self._inWind = True
        
    def flip(self):
        """Flips the card over. If face down, the card is flipped to face up,
        or vice versa. This visually flips the card over as well. May be called
        on all cards whether they have been added to a window or not."""
        x = self._back.getDepth()
        y = self._face.getDepth()
    
        self._back.setDepth(y)
        self._face.setDepth(x)
    
    def move(self, dx, dy):
        """Moves a card by dx and dy."""
        self._face.move(dx, dy)
        self._back.move(dx, dy)
        
    def getReferencePoint(self):
        """The point representing the center of the card image is returned"""
        return self._center
    
    def size(self):
        """Returns the tuple (width, height)"""
        return (self._width, self._height)
    
    def setDepth(self, depth):
        """Sets the depth of graphical objects representing the card to
        depth"""
        bDepth = self._back.getDepth()
        fDepth = self._face.getDepth()
        
        if bDepth < fDepth:
            self._face.setDepth(depth +1)
            self._back.setDepth(depth)
        else:
            self._face.setDepth(depth)
            self._back.setDepth(depth +1)
        
class Controller(EventHandler):
    def __init__(self, win, board):
        """Sets up objects in the window for display"""
        
        EventHandler.__init__(self)
        self._window = win
        self._board = board
        self._deck = Deck()
        self._deck.shuffle()
        self._card = self._deck.deal()
        self._card.addTo(win)
        
        self._button = Rectangle(50, 50, (600, 75))
        self._button.setFillColor('blue')
        win.add(self._button)
        self._button.addHandler(self) #the controller is a handler for the 
                                        # buttons events
                                        
    def handleMouseRelease(self, event):
        """Handles the physical action of the user"""
        self._card.flip()
        self._card.move(100, 0)
        if self._deck.empty():
            return
        self._card = self._deck.deal()
        self._card.addTo(self._window)
     
def gameOver(board):
    pass
    print('GAME OVER! YOU HAVE WON!')

def play(win):
    board = Board(win)
    _ = Controller(win, board)


        
StartGraphicsSystem(play, 750, 750)
    
        
