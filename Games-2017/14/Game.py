"""
--------------------------------------------------------------------------------
********************************************************************************
*Project: Game.py                                                              *
*Author: Griffin Dunne                                                         *
*Partner: Pete Ross                                                            *
*Date: 4/10/17                                                                 *
*Description: This project will create the board game Sorry.                   *
********************************************************************************
--------------------------------------------------------------------------------
"""
import random
from cs110graphics import *
        
class Deck:
    """ creates a list of cards and deals them onto the window """
    def __init__(self, win, board):
        """Creates a complete deck of Sorry! playing cards."""
        self._deck = []
        self._win = win          #used to get rid of error
        self._currentDepth = 0
        self._values = []
        self._card = None
        self._board = board
        self._discard = []
        self._value = None

        for value in ['1']:
            for _ in range(5):
                c = Card(self, value)
                self._deck.append(c)
                
        for value in['2', '3', '4', '5', '7', '8', '10', '11', '12', 'sorry']:
            for _ in range(4):
                #create each of the cards
                c = Card(self, value)
                self._card = c
        
                #add the cards to a list
                self._deck.append(c)
                
        
    
    def empty(self):
        """Returns True if the deck no longer contains any cards. Otherwise
           false is returned."""
        if len(self._deck) == 0:
            return True
        return False
    
    def deal(self):
        """Deals a card. A card is removed from the top of the deck and
           returned."""
        #make sure that the top card has the lowest depth and the second has
        #the second lowest and so on...
        self._deck[0].setDepth(self._currentDepth)
        self._currentDepth += 1
        
        #add the first item of the list to the screen and remove the first 
        #item from the list
        self._value = self._deck[0].getValue()
        self._discard.append(self._deck[0])
        self._deck.pop(0).addTo(self._win)
        #CITE: TA
        #DESCRIPTION: A TA helped me with the .pop built into List 
    
    def shuffle(self):
        """All cards currently in the deck are randomly ordered. You will want
           to use Python's randrange function in the random module. You may not
           use any other functions from this module."""
        shuffledDeck = []
        for _ in range(len(self._deck)):
            while len(self._deck) > 0:
                index = random.randrange(0, len(self._deck))
                shuffledDeck.append(self._deck.pop(index))
        self._deck = shuffledDeck
        return self._deck
    
    def getLength(self):
        """return the length of the deck """
        return len(self._deck)
        
    def getDeck(self):
        """return the deck"""
        return self._deck
        
    def reportCardClick(self, card):
        """ tell the board that the card has been clicked """
        self._board.reportCardClick(card)
       
class Card(EventHandler):
    """A class used for building graphical playing cards"""
    def __init__(self, deck, value):
        self._value = value
        imagevalue = value
        if imagevalue == "7" or imagevalue == "11":
            imagevalue += "new"
        faceurl = "http://cs.hamilton.edu/~gdunne/images/sorry" + imagevalue
        self._face = Image(faceurl, center=(WINDOW_WIDTH / 2.4, \
                           WINDOW_WIDTH / 2.4), 
                           width=WINDOW_WIDTH/(25/6), 
                           height=WINDOW_HEIGHT/(3.597))
        backurl = "http://cs.hamilton.edu/~gdunne/images/backofsorry"
        self._back = Image(backurl, center=(167, 170), 
                           width=WINDOW_WIDTH/(25/6), 
                           height=WINDOW_HEIGHT/(3.597))
        self._faceup = False        #the default card will be face down
        self._window = None         #at default, there is no window
        EventHandler.__init__(self) #setup the EventHandler correctly
        self._back.addHandler(self) #add the Handler to the back of the card
        self._flipped = False
        self._deck = deck
    
    def handleMouseRelease(self, event):
        """ when the card is clicked, flip it over and move it to the discard
            pile """
        self.flip()
        self.move(WINDOW_WIDTH / 3.34, WINDOW_WIDTH / 4)
        self._deck.reportCardClick(self)
        
        
    def getValue(self):
        """returns the value of the card that is flipped """
        return self._value
    
    def addTo(self, win):
        """Adds the card to the given graphics window."""
        #make sure that the correct side of the card image is placed
        if self._faceup:
            win.add(self._face)
        else:
            win.add(self._back)
        self._window = win
        
    def removeFrom(self, win):
        """Removes the card from the given graphics window. You cannot remove
           a card that hasn't been added previously."""
        #make sure that the correct side of the card image is removed
        if self._faceup:
            win.remove(self._face)
        else:
            win.remove(self._back)
        self._window = None
    def flip(self):
        """Flips the card over. If face down, the card is flipped to face up,
           or vice versa. This visually flips the card over as well. May be 
           called on all cards whether they have been added to a window ornot"""
        newwindow = self._window
        if newwindow != None:        #if there is a window, then add a card
            self.removeFrom(newwindow)
        if self._faceup:
            self._faceup = False
        else:
            self._faceup = True
        if newwindow != None:
            self.addTo(newwindow)
        #make sure that when the card is flipped, the first one flipped
        #will be under the second card flipped and so on 
        self.setDepth(0)
        
    def move(self, dx, dy):
        """Moves a card by dx and dy."""
        #move both the back and the front images of the card
        self._face.move(dx, dy)
        self._back.move(dx, dy)
        
    def getReferencePoint(self):
        """The point representing the center of the card image is returned"""
        return self._face.getCenter()
    
    def size(self):
        """Returns the tuple (width, height)"""
        return self._face.size()
        
    def setDepth(self, depth):
        """Sets the depth of graphical objects representing the card to
           depth"""
        self._face.setDepth(depth)
        self._back.setDepth(depth)
        
class Board:
    """adds board to the window """
    def __init__(self, win):
        self._board = Image("http://cs.hamilton.edu/~gdunne/images/"
                            + "sorryboardfinished", \
                            center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2), 
                            width=400, height=400)
        self._board.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.addTo(win)
        self._currentCard = 0
        xpos = WINDOW_WIDTH / 32
        ypos = WINDOW_WIDTH / 32
        self._spaces = []
        self._win = win
        self._gotsorry = False
        self._sorrypiece = None
        self._goAgain = False
        self._switchpiece = None
        self._switched = False
        self._tallyRed = 0
        self._tallyBlue = 0
        self._tallyGreen = 0
        self._tallyYellow = 0
        for _ in range(60):
            newSpace = BoardSpace(self, (xpos, ypos))
            newSpace.addTo(win)
            if xpos == (WINDOW_WIDTH * 31) / 32:
                ypos += WINDOW_WIDTH / 16
            if ypos == WINDOW_WIDTH / 32:
                xpos += WINDOW_WIDTH / 16
            if ypos == (WINDOW_WIDTH * 31) / 32:
                xpos -= WINDOW_WIDTH / 16
            if xpos == WINDOW_WIDTH / 32 and ypos <= (WINDOW_WIDTH * 31) / 32\
                and ypos != WINDOW_WIDTH / 32:
                ypos -= WINDOW_WIDTH / 16
            self._spaces.append(newSpace)
        self._players = []    
        colors = ['red', 'blue', 'yellow', 'green']
        depth = 0
        for color in colors:
            player = Player(self, win, color, depth)
            depth += 1
            self._players.append(player)
        self._current = 3
        #self.changeTurn()
        self._deck = self.makeDeck(win)
        while not self._deck.empty():
            self._deck.deal()
        self._card = None
        #there were too many branches, but I could not figure a way around this 
    
    def getWinner(self):
        """determine the winner of the game """
        winner = ""
        for players in self._players:
            pawn = players.getPawns()
            for pawn in players.getPawns():
                if pawn.getColor() == "red":
                    if pawn.getLocation() == ((5 * WINDOW_WIDTH / 32, \
                                              13 * WINDOW_WIDTH / 32)):
                        players.removeList(pawn)
                        self._tallyRed += 1
                if pawn.getColor() == "blue":
                    if pawn.getLocation() == ((19 * WINDOW_WIDTH / 32, \
                                               5 * WINDOW_WIDTH / 32)):
                        self._tallyBlue += 1
                if pawn.getColor() == "yellow":
                    if pawn.getLocation() == ((27 * WINDOW_WIDTH / 32,\
                                               19 * WINDOW_WIDTH / 32)):
                        self._tallyYellow += 1
                if pawn.getColor() == "green":
                    if pawn.getLocation() == ((13 * WINDOW_WIDTH / 32,\
                                               27 * WINDOW_WIDTH / 32)):
                        self._tallyGreen += 1
        if self._tallyRed == 4 or self._tallyBlue == 4 or\
           self._tallyYellow == 4 or self._tallyGreen == 4:
            if self._tallyRed == 4:
                winner = "red"
            if self._tallyBlue == 4:
                winner = "blue"
            if self._tallyGreen == 4:
                winner = "green"
            if self._tallyYellow == 4:
                winner = "yellow"
            self.endGame(winner)
            
    def endGame(self, winner):
        """end the game when it is called from the getWinner function """
        for player in self._players:
            pawns = player.getPawns()
            for pawn in pawns:
                pawn.deactivate()
                pawn.remove(self._win)
        print("Congratulations, " + winner + " won!")
    
    def makeDeck(self, win):
        """ make the deck for the game"""
        deck = Deck(win, self)
        deck.shuffle()
        return deck
        
    def reportCardClick(self, card):
        """ when the card is clicked, activate the player """
        self._card = card.getValue()
        if self._deck.empty():
            self.makeDeck(self._win)
        self._players[self._current].activateAll()
                
        
    def reportPawnClick(self, piece):
        """ when the pawn is clicked, move the piece """
        if self._card == "sorry":
            if self._sorrypiece == None: #was unable to fix the 'expr is none'
                self._sorrypiece = piece
            elif not self._gotsorry:
                newLoc = piece.getLocation()
                self._sorrypiece.moveTo(newLoc)
                self._gotsorry = True
                piece.goHome()
                piece.deactivate()
                self._sorrypiece.deactivate()
                self._sorrypiece = None
                self.changeTurn()
                return
                
                    
        if self._card == "switch":
            if self._switchpiece == None: #was unable to fix the 'expr is none'
                self._switchpiece = piece
            elif not self._switched:
                newLoc = piece.getLocation()
                oldLoc = self._switchpiece.getLocation()
                self._switched = True
                self._switchpiece.moveTo(newLoc)
                piece.moveTo(oldLoc)
                piece.deactivate()
                self._switchpiece.deactivate()
                self._switchpiece = None
                self.changeTurn()
                return

        self.movePawn(piece)
        self.changeTurn()
        self.getWinner()
    
    def changeTurn(self):
        """change the turn by deactivating the correct player """
        if not self._goAgain:
            self._players[self._current].deactivateAll()
            self._current += 1
            self._current %= 4
            self._gotsorry = False
        else:
            self._goAgain = False
        
    def addTo(self, win):
        """ add the board to the window """
        win.add(self._board)
    
    def movePawn(self, piece):
        """ move the pawn the amount of spaces of the card value """
        i = 0
        if self._card == "sorry":
            self.checkOtherPawns()
            
        elif self._card == "10":
            if not piece.isAtStart():
                i = int(input("Do you want to move 10 spaces forward or\
                           one space backward? (10 or 1)"))
                if i == 1:
                    piece.move("-1")
                else:
                    for _ in range(int(self._card)):
                        piece.move("10")
        elif self._card == "2":
            self._goAgain = True
            if not piece.isAtStart():
                for _ in range(int(self._card)):
                    piece.move(self._card)
            else:
                piece.move("1")
        else:
            for _ in range(int(self._card)):
                piece.move(self._card)
            piece.slides()

    def checkOtherPawns(self):
        """ activate all pawns that are not safe """
        for player in self._players:
            pawns = player.getPawns()
            for pawn in pawns:
                if not pawn.isSafe():
                    pawn.activate()
                    
class BoardSpace():
    """ creates the rectangels that will be placed onto the board to make the
        spaces around the game """
    def __init__(self, board, center):
        """class for all of the board spaces """
        self._board = board
        self._center = center
        self._square = Rectangle(WINDOW_WIDTH / 16, WINDOW_WIDTH / 16, center)
        self._square.setBorderColor("black")
    
    def addTo(self, win):
        """add the board spaces to the window """
        win.add(self._square)
        
    def getCenter(self):
        """ return the center of the board tile """
        return self.getCenter()
    
class Pawn(EventHandler):
    """ creates 4 pawns for each color and are clickable to make them move
        around the board """
    def __init__(self, player, color, center, depth):
        """ creates 4 pawns per each player with the correct color """
        self._posx, self._posy = center
        self._piece = Rectangle(WINDOW_WIDTH / 40, WINDOW_WIDTH / 40, center)
        self._piece.setFillColor(color)
        self._piece.setBorderColor("black")
        self._color = color
        EventHandler.__init__(self) #setup the EventHandler correctly
        self._piece.addHandler(self)
        self._active = False
        self._player = player
        self._piece.setDepth(depth)
        self._safe = True
        
    def handleMouseRelease(self, event):
        """when the mouse is clicked and the piece is activated, report the
           pawn click """
        if not self._active:
            return
        else:
            self.updateLocation()
            self._player.reportPawnClick(self)
        
    def addTo(self, win):
        """add the pawns to the window """
        win.add(self._piece)
        
    def move(self, cardval):
        """move the pawns to the correct location """
        self.homeStretch()

        if self._posx < (31 * WINDOW_WIDTH / 32) \
        and self._posy == WINDOW_WIDTH / 32:  #move right
            if cardval == "-1" or cardval == "4":
                self.moveLeft()
            else:
                self.moveRight()
            
        if self._posx == (31 * WINDOW_WIDTH / 32) \
        and self._posy < (31 * WINDOW_WIDTH / 32): #move down
            if cardval == "-1" or cardval == "4":
                self.moveUp()
            else:
                self.moveDown()
            
        if self._posx <= (31 * WINDOW_WIDTH / 32)\
        and self._posy == (31 * WINDOW_WIDTH / 32) \
        and self._posx != WINDOW_WIDTH / 32:
            if cardval == "-1" or cardval == "4":
                self.moveRight()
            else:
                self.moveLeft()
            
        if self._posx == WINDOW_WIDTH / 32\
        and self._posy <= (31 * WINDOW_WIDTH / 32)\
        and self._posy != WINDOW_WIDTH / 32:
            if cardval == "-1" or cardval == "4":
                self.moveDown()
            else:
                self.moveUp()
            
        if self._posx == (9 * WINDOW_WIDTH / 32) \
        and self._posy == WINDOW_WIDTH / 10:
            self.moveStart(cardval)
            
        if self._posx == (23 * WINDOW_WIDTH / 32) \
        and self._posy == (9 * WINDOW_WIDTH / 10):
            self.moveStart(cardval)
            
        if self._posx == (9 * WINDOW_WIDTH / 10) \
        and self._posy == (9 * WINDOW_HEIGHT / 32):
            self.moveStart(cardval)
            
        if self._posx == (WINDOW_WIDTH / 10)\
        and self._posy == (23 * WINDOW_HEIGHT / 32):
            self.moveStart(cardval)
                
        self.updateLocation()
    
    def slides(self):
        """ get the piece to move when it hits the slide """
        #could not find a way around the 3 too many return statements
        if self._color != 'red':
            if self._posx == (3 * WINDOW_WIDTH / 32) and \
            self._posy == (WINDOW_HEIGHT / 32):
                self._piece.moveTo(((9 * WINDOW_WIDTH / 32), \
                WINDOW_HEIGHT / 32))
                return True
            if self._posx == (19 * WINDOW_WIDTH / 32) and \
            self._posy == WINDOW_WIDTH / 32:
                self._piece.moveTo(((WINDOW_WIDTH * 27 / 32), \
                WINDOW_HEIGHT / 32))
                return True
                
        if self._color != 'blue':
            if self._posx == (31 * WINDOW_WIDTH / 32) and \
            self._posy == (3 * WINDOW_WIDTH) / 32:
                self._piece.moveTo(((31 * WINDOW_WIDTH / 32), \
                9 * WINDOW_HEIGHT / 32))
                return True
            if self._posx == (31 * WINDOW_WIDTH / 32) and \
            self._posy == (19 * WINDOW_WIDTH / 32):
                self._piece.moveTo(((31 * WINDOW_WIDTH / 32), \
                (WINDOW_WIDTH * 27 / 32)))
                return True
                
        if self._color != 'yellow':
            if self._posx == (29 * WINDOW_WIDTH / 32) and \
            self._posy == (31 * WINDOW_WIDTH / 32):
                self._piece.moveTo((23 * WINDOW_HEIGHT / 32, \
                (31 * WINDOW_WIDTH / 32)))
                return True
            if self._posx == 13 * WINDOW_HEIGHT / 32 and \
            self._posy == (31 * WINDOW_WIDTH / 32):
                self._piece.moveTo(((5 * WINDOW_WIDTH / 32), \
                (31 * WINDOW_WIDTH / 32)))
                return True
                
        if self._color != 'green':
            if self._posx == WINDOW_WIDTH / 32 and \
            self._posy == (29 * WINDOW_WIDTH / 32):
                self._piece.moveTo((WINDOW_WIDTH / 32, 23 * WINDOW_HEIGHT / 32))
                return True
            if self._posx == WINDOW_WIDTH / 32 and \
            self._posy == 13 * WINDOW_HEIGHT / 32:
                self._piece.moveTo((WINDOW_WIDTH / 32, 5 * WINDOW_WIDTH / 32))
                return True
        return False
                
                 
    def homeStretch(self):
        """go up the home stretch if it is at the correct location """
        if self._color == 'red':
            if self._posx == (5 * WINDOW_WIDTH / 32) and self._posy < \
            (13 * WINDOW_HEIGHT / 32):
                self.moveDown()
                self.updateLocation()
                self._safe = True
                return True
            
        elif self._color == 'blue':    
            if self._posx > (19 * WINDOW_WIDTH / 32) and self._posy == \
            (5 * WINDOW_HEIGHT / 32):
                self.moveLeft()
                self.updateLocation()
                self._safe = True
                return True
        elif self._color == 'green':
            if self._posx < (13 * WINDOW_WIDTH / 32) and \
            self._posy == (27 * WINDOW_HEIGHT / 32):
                self.moveRight()
                self.updateLocation()
                self._safe = True
                return True
        elif self._color == 'yellow':
            if self._posx == (27 * WINDOW_WIDTH / 32) and \
            self._posy > (19 * WINDOW_HEIGHT / 32):
                self.moveUp()
                self.updateLocation()
                self._safe = True
                return True
        else:
            return False
            
        self.updateLocation()
    
    def moveStart(self, cardval):
        """move the piece out of start """
        if self.getColor() == "red" and (cardval == "1" or cardval == "2"):
            self._piece.moveTo((9 * WINDOW_WIDTH / 32, WINDOW_WIDTH / 32))
            self._safe = False
            
        if self.getColor() == "yellow" and (cardval == "1" or cardval == "2"):
            self._piece.moveTo((23 * WINDOW_WIDTH / 32, \
            31 * WINDOW_WIDTH / 32))
            self._safe = False
            
        if self.getColor() == "blue" and (cardval == "1" or cardval == "2"):
            self._piece.moveTo((31 * WINDOW_WIDTH / 32, 9 * WINDOW_HEIGHT / 32))
            self._safe = False
        
        if self.getColor() == "green" and (cardval == "1" or cardval == "2"):
            self._piece.moveTo((WINDOW_WIDTH / 32, 23 * WINDOW_HEIGHT / 32))
            self._safe = False
    
    def moveUp(self):
        """move the piece up """
        self._piece.move(0, -(WINDOW_WIDTH / 16))
    
    def moveLeft(self):
        """move the piece left """
        self._piece.move(-(WINDOW_WIDTH / 16), 0)
            
    def moveDown(self):
        """move the piece down """
        self._piece.move(0, WINDOW_WIDTH / 16)

    def moveRight(self):
        """move the piece right """
        self._piece.move(WINDOW_WIDTH / 16, 0)
        
    def getColor(self):
        """return the color"""
        return self._color
    
    def isSafe(self):
        """ return if the piece is safe"""
        return self._safe
    
    def updateLocation(self):
        """update the self._posx and self._posy to the getCenter location"""
        self._posx, self._posy = self._piece.getCenter()
        
    def activate(self):
        """activate the piece by turning the border color green """
        self._active = True
        self._piece.setBorderColor("limegreen")
    
    def remove(self, win):
        """ remove the piece from the board at the end of the game """
        win.remove(self._piece)
    
    def deactivate(self):
        """deactivate the piece by turning the border color back to black """
        self._active = False
        self._piece.setBorderColor("black")
    
    def getActivated(self):
        """return if it is activated """
        return self._active
        
    def getLocation(self):
        """return the location of the piece """
        return self._posx, self._posy
        
    def moveTo(self, loc):
        """move the piece to a coordinate """
        self._piece.moveTo(loc)
        
    def goHome(self):
        """return the piece to the correct Start """
        if self.getColor() == "red":
            self._piece.moveTo((9 * WINDOW_WIDTH / 32, WINDOW_WIDTH / 10))
            
        if self.getColor() == "yellow":
            self._piece.moveTo(((23 * WINDOW_WIDTH / 32), \
                               (9 * WINDOW_WIDTH / 10)))
                               
        if self.getColor() == "blue":
            self._piece.moveTo(((9 * WINDOW_WIDTH / 10), 9 / 32 * WINDOW_WIDTH))
        
        if self.getColor() == "green":
            self._piece.moveTo(((WINDOW_WIDTH / 10), (23 * WINDOW_HEIGHT / 32)))

    def isAtStart(self):
        """return true if it is at start """
        if self.getColor() == "red" and self.getLocation() ==\
           ((9 * WINDOW_WIDTH / 32), (WINDOW_WIDTH / 10)):
            return True
        if self.getColor() == "blue" and self.getLocation() ==\
           ((23 * WINDOW_WIDTH / 32), (9 * WINDOW_WIDTH / 10)):
            return True
        if self.getColor() == "yellow" and self.getLocation() ==\
           ((9 * WINDOW_WIDTH / 10), ((9 / 32) * WINDOW_WIDTH)):
            return True
        if self.getColor() == "green" and self.getLocation() ==\
           ((WINDOW_WIDTH / 10), (23 * WINDOW_HEIGHT / 32)):
            return True
        return False
    

class Player:
    """ creates a list of pawns and adds them to the win """
    def __init__(self, board, win, color, depth):
        """ each player is associated with a color and will create 4 pieces """
        self._pawns = []
        self._color = color
        self._board = board
        
        if color == 'red':
            center = ((9 * WINDOW_WIDTH / 32), (WINDOW_HEIGHT / 10))
        if color == 'blue':
            center = ((9 * WINDOW_WIDTH / 10), (WINDOW_HEIGHT * 9 / 32))
        if color == 'yellow':
            center = ((23 * WINDOW_WIDTH / 32), (WINDOW_HEIGHT * 9 / 10))
        if color == "green":
            center = ((WINDOW_WIDTH /10), (23 * WINDOW_HEIGHT / 32))
        for _ in range(4):
            pawn = Pawn(self, color, center, depth)
            pawn.addTo(win)
            self._pawns.append(pawn)
                
    def activateAll(self):
        """ activate all of the pawns """
        for pawn in self._pawns:
            pawn.activate()
            
    def deactivateAll(self):
        """deactivate all of the pawns """
        for pawn in self._pawns:
            pawn.deactivate()
    
    def getPawns(self):
        """return the list of pawns """
        return self._pawns
           
    def getColor(self):
        """return the color of the player """
        return self._color
        
    def movePiece(self):
        """move the piece """
        for pawn in self._pawns:
            pawn.move()
            self._board.changeTurn()
    
    def removeList(self, pawn):
        """remove the pawn from the list when it is at 'HOME' """
        self._pawns.remove(pawn)
        
    def changeTurn(self):
        """tell the board to change the turn """
        self._board.changeTurn()
        
    def reportPawnClick(self, piece):
        """ tell the board that the piece has been clicked """
        self._board.reportPawnClick(piece)

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
        
def testGame(win):
    """ test the game """
    _ = Board(win)
    
    
StartGraphicsSystem(testGame, WINDOW_WIDTH, WINDOW_HEIGHT)
