""" 
*******************************************************************************
* Fie:         game.py                                                        *
* Author:      Daniel Gliedman                                                *
* Assignment:  Project 6 Board Game                                           *
* Date:        5/1/17                                                         *
* Partner:     Haley Taft                                                     *
* Description: Write a program that functions as though it is an abbreviated 
               version of the Monopoly Board Game.                            *
*******************************************************************************
"""

import random
from cs110graphics import *

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
WINDOW_CENTER = (400, 300)

IMAGE_WIDTH = 600
IMAGE_HEIGHT = 600
IMAGE_CENTER = (300, 300)

class Board:
    """Creates the board, which manages all other aspects of the game"""
    
    def __init__(self, win):
        self._die = Die(self)
        self._die.addTo(win)
        
        self._deck = Deck(self)
        self._deck.shuffle()
        self._card = self._deck.deal()
        self._card.addTo(win)
        
        self._win = win
        
        self._current = 0
        
        self._player1 = []
        self._player2 = []
     
        #This line is too long because of the url, but in attempting to split it
        #up, the image would not appear on the window.
        url = "https://cs.hamilton.edu/~dgliedma/images/Board_game_pic_2.png"
        self._boardBack = Image(url, IMAGE_CENTER, IMAGE_HEIGHT, IMAGE_WIDTH)
        win.add(self._boardBack)
    
        #This section creates a grid of squares lying underneath the board 
        #graphic so that we can determine where to move the pawns.
        self._top = self.spacesHoriz(115, 35, "add", win) 
        self._bottom = self.spacesHoriz(485, 570, "subtract", win)
        self._right = self.spacesVert(565, 109, "add", win)
        self._left = self.spacesVert(35, 495, "subtract", win)
        
        self._topl = Rectangle(30, 30, (40, 40))
        self._topl.setDepth(100)
        topl = [self._topl.getCenter()]
        
        self._topr = Rectangle(30, 30, (560, 40))
        self._topr.setDepth(100)
        topr = [self._topr.getCenter()]
        
        self._botl = Rectangle(30, 30, (20, 570))
        self._botl.setDepth(100)
        botl = [self._botl.getCenter()]
        
        self._botr = Rectangle(30, 30, (560, 560))
        self._botr.setDepth(100)
        botr = [self._botr.getCenter()]
        
        self._campo = Rectangle(30, 30, (65, 545))
        self._campo.setDepth(100)
        self._campo1 = self._campo.getCenter()
        
        win.add(self._topl)
        win.add(self._topr)
        win.add(self._botl) 
        win.add(self._botr)
        win.add(self._campo)
    
        #This is a master list of all of the centers of all of the possible \  
        #spaces. Because we added several different lists together, we must 
        #index the list to 0 each time we use this master list so that we can 
        #access all of the positions.
        self._mastercentlist = [botr + self._bottom + botl + self._left + topl 
                                + self._top + topr + self._right]
        
        #This is a list of all of the different property cards, which are stored
        #off screen.
        self._properties = []
        for name, ident in [("p2a", 0), ("p1a", 1), ("p23b", 2), ("p3a", 3),
                            ("p4a", 4), ("p5a", 5), ("p6a", 6), ("p7a", 7),
                            ("p8a", 8), ("p24a", 9), ("p9a", 10), ("p10a", 11),
                            ("p11a", 12), ("p12a", 13), ("p13a", 14), 
                            ("p14a", 15), ("p25a", 16), ("p15a", 17), 
                            ("p16a", 18), ("p17a", 19), ("p18a", 20), 
                            ("p19a", 21), ("p20a", 22), ("p26a", 23), 
                            ("p21a", 24), ("p22a", 25)]:
            thisProperty = Properties(self, name, ident, 
                                      faceFileName=name + ".png")
            thisProperty.addTo(win)
            thisProperty.moveTo(-500, 300)
            self._properties.append(thisProperty)
        
        #This is a bogus image which we use as a placeholder for all spaces that
        #aren't a property on the board. 
        self._bogus = []
        for i in range(14):
            prop = Properties(self, "bad", i, faceFileName="bad.png")
            self._bogus.append(prop)
        
        #This is a list of all spaces on the board divided into two categories, 
        #either bogus spaces or property spaces. 
        self._prop = [self._bogus[0], self._properties[0], 
                      self._bogus[1], self._properties[1], 
                      self._bogus[2], self._properties[2], 
                      self._properties[3], self._bogus[3], 
                      self._properties[4], self._properties[5], 
                      self._bogus[4], self._properties[6], 
                      self._bogus[5], self._properties[7], 
                      self._properties[8], self._properties[9], 
                      self._properties[10], self._bogus[6], 
                      self._properties[11], self._properties[12], 
                      self._bogus[7], self._properties[13], 
                      self._bogus[8], self._properties[14], 
                      self._properties[15], self._properties[16], 
                      self._properties[17], self._bogus[9], 
                      self._properties[18], self._properties[19], 
                      self._bogus[10], self._properties[20], 
                      self._properties[21], self._bogus[11], 
                      self._properties[22], self._properties[23], 
                      self._bogus[12], self._properties[24], 
                      self._bogus[13], self._properties[25]]
        
        #This sets up the purchase button displayed on the screen.
        self._purchase = Button(self, win, "purchase", 22, (700, 200))
        self._purchase.addTo(win)
        
        #This sets up the pass button displayed on the screen.
        self._pass = Button(self, win, "pass", 22, (800, 200))
        self._pass.addTo(win)
        
        #This creates the two pawns which the players use to move around.
        self._pawns = []
        for color, which in [("DarkBlue", 0), ("#f5deb3", 1)]: 
            thisPawn = Pawn(self, color, which, 0)
            thisPawn.addTo(win)
            thisPawn.moveTo(self._mastercentlist[0][0])
            self._pawns.append(thisPawn)
            self._updatePawnLocations()

        #This adds text to the window, which appears when a property has already
        #been purchased.
        self._text = Text("This property has been bought. Press pass and pay\
                           rent.", (1250, 250), 15)
        win.add(self._text)
     
        #This sets up the accounts displayed on the screen.
        self._money = []
        for value, center, which in [(2000, (700, 100), 0), 
                                     (2000, (850, 100), 1)]:
            thisMoney = Money(self, win, value, center, which)
            thisMoney.addTo(win)
            self._money.append(thisMoney)
        
        #Puts this text above the account boxes.
        self._player1Text = Text("Player 1", (700, 50), 30)
        self._player2Text = Text("Player 2", (850, 50), 30)
        
        win.add(self._player1Text)
        win.add(self._player2Text)
        
    def spacesHoriz(self, xpos, ypos, direction, win):
        """This method creates the two horizontal rows of squares which lie 
           underneath the board graphic and which we use to determine pawn 
           location."""
           
        self._centlist = []
        self._spaces = []
        
        #This iterates through the list of colors and creates them 46 pixels 
        #apart from one another.
        for _ in range(9):
            thisSpace = BoardSpace(self, (xpos, ypos))
            thisSpace.addTo(win)
            self._spaces.append(thisSpace)
            if direction == "add":
                xpos += 46
            if direction == "subtract":
                xpos -= 46
            self._centlist.append(thisSpace.getCenter())
        return self._centlist
        
    def spacesVert(self, xpos, ypos, direction, win):
        """This method creates the two vertical rows of squares which lie 
           underneath the board graphic and which we use to determine pawn 
           location."""
           
        self._centlist = []
        self._spaces = []
        
        #This also iterates through the list of colors and creates them 48 
        #pixels apart from one another.
        for _ in range(9):
            thisSpace = BoardSpace(self, (xpos, ypos))
            thisSpace.addTo(win)
            self._spaces.append(thisSpace)  
            if direction == "add":
                ypos += 48
            if direction == "subtract":
                ypos -= 48
            self._centlist.append(thisSpace.getCenter())
        return self._centlist

    def reportDieClick(self):  
        """This method executes when the user clicks the die."""
        
        #Take the current position of the pawn as an index of the master list of
        #centers and add to it the current value on the die.
        thePawn = self._pawns[self._current]
        pos = thePawn.getPosition()
        pos = pos + self._die.getValue()
        
        #This ensures that the index of the pawn is not greater than the length
        #of the  board so that the pawns will move around the square.
        pos = pos % len(self._mastercentlist[0])
        thePawn.setPosition(pos)
        
        #This ensures that the pawn's location is updated to the most recent
        #location.
        self._updatePawnLocations()

    def changeTurn(self):
        """This method toggles between the two players."""
        
        #Puts the phrase "GAME OVER" on the window when the balance in someone's
        #account is less than zero.
        p1money = self._money[0].getMoney()
        p2money = self._money[1].getMoney()
        if p1money <= 0 or p2money <= 0:
            endRect = Rectangle(350, 200, (500, 300))
            endRect.setFillColor("red")
            endRect.setDepth(1)
            endText = Text("GAME OVER", (500, 300), 50)
            endText.setDepth(1)
            self._win.add(endRect)
            self._win.add(endText)
        else:
            
        #Set the border of the pawn that just went to black and its border width
        #to one. 
            self._pawns[self._current].setBorderColor("black")
            self._pawns[self._current].setBorderWidth(1)
            self._money[self._current].unhighlight()
            self._current = (self._current + 1) % len(self._pawns)
        
        #Set the border of the pawn whose turn it is to green and its border
        #width to three.
            self._pawns[self._current].setBorderColor("green")
            self._pawns[self._current].setBorderWidth(3)
            self._money[self._current].highlight()

    def _updatePawnLocations(self):
        """This method ensures that the pawns' positions are up to date with 
        where they are situated on the board."""
        
        #This sets the variable theSpace to the index of the tuple of the center
        #of the current place which we acquire from the master center list.
        offsets = [-1, 1]
        pawn = self._pawns[self._current]
        pos = pawn.getPosition()
        theSpace = self._mastercentlist[0]
        
        #This moves the pawn to the designated position and offsets it from the 
        #center slightly so that both pawns can fit on each square.
        pawn.moveTo(theSpace[pos])
        pawn.move(0, offsets[self._current] * 10)
        
        #This calls the following three methods. 
        self.compareSpaceToProperty()
        self.cardSpace(theSpace[pos])
        self.determineGo()
    
    def _updateCardPawnLocations(self, location):
        """This method also ensures that the pawns' positions are up to date 
        with where they are situated on the board."""
        
        #This does essentially the same thing as the previous method; however,
        #we use this one for the Hill Cards spaces.
        offsets = [-1, 1]
        pawn = self._pawns[self._current]
        pos = self.returnPosition(self._mastercentlist[0], location)
        pawn.setPosition(pos)
        pawn.move(0, offsets[self._current] * 10)

    def returnPosition(self, lists, position):
        """Returns the position of the space as an index of the master center 
        list."""
        if type(position) == tuple:
            pos = random.randrange(len(lists))
            return pos
        elif type(position) != tuple:
            for i in range(len(lists)):
                if lists[i] == position:
                    return i
        else:
            return

    def cardSpace(self, location):
        """This organizes all of the locations of the Hill Card spaces."""
        
        #These six indices refer to the tuples of the six centers of the Hill
        #Card board spaces.
        if (location == self._mastercentlist[0][2]
                or location == self._mastercentlist[0][7]
                or location == self._mastercentlist[0][17]
                or location == self._mastercentlist[0][22]
                or location == self._mastercentlist[0][33]
                or location == self._mastercentlist[0][36]):
            
            #If the deck is not empty, flip them over.
            if self._deck.empty() is False:
                self._card = self._deck.deal()
                self._card.flip()
                self._card.addTo(self._win)
                self.cardFunctions()
            #When the deck is empty, reshuffle it and flipt the cards back over.
            else:
                self._deck.discardPileReshuffle()
                for card in self._deck.getDeck():
                    card.flipBack()

    def cardFunctions(self):
        """When the following cards are flipped over from the deck, do the 
        following actions."""
        pawn = self._pawns[self._current]
        
        if self._card.getName() == "ca1":
            #Go to the Bundy East space.
            pawn.moveTo(self._mastercentlist[0][3])
            self._updateCardPawnLocations(self._mastercentlist[0][3])
        
        if self._card.getName() == "ca2":
            #Go to the diner space.
            pawn.moveTo(self._mastercentlist[0][25])
            self._updateCardPawnLocations(self._mastercentlist[0][25])
        
        if self._card.getName() == "ca3":
            #Go to the Dunham space.
            pawn.moveTo(self._mastercentlist[0][6])
            self._updateCardPawnLocations(self._mastercentlist[0][6])
        
        if self._card.getName() == "ca4":
            #Deduct $50 from the player's account.
            money = self._money[self._current]
            money.subtractMoney(50)
        
        if self._card.getName() == "ca5":
            #Add $15 to the player's account.
            money = self._money[self._current]
            money.addMoney(15)
        
        if self._card.getName() == "ca6":
            #Go to the Dunham space.
            pawn.moveTo(self._mastercentlist[0][34])
            self._updateCardPawnLocations(self._mastercentlist[0][34])
        
        if self._card.getName() == "ca7":
            #Add $25 to the player's account.
            money = self._money[self._current]
            money.subtractMoney(25)
        
        if self._card.getName() == "ca8":
            #Go to the campo space.
            pawn.moveTo(self._campo1)
            self._updateCardPawnLocations(self._campo1)
        
        if self._card.getName() == "ca9":
            #Go to the library space.
            pawn.moveTo(self._mastercentlist[0][18])
            self._updateCardPawnLocations(self._mastercentlist[0][18])
            
        if self._card.getName() == "ca10":
            #Go to the Go space.
            pawn.moveTo(self._mastercentlist[0][0])
            self._updateCardPawnLocations(self._mastercentlist[0][0])
        
        if self._card.getName() == "ca11":
            #Go to the Taylor Science Center space.
            pawn.moveTo(self._mastercentlist[0][19])
            self._updateCardPawnLocations(self._mastercentlist[0][19])
        
        if self._card.getName() == "ca12":
            #Add $20 to the player's account.
            money = self._money[self._current]
            money.addMoney(20)
       
    def compareSpaceToProperty(self):
        """This method checks to see if the space the player is on is a 
        property."""
        
        pawn = self._pawns[self._current]
        pos = pawn.getPosition()
        prop = self._prop[pos]
        
        #Run through the list of all of the possible property spaces and move
        #the corresponding property cards on to the screen.
        for name in ["p1a", "p2a", "p3a", "p4a", "p5a", "p6a", "p7a", "p8a",
                     "p9a", "p10a", "p11a", "p12a", "p13a", "p14a", "p15a",
                     "p16a", "917a", "p18a", "p19a", "p20a", "p21a", "p22a",
                     "p23b", "p24a", "p25a", "p26a"]:
            if name == prop.getName():
                prop.moveTo(800, 400)
                if prop.getCanBuy() is False:
                    self._text.moveTo((800, 265))  
    
    def determineIfBought(self):
        """This method checks to see if the property the pawn has landed on has 
        already been pruchased."""
        
        #If the first player lands on the owned property, subtract $20 from the 
        #account and add it to player 2's account. Also, move the property card 
        #and the phrase denoting that it has been purchased off the screen.
        if self._current == 0:
            pawn = self._pawns[1]
            pos = pawn.getPosition()
            prop = self._prop[pos]
            if prop.getCanBuy is False:
                self._money[1].subtractMoney(20)
                self._money[0].addMoney(20)
                prop.moveTo(-500, 300)
                self._text.moveTo((-500, 300))   
                return False
            else:
                return True
        
        #Do the same thing if player 2 lands on the owned property.
        else:
            pawn = self._pawns[0]
            pos = pawn.getPosition()
            prop = self._prop[pos]
            if prop.getCanBuy is False:
                self._money[0].subtractMoney(20)
                self._money[1].addMoney(20)
                prop.moveTo(-500, 300)
                self._text.moveTo((-500, 300))  
                return False
            else:
                return True
    
    def purchaseProperty(self):
        """When the purchase button is pressed, call this method."""
        
        #Subtract $100 from the player's account and make the property off 
        #limits for subsequent purchases. 
        if self._current == 0:
            pawn = self._pawns[1]
            pos = pawn.getPosition()
            prop = self._prop[pos]
            canBuy = prop.getCanBuy()
            if canBuy is True:
                self._money[1].subtractMoney(100)
                self._player2.append(prop)
                prop.canBuy = False
                
        #Do the same thing if player 2 is the one who purchases the property.
        else:
            pawn = self._pawns[0]
            pos = pawn.getPosition()
            prop = self._prop[pos]
            canBuy = prop.getCanBuy()
            if canBuy is True:
                self._money[0].subtractMoney(100)
                self._player1.append(prop)
                prop.canBuy = False
        prop.moveTo(-500, 300)

    def passProperty(self):
        """When the pass button is pressed, call this method."""
        
        #Remove the property card from screen and keep going with the game.
        if self._current == 0:
            pawn = self._pawns[1]
        else:
            pawn = self._pawns[0]
        pos = pawn.getPosition()
        prop = self._prop[pos]
        prop.moveTo(-500, 300)
        self._text.moveTo((-500, 300))
    
    def determineGo(self):
        """Executes when one player passes the Go space."""
        
        #When the index of the pawn is greater than the number of spaces (39), 
        #add $200 to the player's account.
        pawn = self._pawns[self._current]
        pos = pawn.getPosition()
        dieValue = self._die.getValue()
        if pos + dieValue >= 39:
            self._money[self._current].addMoney(200)
        
class Money:
    """This class organizes the player's accounts and deals with the money 
    players receive/spend for various activities."""
    
    def __init__(self, board, win, value, center, ident):
        self._center = center
        self._ident = ident
        self._value = value
        self._board = board
        self._win = win
        
        self._rectangle = Rectangle(100, 80, self._center)
        self._rectangle.setBorderWidth(5)
        
        self._textMoney = Text("$", self._center, 35)
        self._text = Text(value, self._center, 25)
    
    def highlight(self):
        """Change the color of the player's account box to green."""
        self._rectangle.setBorderColor("green")
    
    def unhighlight(self):
        """Change the color of the player's account box to black."""
        self._rectangle.setBorderColor("black")
    
    def addTo(self, win):
        """Adds various elements to the window."""
        
        win.add(self._rectangle)
        self._rectangle.moveTo((self._center))
        
        win.add(self._text)
        self._text.moveTo((self._center[0] + 10, self._center[1] + 10))
        
        win.add(self._textMoney)
        self._textMoney.moveTo((self._center[0] - 30, self._center[1] + 20))
        
    def getIdent(self):
        """Returns the identification of the player."""
        return self._ident
    
    def getValue(self):
        """"Returns the value of the monetary sum."""
        return self._value
    
    def addMoney(self, value):
        """Adds an amount to one player's account."""
        self._value += value
        self._updateValue()
    
    def subtractMoney(self, value):
        """Subtracts money from one player's account."""
        self._value -= value
        self._updateValue()
    
    def _updateValue(self):
        """Updates the value displayed on the board to reflect the player's 
        holdings."""
        self._text.setTextString(str(self._value))
    
    def getMoney(self):
        """Returns the value of the money in one's account."""
        return self._value
        
class BoardSpace(EventHandler):
    """A class to organzie the different types of board spaces present."""
    
    def __init__(self, board, center):
        EventHandler.__init__(self)
        self._board = board
        self._center = center
        
        self._square = Rectangle(30, 30, center)
        self._square.setDepth(100)                      
    
    def getCenter(self):
        """Returns the center of the board spaces."""
        return self._center
    
    def addTo(self, win):
        """Adds the grid of squares underlying the board graphic to the 
        window."""
        win.add(self._square)
    
    def setDepth(self, depth):
        """Sets the depth of the board spaces."""
        self._square.setDepth(depth)

class Die(EventHandler):
    """A class to orient the die on the board and manage the various activities
    associated with it."""
    
    #Initializes the number of sides on the die and the positions of the pips.
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
    
    def __init__(self, board, width=40, center=(400, 400), 
                 diecolor="white", pipcolor="black"):
        EventHandler.__init__(self)
        self._board = board
        self._value = 6
        
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(diecolor)
        self._square.setDepth(20)
        
        self._center = center
        self._width = width
        
        #Adds the pips to the sides of the die.
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(pipcolor)
            pip.setDepth(20)
            self._pips.append(pip)
        self._square.addHandler(self)
        self._update()
    
    def _update(self):
        """Changes the number of pips displayed on the die after it is 
        clicked."""
        
        #Changes the depths of the pips on the window to reflect the number 
        #the player rolled.
        positions = Die.POSITIONS[self._value]
        cx, cy = self._center                   
        for i in range(len(positions)):
            if positions[i] is None:
                self._pips[i].setDepth(25)  
            else:
                self._pips[i].setDepth(15) 
                cx, cy = self._center
                dx = positions[i][0] * self._width
                dy = positions[i][1] * self._width
                self._pips[i].moveTo((cx + dx, cy + dy))
    
    def roll(self):
        """A method to roll the die."""
        self._value = random.randrange(Die.SIDES) + 1
        self._update()
    
    def getValue(self):
        """Returns the value of the die."""
        return self._value
    
    def addTo(self, win):
        """Adds the die and the pips to the window."""
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)
    
    def handleMouseRelease(self, event):
        """When the die is clicked, roll the die."""
        self.roll()
        self._board.reportDieClick()
        self._board.changeTurn()

class Pawn:
    """A class to manage the pawns and their movements around the board."""
    
    def __init__(self, board, color, ident, position):
        self._color = color
        self._board = board
        self._ident = ident
        self._position = position
        
        self._square = Rectangle(15, 15, (0, 0))    
        self._square.setFillColor(color)
   
    def addTo(self, win):
        """Add the pawns to the window."""
        win.add(self._square)

    def getPosition(self):
        """Return the position of the pawns so that we know where they are 
        located on the board."""
        return self._position
    
    def setPosition(self, pos):
        """Sets the position of the pawn to the variable."""
        self._position = pos
    
    def moveTo(self, location):
        """Move the pawn to the designated location on the board."""
        self._square.moveTo(location) 
    
    def move(self, dx, dy):
        """Move the pawn by the specific amount."""
        self._square.move(dx, dy)
        
    def getIdent(self):
        """Return the identification of the pawn."""
        return self._ident
    
    def setBorderColor(self, borderColor):
        """Change the border color of the pawns."""
        self._square.setBorderColor(borderColor)
    
    def setBorderWidth(self, borderWidth):
        """Change the border width of the pawns."""
        self._square.setBorderWidth(borderWidth)

class Deck:
    """A class to organize and create the deck of Hill Cards."""
    
    def __init__(self, board):
        self._board = board
        self._deck = []
        for name in ("ca1", "ca2", "ca3", "ca4", "ca5", "ca6", "ca7", "ca8",
                     "ca9", "ca10", "ca11", "ca12"):
            c = HillCards(name, faceFileName=name + ".png")
            self._deck.append(c)
        self._discardPile = []

    def empty(self):
        """Checks to see if the deck of Hill Cards is empty or not."""
        return len(self._deck) == 0
        
    def deal(self):
        """Take the top card of the randomly shuffled deck and moves it into the
        discard pile."""
        topDeck = self._deck[0]
        self._deck.remove(topDeck)
        self._discardPile.append(topDeck)
        return topDeck
    
    def shuffle(self):
        """Shuffles the 12 Hill Cards in the deck."""
        randomDeck = []
        length = len(self._deck)
        for _ in range(length):
            number = random.randrange(len(self._deck))
            randomDeck.append(self._deck[number])
            self._deck.remove(self._deck[number])
        self._deck = randomDeck
    
    def discardPileReshuffle(self):
        """Reshuffles the discarded cards so that the player's can continue to 
        use the Hill Cards."""
        self._deck = self._discardPile
        self.shuffle()
        self._discardPile = []

    def getDeck(self):
        """Returns the deck of Hill Cards."""
        return self._deck

class HillCards:
    """A class to create and manage the individual cards that make up the 
    deck."""
    
    def __init__(self, name, faceFileName):
        self._width = 150
        self._height = 100
        self._center = (175, 175)
        self._name = name
        self._faceUp = False
        
        faceurl = "https://cs.hamilton.edu/~htaft/images/" + faceFileName
        self._face = Image(faceurl, self._center, self._width, self._height)
        self._face.setDepth(25)
        
        backurl = "https://cs.hamilton.edu/~dgliedma/images/HillCard.jpg"
        self._back = Image(backurl, self._center, self._width, self._height)
        self._back.setDepth(20)
    
    def addTo(self, win):
        """Adds the faces and backs of the cards to the window."""
        win.add(self._face)
        self._face.moveTo((self._center))
        
        win.add(self._back)
        self._back.moveTo((self._center))
    
    def getFaceDepth(self):
        """Returns the depth of the face of the card."""
        return self._face.getDepth()
    
    def getBackDepth(self):
        """Returns the depth of the back of the card."""
        return self._back.getDepth()
        
    def getName(self):
        """Return the name of the cards."""
        return self._name
    
    def getFace(self):
        """Returns the face of the card."""
        return self._face
    
    def getBack(self):
        """Returns the back of the card."""
        return self._back
    
    def removeFrom(self, win):
        """Removes the face and back of the cards from the window."""
        win.remove(self._face)
        win.remove(self._back)
    
    def flip(self):
        """Flips the cards over by changing the depths of the faces and the 
        backs of the cards."""
        faceDepth = self._face.getDepth()
        backDepth = self._back.getDepth()
        
        self._face.setDepth(backDepth)
        self._back.setDepth(faceDepth)
    
    def flipBack(self):
        """Flips the cards back when reshuffling the deck by changing the depths
        of the faces and backs of the cards to their original positions."""
        faceDepth = self._face.getDepth()
        backDepth = self._back.getDepth()
        
        self._face.setDepth(backDepth)
        self._back.setDepth(faceDepth)
        
    def move(self, dx, dy):
        """Move the face and back of the card by the deisgnated amount."""
        self._face.move(dx, dy)
        self._back.move(dx, dy)
    
    def getReferencePoint(self):
        """Returns the center of the face of the card."""
        return self._face.getCenter()
        
    def faceUp(self):
        """Checks to see if the cards are face up by comparing the depths of the
        face and back of the cards."""
        return self._face.getDepth() < self._back.getDepth()
    
    def faceDown(self):
        """Checks to see if the cards are face down by comparing the depths of
        the face and back of the cards."""
        self._back.setDepth(self._face.getDepth() - 1)
    
    def setDepth(self, depth):
        """Sets the depth of the face and back of the cards so that one or the 
        other is showing on top."""
        if self.faceUp():
            self._face.setDepth(depth)
            self._back.setDepth(depth + 1)
        else:
            self._face.setDepth(depth + 1)
            self._back.setDepth(depth)

class Properties:
    """A class to manage and arrange the property spaces of the board."""
    
    def __init__(self, board, name, ident, faceFileName):
        self._width = 225
        self._height = 225
        self._center = (0, 0)
        self._name = name
        self._canBuy = True
        self._ident = ident
        self._board = board
        
        faceUrl = "https://cs.hamilton.edu/~dgliedma/images/" + faceFileName
        self._face = Image(faceUrl, self._center, self._width, self._height)
        self._face.setDepth(25)
    
    def addTo(self, win):
        """Adds the property cards to the window."""
        win.add(self._face)
        
    def moveTo(self, dx, dy):
        """Move the property cards to a specific location on the board."""
        self._face.moveTo((dx, dy))
    
    def getCanBuy(self):
        """Checks to see if the property has already been purchased."""
        return self._canBuy

    def getName(self):
        """Returns the name of the property card."""
        return self._name
        
class Button(EventHandler):
    """A class to create the purchase and pass buttons when buying or passing on
    a specific property."""
    
    def __init__(self, board, win, types, textsize, center):
        EventHandler.__init__(self)
        self._board = board
        self._win = win
        self._type = types
        self._textSize = textsize
        self._center1 = center
        
        self._rect = Rectangle(100, 80, center)
        self._rect.setBorderWidth(5)
        self._rect.setFillColor("white")
        
        self._text = Text(self._type, center, self._textSize)
        self._rect.addHandler(self)
    
    def addTo(self, win):
        """Adds the button and the text in the button to the window."""
        for obj in [self._rect, self._text]:
            win.add(obj)
    
    def handleMouseRelease(self, event):
        """Executes when one of the two buttons is clicked."""
        
        #If the purchase button is clicked, call the purchasePropery method.
        if self._board.determineIfBought():
            if self._type == "purchase":
                self._board.purchaseProperty()
        #If the pass button is clicked, call the purchasePropery method.
            else:
                self._board.passProperty()

def main(win):
    """The main function which initializes the program."""
    Board(win)

StartGraphicsSystem(main, WINDOW_WIDTH, WINDOW_HEIGHT)
