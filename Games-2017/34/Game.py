""" 
*******************************************************************************
File:       Game.py  

Author: Sarah Keefe  

Partner: 

Assignment: Project 6                                                      

Date:       4/30/17                                                         

Description: This file has multiple classes each with multiple methods that
allow the game 'Sorry' to be played. The classes create board spaces and board 
circles and the cards and pawns for the game. There are three event handlers: 
the card, the pawn, and the boardspace. When a card is drawn and a pawn is
clicked the board spaces the pawn can move to are highlighted. When the
highlighted board space is clicked, the graphical pawn object moves. When the 
next card is clicked the turn is changed. 
*******************************************************************************
"""
#There is no way this project would run how it does without the help of the
#wonderful TA's. They helped in too many places to comment in and so many of 
#them helped that I can't name them all. Thanks TA's!

import random
from cs110graphics import *

class BoardSpace(EventHandler):
    """Class to create the spaces in the board"""
    def __init__(self, center, color, index, controller):
        """Creates the board spaces"""
        EventHandler.__init__(self)
        self._center = center
        self._controller = controller
        self._square = Rectangle(25, 25, center)
        self._square.setFillColor(color)
        self._square.addHandler(self)
        self._index = index
        self._active = False 
        
    def addTo(self, win):
        """Adds the board spaces to the window"""
        win.add(self._square)
    
    def getCenter(self):
        """Returns the center of the board space"""
        return self._center 
    
    def getIndex(self):
        """Returns the index of the board space"""
        return self._index 
    
    def setBorderColor(self, color):
        """Sets the border color of the boardspace"""
        self._square.setBorderColor(color)
    
    def boardSpaceActivate(self):
        """Activates the boardspace"""
        self._active = True
    
    def boardSpaceDeactivate(self):
        """Deactivates the board space"""
        self._active = False 
    
    def handleMouseRelease(self, event):
        """"Method that when the highlighted boardspace is clicked the pawn
        moves to that board space and the space is unhighlighted""" 
        if not self._active:
            return
        if self._active:
            self._controller.movePawn(self)
            self._controller.unHighlightSpots()
            
class BoardCircles:
    """Class that creates some of the circles on the board"""
    def __init__(self, radius, center, index, color):
        """Creates the home and start circles"""
        self._center = center
        self._radius = radius 
        self._circle = Circle(radius, center)
        self._circle.setFillColor(color)
        self._index = index 
    
    def getCenter(self):
        """Returns the center of the board circles"""
        return self._center
    
    def setFillColors(self, color):
        """Sets the fill colors of the board circles"""
        self._circle.setFillColor(color)
    
    def getIndex(self):
        """Returns the index of the board circle"""
        return self._index 
    
    def addTo(self, win):
        """Adds the board circle to the window"""
        win.add(self._circle)
    
class Board:
    """Class that will create the graphical objects of the board"""
    #The init for the board is very long because a lot of pieces had to be added
    def __init__(self, win, controller):
        """Creates the game board"""
        self._win = win
        self._controller = controller
        self._active = False 
        
        #makes a deck on the window 
        self._card = Deck(win) 
        
        #adds the button and text to the window 
        self._button = EndGame(win, 30, (500, 50), 'white')
        self._button.addTo(self._win)
        self._text = Text(' ', (600, 75), 20)
        win.add(self._text)
        
       #creates the outside rectangles
        spaceTopLst = []
        spaceRightLst = []
        spaceBottomLst = []
        spaceLeftLst = []
        for i in range(0, 375, 25):
            spaceTop = BoardSpace((12.5 + i, 12.5), 'white', i / 25, 
                                  self._controller)
            spaceTopLst.append(spaceTop)
            spaceTop.addTo(self._win)
            spaceRight = BoardSpace((387.5, 12.5 + i), 'white', (i / 25) + 15, 
                                    self._controller)
            spaceRightLst.append(spaceRight)
            spaceRight.addTo(self._win)
            spaceBottom = BoardSpace((387.5 - i, 387.5), 'white', 
                                     (i / 25) + 30, self._controller)
            spaceBottomLst.append(spaceBottom)
            spaceBottom.addTo(self._win)
            spaceLeft = BoardSpace((12.5, 387.5 - i), 'white', (i / 25) + 45,
                                   self._controller)
            spaceLeftLst.append(spaceLeft)
            spaceLeft.addTo(self._win)
        self._squares = (spaceTopLst + spaceRightLst + spaceBottomLst 
                         + spaceLeftLst)
       
        #creates the safe spaces
        yellowSafe = []
        greenSafe = []
        redSafe = []
        blueSafe = []
        for i in range(0, 125, 25):
            yellowSafeSpace = BoardSpace((62.5, 37.5 + i), 'yellow', (i / 25)
                                         + 60, self._controller)
            yellowSafe.append(yellowSafeSpace)
            yellowSafeSpace.addTo(self._win)
            greenSafeSpace = BoardSpace((362.5 - i, 62.5), 'green', (i / 25) 
                                        + 65, self._controller)
            greenSafe.append(greenSafeSpace)
            greenSafeSpace.addTo(self._win)
            redSafeSpace = BoardSpace((337.5, 362.5 - i), 'red', (i / 25) + 70, 
                                      self)
            redSafe.append(redSafeSpace)
            redSafeSpace.addTo(self._win)
            blueSafeSpace = BoardSpace((37.5 + i, 337.5), 'blue', (i / 25) + 75,
                                       self._controller)
            blueSafe.append(blueSafeSpace)
            blueSafeSpace.addTo(self._win)
        self._safeSpace = yellowSafe + greenSafe + redSafe + blueSafe
        
        #make a list of the centers where the HOME circles are and add a circle
        homes = []
        boardHome = [(62.5, 180), (220, 62.5), (337.5, 220), (180, 337.5)]
        for i in range(len(boardHome)):
            homeSpot = BoardCircles(30, boardHome[i], i + 81, 'white')
            homes.append(homeSpot)
            homeSpot.addTo(self._win)
        coloredHomes = homes
        
        #make a list of the centers where the START circles are and add a circle
        starts = []
        boardStart = [(112.5, 55), (345, 112.5), (292.5, 340), (55, 290)]
        for i in range(len(boardStart)):
            startSpot = BoardCircles(30, boardStart[i], i + 85, 'white')
            starts.append(startSpot)
            startSpot.addTo(self._win)
        coloredStarts = starts
        
        #make a list of the 4 colors and make the different circles the colors
        colors = ['yellow', 'green', 'red', 'blue']  
        for i in range(len(colors)):
            coloredHomes[i].setFillColors(colors[i])
            coloredStarts[i].setFillColors(colors[i])
            
        #is a list of all the board spaces to be accessed later    
        self._totalSpaceLst = (self._squares + self._safeSpace + coloredHomes 
                               + coloredStarts)
        
    def getTotalLst(self):
        """Returns the list of all the indices of the spaces on the board"""
        return self._totalSpaceLst
   
    def getDeck(self):
        """Returns the card"""
        return self._card

    def boardSpaceActivate(self):
        """Activates the board space"""
        #This is also in the boardSpace class but when one of them is removed 
        #the pawn move doesn't work and I couldn't figure out why
        self._active = True

    def boardSpaceDeactivate(self):
        """Deactivates the board space"""
        #This is also in the boardSpace class but when one of them is removed 
        #the pawn move doesn't work and I couldn't figure out why 
        self._active = False 
    
class Deck:
    """A class for building a deck of cards. This class is not graphical"""
    #this class was modified from the deck project 
    def __init__(self, win):
        """Creates a complete deck of 45 playing cards."""
        #the code to create the cards came from class notes 
        self._resetCards = []
        self._win = win
        self._cards = []
        for name in ['1', '1', '1', '1', '1', '2', '2', '2', '2', '3', '3', '3',
                     '3', '4', '4', '4', '4', '5', '5', '5', '5', '7', '7', '7',
                     '7', '8', '8', '8', '8', '10', '10', '10', '10', '11',
                     '11', '11', '11', '12', '12', '12', '12', 'sorry',
                     'sorry', 'sorry', 'sorry', 'sorry']:
            c = Card(name + '.png')
            self._cards.append(c)
        
    def getCards(self):
        """Returns the list of cards"""
        return self._cards
            
    def deal(self):
        """Deals a card"""
        self._resetCards.append(self._cards[-1])
        return self._cards.pop()
    
    def empty(self):
        """Returns True if the deck no longer contains any cards. Otherwise 
        false is returned."""
        return len(self._cards) == 0

    def getDeckLength(self):
        """Returns the number of cards in the deck""" 
        return len(self._cards)
        
    def shuffle(self):
        """All cards currently in the deck are randomly ordered"""
        shuffledCards = []
        while len(self._cards) != 0:
            randomCard = self._cards.pop(random.randrange(len(self._cards)))
            shuffledCards.insert(0, randomCard)
            randomCard.addTo(self._win)
            randomCard.setDepth(len(shuffledCards))
        self._cards = shuffledCards
        
    def addTo(self, win):
        """Adds the cards to the window"""
        for i in range(len(self._cards)):
            self._cards[i].addTo(win)
            
    def reset(self):
        """Resets the deck"""
        self._cards = self._resetCards
        self._resetCards = []
        
class Card:
    """A class used for building graphical playing cards"""
    #This class was modified from the deck project
    def __init__(self, name):
        cardurl = "https://cs.hamilton.edu/~skeefe/images/" + name
        self._card = Image(cardurl, width=142, height=192)
        cardBackurl = "https://cs.hamilton.edu/~skeefe/images/back.png" 
        self._back = Image(cardBackurl, width=142, height=192)
        self._back.setDepth(0)
        self._name = name
    
    def getName(self):
        """Returns an integer if the name of the card is a number"""
        #I was not able to get the sorry card to work because it is saved as 
        #"sorry" when I should have saved it as a number. I realized this too 
        #late and do not have the time to change the name and change other 
        #aspects of this program as well, so I am leaving it
        return int(self._name[0:-4])
            
    def getBack(self):
        """Returns the back of the card"""
        return self._back
        
    def addTo(self, win):
        """Adds the card to the window"""
        win.add(self._back)
        win.add(self._card)
        self._back.moveTo((500, 200))
        self._card.moveTo((500, 200))
            
    def flip(self):
        """Flips the card over"""
        if self._back.getDepth() < self._card.getDepth():
            self._back.setDepth(self._back.getDepth() + 1)
            self._card.setDepth(self._card.getDepth() - 1)
        else: 
            self._back.setDepth(self._back.getDepth() - 1)
            self._card.setDepth(self._card.getDepth() + 1)
            
    def move(self, dx, dy):
        """Moves a card by dx and dy"""
        self._card.move(dx, dy)
        self._back.move(dx, dy)
        
    def setDepth(self, depth):
        """Sets the depth of the card to depth"""
        if self._card.getDepth() < self._back.getDepth():
            self._card.setDepth(depth) 
            self._back.setDepth(depth + 1)
        else:
            self._card.setDepth(depth + 1)
            self._back.setDepth(depth)

class Pawn(EventHandler):
    """Class for creating pawns"""
    def __init__(self, board, center, color, ident, controller, index):
        """Creates a pawn"""
        EventHandler.__init__(self)
        self._board = board
        self._ident = ident
        self._center = center
        self._color = color
        self._controller = controller
        self._index = index
        self._pawn = Circle(8, center)
        self._pawn.setFillColor(self._color)
        self._pawn.addHandler(self)
        self._active = False
        self._started = False 
    
    def isPawnStarted(self):
        """Returns true if the pawn is started"""
        self._started = True 
    
    def pawnStart(self):
        """Returns true or false"""
        return self._started
        
    def pawnActivate(self):
        """Activates the pawn, seen by changing the pawns border color to
        gold"""
        self._active = True
        self._pawn.setBorderColor('gold')
        
    def pawnDeactivate(self):
        """Deactivates the pawn and changes the border color back to black"""
        self._active = False 
        self._pawn.setBorderColor('black')
      
    def isActive(self):
        """Returns true or false"""
        return self._active 
        
    def addTo(self, win):
        """Adds the pawn to the window"""
        win.add(self._pawn)
        
    def getColor(self):
        """Returns the color of the pawn"""
        return self._color 
    
    def getCenter(self):
        """Returns the center of the pawn"""
        return self._center
    
    def getIndex(self):
        """Returns the index of the pawn"""
        return self._index
    
    def setIndex(self, value):
        """Sets the index of the pawn to a value"""
        self._index = value 
    
    def moveTo(self, location):
        """Moves the pawn to a location"""
        self._pawn.moveTo(location)
    
    def handleMouseRelease(self, event):
        """Handles mouse release that will show where the pawn can move once it
        is clicked by highlighting the board space(s) it can move to"""
        if not self._active:
            return
        if self._active:
            self._controller.highlightSpots(self)

class Controller(EventHandler):
    """Creates a class that acts as an event handler"""
    def __init__(self, win):
        """Creates an event handler and calls methods from the previous 
        classes"""
        EventHandler.__init__(self)
        self._win = win
        self._board = Board(win, self)
        self._deck = self._board.getDeck()
        self._deck.shuffle()
        for _ in range(self._deck.getDeckLength()):
            self._deck.deal().getBack().addHandler(self)
        self._deck.reset()
        self._current = 0
        self._players = []
        self._newSpace = None
        self._dealtCard = None
        
        #create the pawns and add them to a list 
        self._pawns = []
        pawnColors = ['yellow', 'yellow', 'yellow', 'yellow', 'green', 'green', 
                      'green', 'green', 'red', 'red', 'red', 'red', 'blue', 
                      'blue', 'blue', 'blue']
        startingCenters = [(100, 45), (100, 65), (122.5, 45), (122.5, 65), 
                           (335, 102.5), (335, 122.5), (355, 102.5), 
                           (355, 122.5), (282.5, 330), (282.5, 350), 
                           (302.5, 330), (302.5, 350), (45, 277.5), 
                           (45, 297.5), (65, 277.5), (65, 297.5)]
        for i in range(len(startingCenters)):
            center = startingCenters[i]
            ident = i
            color = pawnColors[i]
            #the starting index of the pawn is set to 85, 86, 87, or 88 because
            #those are the indices of the start circles where the pawns are 
            #placed at the beginning of the game
            self._pawn = Pawn(self._board, center, color, ident, self, 
                              (i // 4) + 85)
            self._pawn.addTo(win)
            self._pawns.append(self._pawn)
        self._currentPawn = self._pawn
     
    #assigns the created pawns to the four players   
        self._player0 = []
        self._player1 = []
        self._player2 = []
        self._player3 = []
        self._current = 0
        
        for i in range(len(self._pawns)):
            if self._pawns[i].getColor() == 'yellow':
                self._player0.append(self._pawns[i])
            if self._pawns[i].getColor() == 'green':
                self._player1.append(self._pawns[i])
            if self._pawns[i].getColor() == 'red':
                self._player2.append(self._pawns[i])
            if self._pawns[i].getColor() == 'blue':
                self._player3.append(self._pawns[i])
        self._players = [self._player0, self._player1, self._player2, 
                         self._player3]
        #sets the first player's pawns
        self._currentPlayer = self._players[self._current]
        
        #activates the pawns of the first player
        for i in range(len(self._currentPlayer)):
            self._currentPlayer[i].pawnActivate()
    
        #creates the text that will appear on the window showing the color of
        #the pawns that are currently active
        self._text = Text(' ', (200, 200), 20)
        self._win.add(self._text)
        self._text.setText("YELLOW'S TURN")
        
    def changeTurn(self):
        """Changes the turn"""
        #deactivates the current player's pawns
        for i in range(len(self._currentPlayer)):
            self._currentPlayer[i].pawnDeactivate()
        
        #changes the current player
        self._current = (self._current + 1) % 4 
        self._currentPlayer = self._players[self._current]
        
        #activates the current player's pawns
        for j in range(len(self._currentPlayer)):
            self._currentPlayer[j].pawnActivate()
 
        #the text is changed as the turn is changed
        if self._current == 0:
            self._text.setText("YELLOW'S TURN")
        elif self._current == 1:
            self._text.setText("GREEN'S TURN")
        elif self._current == 2:
            self._text.setText("RED'S TURN")
        else: 
            self._text.setText("BLUE'S TURN")
        
    def movePawn(self, boardSpace):
        """Moves the pawn graphical object """
        self._currentPawn.setIndex(boardSpace.getIndex())
        self._currentPawn.moveTo(boardSpace.getCenter())
            
    def highlightSpots(self, pawn): 
        """Highlights the spots (by changing the border color to gold) the pawn
        can move to based on the dealt card"""
        self._currentPawn = pawn
        
        #only allows the pawns to leave start if a 1 or 2 card is drawn
        if self._currentPawn.getIndex() in [85, 86, 87, 88]:
            if self._dealtCard.getName() in [1, 2]:
                firstSpace = int(((self._currentPawn.getIndex() - 85) * 15) + 4)
                self._newSpace = ((firstSpace + self._dealtCard.getName() - 1) 
                                  % 60)
                self._currentPawn.setIndex(self._newSpace)
                self._board.getTotalLst()[self._newSpace].setBorderColor('gold')
                self._board.getTotalLst()[self._newSpace].boardSpaceActivate()
                pawn.isPawnStarted()
            else:
                return
        
        #pawns can move once they have left start 
        #The new spaces are % 60 because that allows the pawn to keep moving 
        #around the board
        elif pawn.pawnStart():
            firstSpace = self._currentPawn.getIndex()
            if self._dealtCard.getName() in [1, 2, 3, 5, 8, 11, 12]:
                self._newSpace = ((firstSpace + self._dealtCard.getName())
                                  % 60)
            elif self._dealtCard.getName() == 4:
                self._newSpace = ((firstSpace - self._dealtCard.getName())
                                  % 60)
            elif self._dealtCard.getName() == 7:
                self._newSpace = ((firstSpace + self._dealtCard.getName())
                                  % 60)
            elif self._dealtCard.getName() == 10:
                self._newSpace = ((firstSpace + self._dealtCard.getName()) 
                                  % 60)
                secondNewSpace = (firstSpace - 1) % 60
                self._board.getTotalLst()[secondNewSpace].setBorderColor('gold')
                self._board.getTotalLst()[secondNewSpace].boardSpaceActivate()
            else:
                return
            self._board.getTotalLst()[self._newSpace].setBorderColor('gold')
            self._board.getTotalLst()[self._newSpace].boardSpaceActivate()
        else:
            return 
        
    def unHighlightSpots(self):
        """Unhighlights the spots by changing the border color back to black"""
        self._board.getTotalLst()[self._newSpace].setBorderColor('black')
        self._board.getTotalLst()[self._newSpace].boardSpaceDeactivate()
            
    def handleMouseRelease(self, event):
        """Deals the cards and places them face down on the table then flips the
        card over and moves it to the discard pile. Does this until the deck is
        empty and then repeats. """
        if self._deck.getDeckLength() != 0:
            gameCard = self._deck.deal()
            self._dealtCard = gameCard
            gameCard.flip()
            gameCard.move(200, 0)
            gameCard.setDepth(1)
            
        if self._deck.getDeckLength() == 0:
            self._deck.reset()
            for card in self._deck.getCards():
                card.flip()
                card.move(-200, 0)

        self.changeTurn()   
        
class EndGame(EventHandler):
    """Class that will end the game"""
    def __init__(self, win, radius, center, color):
        """Creates the text and button"""
        EventHandler.__init__(self)
        self._win = win
        self._radius = radius
        self._center = center
        self._color = color
        self._circle = Circle(radius, center)
        self._circle.setFillColor(color)
        self._circle.addHandler(self)
        self._text = Text(' ', (600, 75), 20)
        
    def addTo(self, win):
        """Adds the button to the window"""
        win.add(self._circle)
    
    def handleMousePress(self, event):
        """When the button is clicked Game over appears"""
        self._text.setText('Game Over')
        self._win.add(self._text)
        
def main(win):
    """Function to run the program"""
    win.setHeight(400)
    win.setWidth(800)
    _ = Controller(win)
StartGraphicsSystem(main)
        
