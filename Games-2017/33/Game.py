"""
 *******************************************************************************
FILE:           Game.py

AUTHOR:         Spencer Dutton

PARTNER:        Kent Campbell

ASSIGNMENT:     Project 6: Board Game

DATE:           05/01/17

DESCRIPTION:    This program allows the user to play Monopoly.

 *******************************************************************************
"""

import random
from cs110graphics import *

SPACES = [None, "Mediterranean Avenue", "Community Chest", "Baltic Avenue",
          "Income Tax", "Reading Railroad", "Oriental Avenue", "Chance",
          "Vermont Avenue", "Connecticut Avenue", None, "St. Charles Place",
          "Electric Company", "States Avenue", "Virginia Avenue",
          "Pennsylvania Railroad", "St. James Place", "Community Chest",
          "Tennessee Avenue", "New York Avenue", None, "Kentucky Avenue",
          "Chance", "Indiana Avenue", "Illinois Avenue", "B. & O. Railroad",
          "Atlantic Avenue", "Ventnor Avenue", "Water Works", "Marvin Gardens",
          None, "Pacific Avenue", "North Carolina Avenue", "Community Chest",
          "Pennsylvania Avenue", "Short Line", "Chance", "Park Place",
          "Luxury Tax", "Boardwalk"]

AVAILSPACES = ["Mediterranean Avenue", "Baltic Avenue", "Reading Railroad",
               "Oriental Avenue", "Vermont Avenue", "Connecticut Avenue",
               "St. Charles Place", "Electric Company", "States Avenue",
               "Virginia Avenue", "Pennsylvania Railroad", "St. James Place",
               "Tennessee Avenue", "New York Avenue", "Kentucky Avenue",
               "Indiana Avenue", "Illinois Avenue", "B. & O. Railroad",
               "Atlantic Avenue", "Ventnor Avenue", "Water Works",
               "Marvin Gardens", "Pacific Avenue", "North Carolina Avenue",
               "Pennsylvania Avenue", "Short Line", "Park Place", "Boardwalk"]

SPACECOLOR = [None, "purple", "blank", "purple", "blank", "blank", "lightblue",
              "blank", "lightblue", "lightblue", None, "maroon", "blank",
              "maroon", "maroon", "blank", "orange", "blank", "orange",
              "orange", None, "red", "blank", "red", "red", "blank", "yellow",
              "yellow", "blank", "yellow", None, "green", "green", "blank",
              "green", "blank", "blank", "darkblue", "blank", "darkblue"]

SQUARES = ["Go", "Jail", "Free Parking", "Go To Jail"]

POS = [(580, 580), (515, 580), (465, 580), (415, 580), (365, 580), (315, 580),
       (265, 580), (215, 580), (165, 580), (115, 580), (50, 580), (50, 515),
       (50, 465), (50, 415), (50, 365), (50, 315), (50, 265), (50, 215),
       (50, 165), (50, 115), (50, 50), (115, 50), (165, 50), (215, 50),
       (265, 50), (315, 50), (365, 50), (415, 50), (465, 50), (515, 50),
       (580, 50), (580, 115), (580, 165), (580, 215), (580, 265), (580, 315),
       (580, 365), (580, 415), (580, 465), (580, 515)]

PRICES = [None, 60, None, 60, None, 200, 100, None, 100, 120, None, 140, 150,
          140, 160, 200, 180, None, 180, 200, None, 220, None, 220, 240, 200,
          260, 260, 150, 280, None, 300, 300, None, 320, 200, None, 350, None,
          400]

RENT = [None, 2, None, 4, None, None, 6, None, 6, 8, None, 10, None, 10, 12,
        None, 14, None, 14, 16, None, 18, None, 18, 20, None, 22, 22, None, 24,
        None, 26, 26, None, 28, None, None, 35, None, 50]

HOUSECOST = [0, 50, 0, 50, 0, 0, 50, 0, 50, 50, 0, 100, 0, 100, 100, 0, 100, 0,
             100, 100, 0, 150, 0, 150, 150, 0, 150, 150, 0, 150, 0, 200, 200, 0,
             200, 0, 0, 200, 0, 200]

PAWNCOLORS = ["purple", "blue", "red", "yellow", "green", "orange"]

PROPWIDTH = 50
PROPHEIGHT = 80
WINWIDTH = 900
WINHEIGHT = 650

NUM = int(input("How many people are playing? (2 to 6 players)"))

PAWNS = []

class Board:
    """Builds the game board"""
    def __init__(self, win):
        win.setWidth(WINWIDTH)
        win.setHeight(WINHEIGHT)
        self._win = win
        
        #builds the background behind the game board
        bgBoard = Rectangle(610, 610, (315, 315))
        bgBoard.setFillColor("#ccffdd")
        bgBoard.setDepth(100)
        win.add(bgBoard)
        
        self._buildProperties()
        self._buildImages()
        self._freeParking = 0
        self._stripes = []
        self._buildStripes()
        
        #builds the background behind the money displays
        self._box = Rectangle(245, 610, (760, 315))
        win.add(self._box)
        self._box.setFillColor("lightblue")
        self._box.setBorderColor("white")
        self._box.setDepth(100)
        
        #builds the boxes that total the money of each player
        self._playerText = []
        self._aroundTextList = []
        dy = 50 
        for i in range(NUM):
            moneyLeft = Text('Player ' + str(i+1) + ': $1500', (750, dy), 30)
            self._playerText.append(moneyLeft)
            win.add(moneyLeft)
            self._outline = Rectangle(235, 50, (760, dy - 10))
            self._outline.setBorderWidth(5)
            self._outline.setBorderColor(PAWNCOLORS[i])
            win.add(self._outline)
            self._aroundText = Rectangle(235, 50, (760, dy - 10))
            self._aroundText.setFillColor("PeachPuff")
            self._aroundText.setDepth(51)
            self._aroundTextList.append(self._aroundText)
            dy += 100
        
        #sets up the free parking display
        win.add(Rectangle(140, 30, (170, 110)))
        win.add(Rectangle(140, 30, (170, 140)))
        win.add(Text("Free Parking", (170, 117), 22))
        self._freeParkingDisplay = Text("$0", (170, 147), 22)
        win.add(self._freeParkingDisplay)
        outlineBox = Rectangle(140, 60, (170, 125))
        outlineBox.setBorderWidth(2)
        win.add(outlineBox)
        
        #sets up the turn display
        win.add(Rectangle(100, 30, (170, 490)))
        win.add(Rectangle(100, 30, (170, 520)))
        win.add(Text("Turn", (170, 497), 22))
        self._turnDisplayNum = 1
        self._turnDisplay = Text(str(self._turnDisplayNum), (170, 527), 22)
        win.add(self._turnDisplay)
        outlineBox2 = Rectangle(100, 60, (170, 505))
        outlineBox2.setBorderWidth(2)
        win.add(outlineBox2)

    def _buildProperties(self):
        """Builds the all of the spaces on the board"""
        url = "https://cs.hamilton.edu/~sdutton/images/"
        
        #builds the bottom nine spaces
        for i in range(1, 10):
            bottomRowSpace = Property(SPACES[i], PROPWIDTH, PROPHEIGHT, POS[i])
            bottomRowSpace.addTo(self._win)
            space = Image(url + str(i) + ".jpg", (POS[i][0], POS[i][1] + 10),
                          PROPWIDTH, PROPHEIGHT * (3/4))
            space.setDepth(55)
            self._win.add(space)
        
        #builds the left nine spaces
        for i in range(11, 20):
            leftColSpace = Property(SPACES[i], PROPWIDTH, PROPHEIGHT, POS[i])
            leftColSpace.rotate(90)
            leftColSpace.addTo(self._win)
            space = Image(url + str(i) + ".jpg", (POS[i][0] - 10, POS[i][1]),
                          PROPWIDTH, PROPHEIGHT * (3/4))
            space.setDepth(55)
            space.rotate(90)
            self._win.add(space)
        
        #builds the top nine spaces
        for i in range(21, 30):
            topRowSpace = Property(SPACES[i], PROPWIDTH, PROPHEIGHT, POS[i])
            topRowSpace.rotate(180)
            topRowSpace.addTo(self._win)
            space = Image(url + str(i) + ".jpg", (POS[i][0], POS[i][1] - 10),
                          PROPWIDTH, PROPHEIGHT * (3/4))
            space.setDepth(55)
            space.rotate(180)
            self._win.add(space)
        
        #builds the right nine spaces
        for i in range(31, 40):
            rightColSpace = Property(SPACES[i], PROPWIDTH, PROPHEIGHT, POS[i])
            rightColSpace.rotate(270)
            rightColSpace.addTo(self._win)
            space = Image(url + str(i) + ".jpg", (POS[i][0] + 10, POS[i][1]),
                          PROPWIDTH, PROPHEIGHT * (3/4))
            space.setDepth(55)
            space.rotate(270)
            self._win.add(space)
        
        #builds the corner spaces
        topLeft = Property(SQUARES[2], PROPHEIGHT, PROPHEIGHT, POS[20])
        topLeft.addTo(self._win)
        topRight = Property(SQUARES[3], PROPHEIGHT, PROPHEIGHT, POS[30])
        topRight.addTo(self._win)
        bottomLeft = Property(SQUARES[1], PROPHEIGHT, PROPHEIGHT, POS[10])
        bottomLeft.addTo(self._win)
        bottomRight = Property(SQUARES[0], PROPHEIGHT, PROPHEIGHT, POS[0])
        bottomRight.addTo(self._win)
    
    def _buildImages(self):
        """Builds all of the images on the board"""
        url = "https://cs.hamilton.edu/~sdutton/images/"
        
        #builds the images of all of the normal spaces
        propChars = [("ComChest", 2, 0), ("ComChest", 17, 90),
                     ("ComChest", 33, 270), ("Chance", 7, 0),
                     ("Chance", 22, 180), ("Chance", 36, 270),
                     ("electric", 12, 90), ("water", 28, 180),
                     ("Luxury", 38, 270), ("income", 4, 0), ("5r", 5, 0),
                     ("15r", 15, 90), ("25r", 25, 180), ("35r", 35, 270)]
        for name, pos, degrees in propChars:
            prop = Image(url + name + ".jpg", POS[pos], PROPWIDTH, PROPHEIGHT)
            prop.setDepth(55)
            prop.rotate(degrees)
            self._win.add(prop)
        
        #builds the images of the corner spaces
        cornerChars = [("Go", 0, 0), ("Jail", 10, 0), ("freeparking", 20, 90),
                       ("Gotojail", 30, 270)]
        for name, pos, degrees in cornerChars:
            corner = Image(url + name + ".jpg", POS[pos], PROPHEIGHT,
                           PROPHEIGHT)
            corner.setDepth(55)
            corner.rotate(degrees)
            self._win.add(corner)
        
        #builds misc graphics on the game board
        graphics = [("Chancecard", (415, 415), 4/3, 4/3, 225),
                    ("comcard", (220, 220), 4/3, 4/3, 45),
                    ("monopoly", (315, 315), 6, 15/16, 315)]
        for name, center, wscale, hscale, degrees in graphics:
            graphic = Image(url + name + ".jpg", center, wscale*PROPWIDTH,
                            hscale*PROPHEIGHT)
            graphic.rotate(degrees)
            self._win.add(graphic)

    def _buildStripes(self):
        """Builds all of the stripes that correspond to each player's owned
           properties"""
        for i in range(len(SPACES)):
            if (SPACES[i] != "Community Chest" and SPACES[i] != "Chance" and 
                    SPACES[i] != "Luxury Tax" and SPACES[i] != "Income Tax" and 
                    SPACES[i] != None):
                stripe = Rectangle(PROPWIDTH, 4, (POS[i][0], POS[i][1] + 42))
                stripe.setPivot(POS[i])
                if i > 10 and i < 20:
                    stripe.rotate(90)
                if i > 20 and i < 30:
                    stripe.rotate(180)
                if i > 30:
                    stripe.rotate(270)
                self._stripes.append(stripe)
            else:
                self._stripes.append(None)

    def showMoney(self, ident, money):
        """Updates the window display with the player's information"""
        self._playerText[ident].setText("Player " + str(ident + 1) + ": $" +
                                        str(money))
    
    def addFreeParking(self, num):
        """Adds a number to the total free parking value"""
        self._freeParking += num
        self._updateFreeParking()
    
    def zeroFreeParking(self):
        """Sets the free parking value to zero"""
        self._freeParking = 0
        self._updateFreeParking()
    
    def getFreeParking(self):
        """Returns the free parking value"""
        return self._freeParking
    
    def payRent(self, tenant, prop):
        """A given tenant pays the rent due to the owner of the property"""
        #finds the owner of the given property
        for i in range(NUM):
            for j in range(len(PAWNS[i].getProperties())):
                if PAWNS[i].getProperties()[j] == prop:
                    owner = PAWNS[i]
        if owner.getIdent() != tenant.getIdent():
            
            #sets up rent system for railroads
            if prop == 5 or prop == 15 or prop == 25 or prop == 35:
                rr = [25, 50, 100, 200][owner.getRailroads() - 1]
                tenant.changeMoney(-rr)
                owner.changeMoney(rr)
                self.showMoney(tenant.getIdent(), tenant.getMoney())
                self.showMoney(owner.getIdent(), owner.getMoney())
            
            #sets up rent system for utilities
            elif prop == 12 or prop == 28:
                ut = [4, 10][owner.getUtilities() - 1] * random.randrange(1, 13)
                tenant.changeMoney(-ut)
                owner.changeMoney(ut)
                self.showMoney(tenant.getIdent(), tenant.getMoney())
                self.showMoney(owner.getIdent(), owner.getMoney())
            
            #sets up rent system for other spaces
            else:
                multiplier = 1
                if owner.checkMonopoly(prop):
                    multiplier = 2
                tenant.changeMoney(-multiplier * RENT[prop])
                owner.changeMoney(multiplier * RENT[prop])
                self.showMoney(tenant.getIdent(), tenant.getMoney())
                self.showMoney(owner.getIdent(), owner.getMoney())
    
    def _updateFreeParking(self):
        """Updates the free parking display on the window"""
        self._freeParkingDisplay.setText('$' + str(self._freeParking))
    
    def showStripe(self, buyer, pos):
        """Shows the stripes alongside a buyer's property in the color of the
           buyer"""
        stripe = self._stripes[pos]
        stripe.setFillColor(buyer.getColor())
        self._win.add(stripe)
    
    def nextTurn(self):
        """Changes the turn on the screen and checks for a winner"""
        #changes the display of the turn number
        self._turnDisplayNum += 1
        self._turnDisplay.setText(str(self._turnDisplayNum))
        
        #declares the winner if the turn limit is reached
        if self._turnDisplayNum == 25:
            best = PAWNS[0].getMoney()
            winner = 0
            for i in range(NUM):
                if PAWNS[i].getMoney() > best:
                    best = PAWNS[i].getMoney()
                    winner = i
            self.declareWinner(winner)
        
        #declares the winner if all other players have lost
        count = 0
        winner = 0
        for i in range(len(PAWNS)):
            if PAWNS[i] != None:
                count += 1
                winner = i
        if count == 1:
            self.declareWinner(winner)
    
    def showTurn(self, ident):
        """Shows the box that highlights a current player"""
        self._win.add(self._aroundTextList[ident])
    
    def hideTurn(self, ident):
        """Hides the box that highlights a current player"""
        self._win.remove(self._aroundTextList[ident])
    
    def loser(self, ident):
        """Changes the money total display of a player to a message that this
           player has lost"""
        self._playerText[ident].setText("Player " + str(ident + 1) +
                                        " has lost")
    
    def declareWinner(self, ident):
        """Builds a screen that celebrates the winner"""
        bg = Rectangle(WINWIDTH, WINHEIGHT, (WINWIDTH/2, WINHEIGHT/2))
        bg.setFillColor("#ff6347")
        bg.setDepth(-5)
        self._win.add(bg)
        winner = Text("Player " + str(ident + 1) + " is the winner!",
                      (WINWIDTH/2, WINHEIGHT/2), 50)
        winner.setDepth(-10)
        self._win.add(winner)
    

class Property:
    """Creates the properties on the board"""
    def __init__(self, name, width, height, center):
        self._name = name
        self._center = center
        self._property = Rectangle(width, height, center)
        pivot = self._property.getPivot()
        self._propcolors = []
        
        #creates the color bars for properties part of monopolies
        for i in range(len(SPACES)):
            if name == SPACES[i]:
                if SPACECOLOR[i] != "blank":
                    self._color = Rectangle(PROPWIDTH, PROPHEIGHT/4,
                                            (self._center[0],
                                             self._center[1] - 30))
                    self._color.setFillColor(SPACECOLOR[i])
                    self._color.setPivot(pivot)
                    self._propcolors.append(self._color)
    
    def addTo(self, win):
        """Adds the properties and their color bars to the window"""
        win.add(self._property)
        for color in self._propcolors:
            win.add(color)
    
    def rotate(self, degrees):
        """Rotates the property and its color bar on the board"""
        self._property.rotate(degrees)
        for color in self._propcolors:
            color.rotate(degrees)


class Pawn:
    """Creates a pawn"""
    def __init__(self, board, color, ident, position, money):
        self._money = money
        self._color = color
        self._board = board
        self._ident = ident
        self._position = position
        self._square = Rectangle(15, 15, POS[0])
        self._square.setFillColor(color)
        self._jailtime = 0
        self._properties = []
        self._railroadCount = 0
        self._utilitiesCount = 0
    
    def addTo(self, win):
        """Adds the pawns to the window"""
        win.add(self._square)
    
    def getPosition(self):
        """Returns the position of a pawn"""
        return self._position
    
    def moveTo(self, pos):
        """Moves a pawn to a specified position"""
        self._square.moveTo(POS[pos])
        self._position = pos
    
    def move(self, num):
        """Moves a pawn a specified number of spaces on the game board"""
        self._position += num
        
        #if the pawn passes go, collect $200
        if self._position > 39:
            self._money += 200
            self._board.showMoney(self._ident, self._money)
        self._position = self._position % 40
        self._square.moveTo(POS[self._position])
        
    def actions(self):
        """Checks what to do for the given position of the pawn"""
        #offsets the pawn on the jail space
        if self._position == 10:
            self._square.move(-25, 25)
        
        #moves the pawn to jail
        elif self._position == 30:
            self._square.moveTo(POS[10])
            self._position = 10
            self.goToJail()
        
        #pays income tax
        elif self._position == 4:
            if self._money >= 200:
                self._money -= 200
                self._board.showMoney(self._ident, self._money)
                self._board.addFreeParking(200)
        
        #pays luxury tax
        elif self._position == 38:
            if self._money >= 100:
                self._money -= 100
                self._board.showMoney(self._ident, self._money)
                self._board.addFreeParking(100)
        
        #collects free parking
        elif self._position == 20:
            self._money += self._board.getFreeParking()
            self._board.showMoney(self._ident, self._money)
            self._board.zeroFreeParking()
        
        #collects $200
        elif self._position == 0:
            self._board.showMoney(self._ident, self._money)
        
        #for the community chest card: gives the pawn a random money value 
        #between -$200 and +$200
        elif (self._position == 2 or self._position == 17 or
              self._position == 33):
            self._money += random.randrange(-200, 200)
            self._board.showMoney(self._ident, self._money)
        
        #for the chance card: puts the pawn at a random position on the board
        elif (self._position == 7 or self._position == 22 or
              self._position == 36):
            self._position += random.randrange(40)
            if self._position > 39:
                self._money += 200
                self._board.showMoney(self._ident, self._money)
                self._position = self._position % 40
            self._square.moveTo(POS[self._position])
            self.actions()
        
        #checks to see if the property is available
        else:
            avail = False
            noBuy = False
            for i in range(len(AVAILSPACES)):
                if AVAILSPACES[i] == SPACES[self._position]:
                    avail = True
                    if self._money >= PRICES[self._position]:
                        if input("Do you want to purchase " +
                                 SPACES[self._position] + " for $" +
                                 str(PRICES[self._position]) +
                                 "? (Type Y or N)") == "Y":
                            self._properties.append(self._position)
                            self._money -= PRICES[self._position]
                            self._board.showMoney(self._ident, self._money)
                            self._board.showStripe(self, self._position)
                        else:
                            noBuy = True
                    else:
                        noBuy = True
            
            #pays rent if the property is not available
            if not avail:
                self._board.payRent(self, self._position)
            
            #removes the property from the available properties list, counts for
            #a railroad or utility
            if avail and not noBuy:
                AVAILSPACES.remove(SPACES[self._position])
                if (self._position == 5 or self._position == 15 or
                        self._position == 25 or self._position == 35):
                    self._railroadCount += 1
                if self._position == 12 or self._position == 28:
                    self._utilitiesCount += 1
            
            #updates the money for the pawn
            if noBuy:
                self._board.showMoney(self._ident, self._money)
        
    def checkMonopoly(self, prop):
        """Checks the pawn for a monopoly with the group of the given
           property"""
        count = 0
        
        #boosts the count if the property is part of a Duo-Monopoly
        if prop == 1 or prop == 3 or prop == 37 or prop == 39:
            count = 1
        for space in self._properties:
            if SPACECOLOR[space] == SPACECOLOR[prop]:
                count += 1
        return count == 3 
    
    def setDepth(self, depth):
        """Sets the depth of a pawn on a window"""
        self._square.setDepth(depth)
    
    def highlight(self):
        """Highlights and scales up the pawn"""
        self._square.setBorderColor("gold")
        self._square.scale(1.6)
        self._board.showTurn(self._ident)
    
    def dehighlight(self):
        """Returns the pawn to normal size and color"""
        self._square.setBorderColor("black")
        self._square.scale(.625)
        self._board.hideTurn(self._ident)
    
    def getMoney(self):
        """Returns the amount of money that the pawn has"""
        return self._money
    
    def getJailtime(self):
        """Returns the jailtime of the pawn"""
        return self._jailtime
    
    def subtractJailtime(self):
        """Subtracts 1 from the pawn's jailtime"""
        self._jailtime -= 1
    
    def zeroJailtime(self):
        """Sets the pawn's jailtime to zero"""
        self._jailtime = 0
    
    def changeMoney(self, num):
        """Adds the given amount to the pawn's money total"""
        self._money += num
    
    def goToJail(self):
        """Sets the pawn's jailtime to 3, for three turns"""
        self._jailtime = 3
    
    def getIdent(self):
        """Returns the identification number of the pawn"""
        return self._ident
    
    def getProperties(self):
        """Returns the list of properties that the pawn owns"""
        return self._properties
    
    def getColor(self):
        """Returns the color of the pawn"""
        return self._color
    
    def getRailroads(self):
        """Returns the number of railroads owner by this pawn"""
        return self._railroadCount
    
    def getUtilities(self):
        """Returns the number of utilities owned by this pawn"""
        return self._utilitiesCount
    
    def lose(self):
        """Implements the losing display for this pawn"""
        self._board.loser(self._ident)

class Die:
    """ A six-sided die """
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
                 
    def __init__(self, board, center, width=50, bgcolor='white', 
                 fgcolor='black'):
        self._board = board
        self._value = 6
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgcolor)
        self._square.setDepth(20)
        self._width = width
        self._center = center
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgcolor)
            pip.setDepth(20)
            self._pips.append(pip)
        self._update()
        
    def addTo(self, win):
        """Adds the die and the pips to the window"""
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)

    def roll(self):
        """Changes the value of this die to a random number between 1 and 
            the number of sides of a die"""
        self._value = random.randrange(Die.SIDES) + 1
        self._update()
    
    def getValue(self):
        """Returns the current value of this die"""
        return self._value
        
    def _update(self):
        """Private method: make this die's appearance match its value"""
        positions = Die.POSITIONS[self._value]
        for i in range(len(positions)):
            if positions[i] is None:
                self._pips[i].setDepth(25)
            else:
                self._pips[i].setDepth(15)
                cx, cy = self._center
                dx = positions[i][0] * self._width
                dy = positions[i][1] * self._width  
                self._pips[i].moveTo((cx + dx, cy + dy))


class Controller(EventHandler):
    """Puts together all of the components of the game"""
    def __init__(self, win):
        EventHandler.__init__(self)
        self._board = Board(win)
        self._win = win
        self._die1 = Die(self._board, (440, 120))
        self._die1.addTo(win)
        self._die2 = Die(self._board, (500, 120))
        self._die2.addTo(win)
        
        #adds a button to roll the dice
        self._button = Rectangle(110, 50, (350, 120))
        self._button.setFillColor('orange')
        win.add(self._button)
        self._button.addHandler(self)
        self._rollText = Text("Roll", (350, 130), 30)
        win.add(self._rollText)
        self._rollText.addHandler(self)
        
        self._value = 0
        self._current = 0
        self._doubles = 0
        self._doublesCond = False
        
        #creates the pawns used in this game
        for i in range(NUM):
            thisPawn = Pawn(self._board, PAWNCOLORS[i], i, 0, 1500)
            thisPawn.addTo(win)
            thisPawn.setDepth(i)
            PAWNS.append(thisPawn)
        PAWNS[self._current].highlight()
        
    
    def handleMousePress(self, event):
        #checks if the pawn is in jail
        if PAWNS[self._current].getJailtime() != 0:
            if PAWNS[self._current].getMoney() >= 50:
                x = input("You're in jail! Pay $50 to get out this roll? "
                          "(Type Y or N)")
                if x == "Y":
                    PAWNS[self._current].changeMoney(-50)
                    self._board.showMoney(PAWNS[self._current].getIdent(),
                                          PAWNS[self._current].getMoney())
                else:
                    self._doublesCond = True
            else:
                self._doublesCond = True
        
        #rolls the dice
        self._die1.roll()
        self._die2.roll()
        self._value = self._die1.getValue() + self._die2.getValue()
        
        #checks if the pawn is in rolling from jail, else rolls normally
        if self._doublesCond:
            if self._die1.getValue() == self._die2.getValue():
                PAWNS[self._current].move(self._value)
                PAWNS[self._current].zeroJailtime()
                self._doublesCond = False
                self._doubles = 0
                self.changeTurn()
            else:
                PAWNS[self._current].subtractJailtime()
                if PAWNS[self._current].getJailtime() == 0:
                    PAWNS[self._current].changeMoney(-50)
                    PAWNS[self._current].move(self._value)
                self._doublesCond = False
                self.changeTurn()
        else:
            PAWNS[self._current].move(self._value)
    
    def handleMouseRelease(self, event):
        PAWNS[self._current].actions()
        
        #checks if there were doubles or not
        if self._die1.getValue() != self._die2.getValue():
            self._doubles = 0
            self.changeTurn()
        else:
            if PAWNS[self._current].getJailtime() == 0:
                self._doubles += 1
            else:
                self.changeTurn()
        PAWNS[self._current].zeroJailtime()
        
        #moves the pawn to jail if they rolled three doubles in a row
        if self._doubles == 3:
            PAWNS[self._current].moveTo(10)
            PAWNS[self._current].goToJail()
            self.changeTurn()
        
        #makes the player lose if they have negative money
        if PAWNS[self._current].getMoney() < 0:
            PAWNS[self._current].lose()
            PAWNS[self._current] = None
    
    def changeTurn(self):
        """Changes the current player"""
        PAWNS[self._current].dehighlight()
        self._current += 1
        self._current = self._current % NUM
        if self._current == 0:
            self._board.nextTurn()
        PAWNS[self._current].highlight()
        self._board.showMoney(self._current, PAWNS[self._current].getMoney())

def main(win):
    """runs the program"""
    _ = Controller(win)
    

StartGraphicsSystem(main)


























