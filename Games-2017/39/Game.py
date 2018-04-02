"""
 *******************************************************************************
    FILE:       Game.py
    
    AUTHOR:     William Benthem de Grave
    
    PARTNER:    Jeff Welch
    
    ASSIGNMENT: Project 6
    
    DATE:       4/7/2017
    
    DESCRIPTION:This program creates a game of Sorry for 4 players
 *******************************************************************************
"""

import random
from cs110graphics import *

class Player:
    """ Contstructs the players, each containing 4 pawns of their color """
    def __init__(self, playerColor, pawnColor, startLocations, startPos, board):
        """ Initializes the attributes of the Player class """
        self._board = board
        self._playerColor = playerColor
        self._pawnColor = pawnColor
        self._startPositions = startPos
        self._startLocations = startLocations
        self._pawns = []
        #pawnColors = ['#990000', '#00BFFF', '#DAA520', '#014421']
        for i in range(4):
            # Uniquely creates a pawn 4 times
            thisPawn = Pawn(board, self._pawnColor, self._startLocations[i],\
                            self._startPositions, self._playerColor)
            self._pawns.append(thisPawn)
        
    def addToWindow(self, win):
        """ Adds the pawns to the window """
        for item in self._pawns:
            item.addToWindow(win)
    
    def activateAll(self):
        """ Activates the pawns """
        for pawn in self._pawns:
            if not pawn.isInHomeCircle():
                pawn.activate()
            
    def deactivateAll(self):
        """ Deactivates the pawns """
        for pawn in self._pawns:
            pawn.deactivate()
    
    def returnPawns(self):
        """Returns all pawns belonging to a player"""
        return self._pawns
            

class Squares:
    """ Constructs the sqaure spaces of the board game """
    def __init__(self, color, center):
        """ Initializes the attributes of the Square class """
        self._rectangle = Rectangle(50, 50, center)
        self._rectangle.setDepth(1)
        self._rectangle.setFillColor(color)
        self._center = center
        self._index = 0
        self._pawn = None
        
    def placePawn(self, pawn):
        """Adds a given pawn to the square, so it can be identified"""
        self._pawn = pawn
        
    def returnCenter(self):
        """ Returns the center of the square """
        return self._center
        
    def returnPawn(self):
        """Returns the pawn that is in the square"""
        return self._pawn
        
    def occupied(self):
        """Returns True if self._pawn is not null, meaning the square is 
        occupied"""
        return self._pawn != None
        
    def removePawn(self):
        """Removes the pawn from the square"""
        self._pawn = None
        
    def addToWindow(self, win):
        """ Adds the spaces to the window """
        win.add(self._rectangle)
    
    def setIndex(self, num):
        """ Assigns an index to each space """
        self._index = num
        
class Slidesquares(Squares):
    """ Constructs the slide squares that trigger pawns to slide """
    def __init__(self, color, length, center):
        """ Initializes the attributes of the Slidesquare class """
        super().__init__(color, center)
        self._lengthOfSlide = length
        self._color = color
        
    def returnSlide(self):
        """Returns the length that the pawn will slide"""
        return self._lengthOfSlide
    
    def returnColor(self):
        """ Returns the color of the slidesquare """
        return self._color

class Sliderec:
    """ Constructs the rectangles of the slides. Purely graphical """
    def __init__(self, length, width, color, center):
        """ Initializes the attributes of the Sliderec class """
        self._sliderec = Rectangle(length, width, center)
        self._sliderec.setDepth(1)
        self._sliderec.setFillColor(color)
        
    def addToWindow(self, win):
        """ Adds the rectangle to the window """
        win.add(self._sliderec)

class Safesquares(Squares):
    """ Constructs the Safesquares of the board """
    def __init__(self, color, center):
        """ Initializes the attributes of the Safesquare class """
        super().__init__(color, center)
        
class Startcircles:
    """ Constructs the Startcircles on the board for the pawns to start in """
    def __init__(self, color, center):
        """ Initializes the attributes of the Startcircles class """
        self._circle = Circle(50, center)
        self._circle.setDepth(1)
        self._circle.setFillColor(color)
        self._index = 0
        
    def addToWindow(self, win):
        """ Adds the circles to the window """
        win.add(self._circle)
        
    def setIndex(self, num):
        """Sets the index of the circle in the master list"""
        self._index = num
        
class Homecircles:
    """ Constructs the Homecircles on the board for the pawns to end in """
    def __init__(self, color, center):
        """ Initializes the attributes of the Homecircles class """
        self._circle = Circle(50, center)
        self._circle.setDepth(1)
        self._circle.setFillColor(color)
        self._center = center
        #self._index = 0
        self._pawnsInHome = 0
        self._rectangle = Rectangle(800, 800, (400, 400))
        self._rectangle.setDepth(-1)
        self._rectangle.setFillColor(color)
        self._text = Text("The winner is " + color + "!!!", (400, 400), 78)
        self._text.setDepth(-2)
        self._lastCounterText = None
        
    def addToWindow(self, win):
        """ Adds the circles to the window """
        win.add(self._circle)
        
    def addPawn(self, win):
        """ Counts the amount of pawns that have entered the Homecircle """
        self._pawnsInHome += 1
        counterText = Text(self._pawnsInHome, (self.returnCenter()[0],\
        self.returnCenter()[1] + 7), 20)
        counterText.setDepth(-1)
        # If counter reaches 4, game is over
        if self._lastCounterText != None:
            win.remove(self._lastCounterText)
        self._lastCounterText = counterText
        win.add(counterText)
    
    def returnCenter(self):
        """ Returns the cetner of the Homecircle """
        return self._center
        
    def occupied(self):
        """ Returns if the Homecircle is occupied, which is always False """
        return False
    
    def determineWinner(self, win):
        """ If 4 pawns have entered Homecircle, the game ends """
        if self._pawnsInHome == 4:
            win.add(self._rectangle)
            win.add(self._text)
            # Determines the winner
        
class Slidecircles:
    """ Constructs the Slidecircles on the board. Purely graphical """
    def __init__(self, color, center):
        """ Initializes the attributes of the Slidecircles class """
        self._circle = Circle(22, center)
        self._circle.setDepth(1)
        self._circle.setFillColor(color)
        
    def addToWindow(self, win):
        """ Adds the circle to the window """
        win.add(self._circle)
        
class Deck(EventHandler):
    """ Constructs a non graphical deck of 45 sorry cards """
    def __init__(self, board, win):
        """ Initializes the attributes of the Deck class """
        EventHandler.__init__(self)
        # "1" occurs 5 times in a sorry deck, so one is added before
        self._cards = [1]
        self._deck = []
        self._win = win
        self._board = board
        backurl = "https://cs.hamilton.edu/~jbwelch/images/sorryBack.png"
        self._cardButton = Image(backurl, (300, 396), 152, 204)
        self._cardButton.setDepth(0)
        self._cardButton.addHandler(self)
        self._currentCard = None
        self._active = True
        self._previousCard = None
        
        for _ in range(4):
            # Creates each card 4 times in the deck
            for item in [1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 'Sorry!']:
                self._cards.append(item)
                
        for i in range(len(self._cards)):
            self._deck.append(Card(self._cards[i]))
            self.shuffle()
    
    def activate(self):
        """Changes the boolean that activates the draw button"""
        self._active = True
        
    def deactivate(self):
        """Changes the boolean that deactivates the draw button"""
        self._active = False
                
    def handleMouseRelease(self, event):
        """ Handles when the deck is clicked """
        if not self._active:
            return
        else:
            # When the game has started, cards can be dealt
            if self._currentCard is None:
                self._board.startGame()
            else:
            # Changes turns on the next deck click
                self._board.changeTurn()
            self.deal()
    
    def addToWindow(self, win):
        """ Adds the deck (back) to the widnow """
        win.add(self._cardButton)
        
        
    def empty(self):
        """ Determines whether the deck is empty or not """
        if len(self._deck) == 0:
            return True
        return False
        
    def deal(self):
        """Deals a card, which is removed and returned """
        if self.empty():
            # Reshuffles if empty
            for i in range(len(self._cards)):
                self._deck.append(Card(self._cards[i]))
            self.shuffle()
        # Removes the drawn card from the deck and makes it equal to a value
        dealtCard = self._deck[0]
        dealtCard.addToWindow(self._win)
        self._deck.remove(dealtCard)
        dealtCard.move(198, 0)
        self._currentCard = dealtCard
        if self._previousCard is not None:
            self._previousCard.removeFrom(self._win)
        self._previousCard = dealtCard

    def getValue(self):
        """ Returns the value of the drawn card """
        return self._currentCard.returnVal()
    
    def shuffle(self):
        """ All cards currently in the deck are randomly ordered """
        lenOfDeck = len(self._deck)
        newDeck = []
        for _ in range(lenOfDeck):
            randomCard = self._deck[random.randrange(len(self._deck))]
            newDeck.append(randomCard)
            self._deck.remove(randomCard)
        self._deck = newDeck
        
class Card:
    """ Constructs a graphical card when given a value from the Deck class """
    def __init__(self, val):
        """ Initializes the attributes of the Card class """
        self._value = val
        self._face = Rectangle(152, 204, (300, 396))
        self._text = Text(self._value, self.getReferencePoint(), 56)
        self._cardParts = [self._face, self._text]
        self._face.setFillColor('white')
        self._depth = 0
        self._dimensions = (154, 204)
        self._flipped = False
        
    def returnVal(self):
        """ Returns the value to the deck class """
        return self._value
        
    def addToWindow(self, win):
        """Adds the card to the given graphics window."""
        for part in self._cardParts:
            win.add(part)
        self.update(self._depth)
        
    def removeFrom(self, win):
        """Removes the card from the given graphics window """
        for part in self._cardParts:
            win.remove(part)
            
    def move(self, dx, dy):
        """ Moves a card by dx and dy """
        for part in self._cardParts:
            part.move(dx, dy)
        
    def getReferencePoint(self):
        """ The point representing the center of the card image is returned """
        return self._face.getCenter()
        
    def setDepth(self, depth):
        """ Sets the depth of graphical objects representing the card to
        depth"""
        self._depth = depth
        self.update(depth)
    
    def update(self, depth):
        """ Prevents overlapping when the cards stack on top of eachother """
        self._text.setDepth(depth)
        self._face.setDepth(depth + 1)

class Pawn(EventHandler):
    """ Constructs 4 pawns per player in the game """
    def __init__(self, board, color, location, position, playerColor):
        """ Initializes the attibutes of the Pawn class """
        EventHandler.__init__(self)
        self._color = color
        self._playerColor = playerColor
        self._board = board
        # Location and Position are to be used and changed seperatly
        self._location = location
        self._position = position # Current logical position on the board
        self._circle = Circle(15, location)
        self._circle.setDepth(0)
        self._circle.setFillColor(color)
        self._circle.setBorderWidth(2)
        self._circle.addHandler(self)
        # Pawn booleans that are subject to change
        self._isInStart = True
        self._isInSafesquare = False
        self._active = False
        self._homeStretch = False
        self._isInHomeCircle = False
        
        # These attributes will not change, for reference
        self._startPosition = position
        self._startLocation = location
    
    def addToWindow(self, win):
        """ Adds the pawns to the window """
        win.add(self._circle)
        
    def activate(self):
        """ Activates the pawn """
        if not self.isInHomeCircle():
            self._active = True
            self._circle.setBorderColor('green')
        
    def deactivate(self):
        """ Deactivates the pawn """
        self._active = False
        self._circle.setBorderColor('black')
    
    def handleMouseRelease(self, event):
        """ Reports the pawn being clicked to the board """
        if self._active:
            self._board.reportPawnClick(self)
    
    def getPosition(self):
        """ Returns the position of the pawn """
        return self._position
        
    def returnColor(self):
        """ Returns the color of the pawn """
        return self._playerColor
        
    def changeIsInStart(self):
        """ Changes the boolean of whether or not the pawn is in the start 
        circle """
        self._isInStart = not self._isInStart
    
    def isInSafesquareTrue(self):
        """ Changes the boolean of whether the pawn is in a safe square to 
        true """
        self._isInSafesquare = True
        
    def isInSafesquareFalse(self):
        """ Changes the boolean of whether the pawn is in a safe square to 
        false """
        self._isInSafesquare = False
        
    def homeStretchTrue(self):
        """ Changes the boolean of whether the pawn is in the home stretch to 
        true """
        self._homeStretch = True
        
    def homeStretchFalse(self):
        """ Changes the boolean of whether the pawn is in the home stretch to 
        false """
        self._homeStretch = False
        
    def isInHomeCircleTrue(self):
        """ Changes the boolean of whether the pawn is in the home circle to 
        true """
        self._isInHomeCircle = True
        
    def isInStart(self):
        """ Returns the boolean that determines if the pawn is in start """
        return self._isInStart
        
    def isInSafesquare(self):
        """ Returns the boolean that determines if the pawn is in a safe 
        square """
        return self._isInSafesquare
        
    def isHomeStretch(self):
        """ Returns the boolean that determines if the pawn is in the home
        stretch, changing its move track to that of its color """
        return self._homeStretch
    
    def isInHomeCircle(self):
        """ Returns the boolean that determines if the pawn is in the home 
        circle """
        return self._isInHomeCircle
    
    def setPosition(self, pos):
        """ Sets the position of the pawn """
        self._position = pos
        
    def moveTo(self, location):
        """ Moves the pawn to a given location """
        self._circle.moveTo(location)
        
    def returnToStart(self):
        """ Returns the given pawn to start, changing any attributes """
        self._isInStart = True
        self.moveTo(self._startLocation)
        self._position = self._startPosition
        
class Board:
    """ Constructs the board so the game can be played (yay!) """
    def __init__(self, win):
        """ Initializes the attributes of the Board class """
        
        self._deck = Deck(self, win)
        
        # Graphical lists with events
        self._trackSquares = []
        self._trackCircles = []
        self._trackSafeSquares = []
        self._masterList = []
        
        # Graphical lists without events
        self._trackSC = []
        self._trackRec = []
        
        # End tracks of each color of pawn
        self._redTrack = [51, 52, 53, 54, 55, 56, 57, 58, 59, 0, 1, 2, 68, 69,
                          70, 71, 72, 64]
        self._blueTrack = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 73, 74, 
                           75, 76, 77, 65]
        self._yellowTrack = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 78,
                             79, 80, 81, 82, 66]
        self._greenTrack = [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 83,
                            84, 85, 86, 87, 67]
        
        # Assigns each pawn of each player a starting position on the board
        self._pawnStartLocations = [[(250, 125), (200, 125), (250, 75),
                                     (200, 75)],
                                    [(675, 250), (675, 200), (725, 250),
                                     (725, 200)],
                                    [(550, 675), (600, 675), (550, 725),
                                     (600, 725)],
                                    [(125, 550), (125, 600), (75, 550),
                                     (75, 600)]]
        self._players = []
        playerColors = ['red', 'blue', 'yellow', 'green']
        # Pawns are different colors so they don't blend in with the board
        pawnColors = ['#990000', '#00BFFF', '#DAA520', '#014421']
        startPositions = [60, 61, 62, 63]
        for i in range(len(playerColors)):
            self._players.append(Player(playerColors[i], pawnColors[i],\
                                        self._pawnStartLocations[i],\
                                        startPositions[i], self))
                                        
        self._current = None
        
        self._win = win
        
        trackSqColors = [('red', 50, 0), ('blue', 0, 50), ('yellow', -50, 0),
                         ('green', 0, -50)]
        x = 25
        y = 25
        
        # Adds both regular sqaures and slide sqaures in order to the board
        for color in trackSqColors:
            self._trackSquares.append(Squares('white', (x, y)))
            x += color[1]
            y += color[2]
            self._trackSquares.append(Slidesquares(color[0], 3, (x, y)))
            x += color[1]
            y += color[2]
            for _ in range(7):
                self._trackSquares.append(Squares('white', (x, y)))
                x += color[1]
                y += color[2]
            self._trackSquares.append(Slidesquares(color[0], 4, (x, y)))
            x += color[1]
            y += color[2]
            for _ in range(5):
                self._trackSquares.append(Squares('white', (x, y)))
                x += color[1]
                y += color[2]

        redSafeSquares = []
        blueSafeSquares = []
        yellowSafeSquares = []
        greenSafeSquares = []

        for i in range(5):
            redSafeSquares.append(Safesquares('red', (125, 75 + i * 50)))
            blueSafeSquares.append(Safesquares('blue', (725 - 50 * i, 125)))
            yellowSafeSquares.append(Safesquares('yellow', (675, 725 - i * 50)))
            greenSafeSquares.append(Safesquares('green', (75 + i * 50, 675)))
        
        self._firstPawn = None
        self._secondClick = False
        
        # Creates the rest of the graphical board
        
        self._trackCircles.append(Startcircles('red', (225, 100)))
        self._trackCircles.append(Startcircles('blue', (700, 225)))
        self._trackCircles.append(Startcircles('yellow', (575, 700)))
        self._trackCircles.append(Startcircles('green', (100, 575)))
        
        self._trackCircles.append(Homecircles('red', (125, 350)))
        self._trackCircles.append(Homecircles('blue', (450, 125)))
        self._trackCircles.append(Homecircles('yellow', (675, 450)))
        self._trackCircles.append(Homecircles('green', (350, 675)))
        
        self._trackSC.append(Slidecircles('red', (225, 25)))
        self._trackSC.append(Slidecircles('red', (675, 25)))
        self._trackSC.append(Slidecircles('blue', (775, 225)))
        self._trackSC.append(Slidecircles('blue', (775, 675)))
        self._trackSC.append(Slidecircles('yellow', (575, 775)))
        self._trackSC.append(Slidecircles('yellow', (125, 775)))
        self._trackSC.append(Slidecircles('green', (25, 575)))
        self._trackSC.append(Slidecircles('green', (25, 125)))
        
        self._trackRec.append(Sliderec(140, 25, 'red', (170, 25)))
        self._trackRec.append(Sliderec(190, 25, 'red', (595, 25)))
        self._trackRec.append(Sliderec(25, 140, 'blue', (775, 170)))
        self._trackRec.append(Sliderec(25, 190, 'blue', (775, 595)))
        self._trackRec.append(Sliderec(140, 25, 'yellow', (630, 775)))
        self._trackRec.append(Sliderec(190, 25, 'yellow', (205, 775)))
        self._trackRec.append(Sliderec(25, 140, 'green', (25, 630)))
        self._trackRec.append(Sliderec(25, 190, 'green', (25, 205)))
        
        background = Square(800, (400, 400))
        background.setDepth(10)
        background.setFillColor("lightgreen")
        win.add(background)
        sorry = Text("SORRY!", (400, 275), 100)
        sorry.setDepth(0)
        win.add(sorry)
    
        # Adds the safe squares to a larger list
        self._trackSafeSquares = self._trackSafeSquares + redSafeSquares +\
        blueSafeSquares + yellowSafeSquares + greenSafeSquares
        
        # Compiles all indexed squares into a master list
        self._masterList += self._trackSquares + self._trackCircles +\
        self._trackSafeSquares
        
    
    def addToWindow(self):
        """ Adds the elements of the board to the window """
        for item in self._masterList:
            item.addToWindow(self._win)
        for rectangle in self._trackRec:
            rectangle.addToWindow(self._win)
        for circle in self._trackSC:
            circle.addToWindow(self._win)
        for player in self._players:
            player.addToWindow(self._win)
        self._deck.addToWindow(self._win)
    
    def changeTurn(self):
        """ Changes what player's turn it is """
        for player in self._players:
            player.deactivateAll()
        if self._deck.getValue() != 2:
            self._current += 1
        if self._secondClick:
            self._secondClick = not self._secondClick
        self._current %= 4
        self._players[self._current].activateAll()

    def startGame(self):
        """ Starts the game """
        self._current = 0
        self._players[self._current].activateAll()
        
    def isSecondClick(self):
        """ Reports when a second click has been made for cards 10, 11, and
        Sorry! """
        return self._secondClick
        
    def moveFromStart(self, pos, thePawn):
        """ Moves the pawn out of the Startcircle if it can """
        # Allows the pawn to move, unless its own pawn is blocking it
        if not self._masterList[pos].occupied():
            thePawn.setPosition(pos)
            thePawn.moveTo(self._masterList[pos].returnCenter())
            thePawn.changeIsInStart()
            self._masterList[pos].placePawn(thePawn)
            self._players[self._current].deactivateAll()
        elif self._masterList[pos].returnPawn().returnColor() !=\
        thePawn.returnColor():
            self._masterList[pos].returnPawn().returnToStart()
            self._masterList[pos].removePawn()
            thePawn.setPosition(pos)
            thePawn.moveTo(self._masterList[pos].returnCenter())
            thePawn.changeIsInStart()
            self._masterList[pos].placePawn(thePawn)
            self._players[self._current].deactivateAll()
        
    def moveToStartPoint(self, pos, thePawn):
        """ Moves the pawn to its starting position """
        # Each color has its own starting position
        if pos == 60:
            pos = 4
            self.moveFromStart(pos, thePawn)
        elif pos == 61:
            pos = 19
            self.moveFromStart(pos, thePawn)
        elif pos == 62:
            pos = 34
            self.moveFromStart(pos, thePawn)
        elif pos == 63:
            pos = 49
            self.moveFromStart(pos, thePawn)
    
    def checkSlide(self, moveToPos, landingPos, thePawn):
        """ Checks if the pawn has landed on a slide square """
        # Checks the type of the square the pawn lands on
        if type(landingPos) == Slidesquares and landingPos.returnColor() !=\
        thePawn.returnColor():
            for i in range(landingPos.returnSlide()):
                checkNextPos = self._masterList[(moveToPos + 1) + i]
                if checkNextPos.occupied():
                    checkNextPos.returnPawn().returnToStart()
                    checkNextPos.removePawn()
            moveToPos = moveToPos + landingPos.returnSlide()
        return moveToPos
        
    def checkIfGoingHome(self, thePawn):
        # If the pawn reaches within 12 spaces of home, since 12 is largest move
        # The pawn switches the track that it will follow
        """ Checks if the pawn is on it's way to it's home circle """
        isBetween = thePawn.getPosition()
        if thePawn.returnColor() == 'red' and ((59 >= isBetween >= 51) or\
        (isBetween <= 2) or (72 >= isBetween >= 68)):
            thePawn.homeStretchTrue()
        elif thePawn.returnColor() == 'blue' and ((17 >= isBetween >= 6) or\
        (77 >= isBetween >= 73)):
            thePawn.homeStretchTrue()
        elif thePawn.returnColor() == 'yellow' and ((32 >= isBetween >= 21) or\
        (82 >= isBetween >= 78)):
            thePawn.homeStretchTrue()
        elif thePawn.returnColor() == 'green' and ((47 >= isBetween >= 36) or\
        (87 >= isBetween >= 83)):
            thePawn.homeStretchTrue()
        else:
            thePawn.homeStretchFalse()

    def checkIfSafesquare(self, thePawn):
        """ Checks if the pawn is within a safe square, so it cannot switch """
        # Pawns in safe squares cannot be switched with
        if thePawn.returnColor() == 'red':
            if 68 <= thePawn.getPosition() <= 72:
                thePawn.isInSafesquareTrue()
            else:
                thePawn.isInSafesquareFalse()
        elif thePawn.returnColor() == 'blue':
            if 73 <= thePawn.getPosition() <= 77:
                thePawn.isInSafesquareTrue()
            else:
                thePawn.isInSafesquareFalse()
        elif thePawn.returnColor() == 'yellow':
            if 78 <= thePawn.getPosition() <= 82:
                thePawn.isInSafesquareTrue()
            else:
                thePawn.isInSafesquareFalse()
        elif thePawn.returnColor() == 'green':
            if 83 <= thePawn.getPosition() <= 87:
                thePawn.isInSafesquareTrue()
            else:
                thePawn.isInSafesquareFalse()
    
    def shouldMove(self, checkMove, colorTrack):
        """
        Checks if the pawn should be able to move towards its home square
        """
        if checkMove > len(colorTrack):
            return False
        else:
            return True
    
    def finalDestination(self, pos, checkMove, colorTrack, thePawn):
        """ Checks if the pawn can move into it's home circle """
        if checkMove == len(colorTrack):
            self._masterList[pos].addPawn(self._win)
            self._masterList[pos].determineWinner(self._win)
            thePawn.isInHomeCircleTrue()
    
    def reportPawnClick(self, thePawn):
        """ When the pawn is clicked, it moves according to a given value """
        deckVal = self._deck.getValue()
        if thePawn.isInStart():
            # Allows a move out of start
            if deckVal == 1 or deckVal == 2:
                self.moveToStartPoint(thePawn.getPosition(), thePawn)
            
            if deckVal == 'Sorry!' and not self._secondClick:
                # Waits for the second click, which will be on the other pawn
                self._secondClick = True
                self._firstPawn = thePawn
                for i in range(len(self._players)):
                    for pawn in self._players[i].returnPawns():
                        if not pawn.isInStart() and not pawn.isInSafesquare():
                            pawn.activate()
                self._players[self._current].deactivateAll()
                
        else:
            
            # DeckVals are changed based on the move that needs to be made
            if deckVal == 4:
                deckVal = -4
            if deckVal == 10:
                choice = None
                while choice != '1' and choice != '2':
                    choice = input( \
                    "Enter '1' to move forward 10 spaces. Enter '2' to move" +\
                    " backwards 1 space.")
                if choice == '1':
                    deckVal = 10
                elif choice == '2':
                    deckVal = -1
                    
            if deckVal == 11 and not self._secondClick:
                choice = None
                while choice != '1' and choice != '2':
                    choice = input( \
                    "Enter '1' to move forward 11 spaces. Enter '2' to" +\
                    " switch places with an opponent's pawn.")
                if thePawn.isInSafesquare():
                    return
                if choice == '2' and not self._secondClick:
                    self._secondClick = True
                    self._firstPawn = thePawn
                    for i in range(len(self._players)):
                        for pawn in self._players[i].returnPawns():
                            if not pawn.isInStart() and\
                            not pawn.isInSafesquare():
                                pawn.activate()
                    self._players[self._current].deactivateAll()
                    return
                elif choice == '1':
                    deckVal = 11
                
            elif deckVal == 11 and self._secondClick:
                firstMoveToPos = thePawn.getPosition()
                secondMoveToPos = self._firstPawn.getPosition()
                firstLandingPos = self._masterList[firstMoveToPos]
                secondLandingPos = self._masterList[secondMoveToPos]
                firstLandingPos.removePawn()
                secondLandingPos.removePawn()
                # Takes info of both pawns and switches them
                firstMoveToPos = self.checkSlide(firstMoveToPos,\
                                                 firstLandingPos,\
                                                 self._firstPawn)
                secondMoveToPos = self.checkSlide(secondMoveToPos,\
                                                  secondLandingPos, thePawn)
                firstLandingPos = self._masterList[firstMoveToPos]
                secondLandingPos = self._masterList[secondMoveToPos]
                self._firstPawn.setPosition(firstMoveToPos)
                thePawn.setPosition(secondMoveToPos)
                # Checks if pawn can even be switched with
                self.checkIfGoingHome(self._firstPawn)
                self.checkIfGoingHome(thePawn)
                self._firstPawn.moveTo(firstLandingPos.returnCenter())
                thePawn.moveTo(secondLandingPos.returnCenter())
                firstLandingPos.placePawn(self._firstPawn)
                secondLandingPos.placePawn(thePawn)
                self._secondClick = False
                for player in self._players:
                    player.deactivateAll()
                return
                    
                    
                               
            if deckVal == 'Sorry!' and self._secondClick:
                moveToPos = thePawn.getPosition()
                landingPos = self._masterList[moveToPos]
                thePawn.returnToStart()
                self._firstPawn.changeIsInStart()
                moveToPos = self.checkSlide(moveToPos, landingPos,\
                                            self._firstPawn)
                self._firstPawn.setPosition(moveToPos)
                # Checks if pawn can even be switched with
                self.checkIfGoingHome(self._firstPawn)
                self._firstPawn.moveTo(self._masterList[moveToPos].\
                                       returnCenter())
                self._masterList[moveToPos].placePawn(self._firstPawn)
                self._secondClick = False
                for player in self._players:
                    player.deactivateAll()
                return
            
            elif deckVal == 'Sorry!' and not self._secondClick:
                return
            
            # This code actually executes the move   
            pos = thePawn.getPosition()
            originalPos = thePawn.getPosition()
            moveLen = deckVal
            landingPos = self._masterList[(originalPos + moveLen) % 60]
            if type(landingPos) == Slidesquares and landingPos.returnColor() !=\
            thePawn.returnColor():
                pos = pos + moveLen
                # % 60 since there are 60 spaces on the board
                pos = pos % 60
                for i in range(landingPos.returnSlide() + 1):
                    checkNextPos = self._masterList[pos + i]
                    if checkNextPos.occupied():
                        if checkNextPos.returnPawn() != thePawn:
                            checkNextPos.returnPawn().returnToStart()
                        checkNextPos.removePawn()
                if not thePawn.isHomeStretch():        
                    pos = pos + self._masterList[pos].returnSlide()
                    pos = pos % 60
                else:
                    colorTrack = None
                    # Changes the track that the pawn is on
                    if thePawn.returnColor() == 'red':
                        colorTrack = self._redTrack
                    elif thePawn.returnColor() == 'blue':
                        colorTrack = self._blueTrack
                    elif thePawn.returnColor() == 'yellow':
                        colorTrack = self._yellowTrack
                    elif thePawn.returnColor() == 'green':
                        colorTrack = self._greenTrack
                    pos = colorTrack[colorTrack.index(originalPos) +\
                    moveLen + self._masterList[pos].returnSlide()]
            else:
                if not thePawn.isHomeStretch():
                    pos = pos + moveLen
                    pos = pos % 60
                else:
                    colorTrack = None
                    # Changes the track that the pawn is on
                    if thePawn.returnColor() == 'red':
                        colorTrack = self._redTrack
                    elif thePawn.returnColor() == 'blue':
                        colorTrack = self._blueTrack
                    elif thePawn.returnColor() == 'yellow':
                        colorTrack = self._yellowTrack
                    elif thePawn.returnColor() == 'green':
                        colorTrack = self._greenTrack
                    if (colorTrack.index(originalPos) + moveLen) < 0:
                        pos = pos + moveLen
                        pos = pos % 60
                    else:
                        checkMove = colorTrack.index(originalPos) + moveLen + 1
                        shouldMove = self.shouldMove(checkMove, colorTrack)
                        if not shouldMove:
                            return
                        pos = colorTrack[colorTrack.index(originalPos) +\
                        moveLen]
                        self.finalDestination(pos, checkMove, colorTrack,\
                                              thePawn)
                
            if self._masterList[pos].occupied():
                # If the pawn moves to a space that is occupied, kicks the
                # other pawn back to its starting position
                if thePawn.returnColor() !=\
                self._masterList[pos].returnPawn().returnColor():
                    self._masterList[originalPos].removePawn()
                    self._masterList[pos].returnPawn().returnToStart()
                    self._masterList[pos].removePawn()
                    thePawn.setPosition(pos)
                    self.checkIfGoingHome(thePawn)
                    self.checkIfSafesquare(thePawn)
                    thePawn.moveTo(self._masterList[pos].returnCenter())
                    self._masterList[pos].placePawn(thePawn)
                    self._players[self._current].deactivateAll()
            
            if not self._masterList[pos].occupied():
                self._masterList[originalPos].removePawn()
                thePawn.setPosition(pos)
                self.checkIfGoingHome(thePawn)
                self.checkIfSafesquare(thePawn)
                thePawn.moveTo(self._masterList[pos].returnCenter())
                if type(self._masterList[pos]) != Homecircles:
                    self._masterList[pos].placePawn(thePawn)
                self._players[self._current].deactivateAll()

def first(win):
    """ Runs the game through the board class """
    board = Board(win)
    board.addToWindow()

StartGraphicsSystem(first, 800, 800)
