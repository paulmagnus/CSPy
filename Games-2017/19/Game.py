"""
*****************************************************************************
FILE: Game.py
AUTHOR: Jeff Welch
PARTNER: Will Benthem De Grave
ASSIGNMENT: Project 6
DATE: 04/09/17
DESCRIPTION: This program runs a fully functional game of sorry with 4 players.

*****************************************************************************
"""
import random
from cs110graphics import *

class Player:
    """Contstructs the players, each creating 4 pawns of their color"""
    def __init__(self, playerColor, pawnColor, startLoc, startPos, board):
        """ Constructor for attributes of 'Player' """
        self._board = board
        self._playerColor = playerColor
        self._pawnColor = pawnColor
        self._startPositions = startPos # on board
        self._startLocation = startLoc # on window
        self._pawns = []
        #pawnColors = ['#990000', '#00BFFF', '#DAA520', '#014421']
        for i in range(4):
            thisPawn = Pawn(board, self._pawnColor, self._startLocation[i],\
                            self._startPositions, self._playerColor)
            self._pawns.append(thisPawn)
    
    def addToWindow(self, win):
        """Adds the graphical parts of pawns created by 'Player' to the
        window"""
        for item in self._pawns:
            item.addToWindow(win)
    
    def activateAll(self):
        """Activates all pawns belonging to a player, unless a pawn has been 
        moved into the final home circle"""
        for pawn in self._pawns:
            if not pawn.isInHomeCircle():
                pawn.activate()
            
    def deactivateAll(self):
        """Deactivates all pawns belonging to a player"""
        for pawn in self._pawns:
            pawn.deactivate()
            
    def returnPawns(self):
        """Returns all pawns belonging to a player"""
        return self._pawns
            
class Pawn(EventHandler):
    
    """A clickable object that is created by player that moves around the board.
    Keeps track of its logical position on the board as well as its position on
    the window, as well as multiple booleans that determine how the pawn acts
    when clicked."""
    def __init__(self, board, color, location, position, playerColor):
        """ Constructor for the attributes of 'Pawn' """
        EventHandler.__init__(self)
        self._color = color
        self._playerColor = playerColor
        self._board = board
        self._position = position # current logical position on the board
        self._location = location # current logical position on the window
        self._circle = Circle(15, location)
        self._circle.setDepth(0)
        self._circle.setFillColor(color)
        self._circle.setBorderWidth(2)
        self._circle.addHandler(self)
        self._isInStart = True
        self._isInSafesquare = False
        self._active = False
        self._homeStretch = False
        self._isInHomeCircle = False
        
        # Starting position on the Board. Not changed.
        self._startPosition = position
        self._startLocation = location
    
    def addToWindow(self, win):
        """Adds the graphical part of the 'Pawn' to the window"""
        win.add(self._circle)
        
    def activate(self):
        """Activates a pawn, provided that it is not in the home circle, and
        provides a visual indicator of the player's turn by highlighting the 
        pawn."""
        if not self.isInHomeCircle():
            self._active = True
            self._circle.setBorderColor('green')
        
    def deactivate(self):
        """Deactivates the pawn, and gives a visual indicator that the pawn 
        cannot be clicked."""
        self._active = False
        self._circle.setBorderColor('black')
    
    def handleMouseRelease(self, event):
        """If the pawn is actve, report that the pawn has been clicked to the 
        board."""
        if self._active:
            self._board.reportPawnClick(self)
    
    def getPosition(self):
        """Returns the logical position of the pawn on the board"""
        return self._position
        
    def returnColor(self):
        """Returns the color of the pawn"""
        return self._playerColor
    
    def changeIsInStart(self):
        """Changes the boolean of whether or not the pawn is in the start 
        circle"""
        self._isInStart = not self._isInStart
        
    def isInSafesquareTrue(self):
        """Changes the boolean of whether the pawn is in a safe square to 
        true"""
        self._isInSafesquare = True
        
    def isInSafesquareFalse(self):
        """Changes the boolean of whether the pawn is in a safe square to 
        false"""
        self._isInSafesquare = False
        
    def homeStretchTrue(self):
        """Changes the boolean of whether the pawn is in the home stretch to 
        true"""
        self._homeStretch = True
        
    def homeStretchFalse(self):
        """Changes the boolean of whether the pawn is in the home stretch to 
        false"""
        self._homeStretch = False
        
    def isInHomeCircleTrue(self):
        """Changes the boolean of whether the pawn is in the home circle to 
        true"""
        self._isInHomeCircle = True
        
    def isInStart(self):
        """Returns the boolean that determines if the pawn is in start"""
        return self._isInStart
        
    def isInSafesquare(self):
        """Returns the boolean that determines if the pawn is in a safe 
        square"""
        return self._isInSafesquare
        
    def isHomeStretch(self):
        """
        Returns the boolean that determines if the pawn is in the home stretch.
        The home stretch determines if the pawn is within a certain move length 
        of turning into the safe squares, and then changes the track of the pawn
        so that it will turn into the correct safe squares on the board.
        """
        return self._homeStretch
    
    def isInHomeCircle(self):
        """Returns the boolean that determines if the pawn is in the home 
        circle"""
        return self._isInHomeCircle
    
    def setPosition(self, pos):
        """Given a position, sets the logical position of the pawn on the 
        board"""
        self._position = pos
        
    def moveTo(self, location):
        """Moves the graphical pawt of the pawn to a given location on the 
        window"""
        self._circle.moveTo(location)
    
    def returnToStart(self):
        """
        Returns the given pawn to start, changing the needed attributes and 
        moving the pawn to its correct starting location.
        """
        self._isInStart = True
        self.moveTo(self._startLocation)
        self._position = self._startPosition
            
class Deck(EventHandler):
    """A class for building a deck of cards. This class is not graphical"""
    def __init__(self, board, win):
        """Creates a complete deck of 45 sorry playing cards. Also creates a
        button that graphically imitates the back of a card that is used to
        draw the cards."""
        EventHandler.__init__(self)
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
        """
        Reports the click of the draw button, which calls the draw method to
        simulate drawing a card.
        """
        if not self._active:
            return
        else:
            if self._currentCard is None:
                self._board.startGame()
            else:
                self._board.changeTurn()
            self.deal()

    def addToWindow(self, win):
        """Adds the card button to the window."""
        win.add(self._cardButton)
        
    def empty(self):
        """Returns True if the deck no longer contains any cards. Otherwise
        false is returned."""
        if len(self._deck) == 0:
            return True
        return False
        
    def deal(self):
        """Deals a card. A card is removed from the top of the deck and
        returned. If the deck is empty, the deck rebuiulds and shuffles 
        itself"""
        if self.empty():
            for i in range(len(self._cards)):
                self._deck.append(Card(self._cards[i]))
            self.shuffle()
        dealtCard = self._deck[0]
        dealtCard.addToWindow(self._win)
        self._deck.remove(dealtCard)
        dealtCard.move(198, 0)
        self._currentCard = dealtCard
        if self._previousCard is not None:
            self._previousCard.removeFrom(self._win)
        self._previousCard = dealtCard
    
    def returnCurrentVal(self):
        """Returns value of the card that has been drawn"""
        return self._currentCard.returnVal()
    
    def shuffle(self):
        """All cards currently in the deck are randomly ordered."""
        lenOfDeck = len(self._deck)
        newDeck = []
        for _ in range(lenOfDeck):
            randomCard = self._deck[random.randrange(len(self._deck))]
            newDeck.append(randomCard)
            self._deck.remove(randomCard)
        self._deck = newDeck

class Card:
    """Graphical object that returns the current value displayed on the card"""
    def __init__(self, val):
        """ Constructs a graphical card with a given value """
        self._value = val
        self._face = Rectangle(152, 204, (300, 396))
        self._text = Text(self._value, self.getReferencePoint(), 56)
        self._cardParts = [self._face, self._text]
        self._face.setFillColor('white')
        self._depth = 0
        self._dimensions = (154, 204)
        self._flipped = False
        
    def returnVal(self):
        """Returns the value of the card"""
        return self._value
        
    def addToWindow(self, win):
        """Adds the card to the given graphics window."""
        for part in self._cardParts:
            win.add(part)
        self.update(self._depth)
        
    def removeFrom(self, win):
        """Removes the card from the given graphics window"""
        for part in self._cardParts:
            win.remove(part)
            
    def move(self, dx, dy):
        """Moves a card by dx and dy."""
        for part in self._cardParts:
            part.move(dx, dy)
        
    def getReferencePoint(self):
        """The point representing the center of the card is returned"""
        return self._face.getCenter()
        
    def setDepth(self, depth):
        """Sets the depth of graphical objects representing the card to
        depth"""
        self._depth = depth
        self.update(depth)
    
    def update(self, depth):
        """Maintains consistency when setting the depth of cards"""
        self._text.setDepth(depth)
        self._face.setDepth(depth + 1)


class Squares:
    '''Constructs the squares on the board'''
    def __init__(self, color, center):
        self._rectangle = Rectangle(50, 50, center)
        self._rectangle.setDepth(1)
        self._rectangle.setFillColor(color)
        self._center = center
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
        """Adds the graphical square to the window"""
        win.add(self._rectangle)

class Slidesquares(Squares):
    """Constructs the slider squares. Inherits from the square object."""
    def __init__(self, color, length, center):
        super().__init__(color, center)
        self._lengthOfSlide = length
        self._color = color
    
    def returnSlide(self):
        """Returns the length that the pawn will slide"""
        return self._lengthOfSlide
    
    def returnColor(self):
        """Returns the color of the slidesquare"""
        return self._color
    
class Safesquares(Squares):
    """Constructs safe squares with a given color."""
    def __init__(self, color, center):
        super().__init__(color, center)
        
class Startcircles:
    """Constructs the starting circle for the pawns"""
    def __init__(self, color, center):
        self._circle = Circle(50, center)
        self._circle.setDepth(1)
        self._circle.setFillColor(color)
        
    def addToWindow(self, win):
        """Adds the graphical part of the start circle to the window."""
        win.add(self._circle)

class Homecircles:
    """Constructs the home circle for the pawns, determines the endgame"""
    def __init__(self, color, center):
        self._circle = Circle(50, center)
        self._circle.setDepth(1)
        self._circle.setFillColor(color)
        self._center = center
        self._pawnsInHome = 0
        self._rectangle = Rectangle(800, 800, (400, 400))
        self._rectangle.setDepth(-1)
        self._rectangle.setFillColor(color)
        self._text = Text("Congrats " + color + "!!!", (400, 400), 78)
        self._text.setDepth(-2)
        self._lastCounterText = None
        
    def addToWindow(self, win):
        """Adds the graphical aspect of the cirlces to the window"""
        win.add(self._circle)
    
    def addPawn(self, win):
        """Adds a pawn to the home circle, and places a counter of how many
        pawns are occupying the home circle"""
        self._pawnsInHome += 1
        counterText = Text(self._pawnsInHome, (self.returnCenter()[0],\
        self.returnCenter()[1] + 7), 20)
        counterText.setDepth(-1)
        if self._lastCounterText != None:
            win.remove(self._lastCounterText)
        self._lastCounterText = counterText
        win.add(counterText)
    
    def returnCenter(self):
        """Returns the center of the circle"""
        return self._center
        
    def occupied(self):
        """returns False when reportPawnClick asks the home circle if it is     
        occupied"""
        return False
    
    def determineWinner(self, win):
        """Determines if 4 pawns are in the homecircle, and if so, adds the 
        winning window."""
        if self._pawnsInHome == 4:
            win.add(self._rectangle)
            win.add(self._text)
            # determine the winner
            
      

class Board:
    """The board handles all aspects of the game in one class, such as placing 
    the squares on the board, creating the players, and handling mouse clicks
    from the pawn class"""
    def __init__(self, win):
        """Constructs graphical and other attrbutes of the board"""
        self._deck = Deck(self, win)
        
        # #990000 = Dark Red
        # #00BFFF = Light Blue
        # #DAA520 = Dark Yellow
        # #014421 = Dark Green
        
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
        pawnColors = ['#990000', '#00BFFF', '#DAA520', '#014421']
        startPositions = [60, 61, 62, 63]
        for i in range(len(playerColors)):
            self._players.append(Player(playerColors[i], pawnColors[i],\
                                        self._pawnStartLocations[i],\
                                        startPositions[i], self))
        
        self._trackSquares = []
        self._trackCircles = []
        self._trackSafeSquares = []
        self._masterList = []
        self._redTrack = [51, 52, 53, 54, 55, 56, 57, 58, 59, 0, 1, 2, 68, 69,
                          70, 71, 72, 64]
        self._blueTrack = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 73, 74, 
                           75, 76, 77, 65]
        self._yellowTrack = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 78,
                             79, 80, 81, 82, 66]
        self._greenTrack = [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 83,
                            84, 85, 86, 87, 67]
        
        self._win = win
        
        # Current player
        self._current = None
        
        #Purely visual parts of the board
        sorryText = Text('SORRY!', (400, 420), 48)
        sorryText.setDepth(2)
        win.add(sorryText)
        
        sorryRectangle = Rectangle(150, 150, (400, 400))
        sorryRectangle.setFillColor('#89ffa1')
        sorryRectangle.setBorderColor('##89ffa1')
        sorryRectangle.rotate(45)
        sorryRectangle.setDepth(3)
        win.add(sorryRectangle)
        
        background = Rectangle(700, 700, (400, 400))
        background.setDepth(4)
        background.setFillColor('#ADD8E6')
        win.add(background)
        
        redSlideOne = Rectangle(120, 15, (160, 25))
        redSlideOne.setFillColor('red')
        redSlideOne.setDepth(0)
        win.add(redSlideOne)
        redCircleOne = Circle(20, (225, 25))
        redCircleOne.setFillColor('red')
        redCircleOne.setDepth(0)
        win.add(redCircleOne)
        
        redSlideTwo = Rectangle(170, 15, (585, 25))
        redSlideTwo.setFillColor('red')
        redSlideTwo.setDepth(0)
        win.add(redSlideTwo)
        redCircleTwo = Circle(20, (675, 25))
        redCircleTwo.setFillColor('red')
        redCircleTwo.setDepth(0)
        win.add(redCircleTwo)
        
        blueSlideOne = Rectangle(15, 120, (775, 160))
        blueSlideOne.setFillColor('blue')
        blueSlideOne.setDepth(0)
        win.add(blueSlideOne)
        blueCircleOne = Circle(20, (775, 225))
        blueCircleOne.setFillColor('blue')
        blueCircleOne.setDepth(0)
        win.add(blueCircleOne)
        
        blueSlideTwo = Rectangle(15, 170, (775, 585))
        blueSlideTwo.setFillColor('blue')
        blueSlideTwo.setDepth(0)
        win.add(blueSlideTwo)
        blueCircleTwo = Circle(20, (775, 675))
        blueCircleTwo.setFillColor('blue')
        blueCircleTwo.setDepth(0)
        win.add(blueCircleTwo)
        
        yellowSlideOne = Rectangle(120, 15, (640, 775))
        yellowSlideOne.setFillColor('yellow')
        yellowSlideOne.setDepth(0)
        win.add(yellowSlideOne)
        yellowCircleOne = Circle(20, (575, 775))
        yellowCircleOne.setFillColor('yellow')
        yellowCircleOne.setDepth(0)
        win.add(yellowCircleOne)
        
        yellowSlideTwo = Rectangle(170, 15, (215, 775))
        yellowSlideTwo.setFillColor('yellow')
        yellowSlideTwo.setDepth(0)
        win.add(yellowSlideTwo)
        yellowCircleTwo = Circle(20, (125, 775))
        yellowCircleTwo.setFillColor('yellow')
        yellowCircleTwo.setDepth(0)
        win.add(yellowCircleTwo)
        
        greenSlideOne = Rectangle(15, 120, (25, 640))
        greenSlideOne.setFillColor('green')
        greenSlideOne.setDepth(0)
        win.add(greenSlideOne)
        greenCircleOne = Circle(20, (25, 575))
        greenCircleOne.setFillColor('green')
        greenCircleOne.setDepth(0)
        win.add(greenCircleOne)
        
        greenSlideTwo = Rectangle(15, 170, (25, 215))
        greenSlideTwo.setFillColor('green')
        greenSlideTwo.setDepth(0)
        win.add(greenSlideTwo)
        greenCircleTwo = Circle(20, (25, 125))
        greenCircleTwo.setFillColor('green')
        greenCircleTwo.setDepth(0)
        win.add(greenCircleTwo)
        
        trackSqColors = [('red', 50, 0), ('blue', 0, 50), ('yellow', -50, 0), 
                         ('green', 0, -50)]
        x = 25
        y = 25
        
        
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
        
        
        self._trackSafeSquares = self._trackSafeSquares + redSafeSquares +\
        blueSafeSquares + yellowSafeSquares + greenSafeSquares
        
        
        self._trackCircles.append(Startcircles('red', (225, 100)))
        self._trackCircles.append(Startcircles('blue', (700, 225)))
        self._trackCircles.append(Startcircles('yellow', (575, 700)))
        self._trackCircles.append(Startcircles('green', (100, 575)))
        
        self._trackCircles.append(Homecircles('red', (125, 350)))
        self._trackCircles.append(Homecircles('blue', (450, 125)))
        self._trackCircles.append(Homecircles('yellow', (675, 450)))
        self._trackCircles.append(Homecircles('green', (350, 675)))
        
        self._masterList += self._trackSquares + self._trackCircles +\
        self._trackSafeSquares
        
        self._firstPawn = None
        self._secondClick = False
        
    def addToWindow(self):
        """Adds the board spaces, pawns, and the deck button to the window"""
        for item in self._masterList:
            item.addToWindow(self._win)
        for player in self._players:
            player.addToWindow(self._win)
        self._deck.addToWindow(self._win)
        
            
    def changeTurn(self):
        """Changes the turn so that the current player can only move his or her
        own pieces"""
        for player in self._players:
            player.deactivateAll()
        if self._deck.returnCurrentVal() != 2:
            self._current += 1
        if self._secondClick:
            self._secondClick = not self._secondClick
        self._current %= 4
        self._players[self._current].activateAll()

    def startGame(self):
        """Sets the turn and activates the first player if no card has been 
        drawn"""
        self._current = 0
        self._players[self._current].activateAll()
        
    def isSecondClick(self):
        """Used for sorry and 11 cards in order to handle the second click, so 
        that pawns can switch places."""
        return self._secondClick
        
    def moveFromStart(self, pos, thePawn):
        """Handles the mouse click if the clicked pawn is in start"""
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
        """Moves the pawn to its correct first square on the board, determined 
        by its starting position"""
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
        """Checks the length of the slide if the pawn lands on a safe square,
        and enforces the rules of when a safe square is landed on"""
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
        """Checks if the pawn is within 12 spaces of moving into the home 
        square. If it is, then the track for the pawn is switched so that it 
        will move correctly into its home square"""
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
        """Checks if the pawn is in a safe square. If true, then the method 
        changes the attribute of the pawn"""
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
        """If a card has been drawn that would allow the pawn to move past its 
        home circle, this method will prevent the move"""
        if checkMove > len(colorTrack):
            return False
        else:
            return True
    
    def finalDestination(self, pos, checkMove, colorTrack, thePawn):
        """Determines if a pawn has moved into its final home circle, and if so,
        permanantly deactivates the piece and checks if there is a winner"""
        if checkMove == len(colorTrack):
            self._masterList[pos].addPawn(self._win)
            self._masterList[pos].determineWinner(self._win)
            thePawn.isInHomeCircleTrue()
    
    def reportPawnClick(self, thePawn):
        """When a pawn is clicked, return the correct value of the card, and 
        move the pawn accordingly. If the pawn is not supposed to move, prevent
        it from moving"""
        deckVal = self._deck.returnCurrentVal()
        if thePawn.isInStart():
            if deckVal == 1 or deckVal == 2:
                self.moveToStartPoint(thePawn.getPosition(), thePawn)
            
            if deckVal == 'Sorry!' and not self._secondClick:
                self._secondClick = True
                self._firstPawn = thePawn
                for i in range(len(self._players)):
                    for pawn in self._players[i].returnPawns():
                        if not pawn.isInStart() and not pawn.isInSafesquare():
                            pawn.activate()
                self._players[self._current].deactivateAll()
                
        else:
            
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
                firstMoveToPos = self.checkSlide(firstMoveToPos,\
                                                 firstLandingPos,\
                                                 self._firstPawn)
                secondMoveToPos = self.checkSlide(secondMoveToPos,\
                                                  secondLandingPos, thePawn)
                firstLandingPos = self._masterList[firstMoveToPos]
                secondLandingPos = self._masterList[secondMoveToPos]
                self._firstPawn.setPosition(firstMoveToPos)
                thePawn.setPosition(secondMoveToPos)
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
            
                
            pos = thePawn.getPosition()
            originalPos = thePawn.getPosition()
            moveLen = deckVal
            landingPos = self._masterList[(originalPos + moveLen) % 60]
            if type(landingPos) == Slidesquares and landingPos.returnColor() !=\
            thePawn.returnColor():
                pos = pos + moveLen 
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
    """Function that calls the board to be added to the window"""
    board = Board(win)
    board.addToWindow()
        
StartGraphicsSystem(first, 800, 800)
