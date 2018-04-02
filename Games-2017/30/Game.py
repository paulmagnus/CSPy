"""
--------------------------------------------------------------------------------
********************************************************************************
*Project: Game.py                                                              *
*Author: Pete Ross                                                             *
*Partner: Griffin Dunne                                                        *
*Date: 4/10/17                                                                 *
*Description: This project will create the board game Sorry.                   *
********************************************************************************
--------------------------------------------------------------------------------
"""

import random
from cs110graphics import *

class Board:
    """This class creates the board"""
    
    def __init__(self, win):
        """#T#his function uses an image as the board after resizing it to the\
           correct window lengths."""
           
        self._board = Image("http://cs.hamilton.edu/~gdunne/images/" +
                            "sorryboardfinished",\
                            center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2),
                            width=400, height=400)
                            
        self._board.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.addTo(win)                         #adds board to window
        self._currentCard = 0
        xpos, ypos = 0, 0
        self._spaces = []
        self._gotsorry = False
        self._sorrypiece = None
        self._goAgain = False
        self._switched = False
        self._switchpiece = None
        self._tallyred = 0
        self._tallyblue = 0
        self._tallygreen = 0
        self._tallyyellow = 0
        d1 = Deck(win, self)                    #adds deck to window
        d1.shuffle()
        while not d1.empty():
            d1.deal()                           #deals the shuffled deck
                
        self._card = None
    
        for _ in range(60):
            allSpaces = BoardSpace(self, (xpos, ypos))
            allSpaces.addTo(win)                #adds board spaces to the window
            if xpos == WINDOW_WIDTH:
                ypos += (WINDOW_HEIGHT / 16)
            if ypos == 0:
                xpos += (WINDOW_WIDTH / 16)
            if ypos == WINDOW_HEIGHT:
                xpos -= (WINDOW_WIDTH / 16)
            if xpos == 0 and ypos <= WINDOW_HEIGHT and ypos != 0:
                ypos -= (WINDOW_HEIGHT / 16)
            self._spaces.append(allSpaces)
            
        self._players = []
        colors = ['red', 'green', 'yellow', 'blue']
        depth = 0
        for color in colors:
            pawn1 = Player(self, win, color, depth)
            self._players.append(pawn1)         #adds the players to the board
        self._current = 1
        self.changeTurn()                       #changes turn once movement

        
    def addTo(self, win):
        """Adds the squares to the boards"""
        
        win.add(self._board)
    
    def changeTurn(self):
        """This function changes the turn after a player moves"""
        if not self._goAgain:
            self._players[self._current].deactivateAll()
            self._current -= 1                      #Changes the turn of players
            self._current %= 4
            self._gotsorry = False
        else:
            self._goAgain = False
        
        
    def reportCardClick(self, card):
        """This allows the classes to communicate with each other"""
        self._players[self._current].activateAll()
        self._card = card.getValue()            #Returns the value of the card
    
    def reportPawnClick(self, piece):
        """This function moves the Pawn when it is clicked"""
        if self._card == 'sorry':
            if self._sorrypiece == None:
                self._sorrypiece = piece
            elif not self._gotsorry:
                newLoc = piece.getCenter()
                self._sorrypiece.moveTo(newLoc)
                self._gotsorry = True
                piece.sendHome()
                piece.deactivate()
                self._sorrypiece.deactivate()
                self._sorrypiece = None
                self.changeTurn()
                return
            
        if self._card == 'switch':
            if self._switchpiece == None:
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
        self.endGame()
        
        
    def movePawn(self, piece):
        """Calls the move function"""
        
        i = 0
        if self._card == 'sorry':
            self.checkOtherPawns()
            
        elif self._card == '10':
            if not piece.isAtHome():
                i = int(input("10 Spaces forward or 1 backward (10 or 1)"))
                if i == 1:
                    piece.move("-1")
                else:
                    for _ in range(int(self._card)):
                        piece.move('10')
        
        elif self._card == '2':
            self._goAgain = True
            if not piece.isAtHome():
                for _ in range(int(self._card)):
                    piece.move(self._card)
            else:
                piece.move('1')
        else:
            for _ in range(int(self._card)):
                piece.move(self._card)
            piece.slides()        
        
    
    def endGame(self):
        for player in self._players:
            pawn = player.getPawns()
            for pawn in player.getPawns():
                if pawn.getColor() == 'red':
                    if pawn.getCenter() == ((5 * WINDOW_HEIGHT / 32, \
                                             13 * WINDOW_HEIGHT / 32)):
                        player.removeList(pawn)
                        self._tallyred += 1
                if pawn.getColor() == 'blue':
                    if pawn.getCenter() == ((19 * WINDOW_HEIGHT / 32, \
                                             5 * WINDOW_HEIGHT / 32)):
                        player.removeList(pawn)
                        self._tallyblue += 1
                if pawn.getColor() == 'yellow':
                    if pawn.getCenter() == ((27 * WINDOW_HEIGHT / 32, \
                                             19 * WINDOW_HEIGHT / 32)):
                        player.removeList(pawn)
                        self._tallyyellow += 1
                if pawn.getColor() == 'green':
                    if pawn.getCenter() == ((13 * WINDOW_HEIGHT / 32, \
                                             27 * WINDOW_HEIGHT / 32)):
                        player.removeList(pawn)
                        self._tallygreen += 1
        if self._tallyred == 4:
            print('The winner is red!')
        if self._tallyblue == 4:
            print('The winner is blue!')
        if self._tallyyellow == 4:
            print('The winner is yellow!')
        if self._tallygreen == 4:
            print('The winner is green!')
        self.endSequence()
        
    def endSequence(self):
        """Deactivates completed pawns"""
        for player in self._players:
            pawns = player.getPawns()
            for pawn in pawns:
                pawn.deactivate()
        
        
    def checkOtherPawns(self):
        """Checks if pawns are safe"""
        for player in self._players:
            pawns = player.getPawns()
            for pawn in pawns:
                if not pawn.isSafe():
                    pawn.activate()
    
class Card(EventHandler):
    """This class creates the cards that will be drawn randomly"""
    
    def __init__(self, value, deck):
        """Creates the cards that players will draw"""
        
        faceurl = "http://cs.hamilton.edu/~gdunne/images/sorry" + value
        self._face = Image(faceurl, center=((WINDOW_WIDTH * 27 / 64), \
                          (WINDOW_HEIGHT * 28 / 64)), 
                           width=WINDOW_HEIGHT/(25/6), 
                           height=WINDOW_HEIGHT/3.597)
                           
        backurl = "http://cs.hamilton.edu/~gdunne/images/backofsorry"
        self._back = Image(backurl, center=((WINDOW_WIDTH * 27 / 64), \
                          (WINDOW_HEIGHT * 28 / 64)), 
                           width=WINDOW_HEIGHT/(25/6), 
                           height=WINDOW_HEIGHT/3.597)
                           
        self._faceup = False
        self._window = None
        self._value = value
        EventHandler.__init__(self)
        self._back.addHandler(self)
        self._deck = deck
       
        
    def handleMouseRelease(self, event):
        """When the mouse clicks the deck, a card will flip and move to a new\
           deck"""
           
        self.flip()                             #flips the cards
        self.move((WINDOW_WIDTH / 4), (WINDOW_HEIGHT / 4))
        self._deck.reportCardClick(self)
       
    def getValue(self):
        """Returns the values of the card"""
        
        return self._value
  

    def addTo(self, win):
        """Adds the cards to the window"""
        
        if self._faceup:
            win.add(self._face)
        else:
            win.add(self._back)
        self._window = win
        
    def removeFrom(self, win):
        """Removes the cards from the window"""
        
        if self._faceup:
            win.remove(self._face)              #removes drawn cards from the
        else:                                   #deck
            win.remove(self._back)
        self._window = None
        
    def flip(self):
        """Flips the card over. If face down, the card is flipped to face up,
        or vice versa. This visually flips the card over as well. May be called
        on all cards whether they have been added to a window or not."""
        
        newwindow = self._window
        
        if newwindow != None:
            self.removeFrom(newwindow)      
            
        if self._faceup:
            self._faceup = False
        else:
            self._faceup = True
            
        if newwindow != None:
            self.addTo(newwindow)
    
        self.setDepth(0)
    
    def move(self, dx, dy):
        """Moves a card by dx and dy."""
        
        self._face.move(dx, dy)                 #moves the flipped cards
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
        
        
class Deck:
    """This class is a deck of cards"""
       
    def __init__(self, win, board):
        """Creates a complete deck of sorry cards."""
        self._deck = []                     #creates an empty list for the deck
        self._win = win
        self._currentDepth = 0              #sets depth to 0
        self._piece = []
        self._board = board
        self._spaces = []

        for value in ['1']:
            for _ in range(20):
                c = Card(value, self)
                self._deck.append(c)
                
        for value in ['2', '3', '4', '5', '7', '8', '10', '11', '12',\
                      'sorry']:
            for _ in range(16):
                c = Card(value, self)
                self._deck.append(c)
                                            
                                        #adds all cards to the deck
            
            

    def empty(self):
        """Returns True if the deck no longer contains any cards. Otherwise
        false is returned."""
        
        if len(self._deck) == 0:
            return True                 #returns true if deck is empty
            
        return False
        
    
    def deal(self):
        """Deals a card. A card is removed from the top of the deck and
        returned."""
        
        self._deck[0].setDepth(self._currentDepth)
        self._currentDepth += 1             #raises the card to the top
        
        #self._value = self._deck[0].getValue()
        self._deck.pop(0).addTo(self._win)
       # print(getValue())
        
    
    def shuffle(self):
        """All cards currently in the deck are randomly ordered """
        
        shuffledSet = []
        for _ in range(len(self._deck)):  #shuffles all of the cards
            while len(self._deck) > 0:
                index = random.randrange(0, len(self._deck))
                shuffledSet.append(self._deck.pop(index))
        
        self._deck = shuffledSet
        return self._deck
        
    def reportCardClick(self, card):
        """Allows the cards to communicate with the board"""
        self._board.reportCardClick(card)


 

class Pawn(EventHandler):
    """This class creates all of the pawns which players move around the
       board """
       
    def __init__(self, color, center, board, player, depth):
        """Creates the pawns and makes them event handlers."""
        
        self._piece = Rectangle((WINDOW_WIDTH / 40), (WINDOW_HEIGHT / 40),\
                      center)
                      
        self._posx, self._posy = center
        self._piece.setFillColor(color)
        EventHandler.__init__(self)
        
        self._piece.addHandler(self)
        self._color = color                     #initializes variables
        self._board = board
        self._active = False
        self._player = player
        self._safe = True
        self._piece.setDepth(depth)


    def handleMouseRelease(self, event):
        """When the mouse clicks the pawn, it moves a certain distance"""
        
        
        if not self._active:
            return
        else:
            self.updateLocation()
            self._player.reportPawnClick(self)

        
    def move(self, cardValue):
        """Allows the pawns to move in certain directions based on their
           positions on the board"""
           
        self.homeStretch()
        
        if self._posx < (31 * WINDOW_WIDTH / 32) and self._posy == \
        (WINDOW_HEIGHT / 32):
            if cardValue == '-1' or cardValue == '4':
                self.moveLeft()
            else:
                self.moveRight()
        if self._posx == (31 * WINDOW_WIDTH / 32) and self._posy < \
        (31 * WINDOW_HEIGHT / 32):
            if cardValue == '-1' or cardValue == '4':
                self.moveUp()
            else:
                self.moveDown()
        
        if self._posx <= (31 * WINDOW_WIDTH / 32) and self._posy == \
        (31 * WINDOW_HEIGHT / 32) and self._posx != (WINDOW_WIDTH / 32):
            if cardValue == '-1' or cardValue == '4':
                self.moveRight()
            else:
                self.moveLeft()
        if self._posx == (WINDOW_WIDTH / 32) and self._posy <= \
        (31 * WINDOW_HEIGHT / 32) and self._posy != (WINDOW_HEIGHT / 32):
            if cardValue == '-1' or cardValue == '4':
                self.moveDown()
            else:
                self.moveUp()
        
        
        if cardValue == '1' or cardValue == '2':
            if self._posx == (9 * WINDOW_WIDTH / 32) and self._posy == \
            (WINDOW_HEIGHT / 10):
                self._piece.moveTo((9 * WINDOW_WIDTH / 32, WINDOW_HEIGHT / 32))
                return True
                
            if self._posx == (23 * WINDOW_WIDTH / 32) and self._posy == \
            (9 * WINDOW_HEIGHT / 10):              
                self._piece.moveTo((23 * WINDOW_WIDTH / 32, 31 * \
                WINDOW_HEIGHT / 32))
                return True
                
            if self._posx == (9 * WINDOW_WIDTH / 10) and self._posy == \
            (9 * WINDOW_HEIGHT / 32):
                self._piece.moveTo((31 * WINDOW_WIDTH / 32, \
                9 * WINDOW_HEIGHT / 32))
                return True
            
            if self._posx == (WINDOW_WIDTH / 10) and self._posy == \
            (23 * WINDOW_HEIGHT / 32):
                self._piece.moveTo(((WINDOW_WIDTH / 32), \
                23 * WINDOW_HEIGHT / 32))
            return True
        
        self.updateLocation()
        
    def slides(self):
        """Allows the pawns to slide when the reach a slide that is not their
           own color """
        
        if self._color != 'red':
            if self._posx == (3 * WINDOW_WIDTH / 32) and \
            self._posy == (WINDOW_HEIGHT / 32):
                self._piece.moveTo(((9 * WINDOW_WIDTH / 32), \
                WINDOW_HEIGHT / 32))
            if self._posx == (19 * WINDOW_WIDTH / 32) and \
            self._posy == WINDOW_WIDTH / 32:
                self._piece.moveTo(((WINDOW_WIDTH * 27 / 32), \
                WINDOW_HEIGHT / 32))
                
        if self._color != 'blue':
            if self._posx == (31 * WINDOW_WIDTH / 32) and \
            self._posy == 3 * WINDOW_WIDTH / 32:
                self._piece.moveTo(((31 * WINDOW_WIDTH / 32), \
                9 * WINDOW_HEIGHT / 32))
            if self._posx == (31 * WINDOW_WIDTH / 32) and \
            self._posy == (19 * WINDOW_WIDTH / 32):
                self._piece.moveTo(((31 * WINDOW_WIDTH / 32), \
                (WINDOW_WIDTH * 27 / 32)))
                
        if self._color != 'yellow':
            if self._posx == (29 * WINDOW_WIDTH / 32) and \
            self._posy == (31 * WINDOW_WIDTH / 32):
                self._piece.moveTo((23 * WINDOW_HEIGHT / 32, \
                (31 * WINDOW_WIDTH / 32)))
            if self._posx == 13 * WINDOW_HEIGHT / 32 and \
            self._posy == (31 * WINDOW_WIDTH / 32):
                self._piece.moveTo(((5 * WINDOW_WIDTH / 32), \
                (31 * WINDOW_WIDTH / 32)))
            
        if self._color != 'green':
            if self._posx == WINDOW_WIDTH / 32 and \
            self._posy == (29 * WINDOW_WIDTH / 32):
                self._piece.moveTo((WINDOW_WIDTH / 32, 23 * WINDOW_HEIGHT / 32))
            if self._posx == WINDOW_WIDTH / 32 and \
            self._posy == 13 * WINDOW_HEIGHT / 32:
                self._piece.moveTo((WINDOW_WIDTH / 32, 5 * WINDOW_WIDTH / 32))
                 
    def homeStretch(self):
        """Moves the pieces down the final stretch and to the end goal"""
       
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
    
    def sendHome(self):
        """Sends the piece to its home position"""
        
        if self.getColor() == 'red':
            self._piece.moveTo(((9 * WINDOW_WIDTH / 32), (WINDOW_HEIGHT / 10)))
            
        if self.getColor() == 'yellow':
            self._piece.moveTo(((23 * WINDOW_WIDTH / 32), \
            (9 * WINDOW_HEIGHT / 10)))
            
        if self.getColor() == 'blue':
            self._piece.moveTo(((9 * WINDOW_WIDTH / 10),  \
            (9 * WINDOW_HEIGHT / 32)))
            
        if self.getColor() == 'green':
            self._piece.moveTo(((WINDOW_WIDTH / 10), \
            (23 * WINDOW_HEIGHT / 32)))
    
    def isAtHome(self):
        """Sends the piece to its home position"""
        
        if self.getColor() == 'red' and self.getCenter() == \
        (((9 * WINDOW_WIDTH / 32), (WINDOW_HEIGHT / 10))):
            return True
            
        if self.getColor() == 'yellow' and self.getCenter() == \
        (((23 * WINDOW_WIDTH / 32), (9 * WINDOW_HEIGHT / 10))):
            return True
            
        if self.getColor() == 'blue' and self.getCenter() == \
        (((9 * WINDOW_WIDTH / 10), (9 * WINDOW_HEIGHT / 32))):
            return True
            
        if self.getColor() == 'green' and self.getCenter() == \
        (((WINDOW_WIDTH / 10), (23 * WINDOW_HEIGHT / 32))) :
            return True
     
        
    def updateLocation(self):
        """Returns the location of the pawn"""
        
        self._posx, self._posy = self._piece.getCenter()
    
    def isSafe(self):
        """Pawns are safe if they are in the home stretch"""
        return self._safe
    
    def addTo(self, win):
        """Adds the pawns to the window"""
        
        win.add(self._piece)
    
    def moveTo(self, loc):
        """Moves pawns to a speicific location """
        self._piece.moveTo(loc)
     
    def moveLeft(self):
        """Moves the piece to the left"""
        self._piece.move(-(WINDOW_WIDTH) / 16, 0)
            
    def moveRight(self):
        """Moves the piece to the right"""
        self._piece.move(WINDOW_WIDTH / 16, 0)
        
    def moveUp(self):
        """Moves the piece up"""
        self._piece.move(0, -(WINDOW_WIDTH)/16)
        
    def moveDown(self):
        """Moves the piece down"""
        self._piece.move(0, WINDOW_WIDTH / 16)
        
    def getCenter(self):
        """Returns the center of the piece"""
        return self._posx, self._posy
            
    def getColor(self):
        """Returns the color of the piece """
        return self._color
    
    def activate(self):
        """If a piece is activated, the border will change colors"""
        self._active = True
        self._piece.setBorderColor("limegreen")
        
    def deactivate(self):
        """If the piece is unactivated, the border will return to black"""
        self._active = False
        self._piece.setBorderColor("black")
        
    

class Player:
    """This class deals with the four players who are playing"""
    
    def __init__(self, board, win, color, depth):
        """Sets the center of the pawns and adds them to the board"""
        self._pawns = []
        self._board = board
    
        if color == 'red':
            center = ((9 * WINDOW_WIDTH / 32), (WINDOW_HEIGHT / 10))
        if color == 'blue':
            center = ((9 * WINDOW_WIDTH / 10), (WINDOW_HEIGHT * 9 / 32))
        if color == 'yellow':
            center = ((23 * WINDOW_WIDTH / 32), (WINDOW_HEIGHT * 9 / 10))
        if color == 'green':
            center = ((WINDOW_WIDTH / 10), (23 * WINDOW_HEIGHT / 32))
            
        for _ in range(4):
            pawn1 = Pawn(color, center, board, self, depth)
            pawn1.addTo(win)       
            self._pawns.append(pawn1)
            
        
    def deactivateAll(self):
        """Deactivates all of the pawns"""
        for pawn in self._pawns:
            pawn.deactivate()
            
            
    def activateAll(self):
        """Activates all of the pawns"""
        for pawn in self._pawns:
            pawn.activate()
            
    def movePiece(self):
        """Moves the piece around the board"""
        for pawn in self._pawns:
            pawn.move()
            self._board.changeTurn()
            
    def reportPawnClick(self, piece):
        """Allows the pawns to communicate with the board"""
        self._board.reportPawnClick(piece)

    def getPawns(self):
        """Returns a list of pawns"""
        return self._pawns
        
    def removeList(self, pawn):
        """Remove the pawn from the list when it is at the finishing place"""
        self._pawns.remove(pawn)
        
    
class BoardSpace(EventHandler):
    """Creates the board spaces around the board"""
    
    def __init__(self, board, center):
        """Makes the spaces around the board"""
        
        EventHandler.__init__(self)
        self._board = board
        self._center = center
        self._square = Rectangle(WINDOW_WIDTH / 8, WINDOW_HEIGHT / 8, center)
        self._square.setBorderColor('black')
        
    def addTo(self, win):
        """Adds the squares to the boards"""
        
        win.add(self._square)

def testgame(win):
    """Tests the game"""
    _ = Board(win)
 
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400 
        
StartGraphicsSystem(testgame, WINDOW_WIDTH, WINDOW_HEIGHT)
