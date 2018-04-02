"""
*******************************************************************************
*File: Game.py                                                                *
*                                                                             *
*Author: Haley Taft                                                           *
*                                                                             *
*Partner: Daniel Gliedman                                                     *
*                                                                             *
*Assignment: Collections of Objects                                           *
*                                                                             *
*Date: April 7th 2017                                                         *
*                                                                             *
*Description: Makeing the game Monopoly using the graphics system. This game  *
*             Hamilton themed.                                                *
*******************************************************************************
"""
import random
from cs110graphics import*

IMAGE_WIDTH = 600
IMAGE_HEIGHT = 600
IMAGE_CENTER = (300, 300)

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600 
WINDOW_CENTER = (400, 300)

class Die(EventHandler):
    """ The class that creates the die and the various methods associated with 
        it. """
    SIDES = 6
    POSITIONS = [None,
                 [(0, 0), None, None, None, None, None],
                 [(-.25, .25), (.25, -.25), None, None, None, None],
                 [(-.25, .25), (0, 0), (.25, -.25), None, None, None],
                 [(-.25, -.25), (-.25, .25), (.25, -.25), (.25, .25), 
                  None, None],
                 [(-.25, -.25), (-.25, .25), (.25, -.25), (.25, .25), 
                  (0, 0), None],
                 [(-.25, -.25), (-.25, .25), (.25, -.25), (.25, .25), 
                  (-.25, 0), (.25, 0)]]
              
    def __init__(self, board, width=40, center=(400, 400), bgColor='white', 
                 fgColor='black'):
        EventHandler.__init__(self)
        self._board = board 
        self._value = 6 
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgColor)
        self._square.setDepth(20) 
        self._center = center
        self._width = width
        
        #adds the pips to the die
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgColor)
            pip.setDepth(20)
            self._pips.append(pip)
        self._square.addHandler(self)
        self._update() 

    def addTo(self, win):
        """ Method that adds the visual attributes of the die to the window. """
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)
            
    def roll(self):
        """ Method that computes a randome value for the die and updates it 
            visually."""
        self._value = random.randrange(Die.SIDES) + 1
        self._update()
        
    def getValue(self): 
        """ Method that returns the value of the die. """
        return self._value
        
    def _update(self):
        """ Private method that visually updates the die. """
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
    
    def handleMouseRelease(self, event):
        """ Method that rolls the die, reports the click and changes the turn
            when the die is clicked. """
        self.roll()
        self._board.reportDieClick()
        self._board.changeTurn()

class Pawn: 
    """ A class that creates the pawns and the methods that correpsond with 
        them. """
        
    def __init__(self, board, color, ident, position):
        self._color = color
        self._board = board 
        self._ident = ident  
        self._position = position 
        self._square = Rectangle(15, 15, (0, 0))
        self._square.setFillColor(color)

    def addTo(self, win):
        """ Method that adds the pawn to the window. """
        win.add(self._square)
        
    def getPosition(self):
        """ Method that returns the pawn's position. """
        return self._position 
    
    def setPosition(self, pos):
        """ Method that sets the pawn's position. """
        self._position = pos
    
    def moveTo(self, location):
        """ Method that moves the pawn. """
        self._square.moveTo(location)
        
    def getIdent(self):
        """ Method that returns the identifier of the pawn. """
        return self._ident
    
    def move(self, dx, dy):
        """ Method that moves the pawn. """
        self._square.move(dx, dy)
    
    def setBorderColor(self, color):
        """ Method that sets the boarder color of the pawn. """
        self._square.setBorderColor(color)
    
    def setBorderWidth(self, width):
        """ Method that sets the border width of the pawn. """
        self._square.setBorderWidth(width)

class BoardSpace:
    """ Creates the graphical space to record the centers. """
    
    def __init__(self, board, center):       
        self._board = board
        self._center = center
        self._square = Rectangle(30, 30, center)
        self._square.setDepth(100)
    
    def addTo(self, win):
        """ Method that adds the space to the window. """
        win.add(self._square)
    
    def getCenter(self):
        """ Method that returns the center of the space. """
        return self._center

    def setDepth(self, depth):
        """ Method that sets the depth of the space. """
        self._square.setDepth(depth)

class Board:
    """ Creates the board and is where all other class objects are created. """
    
    def __init__(self, win):

        self._win = win
        
        #sets the current player to 0 
        self._current = 0
        
        #two empty lists that will append the properties each player buys
        self._player1 = []
        self._player2 = []
        
        self._player1Text = Text("Player 1", (700, 50), 30)
        self._win.add(self._player1Text)
        self._player2Text = Text("Player 2", (850, 50), 30)
        self._win.add(self._player2Text)
        
        #the text that shows up for purchased properties 
        self._text = Text("This property has been bought. Press pass and pay\
                           rent.", (1250, 350), 15)
        self._win.add(self._text)
        
        #creates the die from the Die class
        self._die = Die(self)
        self._die.addTo(win)
        
        #creates the deck from the Deck class
        self._deck = Deck(self)
        self._deck.shuffle()
        self._card = self._deck.deal()
        self._card.addTo(self._win)
        
        #this line is too long but when we tried to put it on two lines
        #   the image would never load 
        url = ("https://cs.hamilton.edu/~htaft/images/Screen_Shot_2017-04-14_at_1.42.59_PM.png")

        #creates the board image
        self._boardBack = Image(url, IMAGE_CENTER, IMAGE_WIDTH, IMAGE_HEIGHT)
        self._win.add(self._boardBack)
        
        #creates non-visible board spaces to move the pawns around the board
        self._top = self.createSpacesHorizontal(115, 35, 'add', win)
        self._bottom = self.createSpacesHorizontal(485, 570, 'subtract', win)
        self._right = self.createSpacesVertical(565, 109, 'add', win)
        self._left = self.createSpacesVertical(35, 492, 'subtract', win)
        self._topLeft = Rectangle(30, 30, (40, 40))
        self._topLeft.setDepth(100)
        self._topLeft1 = self._topLeft.getCenter()
        self._win.add(self._topLeft)
        self._topRight = Rectangle(30, 30, (560, 40))
        self._topRight.setDepth(100)
        self._topRight1 = self._topRight.getCenter()
        self._win.add(self._topRight)
        self._bottomLeft = Rectangle(30, 30, (20, 570))  
        self._bottomLeft.setDepth(100)
        self._bottomLeft1 = self._bottomLeft.getCenter()
        self._win.add(self._bottomLeft)
        self._bottomRight = Rectangle(30, 30, (560, 560))
        self._bottomRight.setDepth(100)
        self._bottomRight1 = self._bottomRight.getCenter()
        self._win.add(self._bottomRight)
        self._campo = Rectangle(30, 30, (65, 545))
        self._campo.setDepth(100)
        self._campo1 = self._campo.getCenter()
        self._win.add(self._campo)
        
        #master list of a list of all the centers of the board spaces
        self._mastCenterList = [[self._bottomRight1] + self._bottom + 
                                [self._bottomLeft1] + self._left + 
                                [self._topLeft1] + self._top + 
                                [self._topRight1] + self._right]
        
        #creates the properties 
        self._properties = []
        
        #loop of names and identifications for each property to be created 
        for name, ident in [("p2a", 0), ("p1a", 1), ("p23b", 2), ("p3a", 3), 
                            ("p4a", 4), ("p5a", 5), ("p6a", 6), ("p7a", 7), 
                            ("p8a", 8), ("p24a", 9), ("p9a", 10), ("p10a", 11),
                            ("p11a", 12), ("p12a", 13), ("p13a", 14), 
                            ("p14a", 15), ("p25a", 16), ("p15a", 17), 
                            ("p16a", 18), ("p17a", 19), ("p18a", 20), 
                            ("p19a", 21), ("p20a", 22), ("p26a", 23),
                            ("p21a", 24), ("p22a", 25)]:
                            
            thisProperty = Properties(self, name, ident, 
                                      faceFileName=name+".png")
            thisProperty.addTo(self._win)
            thisProperty.moveTo(-500, 300) #moves the properties off the screen 
            self._properties.append(thisProperty)
        
        #creates bogus properties not to be used 
        self._bogus = []
        for i in range(14): 
            prop = Properties(self, "bad", i, faceFileName="bad.png")
            self._bogus.append(prop)
    
        #list of properties and bogus properties so that the idices correspond
        #   between property objects and boardspace 
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
        
        #creates purchase button
        self._purchase = Button(self, self._win, "purchase", 15, (700, 400))
        self._purchase.addTo(win)
        
        #creates pass button
        self._pass = Button(self, self._win, "pass", 40, (800, 400))
        self._pass.addTo(win)
        
        #creates pawns 
        self._pawns = []
        
        #loop for the color and identification of the pawns
        for color, which in [('DarkBlue', 0), ('#F5DEB3', 1)]:
            thisPawn = Pawn(self, color, which, 0)
            thisPawn.addTo(self._win)
            thisPawn.moveTo(self._mastCenterList[0][0])
            self._pawns.append(thisPawn)
            self._updatePawnLocations()
        
        #creates the money     
        self._money = []
        
        #loops through the value, center and identification to create the 
        #   two moneys 
        for value, center, which in [(2000, (700, 100), 0), 
                                     (2000, (850, 100), 1)]:
            thisMoney = Money(self, win, value, center, which)
            thisMoney.addTo(self._win)
            self._money.append(thisMoney)
        
    def createSpacesHorizontal(self, xpos, ypos, direction, win):
        """ Method to create the horizontal board spaces. Creates a list of 
            all the centers of those spaces to then be appended to the master 
            list. """
            
        self._centerList = []
        self._spaces = [] 
        
        #creates 9 spaces with depths below the board
        for _ in range(9):
            thisSpace = BoardSpace(self, (xpos, ypos)) 
            thisSpace.setDepth(100)
            thisSpace.addTo(win)
            self._spaces.append(thisSpace)
            
            #depending on what part of the board, will either add or subtract 
            #   to create the spaces
            if direction == 'add':
                xpos += 46
            if direction == 'subtract':
                xpos -= 46
                
            #appends the centers of the space to the list
            self._centerList.append(thisSpace.getCenter())
        return self._centerList
    
    def createSpacesVertical(self, xpos, ypos, direction, win):
        """ Method to create the vertical board spaces. Creates a list of all 
            the centers of those spaces and to then be appended to the master
            list. """
            
        self._centerList = []
        self._spaces = [] 
        
        #creates 9 spaces with the depths below the board
        for _ in range(9):
            thisSpace = BoardSpace(self, (xpos, ypos)) 
            thisSpace.addTo(win)
            self._spaces.append(thisSpace)
            
            #depending on what part of the board, will either add or subtract 
            #   to create certain spaces 
            if direction == 'add':
                ypos += 48
            if direction == 'subtract':
                ypos -= 48
            
            #appends the centers of the space to the list
            self._centerList.append(thisSpace.getCenter())
        return self._centerList
    
    def reportDieClick(self):
        """ Method to report the die click and update the pawn's location on
            that click. """
            
        thePawn = self._pawns[self._current]
        pos = thePawn.getPosition() 
        pos = pos + self._die.getValue()
        pos = pos % len(self._mastCenterList[0])
        thePawn.setPosition(pos)
        self._updatePawnLocations()
        
    def changeTurn(self):
        """ Method to change and actively show the current player. """
        
        player1Money = self._money[0].getValue()
        player2Money = self._money[1].getValue()
        
        if player1Money <= 0 or player2Money <= 0:
            endRect = Rectangle(350, 200, (500, 300))
            endRect.setFillColor("red")
            endRect.setDepth(1)
            endText = Text("GAME OVER!", (500, 300), 50)
            endText.setDepth(1)
            self._win.add(endRect)
            self._win.add(endText)
        else:        
            self._pawns[self._current].setBorderColor("black")
            self._current = (self._current + 1) % len(self._pawns)
            self._pawns[self._current].setBorderColor("green")
            self._pawns[self._current].setBorderWidth(3)

    def _updatePawnLocations(self):
        """ Method to update the pawn's position on the board and compare its 
            current space to a property space or a card space and if it has
            passed Go. """
            
        offsets = [-1, 1]
        pawn = self._pawns[self._current]
        pos = pawn.getPosition()
        theSpace = self._mastCenterList[0]
        
        #this moves the pawn to the new space and offsets it so that pawns 
        #   are not on top of each other 
        pawn.moveTo(theSpace[pos])
        pawn.move(0, offsets[self._current] * 10)
        
        #determines if the space is a property 
        self.compareSpaceToProperty()
        
        #determines if the space is a Hillcard
        self.determineCardSpace(theSpace[pos])
        
        #determines if the pawn has passed go
        self.determineGo()

    def _updateCardPawnLocations(self, location):
        """Method to update the pawn's position on the board, but is only called
            if the pawn is on a hillcard space. """
        
        #this does essentially the same thing as above but does not call the
        #   other methods 
        offsets = [-1, 1]
        pawn = self._pawns[self._current] 
        pos = self._returnPosition(self._mastCenterList[0], location)
        pawn.setPosition(pos)
        pawn.move(0, offsets[self._current] * 10) 

    def _returnPosition(self, lists, position):
        """ Private method that returns the position of a pawn in the 
            form of an integer. """
        #this method could be a function,
        #could not figure out "using type() instead of isinstance() for a 
        #   typecheck" convention error here
        if type(position) is tuple:
            
            #the campo location is given in a tuple, so our rule is that it 
            #   will just spit the pawn out on a random space
            pos = random.randrange(len(lists))
            return pos
            
        #same error as above    
        if type(position) != tuple:
            
            #for when the location is not a tuple, but returns the correct
            #   corresponding integer
            for i in range(len(lists)):
                if lists[i] == position:
                    return i 
    
    def determineCardSpace(self, location):
        """ Method to determine if the pawn is on a Hillcard board space. """
        
        #if the pawn is at any of these locations of the Hillcards
        #there is one too many boolean expressions here, but didn't have time 
        #   to fix that
        if (location == (439, 570) or location == (209, 570) or 
                location == (35, 204) or location == (161, 35) or 
                location == (565, 205) or location == (565, 349)):
                    
            #if the deck isn't empy deal the card 
            if self._deck.empty() is False:
                self._card = self._deck.deal()
                self._card.flip()
                self._card.addTo(self._win)
                
                #calls the fuction of the card 
                self.cardFunctions(self._card) 
            else:
                
                #fix the empty deck
                self._deck.discardPileShuffle()
                for card in self._deck.getDeck():
                    card.flipBack()

    def cardFunctions(self, card):
        """ Method to compute the card's function when card is drawn. This 
            does not draw the property cards."""
        pawn = self._pawns[self._current]
        self._card = card

        if self._card.getName() == "ca1":
            #Go the the Bundy East space
            pawn.moveTo(self._mastCenterList[0][3])
            self._updateCardPawnLocations(self._mastCenterList[0][3])

        if self._card.getName() == "ca2":
            #Go to hte Diner space
            pawn.moveTo(self._mastCenterList[0][25])
            self._updateCardPawnLocations(self._mastCenterList[0][25])

        if self._card.getName() == "ca3":
            #Go to the Dunham space
            pawn.moveTo(self._mastCenterList[0][6])
            self._updateCardPawnLocations(self._mastCenterList[0][6])

        if self._card.getName() == "ca4":
            #Pay $50 to the bank
            money = self._money[self._current]
            money.subtractMoney(50)
            
        if self._card.getName() == "ca5":
            #Collect $50 from the bank
            money = self._money[self._current]
            money.addMoney(15)
        
        if self._card.getName() == "ca6":
            #Go to the Morris space
            pawn.moveTo(self._mastCenterList[0][34])
            self._updateCardPawnLocations(self._mastCenterList[0][34])

        if self._card.getName() == "ca7":
            #Pay $25 to the bank
            money = self._money[self._current]
            money.subtractMoney(25)
            
        if self._card.getName() == "ca8":
            #Go to the Campo space
            pawn.moveTo(self._campo1)
            self._updateCardPawnLocations(self._campo1)

        if self._card.getName() == "ca9":
            #Go to the library space
            pawn.moveTo(self._mastCenterList[0][18])
            self._updateCardPawnLocations(self._mastCenterList[0][18])

        if self._card.getName() == "ca10":
            #Go to the Go space
            pawn.moveTo(self._mastCenterList[0][0])
            self._updateCardPawnLocations(self._mastCenterList[0][0])

        if self._card.getName() == "ca11":
            #Go the Science Center space
            pawn.moveTo(self._mastCenterList[0][19])
            self._updateCardPawnLocations(self._mastCenterList[0][19])

        if self._card.getName() == "ca12":
            #Collect $20 from the bank
            money = self._money[self._current]
            money.addMoney(20)

    def compareSpaceToProperty(self):
        """ Method that chekc to see if the pawn's location is a property 
            space and move the corresponding card into the window. """
        pawn = self._pawns[self._current]
        pos = pawn.getPosition()
        prop = self._prop[pos]
        
        #runs through all the possible property names and sees if the position's
        #   name is the same
        for name in ["p1a", "p2a", "p3a", "p4a", "p5a", "p6a", "p7a", "p8a",
                     "p9a", "p10a", "p11a", "p12a", "p13a", "p14a", "p15a", 
                     "p16a", "p17a", "p18a", "p19a", "p20a", "p21a", "p22a", 
                     "p23b", "p24a", "p25a", "p26a"]:
            if name == prop.getName():
                #moves the corresponding card
                prop.moveTo(750, 500)  
                if prop.getCanBuy() is False:
                    self._text.moveTo((800, 300))
                
    def determineIfBought(self):
        """ Method to determine if the pawn has landed on a owned property. 
            ALso pays rent to the owner. """
        
        #the current player is switched before this method is called so the pawn
        #   has to be switched 
        if self._current == 0:
            pawn = self._pawns[1]
            pos = pawn.getPosition()
            prop = self._prop[pos]
            #if the pawn is owned, pay rent and move the property card and text
            #   off the screen 
            if prop.getCanBuy() is False:
                self._money[1].subtractMoney(20)
                self._money[0].addMoney(20)
                prop.moveTo(1100, 300)
                self._text.moveTo((1250, 300))
                return False
            else:
                return True
        else:
            #same thing just for other pawn
            pawn = self._pawns[0]
            pos = pawn.getPosition()
            prop = self._prop[pos]
            if prop.getCanBuy() is False:
                self._money[0].subtractMoney(20)
                self._money[1].addMoney(20)
                prop.moveTo(1100, 300)
                self._text.moveTo((1250, 300))
                return False
            else:
                return True
        
    def purchaseButton(self):
        """ Method for the purchase button. """
        if self._current == 0:
            pawn = self._pawns[1] 
            pos = pawn.getPosition()
            prop = self._prop[pos]
            canBuy = prop.getCanBuy()
            if canBuy is True:
                #subtracts $100 from the players account 
                self._money[1].subtractMoney(100)
                self._player2.append(prop)
                #now the attribute of the property must be made False
                #there is a warning for this line below, but didn't have time
                #   to figure out how to properly fix it
                prop._canBuy = False
        else: 
            #same thing for the other pawn 
            pawn = self._pawns[0]
            pos = pawn.getPosition()
            prop = self._prop[pos]
            canBuy = prop.getCanBuy()
            if canBuy is True:
                self._money[0].subtractMoney(100)
                self._player1.append(prop)
                prop._canBuy = False
                
        #moves the property card out of the window
        prop.moveTo(1100, 300)
        
    def passButton(self): 
        """ Method for when purhcase button is pressed. """
        if self._current == 0: 
            pawn = self._pawns[1]
        else: 
            pawn = self._pawns[0]
        #remove the corresponding property card off of the screen 
        pos = pawn.getPosition()
        prop = self._prop[pos]
        prop.moveTo(1100, 300)
        
    def determineGo(self):
        """ Method that determines if the player has passed Go. Does not take 
            into account if a card has moved the player passed go, only if it
            rolls passed go. """
        pawn = self._pawns[self._current]
        pos = pawn.getPosition()
        dieValue = self._die.getValue()
        if pos + dieValue >= 39: 
            self._money[self._current].addMoney(200)

class Money:
    """ Makes the outline of the Money class object. """
    
    def __init__(self, board, win, value, center, ident):
        
        self._center = center
        self._ident = ident
        self._value = value
        self._board = board
        self._win = win
        self._rectangle = Rectangle(100, 80, self._center)
        self._rectangle.setBorderWidth(10)
        self._textMon = Text("$", self._center, 50)
        self._text = Text(value, self._center, 20)
    
    def addTo(self, win): 
        """ Method to add the graphical elements of this class to the window."""
        
        win.add(self._rectangle)
        self._rectangle.moveTo((self._center))
        win.add(self._text)
        self._text.moveTo((self._center[0] + 10, self._center[1] + 10))
        win.add(self._textMon)
        self._textMon.moveTo((self._center[0] - 30, self._center[1] + 20))
        
    def getIdent(self):
        """ Returns the identifier. """
        
        return self._ident
        
    def getValue(self):
        """ Returns the value. """
        return self._value
        
    def addMoney(self, value):
        """ Adds money and visually updates the account. """
        self._value += value
        self._updateValue()
    
    def subtractMoney(self, value):
        """ Subtracts money and visually updates the account. """
        self._value -= value
        self._updateValue()
    
    def _updateValue(self):
        """ Private method for update the visual account in window. """
        self._text.setTextString(str(self._value))
    
class Deck:
    """ A class to organize and create the deck of the Hillcards. """
    
    def __init__(self, board): 
        self._discardPile = []
        self._board = board 
        self._deck = []
        for name in ("ca1", "ca2", "ca3", "ca4", "ca5", "ca6", "ca7", "ca8", 
                     "ca9", "ca10", "ca11", "ca12"):
            card = HillCard(name, faceFileName=name+".png")
            self._deck.append(card)
        
    def empty(self):
        """ Method that returns True if the length of the deck is zero. """
        return len(self._deck) == 0
    
    def getDeck(self):
        """ Method that returns the deck. """
        return self._deck
    
    def deal(self):
        """ Method that deals a card, removes it from the deck and adds it to
            the discard pile. """
            
        topCard = self._deck[0]
        self._deck.remove(topCard)
        self._discardPile.append(topCard)
        return topCard
        
    def shuffle(self):
        """ Method that shuffles the deck. """
        shuffledDeck = []
        length = len(self._deck)
        for _ in range(length):
            number = random.randrange(len(self._deck))
            shuffledDeck.append(self._deck[number])
            self._deck.remove(self._deck[number])
        self._deck = shuffledDeck
        
    def discardPileShuffle(self):
        """ Method that reassigns the discard pile to the deck and 
            shuffles it."""
        self._deck = self._discardPile
        self.shuffle()
        self._discardPile = []
    
class HillCard:
    """ A class to create and manage the individual cards that make up the 
        deck. """
        
    def __init__(self, name, faceFileName):
        self._width = 150
        self._height = 100
        self._center = (175, 175)
        self._name = name 
        self._faceUp = False
        
        faceurl = "https://cs.hamilton.edu/~htaft/images/" + faceFileName
        self._face = Image(faceurl, self._center, self._width, self._height)
        self._face.setDepth(25)
       
        #this line is also too long for the same reasons as before
        backurl = ("https://cs.hamilton.edu/~htaft/images/Screen_Shot_2017-04-21_at_10.15.13_AM.png")
        self._back = Image(backurl, self._center, self._width, self._height)
        self._back.setDepth(20)
        
    def addTo(self, win):
        """ Method to add the card to the window."""
        win.add(self._face)
        self._face.moveTo((self._center))

        win.add(self._back)
        self._back.moveTo((self._center))
    
    def getName(self):
        """ Method that returns the name."""
        return self._name
        
    def getFace(self):
        """ Method that returns the face of the hillcard. """
        return self._face                   
        
    def getBack(self):
        """ Method that returns the back of the hillcard. """
        return self._back                  
        
    def faceUp(self):
        """ Method that determines if the card is face up. """
        return self._face.getDepth() < self._back.getDepth()
    
    def removeFrom(self, win):
        """ Method that removes the card. """
        win.remove(self._face)
        win.remove(self._back)
        
    def flip(self):
        """Method that flips the card. """
        faceDepth = self._face.getDepth()
        backDepth = self._back.getDepth()
        
        self._face.setDepth(backDepth)
        self._back.setDepth(faceDepth)
        
    def flipBack(self):
        """ Method that flips the card back. """
        faceDepth = self._face.getDepth()
        backDepth = self._back.getDepth()
        
        self._face.setDepth(backDepth)
        self._back.setDepth(faceDepth)
        
    def move(self, dx, dy):
        """ Method that moves the card. """
        self._face.move(dx, dy)
        self._back.move(dx, dy)
    
    def getReferencePoint(self): 
        """ Method that gets the center of the hillcard. """
        return self._face.getCenter()
        
    def setDepth(self, depth):
        """ Method that sets the depths of the cards. """
        if self._faceUp:
            self._face.setDepth(depth)
            self._back.setDepth(depth + 1)
        else:
            self._face.setDepth(depth + 1)
            self._back.setDepth(depth)
    
class Properties: 
    """ A class to manage and arrange the property space cards on the board."""
    
    def __init__(self, board, name, ident, faceFileName):
        self._width = 95
        self._height = 95
        self._center = (0, 0)
        self._name = name 
        self._canBuy = True
        self._ident = ident
        self._board = board
        
        faceUrl = "https://cs.hamilton.edu/~dgliedma/images/" + faceFileName
        self._face = Image(faceUrl, self._center, self._width, self._height)
        self._face.setDepth(25)
        
    def addTo(self, win):
        """ Method to add the property cards to the window. """
        win.add(self._face)

    def moveTo(self, dx, dy):
        """ Method to move the property cards. """
        self._face.moveTo((dx, dy))
        
    def getCanBuy(self):
        """ Mehtod that returns whether the property can be bought. """
        return self._canBuy
    
    def getName(self):
        """ Method that returns the name of the card. """
        return self._name 

class Button(EventHandler):
    """ A class to create the purchase and pass buttons when buying or passing
        on a property. """
        
    def __init__(self, board, win, types, textsize, center): 
        EventHandler.__init__(self)
        self._board = board
        self._win = win
        self._type = types
        self._textSize = textsize
        self._center = center 

        self._rect = Rectangle(100, 80, self._center)
        self._rect.setBorderWidth(5)
        self._rect.setFillColor("blue")
        self._text = Text(self._type, self._center, self._textSize)
        self._rect.addHandler(self)
        
    def addTo(self, win):
        """Method that adds the button to the window. """
        for obj in [self._rect, self._text]:
            win.add(obj)

    def handleMouseRelease(self, event):
        """ Method that determines if the purchase or passed button were pressed
            and calls the corresponding method of the board class. """
        if self._board.determineIfBought():
            if self._type == "purchase":
                self._board.purchaseButton()
            else:
                self._board.passButton()
                
def main(win):
    """ The main function which initializes the program. """
    Board(win)
    
StartGraphicsSystem(main, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    
    
    
    
    
    
    
    
    
    
    
    
