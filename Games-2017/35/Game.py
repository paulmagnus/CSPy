""" 
-------------------------------------------------------------------------------
*******************************************************************************
* Project: Game.py                                                            *
* Author: Sam Knollmeyer                                                      *
* Date: May 1, 2017                                                           *
* Partner: Will Jordan                                                        *
*                                                                             * 
* Description: This program runs a game of Sorry that goes through 3 round of *
*              gameplay. Player order is maintained throughout and the game   *
*              ends after all players have had 3 turns. Certain rules like    *
*              Sorry card, spliting a 7 between pawns, and others have not    *
*              implemented.                                                   *
*******************************************************************************
"""

import random
from cs110graphics import *

#Universal variables for the locations that each piece moves out to when a 1 
#or 2 is drawn
REDSTART = 4
BLUESTART = 19
YELLOWSTART = 34
GREENSTART = 49


class Piece(EventHandler):
    '''Creates template for a piece to be made'''
    
    def __init__(self, color, player, position, board, deck):
        '''Initializes attributes of piece'''
        
        EventHandler.__init__(self)
    
        self._board = board
        self._color = color
        self._player = player
        self._deck = deck
        self._pawn = Circle(6, position)
        self._pawn.setFillColor(color)
        self._pawn.addHandler(self)
        self._inHome = True
        self._currentSpace = None
        self._spaceNumber = 0
        self._active = False
        self._startPos = None
        self._location = (0, 0)
        self._cardValue = self._deck.getTop().getValue()
        
        #Start and end locations for the 8 slides strips on the board
        #Used in slideEnd below
        self._slideStarts = [1, 9, 16, 24, 31, 39, 46, 54]
        self._slideEnds = [4, 13, 19, 28, 34, 43, 49, 58]
        
        
    def activate(self):
        '''Activates piece so only one player can move at a time'''
        self._active = True
    
    def deactivate(self):
        '''Deactivates piece'''
        self._active = False
        
    def addTo(self, win):
        '''Adds piece to window'''
        win.add(self._pawn)
        
    def moveTo(self, pos):
        '''Moves piece to new position'''
        self._pawn.moveTo(pos)
        self._location = pos

    def getLocation(self):
        '''Returns location of piece'''
        return self._location
        
    def setDepth(self, depth):
        '''Sets the depth of the piece'''
        self._pawn.setDepth(depth)
        
    def getCurrentSpaceIndex(self):
        '''Returns index of the piece'''
        return self._currentSpace.getIndex()
        
    def slideEnd(self):
        '''Returns end location of where piece should go if it is on a slide'''
        for i in range(len(self._slideStarts)):
            if self._spaceNumber == self._slideStarts[i]:
                return self._board._spaces[self._slideEnds[i]].getLocation()
                
    def computeEndPosition(self, cardvalue):
        '''Returns end position given the value of the face up card'''
        return self._board._spaces[(self._currentSpace.getIndex() + cardvalue)\
        % 59].getLocation()
        
    def handleMouseRelease(self, event):
        '''When mouse is released the piece moves a certain number of spaces'''
        
        #Set the value for number of spaces the piece should move
        cardValue = self._deck.getTop().getValue()
        
        #Piece can only move out of home if a 1 or 2 is drawn and it is that
        #players turn (their pieces are active)
        if self._inHome and self._active and \
        (cardValue == 1 or cardValue == 2):
            
            #The pieces move to their universal variable start positions when a
            #1 or 2 is drawn. self._inHome becomes False when this happens
            if self._color == 'red':
                self._pawn.moveTo(self._board._spaces[REDSTART].getLocation())
                self._inHome = False
                self._currentSpace = self._board._spaces[REDSTART]
                self._spaceNumber = REDSTART
            if self._color == 'blue':
                self._pawn.moveTo(self._board._spaces[BLUESTART].getLocation())
                self._inHome = False
                self._currentSpace = self._board._spaces[BLUESTART]
                self._spaceNumber = BLUESTART
            if self._color == 'yellow':
                self._pawn.moveTo(self._board._spaces[YELLOWSTART].getLocation\
                ())
                self._inHome = False
                self._currentSpace = self._board._spaces[YELLOWSTART]
                self._spaceNumber = YELLOWSTART
            if self._color == 'green':
                self._pawn.moveTo(self._board._spaces[GREENSTART].getLocation())
                self._inHome = False
                self._currentSpace = self._board._spaces[GREENSTART]

            #If a player draws a 2 in order to move out of home, it is still 
            #their turn (their pieces are still active) and they may draw again
            if cardValue == 2:
                return
            self._board.changeTurn()
            
        #Turn changes if a player draws a card not equal to 1 or 2 and they
        #can't move out of their home space
        elif self._inHome and cardValue != 1 and cardValue != 2:
            self._board.changeTurn()
            
        #The value 4 moves pieces backwards    
        else:
            if self._active:
                if cardValue == 4:
                    cardValue = -4
                
                #Move the number of spaces dictated by card value
                self._pawn.moveTo(self.computeEndPosition(cardValue))
                
                #Makes sure pieces can move around the corner from space 59 to 0
                self._spaceNumber = (self._spaceNumber + cardValue) % 59
                
                #Sliding
                self._currentSpace = self._board._spaces[self._spaceNumber]
                for i in range(len(self._slideStarts)):
                    if self._spaceNumber == self._slideStarts[i]:
                        self._pawn.moveTo(self.slideEnd())
                if cardValue == 2:
                    return
                self._board.changeTurn()
           
                
class Space:
    '''Creates template for creating spaces of the board'''
    
    def __init__(self, win, pos, color, index):
        '''Initializes attributes of a space'''
        self._location = pos
        self._index = index
        self._color = color
        self._square = Rectangle(20, 20, pos)
        win.add(self._square)
        
    def getLocation(self):
        '''Returns location of the space'''
        return self._location
        
    def addTo(self, win):
        '''Adds space to the window'''
        win.add(self._square)
        
    def colorIt(self, color):
        '''Sets the fill color of the space'''
        self._square.setFillColor(color)
    
    def getIndex(self):
        '''Returns the index of a given space'''
        return self._index
        
        
class Player:
    '''Creates template for creating players'''
    
    def __init__(self, win, color, board, deck):
        '''Initializes the attributes of Player'''
        self._pieces = []
        self._board = board
        self._deck = deck
        
        #Create red pieces and add them to piece list
        if color == 'red':
            for which, position in [(0, (121, 71)), (1, (139, 71)), \
                                    (2, (121, 89)), (3, (139, 89))]:
                thisPieceR = Piece(color, which, position, board, deck)
                thisPieceR.setDepth(1)
                thisPieceR.addTo(win)
                
                self._pieces.append(thisPieceR)
                
        #Create blue pieces and add them to piece list
        elif color == 'blue':  
            for which, position in [(0, (311, 121)), (1, (329, 121)), \
                                        (2, (311, 139)), (3, (329, 139))]:
                thisPieceB = Piece(color, which, position, board, deck)
                thisPieceB.setDepth(1)
                thisPieceB.addTo(win)
                
                self._pieces.append(thisPieceB)
                
        #Create yellow pieces and add them to piece list
        elif color == 'yellow':      
            for which, position in [(0, (261, 311)), (1, (279, 311)), \
                                        (2, (261, 329)), (3, (279, 329))]:
                thisPieceY = Piece(color, which, position, board, deck)
                thisPieceY.setDepth(1)
                thisPieceY.addTo(win)
                
                self._pieces.append(thisPieceY)
        
        #Create green pieces and add them to piece list
        else:    
            for which, position in [(0, (71, 261)), (1, (89, 261)), \
                                        (2, (71, 279)), (3, (89, 279))]:
                thisPieceG = Piece(color, which, position, board, deck)
                thisPieceG.setDepth(1)
                thisPieceG.addTo(win)
                
                self._pieces.append(thisPieceG)    
                
    #Activation and deactivation of pieces to enable player turns
    def deactivate(self):
        '''Deactivates the pieces of the player'''
        for piece in self._pieces:
            piece.deactivate()
            
    def activate(self):
        '''Activates the pieces of the player'''
        for piece in self._pieces:
            piece.activate()


class Board:
    '''Creates the Board space, players and deck'''
    
    def __init__(self, win):
        '''Initiallizes the attributes of the Board'''
        self._window = win
        self._players = []
        self._deck = Deck()
        #self._comment = Comment(win, self._deck, self)
        self._currentPlayerNum = 0
        self._priorPlayerNum = 0
        self._deck.shuffle()
        self._colors = ['red', 'blue', 'yellow', 'green']
        self._numberOfTurns = 0
            
        #Create 4 players, one for each color
        for color in self._colors:
            self._player = Player(win, color, self, self._deck)
            self._players.append(self._player)
            
        #Activate red pieces as the first player
        self._players[0].activate()
        
        #Deactivate pieces of all the other players
        for i in range(1, 4):
            self._players[i].deactivate()
        
        self._spaces = []
        xpos = 50
        ypos = 50
        color = 'white'
        
        self._homeSpacesRed = []
        self._homeSpacesBlue = []
        self._homeSpacesYellow = []
        self._homeSpacesGreen = []
        
        #Creates the top (red) portion of the board
        for i in range(15):
            thisSpace1 = Space(win, (xpos, ypos), color, i)
            thisSpace1.addTo(win)
            self._spaces.append(thisSpace1)
            xpos += 20
            
            #Color red slide strips
            centersR = [(70, 50), (90, 50), (110, 50), (130, 50), (230, 50),\
                        (250, 50), (270, 50), (290, 50), (310, 50)]
            if thisSpace1.getLocation() in centersR:
                thisSpace1.colorIt('red')
            
            #Create red home strip
            if i == 1: 
                color = 'red'
                for _ in range(5):
                    ypos += 20
                    thisSpaceHome1 = Space(win, (xpos, ypos), color, i)
                    thisSpaceHome1.addTo(win)
                    thisSpaceHome1.colorIt('red')
                    self._homeSpacesRed.append(thisSpaceHome1)
                self._circleHomeR = Circle(20, (90, 180))
                self._circleHomeR.setFillColor('red')
                win.add(self._circleHomeR)
                self._homeSpacesRed.append(self._circleHomeR)
                ypos -= 100    
            color = 'white'
            
            #Create red home space
            if i == 3:
                self._circleStartR = Circle(20, (130, 80))
                self._circleStartR.setFillColor('red')
                self._circleStartR.setDepth(10)
                win.add(self._circleStartR)
                
        
        #Creates the right (blue) portion of the board
        for i in range(15):
            thisSpace2 = Space(win, (xpos, ypos), color, i + 15)
            thisSpace2.addTo(win)
            self._spaces.append(thisSpace2)
            ypos += 20
            
            #Color the blue slide strips
            centersB = [(350, 70), (350, 90), (350, 110), (350, 130),\
                        (350, 230), (350, 250), (350, 270), (350, 290),\
                        (350, 310)]
            if thisSpace2.getLocation() in centersB:
                thisSpace2.colorIt('blue')
            
            #Create blue home strip
            if i == 1: 
                color = 'blue'
                for _ in range(5):
                    xpos -= 20
                    thisSpaceHome2 = Space(win, (xpos, ypos), color, i)
                    thisSpaceHome2.addTo(win)
                    thisSpaceHome2.colorIt('blue')
                    self._homeSpacesBlue.append(thisSpaceHome2)
                self._circleHomeB = Circle(20, (220, 90))
                self._circleHomeB.setFillColor('blue')
                win.add(self._circleHomeB)
                self._homeSpacesBlue.append(self._circleHomeB)
                xpos += 100     
            color = 'white'
            
            #Create blue home space
            if i == 3:
                self._circleStartB = Circle(20, (320, 130))
                self._circleStartB.setFillColor('blue')
                self._circleStartB.setDepth(10)
                win.add(self._circleStartB)
        
        #Create the bottom (yellow) portion of the board
        for i in range(15):
            thisSpace3 = Space(win, (xpos, ypos), color, i + 30)
            thisSpace3.addTo(win)
            self._spaces.append(thisSpace3)
            xpos -= 20
            
            #Color the yellow slide strips
            centersY = [(330, 350), (310, 350), (290, 350), (270, 350),\
                        (170, 350), (150, 350), (130, 350), (110, 350),\
                        (90, 350)]
            if thisSpace3.getLocation() in centersY:
                thisSpace3.colorIt('yellow')
            
            #Create the yellow home strip
            if i == 1: 
                color = 'yellow'
                for _ in range(5):
                    ypos -= 20
                    thisSpaceHome3 = Space(win, (xpos, ypos), color, i)
                    thisSpaceHome3.addTo(win)
                    thisSpaceHome3.colorIt('yellow')
                    self._homeSpacesYellow.append(thisSpaceHome3)
                self._circleHomeY = Circle(20, (310, 220))
                self._circleHomeY.setFillColor('yellow')
                win.add(self._circleHomeY)
                self._homeSpacesYellow.append(self._circleHomeY)
                ypos += 100     
            color = 'white'
            
            #Create the yellow home space
            if i == 3:
                self._circleStartY = Circle(20, (270, 320))
                self._circleStartY.setFillColor('yellow')
                self._circleStartY.setDepth(10)
                win.add(self._circleStartY)
        
        #Create the left (green) portion of the board
        for i in range(15):
            thisSpace4 = Space(win, (xpos, ypos), color, i + 45)
            thisSpace4.addTo(win)
            self._spaces.append(thisSpace4)
            ypos -= 20
            
            #Color the green slide strips
            centersG = [(50, 330), (50, 310), (50, 290), (50, 270), (50, 170),\
                        (50, 150), (50, 130), (50, 110), (50, 90)]
            if thisSpace4.getLocation() in centersG:
                thisSpace4.colorIt('green')
            
            #Create the green home strip
            if i == 1: 
                color = 'green'
                for _ in range(5):
                    xpos += 20
                    thisSpaceHome4 = Space(win, (xpos, ypos), color, i)
                    thisSpaceHome4.addTo(win)
                    thisSpaceHome4.colorIt('green')
                    self._homeSpacesGreen.append(thisSpaceHome4)
                self._circleHomeG = Circle(20, (180, 310))
                self._circleHomeG.setFillColor('green')
                win.add(self._circleHomeG)
                self._homeSpacesGreen.append(self._circleHomeG)
                xpos -= 100  
            color = 'white'
            
            #Create the green home space
            if i == 3:
                self._circleStartG = Circle(20, (80, 270))
                self._circleStartG.setFillColor('green')
                self._circleStartG.setDepth(10)
                win.add(self._circleStartG)

    
    def getDeck(self):
        '''Returns the deck'''
        return self._deck

    #Sets maximum number of turns for the game
    def checkNumTurns(self):
        '''Returns True if game has reached the desired number of turns, False
        otherwise'''
        if self._numberOfTurns == 12:
            return True
        else:
            return False
            
    #Ensures order of play is correct
    def changeTurn(self):
        '''Changes the turn after a play is made'''
        self._priorPlayerNum = self._currentPlayerNum
        
        self._priorPlayer = self._players[self._priorPlayerNum]
        self._priorPlayer.deactivate()
        
        
        self._currentPlayerNum = (self._currentPlayerNum + 1) % 4
        self._currentPlayer = self._players[self._currentPlayerNum]
        self._currentPlayer.activate()
        
        self._numberOfTurns += 1
        if self.checkNumTurns():
            self.endGame()
        
    #End game screen for when maximum number of turns is reached    
    def endGame(self):
        '''Ends the game'''
        endGameRect = Rectangle(1000, 600, (500, 300))
        endGameRect.setDepth(-10)
        endGameRect.setFillColor('white')
        self._window.add(endGameRect)
        endGameText = Text('GAME OVER', (500, 300), 30)
        endGameText.setDepth(-11)
        self._window.add(endGameText)
        

class Deck:
    """A class for building a deck of cards. This class is not graphical"""
    
    def __init__(self):
        """Creates a complete deck of 41 playing cards."""
        
        #Initializes objects of empty list for deck generation
        self._deck = []
        self._shuffledDeck = []
        
        #The cards of a sorry deck
        values = [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, \
                5, 7, 7, 7, 7, 8, 8, 8, 8, 10, 10, 10, 10, 11, 11, 11, 11,\
                12, 12, 12, 12]
        
        for value in values:
            self._deck.append(Card(value, value, 'Back'))
        
    def empty(self):
        """Returns True if the deck no longer contains any cards. Otherwise
        false is returned."""
        
        #returns true if deck is empty
        return self._deck == []
            
    def shuffle(self):
        """All cards currently in the deck are randomly ordered."""
        
        #Create and return new shuffled deck
        for i in range(len(self._deck)):
            cardposition = random.randrange(41 - i)
            self._shuffledDeck.append(self._deck[cardposition])
            self._deck.remove(self._deck[cardposition])
        self._deck = self._shuffledDeck
        return self._deck
        
    def deal(self):
        """Deals a card. A card is removed from the top of the deck and
        returned."""
        
        self._deck.remove(self._deck[0])
        return self._deck[0]
        

    def getTop(self):
        '''Returns the top card on the deck'''
        return self._deck[0]

    def getValue(self):
        '''Returns the value of the top card'''
        return self.getTop().getValue()
        
class Card:
    """A class used for building graphical playing cards"""
    
    def __init__(self, value, faceFileName, backFileName):
        '''Creates a playing card with a given value'''
        
        #Card dimensions
        self._width = 142
        self._height = 192
        self._center = 800, 200
        self._value = value

        #Retrieve the card photos we took from photo library
        self._faceFileName = faceFileName
        self._backFileName = backFileName
        faceurl = "https://cs.hamilton.edu/~wjordan/images/Sorry_card_-_" + \
        str(faceFileName) + ".jpg"
        self._face = Image(faceurl, self._center, self._width, self._height)
        backurl = "https://cs.hamilton.edu/~wjordan/images/Back.jpg"
        self._back = Image(backurl, self._center, self._width, self._height)
        self._depth = 10
        self._face.setDepth(self._depth + 1)
        self._back.setDepth(self._depth)
      
    def getValue(self):
        '''Returns the value of a given card'''
        return self._value
    
    def addTo(self, win):
        '''Adds the card to the given graphics window.'''
        win.add(self._face)
        win.add(self._back)
        
    def removeFrom(self, win):
        """Removes the card from the given graphics window."""
        win.remove(self._face)
        win.remove(self._back)
        
    def flip(self):
        '''Flips the card over.'''
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
        
        #Retrieves depth of front and back of card
        backDepth = self._back.getDepth()
        faceDepth = self._face.getDepth()
        
        #Resets depths so that card is face down
        if backDepth < faceDepth:
            self._face.setDepth(depth + 1)
            self._back.setDepth(depth)
        else:
            self._face.setDepth(depth)
            self._back.setDepth(depth + 1)


class Controller(EventHandler):
    """Creates a controller and adds an event handler to the button"""
    
    def __init__(self, win, board):
        """Set up all objects on the window """
        
        self._board = board
        #Initializes handle
        EventHandler.__init__(self)
        
        #Creates deck of cards in controller
        self._window = win
        self._prevCard = None
        self._deck = self._board.getDeck()
        self._card = self._deck.getTop()
        self._card.addTo(win)
        
        #Creates button with text, when clicked, a card is flipped
        self._button = Rectangle(100, 50, (800, 75))
        self._button.setFillColor('salmon')
        win.add(self._button)
        self._button.addHandler(self) 
        self._flipText = Text("Press to flip card", (800, 75), 12)
        win.add(self._flipText)

    def handleMouseRelease(self, event):
        """Creates an event handler that runs through a series of code when the
        event occurs"""
        self._card = self._deck.deal()          #Reassigns card to top card
        self._card.addTo(self._window)
        self._card.flip()
        

def play(win):
    '''Creates an instance of the Board and Controller'''
    board = Board(win)
    
    _ = Controller(win, board)
    
StartGraphicsSystem(play, 1000, 425)
