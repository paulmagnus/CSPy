"""
********************************************************************************
FILE:        Game.py

AUTHOR:      Julia McGuire

PARTNER:     

ASSIGNMENT:  Project 6

DATE:        05/01/17

DESCRIPTION: This is a program that creates a version of the board game
             "Scrabble" through the use of classes. Certain classes will hold
             different ojects and methods for the game and each class is
             seperate from one another, only to be accessed by the controller
             class. The controller is ultimately the central command for 
             action in the game.
********************************************************************************
"""

import random
from cs110graphics import *

class BoardSpace:
    """A class for creating an individual space that will be used for making 
       the full board"""
    def __init__(self, board, center, color, pos):
        """Creates the attributes for a scrabble game space"""
        self._board = board
        self._center = center
        self._location = pos
        self._square = Rectangle(30, 30, center)
        self._square.setFillColor(color)

    def changeColor(self, color):
        """Method for changing color of a boardspace"""
        self._square.setFillColor(color)

    def addTo(self, win):
        """Adds the graphical object to the window"""
        win.add(self._square)

class Board:
    """A class that creates the full game board and identifies special spaces"""
    def __init__(self, win):
        """Creates the board using a list of spaces"""
        self._spaces = []
        xpos = 120
        ypos = 120
        
        #makes the 15 x 15 board by utilizing a rows of rows
        for _ in range(15):
            row = []
            for __ in range(15):
                thisSpace = BoardSpace(self, (xpos, ypos), 'tan', (xpos, ypos))
                thisSpace.addTo(win)
                row.append(thisSpace)
                xpos += 30
            xpos = 120
            ypos += 30
            self._spaces.append(row)
        
        #identifying the special tile for the start of the game at the center 
        #of the board by changing its color
        self._startTile = self._spaces[7][7].changeColor('green')
        
        self._DWS = []
        #list with the row index for each tile used in a DWS (double word score)
        lstDWS = [1, 2, 3, 4, 10, 11, 12, 13]
        begin = len(lstDWS) - 1
        for row in lstDWS:
            col = lstDWS[begin]
            self._DWS.append(self._spaces[row][row])
            self._spaces[row][row].changeColor('deeppink')
            self._DWS.append(self._spaces[row][col])
            self._spaces[row][col].changeColor('deeppink')
            begin -= 1
        
        self._TWS = []
        #list with the row index for each tile used in a TWS (triple word score)
        lstTWS = [0, 14]
        begin = len(lstTWS) - 1
        for row in lstTWS:
            col = lstTWS[begin]
            self._TWS.append(self._spaces[row][row])
            self._spaces[row][row].changeColor('orangered')
            self._TWS.append(self._spaces[row][col])
            self._spaces[row][col].changeColor('orangered')
            begin -= 1
        self._TWS.append(self._spaces[0][7])    
        self._spaces[0][7].changeColor('orangered')
        self._TWS.append(self._spaces[7][0])    
        self._spaces[7][0].changeColor('orangered')
        self._TWS.append(self._spaces[7][14])    
        self._spaces[7][14].changeColor('orangered')
        self._TWS.append(self._spaces[14][7])    
        self._spaces[14][7].changeColor('orangered')
        
        #using loop to match up indices for double letter score spaces
        self._DLS = []
        rowDLS = [0, 0, 2, 2, 3, 3, 3, 6, 6, 6, 6, 7, 7, 8, 8, 8, 8, 11, 
                  11, 11, 12, 12, 14, 14]
        colDLS = [3, 11, 6, 8, 0, 7, 14, 2, 6, 8, 12, 3, 11, 2, 6, 8, 12, 
                  0, 7, 14, 6, 8, 3, 11]
        for i in range(len(rowDLS)):
            self._DLS.append(self._spaces[rowDLS[i]][colDLS[i]])
            self._spaces[rowDLS[i]][colDLS[i]].changeColor('lightblue')
            
        #using loop to match up indices for triple letter score spaces
        self._TLS = []
        rowTLS = [1, 1, 5, 5, 5, 5, 9, 9, 9, 9, 13, 13]
        colTLS = [5, 9, 1, 5, 9, 13, 1, 5, 9, 13, 5, 9]
        for i in range(len(rowTLS)):
            self._TLS.append(self._spaces[rowTLS[i]][colTLS[i]])
            self._spaces[rowTLS[i]][colTLS[i]].changeColor('blue')
    
    def computeLanding(self, piece):
        """ Return the empty cell where the user has left the piece """
        x0, y0 = self._spaces[0][0].getLocation()
        x0 -= 15 # left edge
        y0 -= 15 # top
        x1, y1 = piece.getLocation()
        row = (x1 - x0) // 30
        col = (y1 - y0) // 30
        
        if row < 0 or col < 0 or row > 14 or col > 14:
            return None
        if self._spaces[row][col].getPiece() != None:
            return None
        return self._spaces[row][col]
        
    def report(self, piece):
        """Reports that the piece has moved to the cell found in landing"""
        landing = self.computeLanding(piece)
        if landing != None:
            landing.addPiece(piece)
            piece.moveTo(landing.getLocation())
            
class Key:
    """A class primarily for the graphical objects that make up the "Key" 
       for the game"""
    def __init__(self):
        """Creates the following attributes that are all graphical objects 
           for the game's Key"""
        #this class exists mainly because when it was within a previous 
        #class, pynt would run very slowly
        
        self._title = Text('Scrabble!', (330, 65), 58)
        
        self._keyText = Text('Key!', (630, 60), 18)
        self._keyBox = Rectangle(120, 130, (630, 100))
        self._keyBox.setFillColor('pink')
        self._key1 = Rectangle(10, 10, (580, 70))
        self._key1.setFillColor('green')
        self._text1 = Text(' Start Tile', (630, 75), 10)
        self._key2 = Rectangle(10, 10, (580, 90))
        self._key2.setFillColor('deeppink')
        self._text2 = Text('  Double Word Score', (635, 95), 10)
        self._key3 = Rectangle(10, 10, (580, 110))
        self._key3.setFillColor('orangered')
        self._text3 = Text(' Triple Word Score', (630, 115), 10)
        self._key4 = Rectangle(10, 10, (580, 130))
        self._key4.setFillColor('lightblue')
        self._text4 = Text('  Double Letter Score', (635, 135), 10)
        self._key5 = Rectangle(10, 10, (580, 150))
        self._key5.setFillColor('blue')
        self._text5 = Text(' Triple Letter Score', (630, 155), 10)

    def addTo(self, win):
        """Adds each graphical object to the window by looping through a list
           of the objects"""
        features = [self._keyBox, self._keyText, self._title, 
                    self._text1, self._text2, self._text3, self._text4, 
                    self._text5, self._key1, self._key2, self._key3, 
                    self._key4, self._key5]
        for i in range(len(features)):
            win.add(features[i])
            
class Directions(EventHandler):
    """A class that creates a box for game directions"""
    def __init__(self):
        """Initializing the box's features"""
        EventHandler.__init__(self)
        self._directionsBox = Rectangle(120, 60, (630, 200))
        self._directionsBox.setFillColor('teal')
        self._directionsBox.addHandler(self)
        self._directionsText1 = Text('Click Here', (630, 200), 20)
        self._directionsText2 = Text('for Directions', (630, 220), 20)

    def addTo(self, win):
        """Adds the direction box features to the window"""
        win.add(self._directionsBox)
        win.add(self._directionsText1)
        win.add(self._directionsText2)
        
    def handleMouseRelease(self, event):
        """Creates an input that has the game directions"""
        input("Game Directions: (1) Press the space bar to begin the game. \
              The first player will start by moving his/her pieces from the \
              holder to the board to form a word. (2) Once satified with the \
              word, the player will press 'Done with Turn!' button, which \
              will switch turns to the second player. Once a word is made, the \
              second player will press 'Done with Turn'. (3) Now the first  \
              player will click the bag the deal the necessary tiles needed to \
              fill the 7 holders. The dealt pieces will appear in the white \
              square. (4) Should a word be challenged, press the 'Challenge' \
              button and answer the question accordingly. (5) Have fun and \
              scrabble on!")

class Piece(EventHandler):
    """A class for creating the game pieces"""
    def __init__(self, letter, value, player):
        """Initializing each attribute for a piece"""
        EventHandler.__init__(self)
        self._letter = letter
        self._value = value
        self._player = player
        self._place = (75, 77)
        self._FVplace = (85, 85)
        self._frontLetter = Text(letter, (self._place), 16)
        self._frontValue = Text(value, (self._FVplace), 8)
        self._back = Rectangle(27, 27, (self._place))
        self._back.setFillColor('beige')
        self._frontLetter.addHandler(self)
        self._frontValue.addHandler(self)
        self._back.addHandler(self)
        self._moving = False
        self._location = (0, 0)
        self._startLoc = None
        self._active = False
    
    def activate(self):
        """Method that changes piece activation to True and identifies 
           activation by changing border color"""
        self._active = True
        self._back.setBorderColor('green')
        
    def deactivate(self):
        """Method that changes piece activation to False and identifies 
           deactivation by changing border color back to black"""
        self._active = False
        self._back.setBorderColor('black')
    
    def setLocation(self, location):
        """Set the piece's location"""
        self._location = location
    
    def getLocation(self):
        """Return's the piece's location"""
        return self._location
    
    #this method is ultimately not used in the program because I did not 
    #have enough time to implement it correctly but it would have been used 
    #to make scoring easier to calculate    
    def getValue(self):
        """Returns a tuple in the form of (tileValue, word multiplier) 
           depending on the piece's location"""
        if self._location == 'TWS':
            return (self._value, 3)
        elif self._location == 'DWS':
            return (self._value, 2)
        elif self._location == 'TLS':
            return (self._value * 3, 1)
        elif self._location == 'DLS':
            return (self._value * 2, 1)
        elif self._location == 'regular':
            return (self._value, 1)
    
    def moveTo(self, pos):
        """Moves piece to a desired location"""
        #help from TA Emily
        #had to make sure that each part of the piece (both texts and the 
        #actual square) was moving to a location and staying in its 
        #respective spot on the tile
        self._frontLetter.moveTo(pos)
        self._frontValue.moveTo((pos[0] + 10, pos[1] + 8))
        self._back.moveTo(pos)
        self._location = pos

    def move(self, dx, dy):
        """Moves piece by a dx and dy"""
        #reassigns the location by adding the change in distance
        oldx, oldy = self._location
        newx = oldx + dx
        newy = oldy + dy
        self.moveTo((newx, newy))

    def getLetter(self):
        """Returns the letter value of the piece"""
        return self._letter

    def addTo(self, win):
        """Adds each part of the piece to the window"""
        win.add(self._back)
        win.add(self._frontLetter)
        win.add(self._frontValue)
    
    def removeFrom(self, win):
        """Removes each part of the piece from the window"""
        win.remove(self._frontLetter)
        win.remove(self._frontValue)
        win.remove(self._back)
        
    def getReferencePoint(self):
        """Returns the center of the piece"""
        self._back.getCenter()
    
    def handleMouseRelease(self, event):
        """Activates or deactivates a piece depending on if the piece is
           moving"""
        if not self._active:
            return
        if self._moving:
            self._moving = False
            self._player.report(self, event)         
            self.deactivate()
        else:
            self._moving = True
            self._startLoc = event.getMouseLocation()
            
    def handleMouseMove(self, event):
        """Changes the location of the piece of that of the mouse when it 
           is moving"""
        if not self._active:
            return
        if self._moving:
            oldx, oldy = self._startLoc
            newx, newy = event.getMouseLocation()
            self.move(newx - oldx, newy - oldy)
            self._startLoc = self._location

class Bag(EventHandler):
    """A class that creates a bag of game pieces"""
    def __init__(self, win, controller):
        """Creates the bag graphical image and list for tiles"""
        EventHandler.__init__(self)
        self._controller = controller
        self._win = win
        self._bag = Circle(48, (60, 60))
        self._bagText = Text('Bag', (60, 70), 36)
        self._bag.setFillColor('orange')
        self._bag.addHandler(self)
                
        #x-coordinate locations to be used later in the class        
        self._startX = [250, 280, 310, 340, 370, 400, 430]
        
        self._tiles = []
        self._usedTiles = []
        letter = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                  'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                  'V', 'W', 'X', 'Y', 'Z']
        value = [0, 1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 
                 1, 1, 1, 4, 4, 8, 4, 10]
        quantity = [2, 9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2, 6, 8, 2, 1,
                    6, 4, 6, 4, 2, 2, 1, 2, 1]
        #uses a loop to assign the correct letter and number value to a tile 
        #and appends the piece to the tile list the appropriate amount of times
        for i in range(len(letter)):
            for _ in range(quantity[i]):
                tile = Piece(letter[i], value[i], None)
                self._tiles.append(tile)
    
    def handleKeyRelease(self, event):
        """A method that starts the inial tiles deal to each player by 
           pressing a key"""
        self._controller.starting(self._win)
        
    def addTo(self, win):
        """Adds the bag to the window"""
        win.add(self._bag)
        win.add(self._bagText)
    
    def removeFrom(self, win):
        """Removes the bag from the window"""
        win.remove(self._bag)

    def shuffle(self):
        """Shuffles the full set of tiles"""
        #starts with an empty set that will be appended with the used pieces
        #from the original bag
        shuffleTiles = []
        
        #finds a random position in the bag and adds it to the empty list, 
        #then removes that position from the original list. Repeats action 
        #for the number of tiles in the bag.
        for _ in range(len(self._tiles)):
            x = random.randrange(len(self._tiles))
            shuffleTiles.append(self._tiles[x])
            self._tiles.remove(self._tiles[x])
        
        #assigns the full deck of cards to the list of shuffled cards    
        self._tiles = shuffleTiles
        
    def deal(self):
        """Deals a piece from the list of tiles and appends the dealt piece 
           to a list of used tiles"""
        #removes piece from bag and puts it into a list of used pieces
        dealPiece = self._tiles.pop(0)
        self._usedTiles.append(dealPiece)
        return dealPiece        
    
    def handleMouseRelease(self, event):
        """Method that call on the controller to deal a shuffled piece from 
           the bag when clicked"""
        self._controller.bagClicked(self._win)

class Holder:
    """Class for creating tile holders"""
    def __init__(self, board):
        """Initializes the features of the holders"""
        self._board = board
        self._myHolder1 = []
        self._myHolder2 = []
        self._shuffleSquare = Rectangle(35, 35, (200, 625))
        
        distances = [250, 280, 310, 340, 370, 400, 430]
        #loop for the holders at a specific y-coordinate
        for num in range(len(distances)):
            self._holderGraphic = Rectangle(30, 30, (distances[num], 605))
            self._holderGraphic.setFillColor('brown')
            self._myHolder1.append(self._holderGraphic)
            
        #loop for the holders at a different specific y- coordinate     
        for num in range(len(distances)):
            self._holderGraphic = Rectangle(30, 30, (distances[num], 645))
            self._holderGraphic.setFillColor('brown')
            self._myHolder2.append(self._holderGraphic)
    
    def addTo(self, win):
        """Adds the holder objects the the window"""
        win.add(self._shuffleSquare)
        for i in range(len(self._myHolder1)):
            win.add(self._myHolder1[i])
        for i in range(len(self._myHolder2)):
            win.add(self._myHolder2[i])

    def report(self, piece, event):
        """Reports the code from board class"""
        self._board.report(piece, event)

#this class was ultimately not used in my code because I did not have enough
#time to implement it correctly, but this is how I was beginning to calculate
#score

#class Score:
#    def __init__(self, win):
#        score = 0
#        multiplier = 1
#        for s in tilesPlayed:
#            score += s.getValue()[0]
#            multiplier = multiplier * getValue()[1]
#        score *= multplier
    
#        self._scoreBoard = Rectangle(120, 100, (600, 620))
#        self._scoreBoard.setFillColor('yellow')
#        self._myScore = Text(str(score), (600, 625), 16)
#        self._scoreText = Text('My Score!', (600, 595), 14)
        
#    def addTo(self, win):
#       win.add(self._scoreBoard)
#        win.add(self._scoreText)
#        win.add(self._myScore)

class Done(EventHandler):
    """A class that is used to create a done button that will switch 
       players' turns"""
    def __init__(self, win):
        """Creates the parts of the button and the rectangular block"""
        EventHandler.__init__(self)
        self._win = win
        self._button = Rectangle(120, 100, (100, 630))
        self._button.setFillColor('lavender')
        self._text = Text('Done with Turn!', (100, 630), 16)
        self._button.addHandler(self)
        
        #the block is used to hide the opponents pieces from the current player
        self._block = Rectangle(210, 30, (340, 645))
        self._block.setDepth(1)
        self._block.setFillColor('brown')
        
    def addTo(self, win):
        """Adds the button and block to the window"""
        win.add(self._button)
        win.add(self._text)
        win.add(self._block)
        
    def handleMouseRelease(self, event):
        """Changes the block's location to hover over the other holder when 
           the turn is done"""
        if self._block.getCenter() == (340, 645):
            self._block.moveTo((340, 605))
        elif self._block.getCenter() == (340, 605):
            self._block.moveTo((340, 645))

class Challenge(EventHandler):
    """A class that implements a button to challenge a word"""
    def __init__(self, win):
        """Initialize the button and error message"""
        EventHandler.__init__(self)
        self._win = win
        self._challengeButton = Rectangle(120, 100, (600, 630))
        self._challengeButton.setFillColor('lightgreen')
        self._challengeText = Text('Challenge', (600, 630), 16)
        self._challengeButton.addHandler(self)
        
        self._error = Rectangle(700, 700, (350, 350))
        self._error.setFillColor('red')
        #set depths to 1 to make sure no objects would be seen on top of it
        self._error.setDepth(1)
        self._message = Text('Shame!', (350, 350), 66)
        self._message.setDepth(1)
        
    def addTo(self, win):
        """Adds the button and text to the window"""
        win.add(self._challengeButton)
        win.add(self._challengeText)
        
    def showError(self):
        """Displays a red screen with message of "shame" when called"""
        self._win.add(self._error)
        self._win.add(self._message)
        yield 3000
        self._win.remove(self._error)
        self._win.remove(self._message)
        
    def handleMouseRelease(self, event):
        """Displays an input question when challenge button is clicked"""
        answer = input('Opponent, is this a real word? (Answer: "yes" or "no")')
        #Not a real challenge obviously since there is nothing to confirm 
        #wrong word but I wanted to write a message of shame as a GoT reference
        if answer == 'yes':
            return
        if answer == 'no':
            RunWithYieldDelay(self.showError())

class Controller(EventHandler):
    """Class that controlls what happens during the game and what actions 
       are taken"""
    def __init__(self, win):
        """Initializes each class and adds it to the window"""
        EventHandler.__init__(self)
        self._key = Key()
        self._key.addTo(win)
        
        self._done = Done(win)
        self._done.addTo(win)
        
        self._challenge = Challenge(win)
        self._challenge.addTo(win)
        
        self._holder = Holder(1)
        self._holder.addTo(win)
        
        self._directions = Directions()
        self._directions.addTo(win)

        self._board = Board(win)
        
        self._bag = Bag(win, self)
        self._bag.addTo(win)
        self._bag.shuffle()

    def starting(self, win):
        """Starts the game by dealing 7 pieces to the proper locations in the
           holders for both players"""
        startX = [250, 280, 310, 340, 370, 400, 430]
        for num in range(len(startX)):
            aPiece = self._bag.deal()
            aPiece.addTo(win)
            aPiece.activate()
            aPiece.moveTo((startX[num], 605))
        for num in range(len(startX)):
            aPiece = self._bag.deal()
            aPiece.addTo(win)
            aPiece.activate()
            aPiece.moveTo((startX[num], 645))        
    
    def bagClicked(self, win):
        """Method that deals a shuffled piece and moves it to the white square
           shuffleSpot on the window"""
        thePiece = self._bag.deal()
        thePiece.addTo(win)
        thePiece.activate()
        thePiece.moveTo((200, 625))


def main(win):
    """Function to run the controller"""
    Controller(win)
    win.setWidth(700)
    win.setHeight(700)

    
StartGraphicsSystem(main)
