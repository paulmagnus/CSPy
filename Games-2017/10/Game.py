"""
--------------------------------------------------------------------------------
********************************************************************************
* Project 6                                                                    *
* Game.py                                                                      *
* Author:       Donald Holley                                                  *
* Date:         05/01/2017                                                     *
*                                                                              *
* Description:  This project is supposed to mimic the game 'Monopoly' as       *
* closely as possible.                                                         *
*                                                                              *
********************************************************************************
"""

import random
from cs110graphics import *

class Die(EventHandler):
    """Class for making each individual die"""
    SIDES = 6
    # POSITIONS is for the positions of each black dot on a die
    POSITIONS = [0,
                 [(0, 0), 0, 0, 0, 0, 0],
                 [(-.25, .25), (.25, -.25), 0, 0, 0, 0],
                 [(-.25, .25), (0, 0), (.25, -.25), 0, 0, 0],
                 [(-.25, -.25), (-.25, .25), (.25, -.25), 
                  (.25, .25), 0, 0],
                 [(-.25, -.25), (-.25, .25), (.25, -.25), 
                  (.25, .25), (0, 0), 0],                  
                 [(-.25, -.25), (-.25, .25), (.25, -.25), 
                  (.25, .25), (-.25, 0), (.25, 0)]]
                   
    def __init__(self, center, board, width=25, bgcolor='white',
                 fgcolor='black'):
        """Creates the die as a square and each pip as a small black circle"""
        EventHandler.__init__(self)
        self._value = 1
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgcolor)
        self._square.setBorderColor('green')
        self._center = center
        self._square.setDepth(20)
        self._width = width
        self._board = board
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgcolor)
            pip.setDepth(20)
            self._pips.append(pip)
        self._square.addHandler(self)
        self._active = True
            
    def addTo(self, win):
        """Adds the die to a window"""
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)
            
    def remove(self, win):
        """Removes the die from a window"""
        win.remove(self._square)
        for pip in self._pips:
            win.remove(pip)
            
    def roll(self):
        """Gives the die a random value"""
        self._value = random.randrange(Die.SIDES) + 1
        self._update()
        
    def setValue(self, val):
        """Sets the value of the die to a specified number"""
        self._value = val
        
    def _update(self):
        """Updates the die's value after it has been rolled"""
        positions = Die.POSITIONS[self._value]
        cx, cy = self._center
        for i in range(len(positions)):
            if positions[i] == 0:
                self._pips[i].setDepth(25)
            else:
                self._pips[i].setDepth(15)
                dx, dy = positions[i]
                self._pips[i].moveTo((cx + dx * self._width,
                                      cy + dy * self._width))
    def getValue(self):
        """Returns the value of the die"""
        return self._value
        
    def activate(self):
        """Activates the die"""
        self._active = True
        self._square.setBorderColor('green')
        
    def deactivate(self):
        """Deactivates the die"""
        self._active = False
        self._square.setBorderColor('red')
        
    def getActive(self):
        """Returns if the die is active or not"""
        return self._active
        
    def handleMouseRelease(self, event):
        """Rolls the die if the mouse is released over the die"""
        self._board.reportDieClick()
        
class Cell:
    """Creates a single board space"""
    def __init__(self, center):
        """Creates 40 X 40 cell"""
        self._center = center
        self._square = Rectangle(30, 30, center)
        self._square.setDepth(101)
        
    def addTo(self, win):
        """Adds the space to the window"""
        win.add(self._square)
        
    def getCenter(self):
        """Returns the center of the spaces"""
        return self._center
        
    def setDepth(self, depth):
        """Set the depth of the cell to a specified value"""
        self._square.setDepth(depth)
                                   
class Board:
    """Class for making the game"""
    # This is the class where all the magic happens >.<
    # Some values that can be accessed outside of Board
    # POSITIONS is for each space on the board
    POSITIONS = [(150, 150), (204, 150), (240.5, 150), (277, 150),
                 (313.5, 150), (350, 150), (386.5, 150), (423, 150),
                 (459.5, 150), (496, 150), (550, 150), (550, 204),
                 (550, 240.5), (550, 277), (550, 313.5), (550, 350),
                 (550, 386.5), (550, 423), (550, 459.5), (550, 496),
                 (550, 550), (496, 550), (459.5, 550), (423, 550),
                 (386.5, 550), (350, 550), (313.5, 550), (277, 550),
                 (240.5, 550), (204, 550), (150, 550), (150, 496),
                 (150, 459.5), (150, 423), (150, 386.5), (150, 350),
                 (150, 313.5), (150, 277), (150, 240.5), (150, 204)]
    # PROPS holds a tuple for every street property, the first position is for
    # the graphical object that represents each property and the second position
    # is for which player owns it
    PROPS = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
             (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
             (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
    # Each position for teh street properties
    PROPPOS = [1, 3, 6, 8, 9, 11, 13, 14, 16, 18, 19, 21, 23, 24, 26, 27, 29,
               31, 32, 34, 37, 39]
    # PROPHOUSE is for keeping track of how many houses are on each property
    PROPHOUSE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0]
    # CELLS creates a box that houses and hotels can be dragged into to be used
    CELLS = []
    for space in POSITIONS:
        space = Cell(space)
        CELLS.append(space)
    # Variables below only for trading
    TRADEMODE = False
    OFFER = []
    REQUEST = []
    OFFERPRINT = []
    REQUESTPRINT = []
    def __init__(self, win):
        """Sets up the game"""
        self._win = win
        board = Image('http://cs.hamilton.edu/~dholley/images/monop.jpg',
                      (346, 346), 472, 472)
        board.setDepth(100)
        win.add(board)
        # add cells to window
        for cell in Board.CELLS:
            cell.addTo(win)
        # add buttons for ending turn, buying properties, etc.
        self._changeTurn = ChangeTurn(self)
        self._changeTurn.addTo(win)
        Buy(self).addTo(win)
        Pay(self).addTo(win)
        Trade(self).addTo(win)
        # community chest and chance objects and spaces
        self._ccSpaces = [2, 17, 33]
        self._cSpaces = [7, 22, 36]
        self._ccDeck = CommunityChestDeck()
        self._ccDeck.shuffle()
        self._ccCard = CommunityChest(self._ccDeck.deal(), (275, 275), self)
        self._ccCard.addTo(win)
        self._cDeck = ChanceDeck()
        self._cDeck.shuffle()
        self._cCard = Chance(self._cDeck.deal(), (425, 425), self)
        self._cCard.addTo(win)
        # positions for when a property is bought and moves to a plyaer's side
        # of the board
        self._baughtPos = [(450, 620), (620, 250), (40, 450), (250, 40)]
        self._numProps = [0, 0, 0, 0]
        # dice are added
        self._dieA = Die((330, 350), self)
        self._dieA.addTo(win)
        self._dieB = Die((370, 350), self)
        self._dieB.addTo(win)
        self._doub = 0
        # creates a deck of street properties and list for keeping track of each
        # color owned
        self._propDeck = PropertyDeck()
        self._colorOwned = [0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0]
        # railroads and attributes
        self._railPositions = [5, 15, 25, 35]
        self._numRails = [0, 0, 0, 0]
        self._railroads = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self._railNames = ['Reading Railroad', 'Pennsylvania Railroad',
                           'B. & O. Railroad', 'Short Line']
        # utilities and attributes
        self._utilPositions = [12, 28]
        self._numUtil = [0, 0, 0, 0]
        self._utilities = [(0, 0), (0, 0)]
        self._utilNames = ['Electric Company', 'Water Works']
        # add hotel and house
        House((550, 75), self).addTo(win)
        Hotel((530, 75), self).addTo(win)
        self._jailCard = [(400, 650), (650, 400), (50, 400), (400, 50)]
        # for trading
        self._player = None
        self._offer = Text('', (350, 90))
        self._request = Text('', (350, 105))
        win.add(self._offer)
        win.add(self._request)
        # pawns and wealth are added
        self._turn = Text("It's red's turn!", (350, 210))
        win.add(self._turn)
        self._pawns = []
        self._current = 0
        self._wealth = [1500, 1500, 1500, 1500]
        self._wealth0 = Money('Red: $', str(self._wealth[0]), 
                              (350, 650), self, 0)
        self._wealth0.addTo(win)
        self._wealth1 = Money('Blue: $', str(self._wealth[1]), 
                              (650, 350), self, 1)
        self._wealth1.addTo(win)
        self._wealth2 = Money('Green: $', str(self._wealth[2]),
                              (50, 350), self, 2)
        self._wealth2.addTo(win)
        self._wealth3 = Money('Yellow: $', str(self._wealth[3]),
                              (350, 50), self, 3)
        self._wealth3.addTo(win)
        # for starting the game with desired players
        players = self.getPlayers()
        if players == 2:
            for color, which in [('red', 0), ('blue', 1)]:
                thisPawn = Pawn(self, color, which, 0)
                thisPawn.addTo(win)
                self._pawns.append(thisPawn)
                self._wealth[2] = -1
                self._wealth[3] = -1
                self._wealth2.setText(' ')
                self._wealth3.setText(' ')
        if players == 3:
            for color, which in [('red', 0), ('blue', 1), ('green', 2)]:
                thisPawn = Pawn(self, color, which, 0)
                thisPawn.addTo(win)
                self._wealth[3] = -1
                self._wealth3.setText(' ')
                self._pawns.append(thisPawn)
        if players == 4:
            for color, which in [('red', 0), ('blue', 1),
                                 ('green', 2), ('yellow', 3)]:
                thisPawn = Pawn(self, color, which, 0)
                thisPawn.addTo(win)
                self._pawns.append(thisPawn)
        self.updatePawnLocations()
        self._pawns[0].highlight()
        
    def getPlayers(self):
        """Starts the game with desired number of players"""
        while True:
            try:
                val = int(input('How many players?\n(Enter 2, 3, or 4)'))
                if val == 2 or val == 3 or val == 4:
                    return val
            except ValueError:
                pass
        
    def reportPawnClick(self, ident):
        """Tells the board what to do when a pawn is clicked on"""
        if ident == self._current and not self._dieA.getActive():
            if not self._pawns[ident].getJailed():
                thePawn = self._pawns[ident]
                pos = thePawn.getPosition()
                pos = pos + self._dieA.getValue() + self._dieB.getValue()
                if pos > 39:
                    pos = pos % len(Board.POSITIONS)
                    self.addWealth(200, ident)
                thePawn.setPosition(pos)
                self._changeTurn.activate()
                self.updateWealth()
                self.updatePawnLocations()
                self._pawns[ident].deactivate()
                # checks to see if the pawn landed on chance, a tax space, etc
                self.checkSpace()
                self.checkRent()
                self.checkRent2()
                self.checkRent3()
                self.checkTax(self._pawns[ident].getPosition())
                # for when you roll doubles
                if self._dieA.getValue() == self._dieB.getValue():
                    # this prevents getting to roll again if you roll doubles
                    # and land on 'go to jail'
                    if not self._pawns[ident].getJailed():
                        self._dieA.activate()
                        self._dieB.activate()
                        self._changeTurn.deactivate()
            
    def reportDieClick(self):
        """Tells the board what to do when a die is clicked on"""
        if self._dieA.getActive():
            self._dieA.roll()
            self._dieB.roll()
            self._dieA.deactivate()
            self._dieB.deactivate()
            self._pawns[self._current].activate()
            self._pawns[self._current].jailTurn()
            if self._dieA.getValue() == self._dieB.getValue():
                # for if the player is in jail and rolls doubles
                if self._pawns[self._current].getJailed():
                    self._pawns[self._current].makeBail()
                self._doub += 1
            else:
                if self._pawns[self._current].getJailed():
                    self._changeTurn.activate()
                self._doub = 0
            if self._doub == 3:
                self._pawns[self._current].goToJail()
                
    def reportChanceClick(self):
        """Reports to the board when a chance card has been clicked"""
        card = self._cCard
        ok = Ok(self, self._win, card)
        ok.addTo(self._win)
        self._cDeck.append(self._cCard)
        self._cCard = Chance(self._cDeck.deal(), (425, 425), self)
        self._cCard.addTo(self._win)
        
    def getChanceEffect(self, effect):
        """Carries out a selected effect"""
        current = self._current
        pawn = self._pawns[current]
        pos = pawn.getPosition()
        if effect == 1:
            pawn.setPosition(0)
            self.addWealth(200, current)
        elif effect == 2:
            if pos > 24:
                self.addWealth(200, current)
            pawn.setPosition(24)
        elif effect == 3:
            if pos > 11:
                self.addWealth(200, current)
            pawn.setPosition(11)
        elif effect == 4:
            if pos < 12:
                pawn.setPosition(12)
            if pos > 12 and pos < 28:
                pawn.setPosition(28)
            if pos > 28:
                pawn.setPosition(12)
                self.addWealth(200, current)
        elif effect == 5:
            if pos < 5:
                pawn.setPosition(5)
            if pos > 5 and pos < 15:
                pawn.setPosition(15)
            if pos > 15 and pos < 25:
                pawn.setPosition(25)
            if pos > 25 and pos < 35:
                pawn.setPosition(35)
            if pos > 35:
                pawn.setPosition(5)
                self.addWealth(200, current)
        elif effect == 6:
            self.addWealth(50, current)
        elif effect == 7:
            GetOutFree(self._jailCard[current], pawn,
                       self._win).addTo(self._win)
        elif effect == 8:
            pawn.setPosition(pos - 3)
            self.checkTax(self._pawns[self._current].getPosition())
            self.checkSpace()
        elif effect == 9:
            pawn.goToJail()
        elif effect == 10:
            owed = 0
            for i in range(22):
                if Board.PROPS[i][1] == current:
                    if Board.PROPHOUSE[i] == 5:
                        owed += 100
                    if Board.PROPHOUSE[i] < 5:
                        owed += 25 * Board.PROPHOUSE[i]
            self.subtractWealth(owed, current)
        elif effect == 11:
            self.subtractWealth(15, current)
        elif effect == 12:
            if pos > 5:
                self.addWealth(200, current)
            pawn.setPosition(5)
        elif effect == 13:
            pawn.setPosition(39)
        elif effect == 14:
            self.subtractWealth(50 * len(self._pawns), current)
            for i in range(len(self._pawns)):
                self.addWealth(50, i)
        elif effect == 15:
            self.addWealth(150, current)
        elif effect == 16:
            self.addWealth(100, current)
        self.updateWealth()
        self.updatePawnLocations()
        if self._dieA.getValue() != self._dieB.getValue():
            self._changeTurn.activate()
        else:
            self._dieA.activate()
            self._dieB.activate()
            
    def reportCommunityClick(self):
        """Reports to the board when a community chest card has been clicked"""
        card = self._ccCard
        ok = Ok(self, self._win, card)
        ok.addTo(self._win)
        self._ccDeck.append(self._cCard)
        self._ccCard = CommunityChest(self._ccDeck.deal(), (275, 275), self)
        self._ccCard.addTo(self._win)
        
    def getCommunityEffect(self, effect):
        """Carries out a selected effect"""
        current = self._current
        pawn = self._pawns[current]
        if effect == 1:
            self.addWealth(200, current)
            pawn.setPosition(0)
        elif effect == 2:
            self.addWealth(200, current)
        elif effect == 3:
            self.subtractWealth(50, current)
        elif effect == 4:
            self.addWealth(50, current)
        elif effect == 5:
            GetOutFree(self._jailCard[current], pawn, 
                       self._win).addTo(self._win)
        elif effect == 6:
            pawn.goToJail()
        elif effect == 7:
            self.addWealth(50 * len(self._pawns), current)
            for i in range(len(self._pawns)):
                self.subtractWealth(50, i)
        elif effect == 8 or effect == 10 or effect == 16:
            self.addWealth(100, current)
        elif effect == 9:
            self.addWealth(20, current)
        elif effect == 11:
            self.subtractWealth(100, current)
        elif effect == 12:
            self.subtractWealth(150, current)
        elif effect == 13:
            self.subtractWealth(25, current)
        elif effect == 14:
            owed = 0
            for i in range(22):
                if Board.PROPS[i][1] == current:
                    if Board.PROPHOUSE[i] == 5:
                        owed += 115
                    elif Board.PROPHOUSE[i] < 5:
                        owed += 40 * Board.PROPHOUSE[i]
            self.subtractWealth(owed, current)
        elif effect == 15:
            self.addWealth(10, current)
        self.updateWealth()
        self.updatePawnLocations()
        if self._dieA.getValue != self._dieB.getValue():
            self._changeTurn.activate()
        else:
            self._dieA.activate()
            self._dieB.activate()
        
    def reportHouseClick(self, house):
        """Reports the board when a house been clicked"""
        current = self._current
        if house.getActive():
            for i in Board.PROPPOS:
                x = Board.PROPPOS.index(i)
                pos = Board.POSITIONS[i]
                if Board.PROPHOUSE[x] < 4 and self.haveAll(Board.PROPPOS[x]):
                    if not Board.PROPS[x][0].isMortgaged():
                        cx, cy = pos
                        dx, dy = house.getLocation()
                        if dx >= cx - 20 and dx <= cx + 20:
                            if dy >= cy - 20 and dy <= cy + 20:
                                off = Board.PROPHOUSE[x] * 5
                                if i < 10:
                                    house.moveTo((cx + 10 - off, cy + 40))
                                if i > 10 and i < 20:
                                    house.moveTo((cx - 40, cy + 10 - off))
                                if i > 20 and i < 30:
                                    house.moveTo((cx - 10 + off, cy - 40))
                                if i > 30:
                                    house.moveTo((cx + 40, cy - 10 + off))
                                self.subtractWealth(Board.PROPS\
                                [x][0].getHouseCost(), current)
                                self.updateWealth()
                                house.bindTo(x)
                                Board.PROPHOUSE[x] += 1
                                house.deactivate()
                                House((550, 75), self).addTo(self._win)
                                return
            house.moveTo((550, 75))
        else:
            house.remove(self._win)
            Board.PROPHOUSE[house.getBind()] -= 1
            self.addWealth(Board.PROPS[house.getBind()][0]\
            .getHouseCost(), current)
            self.updateWealth()
        
    def reportHotelClick(self, hotel):
        """reports to the board when a hotel has been clicked"""
        current = self._current
        if hotel.getActive():
            for i in Board.PROPPOS:
                x = Board.PROPPOS.index(i)
                pos = Board.POSITIONS[i]
                if Board.PROPHOUSE[x] == 4 and self.haveAll(Board.PROPPOS[x]):
                    cx, cy = pos
                    dx, dy = hotel.getLocation()
                    if dx >= cx - 20 and dx <= cx + 20 and\
                    dy >= cy - 20 and dy <= cy + 20:
                        if i < 10:
                            hotel.setPivot((cx, cy + 40))
                            hotel.rotate(90)
                            hotel.moveTo((cx, cy + 40))
                        if i > 10 and i < 20:
                            hotel.moveTo((cx - 40, cy))
                        if i > 20 and i < 30:
                            hotel.setPivot((cx, cy - 40))
                            hotel.rotate(90)
                            hotel.moveTo((cx, cy - 40))
                        if i > 30:
                            hotel.moveTo((cx + 40, cy))
                        self.subtractWealth(Board.PROPS\
                        [x][0].getHouseCost(), current)
                        self.updateWealth()
                        hotel.bindTo(x)
                        Board.PROPHOUSE[x] += 1
                        hotel.deactivate()
                        Hotel((530, 75), self).addTo(self._win)
                        return
            hotel.moveTo((530, 75))
        else:
            hotel.remove(self._win)
            Board.PROPHOUSE[hotel.getBind()] -= 1
            self.addWealth(Board.PROPS[hotel.getBind()][0]\
            .getHouseCost(), current)
            self.updateWealth()
        
    def changeTurn(self):
        """Changes to the next pawn's turn"""
        if self._changeTurn.getActive():
            while True:
                self.eliminatePlayer()
                self.getWinner()
                self._pawns[self._current].unhighlight()
                self._current = (self._current + 1) % len(self._pawns)
                self.updateTurn()
                self._dieA.activate()
                self._dieB.activate()
                self._pawns[self._current].activate()
                self._pawns[self._current].highlight()
                self._changeTurn.deactivate()
                if not self._pawns[self._current].getBankrupt():
                    return
                
    def updateTurn(self):
        """Updates the text on who's turn it is"""
        text = ''
        if self._current == 0:
            text = 'red'
        if self._current == 1:
            text = 'blue'
        if self._current == 2:
            text = 'green'
        if self._current == 3:
            text = 'yellow'
        self._turn.setText("It's " + text + "'s turn!")
            
    def updatePawnLocations(self):
        """Updates the location of the pawn"""
        offsets = [-1, 1, -1, 1]
        for i in range(len(self._pawns)):
            pos = self._pawns[i].getPosition()
            if pos == 30:
                self._pawns[i].goToJail()
                pos = 10
                self._dieA.deactivate()
                self._dieB.deactivate()
            theSpace = Board.CELLS[pos]
            if i < 2:
                self._pawns[i].moveTo(theSpace.getCenter())
                self._pawns[i].move(0, offsets[i] * 7)
            else:
                self._pawns[i].moveTo(theSpace.getCenter())
                self._pawns[i].move(offsets[i] * 7, 0)
            self._pawns[i].deactivate()
        
    def buyProperty(self):
        """Gives you the option to buy a property if you landed on one"""
        i = self._current
        if not self._pawns[i].getActive():
            for j in range(22):
                if Board.PROPS[j] == (0, 0):
                    if self._pawns[i].getPosition() == Board.PROPPOS[j]:
                        prop = Property((0, 0),
                                        self._propDeck.getAttributes(j)[0],
                                        self._propDeck.getAttributes(j)[1],
                                        self._propDeck.getAttributes(j)[2],
                                        self._propDeck.getAttributes(j)[3],
                                        self._propDeck.getAttributes(j)[4],
                                        self._propDeck.getAttributes(j)[5],
                                        self._propDeck.getAttributes(j)[6],
                                        self._propDeck.getAttributes(j)[7],
                                        self._propDeck.getAttributes(j)[8],
                                        self._propDeck.getAttributes(j)[9],
                                        self)
                        if prop.changePossesion(self._baughtPos[i],
                                                self._numProps[i]):
                            Board.PROPS[j] = (prop, i)
                            self._numProps[i] += 1
                            prop.setDepth(50 - self._numProps[i])
                            self.subtractWealth(prop.getPrice(), i)
                            self.updateWealth()
                            prop.addTo(self._win)
                            self.noteColor(prop, i)
                            
    def buyRailroad(self):
        """Gives you the option to buy a railroad if you landed on one"""
        i = self._current
        if not self._pawns[i].getActive():
            for j in range(4):
                if self._railroads[j] == (0, 0):
                    if self._pawns[i].getPosition() == self._railPositions[j]:
                        rail = Railroad((0, 0), self._railNames[j], self)
                        if rail.changePossesion(self._baughtPos[i],
                                                self._numProps[i]):
                            self._railroads[j] = (rail, i)
                            self._numProps[i] += 1
                            rail.setDepth(50 - self._numProps[i])
                            self.subtractWealth(200, i)
                            self.updateWealth()
                            rail.addTo(self._win)
                            self._numRails[i] += 1
                    
    def buyUtility(self):
        """Gives you the option to buy a utility if you landed on one"""
        i = self._current
        if not self._pawns[i].getActive():
            for j in range(2):
                if self._utilities[j] == (0, 0) and\
                self._pawns[i].getPosition() == self._utilPositions[j]:
                    util = Utility((0, 0), self._utilNames[j], self)
                    if util.changePossesion(self._baughtPos[i],
                                            self._numProps[i]):
                        self._utilities[j] = (util, i)
                        self._numProps[i] += 1
                        util.setDepth(50 - self._numProps[i])
                        self.subtractWealth(150, i)
                        self.updateWealth()
                        util.addTo(self._win)
                        self._numUtil[i] += 1
                        
    def mortgageProp(self, prop):
        """Either gives you the option to mortgage a property or pay it off"""
        if prop.isMortgaged():
            ans = input('Would you like to pay off ' + prop.getName() + '?\
            \n(Type y to pay off)')
            if ans == 'y':
                for i in range(22):
                    if prop == Board.PROPS[i][0]:
                        if self._current == Board.PROPS[i][1]:
                            prop.flip()
                            prop.payOff()
                            self.subtractWealth(prop.getPrice() / 2,
                                                self._current)
                            self.updateWealth()
        else:
            ind = Board.PROPS.index((prop, self._current))
            if Board.PROPHOUSE[ind] == 0:
                ans = input('Would you like to mortgage ' + \
                prop.getName() + '?\n(Type y to mortgage)')
                if ans == 'y':
                    for i in range(22):
                        if prop == Board.PROPS[i][0]:
                            if self._current == Board.PROPS[i][1]:
                                prop.flip()
                                prop.mortgage()
                                self.addWealth(prop.getPrice() / 2,
                                               self._current)
                                self.updateWealth()
                            
    def mortgageRail(self, rail):
        """Gives you the option to either mortgage a railroad or pay it off"""
        if rail.isMortgaged():
            ans = input('Would you like to pay off ' + rail.getName() + '?\
            \n(Type y to pay off)')
            if ans == 'y':
                for i in range(4):
                    if rail == self._railroads[i][0]:
                        if self._current == self._railroads[i][1]:
                            rail.flip()
                            rail.payOff()
                            self.subtractWealth(100, self._current)
                            self.updateWealth()
        else:
            ans = input('Would you like to mortgage ' + rail.getName() + '?\
            \n(Type y to mortgage)')
            if ans == 'y':
                for i in range(4):
                    if rail == self._railroads[i][0]:
                        if self._current == self._railroads[i][1]:
                            rail.flip()
                            rail.mortgage()
                            self.addWealth(100, self._current)
                            self.updateWealth()
                            
    def mortgageUtil(self, util):
        """Gives you the option to either mortgage a utility or pay it off"""
        if util.isMortgaged():
            ans = input('Would you like to pay off ' + util.getName() + '?\
            \n(Type y to pay off)')
            if ans == 'yes':
                for i in range(2):
                    if util == self._utilities[i][0]:
                        if self._current == self._utilities[i][1]:
                            util.flip()
                            util.payOff()
                            self.subtractWealth(75, self._current)
                            self.updateWealth()
        else:
            ans = input('Would you like to mortgage ' + util.getName()+ '?\
            \n(Type y to mortgage)')
            if ans == 'yes':
                for i in range(2):
                    if util == self._utilities[i][0]:
                        if self._current == self._utilities[i][1]:
                            util.flip()
                            util.mortgage()
                            self.addWealth(75, self._current)
                            self.updateWealth()
                        
    def noteColor(self, prop, ident):
        """Keeps track of the number of properties of each color each player
        has"""
        val = prop.getPrice()
        if val < 80:
            self._colorOwned[ident * 8 + 0] += 1
        elif val > 90 and val < 130:
            self._colorOwned[ident * 8 + 1] += 1
        elif val > 130 and val < 170:
            self._colorOwned[ident * 8 + 2] += 1
        elif val > 170 and val < 210:
            self._colorOwned[ident * 8 + 3] += 1
        elif val > 210 and val < 250:
            self._colorOwned[ident * 8 + 4] += 1
        elif val > 250 and val < 290:
            self._colorOwned[ident * 8 + 5] += 1
        elif val > 290 and val < 330:
            self._colorOwned[ident * 8 + 6] += 1
        else:
            self._colorOwned[ident * 8 + 7] += 1
            
    def haveAll(self, pos):
        """Returns True if a player has all of one color"""
        current = self._current
        ind = Board.PROPPOS.index(pos)
        if pos < 5:
            num = 0
        if pos > 5 and pos < 10:
            num = 1
        if pos > 10 and pos < 15:
            num = 2
        if pos > 15 and pos < 20:
            num = 3
        if pos > 20 and pos < 25:
            num = 4
        if pos > 25 and pos < 30:
            num = 5
        if pos > 30 and pos < 35:
            num = 6
        if pos > 35:
            num = 7
        if ind < 2 or ind > 19:
            if self._colorOwned[current * 8 + num] == 2:
                return True
        elif self._colorOwned[current * 8 + num] == 3:
            return True
        return False
        
    def checkTax(self, pos):
        """Checks to see if a pawn landed on a tax space"""
        if pos == 4:
            self.subtractWealth(200, self._current)
        if pos == 38:
            self.subtractWealth(100, self._current)
        self.updateWealth()
                        
    def checkRent(self):
        """Checks to see if a player needs to pay rent on a property"""
        i = self._current
        if not self._dieA.getActive() and not \
        self._pawns[self._current].getActive():
            for j in range(22):
                if self._pawns[i].getPosition() == Board.PROPPOS[j]:
                    if Board.PROPS[j] != (0, 0):
                        if Board.PROPS[j][1] != i:
                            self.subtractWealth(self.getOwed(Board.PROPS\
                                         [j][0], Board.PROPPOS[j]), i)
                            self.addWealth(self.getOwed(Board.PROPS[j][0],
                                                        Board.PROPPOS[j]),
                                           Board.PROPS[j][1])
                            self.updateWealth()
                            
    def checkRent2(self):
        """Checks to see if a player needs to pay rent on a railroad"""
        i = self._current
        if not self._dieA.getActive() and not\
        self._pawns[self._current].getActive():
            for j in range(4):
                if self._pawns[i].getPosition() == self._railPositions[j]:
                    if self._railroads[j] != (0, 0):
                        if self._railroads[j][1] != i:
                            self.subtractWealth(50 * self._numRails[i], i)
                            self.addWealth(50 * self._numRails[i],
                                           self._railroads[j][1])
                            self.updateWealth()
                        
    def checkRent3(self):
        """Checks to see if a player needs to pay rent on a utility"""
        i = self._current
        dieVal = self._dieA.getValue() + self._dieB.getValue()
        mult = 1.0
        if self._numUtil[i] > 1:
            mult = 2.5
        if not self._dieA.getActive() and not\
        self._pawns[self._current].getActive():
            for j in range(2):
                if self._pawns[i].getPosition() == self._utilPositions[j]:
                    if self._utilities[j] != (0, 0):
                        if self._utilities[j][1] != i:
                            self.subtractWealth(4 * mult * dieVal, i)
                            self.addWealth(4 * mult * dieVal,
                                           self._utilities[j][1])
                            self.updateWealth()
                            
    def getOwed(self, prop, pos):
        """Returns the amount of rent owed on a property"""
        ind = Board.PROPPOS.index(pos)
        if Board.PROPHOUSE[ind] == 0:
            if self.haveAll(pos):
                return prop.getRent() * 2
            else:
                return prop.getRent()
        elif Board.PROPHOUSE[ind] == 1:
            return prop.getRentHouse()
        elif Board.PROPHOUSE[ind] == 2:
            return prop.getRentTwoHouse()
        elif Board.PROPHOUSE[ind] == 3:
            return prop.getRentThreeHouse()
        elif Board.PROPHOUSE[ind] == 4:
            return prop.getRentFourHouse()
        elif Board.PROPHOUSE[ind] == 5:
            return prop.getRentHotel()
                
    def checkSpace(self):
        """Checks what the pawn landed on"""
        i = self._current
        for j in range(3):
            if self._pawns[i].getPosition() == self._ccSpaces[j]:
                self._ccCard.activate()
                self._changeTurn.deactivate()
            if self._pawns[i].getPosition() == self._cSpaces[j]:
                self._cCard.activate()
                self._changeTurn.deactivate()
                
    def getPlayerWealth(self, ident):
        """Returns the wealth of a player"""
        return self._wealth[ident]
        
    def addWealth(self, value, ident):
        """Transfers one player's money to another"""
        self._wealth[ident] += value
        
    def subtractWealth(self, value, ident):
        """Removes money to pay for a property"""
        self._wealth[ident] -= value
        
    def updateWealth(self):
        """Updates the wealth displayed on the window"""
        self._wealth0.setText('Red: $' + str(self._wealth[0]))
        self._wealth1.setText('Blue: $' + str(self._wealth[1]))
        if len(self._pawns) > 2:
            self._wealth2.setText('Green: $' + str(self._wealth[2]))
        if len(self._pawns) > 3:
            self._wealth3.setText('Yellow: $' + str(self._wealth[3]))
            
    def reportPayClick(self):
        """Pays bail if the player can afford it"""
        if self._pawns[self._current].getJailed() and self._dieA.getActive():
            self._pawns[self._current].makeBail()
            self.subtractWealth(50, self._current)
            self.updateWealth()
            
    def eliminatePlayer(self):
        """Eliminates a player from the game"""
        if self._wealth[self._current] < 0:
            self._wealth[self._current] = -1
            self.updateWealth()
            for i in range(22):
                if Board.PROPS[i][1] == self._current:
                    if Board.PROPS[i][0] != 0:
                        Board.PROPS[i][0].remove(self._win)
                        Board.PROPS[i] = (0, 0)
            for i in range(4):
                if self._railroads[i][1] == self._current:
                    if self._railroads[i][0] != 0:
                        self._railroads[i][0].remove(self._win)
                        self._railroads[i] = (0, 0)
            for i in range(2):
                if self._utilities[i][1] == self._current:
                    if self._utilities[i][0] != 0:
                        self._utilities[i][0].remove(self._win)
                        self._utilities[i] = (0, 0)
            self._pawns[self._current].bankrupt()
                                
    def getWinner(self):
        """Ends the game if there is a winner"""
        colors = ['red', 'blue', 'green', 'yellow']
        if self._wealth.count(-1) == 3:
            winner = colors[self._wealth.index(max(self._wealth))]
            self._dieA.remove(self._win)
            self._dieB.remove(self._win)
            text = Text(winner + ' wins!', (350, 350))
            self._win.add(text)
            
    def reportTradeClick(self):
        """Changes the board to trade mode"""
        if not self._pawns[self._current].getActive():
            if not self._dieA.getActive():
                Board.TRADEMODE = True
                self._changeTurn.deactivate()
                self._player = input('Which player would you like to\
                trade with?\n(Type r, b, g, or y)')
                if self._player == 'r':
                    self._player = 0
                if self._player == 'b':
                    self._player = 1
                if self._player == 'g':
                    self._player = 2
                if self._player == 'y':
                    self._player = 3
                self.updateTrade()
            
    def addProp(self, prop):
        """Adds a property to the trade"""
        for i in range(22):
            if Board.PROPS[i][0] == prop:
                if Board.PROPS[i][1] == self._current:
                    Board.OFFER.append(prop)
                    Board.OFFERPRINT.append(prop.getName())
                    prop.addTrade()
                if Board.PROPS[i][1] == self._player:
                    Board.REQUEST.append(prop)
                    Board.REQUESTPRINT.append(prop.getName())
                    prop.addTrade()
        for i in range(4):
            if self._railroads[i][0] == prop:
                if self._railroads[i][1] == self._current:
                    Board.OFFER.append(prop)
                    Board.OFFERPRINT.append(self._railNames[i])
                if self._railroads[i][1] == self._player:
                    Board.REQUEST.append(prop)
                    Board.REQUESTPRINT.append(self._railNames[i])
        for i in range(2):
            if self._utilities[i][0] == prop:
                if self._utilities[i][1] == self._current:
                    Board.OFFER.append(prop)
                    Board.OFFERPRINT.append(self._utilNames[i])
                if self._utilities[i][1] == self._player:
                    Board.REQUEST.append(prop)
                    Board.REQUESTPRINT.append(self._utilNames[i])
        self.updateTrade()
        
    def removeProp(self, prop):
        """Removes a property from the trade"""
        for item in Board.OFFER:
            if item == prop:
                Board.OFFER.remove(prop)
                Board.OFFERPRINT.remove(prop.getName())
                prop.removeTrade()
        for item in Board.REQUEST:
            if item == prop:
                Board.REQUEST.remove(prop)
                Board.REQUESTPRINT.remove(prop.getName())
                prop.removeTrade()
        self.updateTrade()
            
    def addMoney(self, money):
        """Adds money to the trade"""
        val = input('How much?')
        if money.getPlayer() == self._current:
            Board.OFFER.append(int(val))
            Board.OFFERPRINT.append(val)
        if money.getPlayer() == self._player:
            Board.REQUEST.append(int(val))
            Board.REQUESTPRINT.append(val)
        self.updateTrade()
        
    def trade(self):
        """Swaps possesion of the items in the trade"""
        if input('Accept trade?\n(Type y to accept)') == 'y':
            for item in Board.OFFER:
                if isinstance(item, int):
                    self.addWealth(item, self._player)
                    self.subtractWealth(item, self._current)
                else:
                    for prop in Board.PROPS:
                        if prop[0] == item:
                            prop[1] = self._player
                    for rail in self._railroads:
                        if rail[0] == item:
                            rail[1] = self._player
                    for util in self._utilities:
                        if util[0] == item:
                            util[1] = self._player
            for item in Board.REQUEST:
                if isinstance(item, int):
                    self.addWealth(item, self._current)
                    self.subtractWealth(item, self._player)
                else:
                    for prop in Board.PROPS:
                        if prop[0] == item:
                            prop[1] = self._current
                    for rail in self._railroads:
                        if rail[0] == item:
                            rail[1] = self._current
                    for util in self._utilities:
                        if util[0] == item:
                            util[1] = self._current
            self.reorder(self._current)
            self.reorder(self._player)
            self.updateWealth()
        offer = []
        request = []
        for item in Board.OFFER:
            if not isinstance(item, int):
                offer.append(item)
        for item in Board.REQUEST:
            if not isinstance(item, int):
                request.append(item)
        for item in offer:
            item.removeTrade()
        for item in request:
            item.removeTrade()
        Board.OFFER = []
        Board.REQUEST = []
        Board.OFFERPRINT = []
        Board.REQUESTPRINT = []
        self._changeTurn.activate()
        self.hideTrade()
        Board.TRADEMODE = False    
        
    def reorder(self, ident):
        """Re-sorts the properties and recounts related variables"""
        cx, cy = self._baughtPos[ident]
        self._numProps[ident] = 0
        for i in range(8):
            self._colorOwned[ident * 8 + i] = 0
        for i in range(22):
            num = self._numProps[ident]
            if Board.PROPS[i][0] != 0 and Board.PROPS[i][1] == ident:
                if num < 6:
                    Board.PROPS[i][0].moveTo((cx, cy + num * 8))
                else:
                    Board.PROPS[i][0].moveTo((cx + 30, cy + (num - 6) * 8))
                Board.PROPS[i][0].setDepth(50 - self._numProps[ident])
                self._numProps[ident] += 1
                self.noteColor(Board.PROPS[i][0], ident)
        for i in range(4):
            num = self._numProps[ident]
            if self._railroads[i][0] != 0 and self._railroads[i][1] == ident:
                if num < 6:
                    self._railroads[i][0].moveTo((cx, cy + num * 8))
                else:
                    self._railroads[i][0].moveTo((cx + 30, cy + (num - 6) * 8))
                self._railroads[i][0].setDepth(50 - self._numProps[ident])
                self._numProps[ident] += 1
        for i in range(2):
            num = self._numProps[ident]
            if self._utilities[i][0] != 0 and self._utilities[i][1] == ident:
                if num < 6:
                    self._utilities[i][0].moveTo((cx, cy + num * 8))
                else:
                    self._utilities[i][0].moveTo((cx + 30, cy + (num - 6) * 8))
                self._utilities[i][0].setDepth(50 - self._numProps[ident])
                self._numProps[ident] += 1
                
    def updateTrade(self):
        """Updates the lists of items being traded"""
        self._offer.setText('Offer: ' + str(Board.OFFERPRINT))
        self._request.setText('Request: ' + str(Board.REQUESTPRINT))
        
    def hideTrade(self):
        """Hides the trade lists"""
        self._offer.setText('')
        self._request.setText('')
            
class Trade(EventHandler):
    """Class for initiating trade"""
    def __init__(self, board):
        """Creates a button"""
        EventHandler.__init__(self)
        self._board = board
        self._button = Rectangle(50, 20, (620, 170))
        self._button.setFillColor('yellow')
        self._text = Text('Trade', (620, 170))
        self._button.addHandler(self)
        self._text.addHandler(self)
        
    def addTo(self, win):
        """Adds the button to a window"""
        win.add(self._button)
        win.add(self._text)
        
    def handleMouseRelease(self, event):
        """Reports the the board when clicked"""
        if Board.TRADEMODE:
            self._board.trade()
        else:
            self._board.reportTradeClick()
            
class ChangeTurn(EventHandler):
    """Creates a button for ending your turn"""
    def __init__(self, board):
        EventHandler.__init__(self)
        self._board = board
        self._button = Rectangle(50, 20, (620, 130))
        self._button.setFillColor('pink')
        self._text = Text('End Turn', (620, 130))
        self._button.addHandler(self)
        self._text.addHandler(self)
        self._active = False
        
    def addTo(self, win):
        """Adds the button to a window"""
        win.add(self._button)
        win.add(self._text)
        
    def activate(self):
        """Activates the button"""
        self._active = True
        
    def deactivate(self):
        """Deactivates the button"""
        self._active = False
        
    def getActive(self):
        """Returns if the button is active or not"""
        return self._active
        
    def handleMouseRelease(self, event):
        """Changes the turn when clicked on"""
        self._board.changeTurn()
        
class Money(EventHandler):
    """Class for displaying each player's wealth"""
    def __init__(self, text, val, center, board, player):
        """Creates the text for wealth"""
        EventHandler.__init__(self)
        self._board = board
        self._player = player
        self._text = Text(text + str(val), center)
        self._text.addHandler(self)
        
    def addTo(self, win):
        """Adds the text to a window"""
        win.add(self._text)
        
    def setText(self, text):
        """Sets the text to something new"""
        self._text.setText(text)
        
    def getPlayer(self):
        """Returns the player assigned to the wealth"""
        return self._player
        
    def handleMouseRelease(self, event):
        """Reports to the board when clicked"""
        if Board.TRADEMODE:
            self._board.addMoney(self)
            
class Buy(EventHandler):
    """Creates a button that you can press to buy a property"""
    def __init__(self, board):
        """Creates the button as an event handler"""
        EventHandler.__init__(self)
        self._board = board
        self._button = Rectangle(50, 20, (620, 150))
        self._button.setFillColor('pink')
        self._text = Text('Buy', (620, 150))
        self._button.addHandler(self)
        self._text.addHandler(self)
        
    def addTo(self, win):
        """Adds the button to a window"""
        win.add(self._button)
        win.add(self._text)
        
    def handleMouseRelease(self, event):
        """Checks if you can and gives you the option to buy a property"""
        self._board.buyProperty()
        self._board.buyRailroad()
        self._board.buyUtility()
        
class Ok(EventHandler):
    """Class the creates a button for after you have read what is on a chance
    or community chest card"""
    def __init__(self, board, win, card):
        """Creats the button as an event handler"""
        EventHandler.__init__(self)
        self._win = win
        self._card = card
        self._win = win
        self._button = Circle(15, (350, 450))
        self._button.setFillColor('blue')
        self._text = Text('OK', (350, 450))
        self._board = board
        self._button.addHandler(self)
        self._text.addHandler(self)
        
    def addTo(self, win):
        """Adds the button to a window"""
        win.add(self._button)
        win.add(self._text)
        
    def handleMouseRelease(self, event):
        """Gets rid of the text and adds a new card to the window when 
        clicked"""
        self._card.setText(' ')
        self._card.remove(self._win)
        self._win.remove(self._button)
        self._text.setText(' ')
        if self._card.getType() == 'Chance':
            self._board.getChanceEffect(self._card.getEffect())
        if self._card.getType() == 'Community':
            self._board.getCommunityEffect(self._card.getEffect())
            
class Pay(EventHandler):
    """Class that creates a button for paying to get out of jail"""
    def __init__(self, board):
        """Creates a button for paying to get out of jail"""
        EventHandler.__init__(self)
        self._board = board
        self._button = Circle(15, (580, 150))
        self._button.setFillColor('red')
        self._text = Text('Pay', (580, 150))
        self._button.addHandler(self)
        self._text.addHandler(self)
        
    def addTo(self, win):
        """Adds the button to a window"""
        win.add(self._button)
        win.add(self._text)
        
    def handleMouseRelease(self, event):
        """Reports to the board when the button is clicked"""
        self._board.reportPayClick()
        
class GetOutFree(EventHandler):
    """Class for creating a get out of jail free card"""
    def __init__(self, center, pawn, win, color='orange'):
        """Creates the card"""
        EventHandler.__init__(self)
        self._center = center
        self._win = win
        self._pawn = pawn
        self._card = Rectangle(60, 35, center)
        self._card.setFillColor(color)
        self._text = Text("Get Out of Jail Free!", center, 6)
        self._card.addHandler(self)
        self._text.addHandler(self)
        
    def addTo(self, win):
        """Adds the card to a window"""
        win.add(self._card)
        win.add(self._text)
        
    def remove(self, win):
        """Removes the card from a window"""
        win.remove(self._card)
        self._text.setText(' ')
        
    def handleMouseRelease(self, event):
        """Reports to the board and removes itself from the window 
        when clicked"""
        if self._pawn.getJailed():
            self._pawn.makeBail()
            self.remove(self._win)
        
class Pawn(EventHandler):
    """Class for making each pawn"""
    def __init__(self, board, color, ident, position):
        """Creates the pawn"""
        EventHandler.__init__(self)
        self._board = board
        self._ident = ident
        self._position = position
        self._pawn = Rectangle(10, 10, (200, 200))
        self._pawn.setFillColor(color)
        self._pawn.addHandler(self)
        self._ccSpaces = [2, 17, 33]
        self._active = False
        self._bankrupt = False
        self._jailCount = 0
        self._jailed = False
        
    def addTo(self, win):
        """Adds the pawn to a window"""
        win.add(self._pawn)
    
    def handleMouseRelease(self, event):
        """Reports to the board after the mouse is clicked over the pawn"""
        if self._active:
            self._board.reportPawnClick(self._ident)
    
    def getPosition(self):
        """Returns the pawn's position"""
        return self._position
    
    def setPosition(self, pos):
        """Changes the pawn's position"""
        self._position = pos
        
    def moveTo(self, location):
        """Moves the pawn to a specified location"""
        self._pawn.moveTo(location)
        
    def move(self, dx, dy):
        """Moves the pawn by a given dx and dy"""
        self._pawn.move(dx, dy)
        
    def highlight(self, color='pink'):
        """Changes the border color of the pawn"""
        self._pawn.setBorderColor(color)
        
    def unhighlight(self):
        """Changes the border back to black"""
        self._pawn.setBorderColor('black')
        
    def getActive(self):
        """"Returns True if active and False if not active"""
        return self._active
        
    def activate(self):
        """Activates the pawn"""
        self._active = True
        
    def deactivate(self):
        """Deactivates the pawn"""
        self._active = False
        
    def bankrupt(self):
        """Makes the pawn bankrupt"""
        self._bankrupt = True
        self._pawn.setFillColor('black')
        
    def getBankrupt(self):
        """Returns if pawn is bankrupt or not"""
        return self._bankrupt
        
    def goToJail(self):
        """Sends the pawn to jail"""
        self._position = 10
        self.jailed()
        
    def jailed(self):
        """Sets the turn counter for going to jail"""
        self._jailCount = 3
        self._jailed = True
        self._pawn.setBorderWidth(5)
        
    def jailTurn(self):
        """Advances the jail counter"""
        if self._jailCount > 0:
            self.deactivate()
            self._jailCount -= 1
            if self._jailCount == 0:
                self.makeBail()
                self._board.subtractWealth(50, self._ident)
                self._board.updateWealth()
                
    def getJailed(self):
        """Returns if the pawn is in jail or not"""
        return self._jailed
        
    def makeBail(self):
        """Frees the pawn from jail"""
        self._jailed = False
        self._jailCount = 0
        self._pawn.setBorderWidth(1)
        self.activate()

class CommunityChestDeck:
    """Creates a non-graphical deck of community chest cards"""
    def __init__(self):
        """Creates a deck of 16 different phrases"""
        self._deck = [('Advance to Go! (Collect $200)', 1),
                      ('Bank error in your favor - Collect $200', 2),
                      ("Doctor's fees - Pay $50", 3),
                      ('From sale of stock you get $50', 4),
                      ('Get Out of Jail Free!', 5),
                      ('Go to Jail-Do not pass Go-Do not collect $200', 6),
                      ('Grand Opera Night-Collect $50 from every player for\
                      opening night seats', 7),
                      ('Xmas Fund matures - Collect $100', 8),
                      ('Income tax refund-Collect $20', 9),
                      ('Life insurance matures-Collect $100', 10),
                      ('Pay hospital fees of $100', 11),
                      ('Pay school tax of $150', 12),
                      ('Receive $25 consultancy fee', 13),
                      ('You are assessed for street repairs-$40 per house-$115\
                      per hotel', 14),
                      ('You have won second prize in a beauty contest-Collect\
                      $10', 15),
                      ('You inherit $100', 16)] 
        
    def getText(self, number):
        """Returns one phrase from the list"""
        return self._deck[number]
        
    def shuffle(self):
        """Shuffles the deck"""
        deckCopy = []
        for _ in range(16):
            newCard = self._deck[random.randrange(len(self._deck))]
            deckCopy.append(newCard)
            self._deck.remove(newCard)
        self._deck = deckCopy
        return self._deck
        
    def append(self, obj):
        """Adds a phrase to the deck"""
        self._deck.append(obj)
        
    def deal(self):
        """Deals and removes one card from the deck"""
        card = self._deck[0]
        self._deck.remove(card)
        return card

class CommunityChest(EventHandler):
    """Class for creating each individual card in the community chest deck"""
    def __init__(self, text, center, board):
        """Creates an individual card"""
        EventHandler.__init__(self)
        self._center = center
        self._text = text
        self._board = board
        self._card = Rectangle(60, 35, center)
        self._card.setFillColor('yellow')
        self._card.rotate(-45)
        self._card.setPivot(center)
        self._cardText = Text(' ', (350, 225))
        self._card.addHandler(self)
        self._active = False
        
    def addTo(self, win):
        """Adds the card to a window"""
        win.add(self._card)
        win.add(self._cardText)
        
    def remove(self, win):
        """Removes the card from a window"""
        win.remove(self._card)
        
    def move(self, dx, dy):
        """Moves the card by a given dx and dy"""
        self._card.move(dx, dy)
        
    def moveTo(self, point):
        """Moves the card to a specified point"""
        self._card.moveTo(point)
        self._cardText.moveTo(point)
        
    def rotate(self, degrees):
        """Rotates the card a specific degrees"""
        self._card.rotate(degrees)
        
    def setDepth(self, depth):
        """Sets the card's depth to a specified value"""
        self._card.setDepth(depth)
        
    def setText(self, text):
        """Makes the text reappear"""
        self._cardText.setText(text)
            
    def showText(self):
        """Reveals the text on the card"""
        self._cardText.setText(self._text[0])
        
    def getEffect(self):
        """Returns the effect number of the card"""
        return self._text[1]
        
    def getType(self):
        """Returns the type of the card"""
        return 'Community'
        
    def activate(self):
        """Activates the card"""
        self._active = True
        self._card.setBorderColor('green')
        
    def deactivate(self):
        """Deactivates the card"""
        self._active = False
        self._card.setBorderColor('black')
        
    def handleMouseRelease(self, event):
        """Shows the text when the mouse is relaeased the card"""
        if self._active:
            self.showText()
            self._board.reportCommunityClick()
            
class ChanceDeck:
    """Class for creating a non-graphical representation of a chance deck"""
    def __init__(self):
        """Creates a deck of 16 different phrases"""
        self._deck = [('Advance to Go! (Collect $200)', 1),
                      ('Advance to Illinois Avenue-If you pass Go, collect\
                      $200', 2),
                      ('Advance to St. Charles Place-If you pass Go collect\
                      $200', 3),
                      ('Advance token to nearest Utility.', 4),
                      ('Advance token to the nearest Railroad.', 5),
                      ('Bank pays you dividend of $50', 6),
                      ('Get Out of Jail Free!', 7), ('Go Back 3 Spaces', 8),
                      ('Go to Jail-Do not pass Go-Do not collect $200', 9),
                      ('Make general repairs on all your property-For each\
                      house pay $25-For each hotel $100', 10),
                      ('Pay poor tax of $15', 11),
                      ('Take a trip to Reading Railroad-If you pass Go,\
                      collect $200', 12),
                      ('Take a walk on the Boardwalk-Advance token to\
                      Boardwalk', 13),
                      ('You have been elected Chairman of the Board - Pay each\
                      player $50', 14),
                      ('Your building loan matures-Collect $150', 15),
                      ('You have won a crossword competition-Collect $100', 16)]
        
    def getText(self, number):
        """Returns one phrase from the list"""
        return self._deck[number]
        
    def shuffle(self):
        """Shuffles the deck"""
        deckCopy = []
        for _ in range(16):
            newCard = self._deck[random.randrange(len(self._deck))]
            deckCopy.append(newCard)
            self._deck.remove(newCard)
        self._deck = deckCopy
        
    def append(self, obj):
        """Adds a phrase to the deck"""
        self._deck.append(obj)
        
    def deal(self):
        """Deals and removes one card from the deck"""
        card = self._deck[0]
        self._deck.remove(card)
        return card
    
class Chance(EventHandler):
    """Class for creating each individual card in the chance deck"""
    def __init__(self, text, center, board):
        """Creates an individual card"""
        EventHandler.__init__(self)
        self._center = center
        self._text = text
        self._board = board
        self._card = Rectangle(60, 35, center)
        self._card.setFillColor('orange')
        self._card.rotate(-45)
        self._card.setPivot(center)
        self._cardText = Text(' ', (350, 225))
        self._card.addHandler(self)
        self._active = False
        
    def addTo(self, win):
        """Adds the card to a window"""
        win.add(self._card)
        win.add(self._cardText)
        
    def remove(self, win):
        """Removes the card from a window"""
        win.remove(self._card)
        
    def move(self, dx, dy):
        """Moves the card by a given dx and dy"""
        self._card.move(dx, dy)
        
    def moveTo(self, point):
        """Moves the card to a specified point"""
        self._card.moveTo(point)
        self._cardText.moveTo(point)
        
    def rotate(self, degrees):
        """Rotates the card a specific degrees"""
        self._card.rotate(degrees)
        
    def setDepth(self, depth):
        """Sets the card's depth to a specified value"""
        self._card.setDepth(depth)
        
    def setText(self, text):
        """Makes the text reappear"""
        self._cardText.setText(text)
            
    def showText(self):
        """Reveals the text on the card"""
        self._cardText.setText(self._text[0])
        
    def getEffect(self):
        """Returns the effect number of the card"""
        return self._text[1]
        
    def activate(self):
        """Activates the card"""
        self._active = True
        self._card.setBorderColor('green')
        
    def deactivate(self):
        """Deactivates the card"""
        self._active = False
        self._card.setBorderColor('black')
    
    def getType(self):
        """Returns the card Type"""
        return 'Chance'
        
    def handleMouseRelease(self, event):
        """Shows the text when the mouse is relaeased the card"""
        if self._active:
            self.showText()
            self._board.reportChanceClick()
    
class PropertyDeck:
    """Class that creates a non-graphical deck of the Street Properties"""
    def __init__(self):
        """Creates all of the values needed for each property"""
        self._properties = ['Mediterranean Avenue', 'Baltic Avenue',
                            'Oriental Avenue', 'Vermont Avenue',
                            'Connecticut Avenue', 'Saint Charles Place',
                            'States Avenue', 'Virginia Avenue',
                            'Saint James Place', 'Tennessee Avenue',
                            'New York Avenue', 'Kentucky Avenue',
                            'Indiana Avenue', 'Illinois Avenue',
                            'Atlantic Avenue', 'Ventnor Avenue',
                            'Marvin Gardens', 'Pacific Avenue',
                            'North Carolina Avenue', 'Pennsylvania Avenue',
                            'Park Place', 'Boardwalk']
        self._prices = [60, 60, 100, 100, 120, 140, 140, 160, 180, 180, 200,
                        220, 220, 240, 260, 260, 280, 300, 300, 320, 350, 400]
        self._rent = [2, 4, 6, 6, 8, 10, 10, 12, 14, 14, 16, 18, 18, 20, 22,
                      22, 24, 26, 26, 28, 35, 50]
        self._rentHouse = [10, 20, 30, 30, 40, 50, 50, 60, 70, 70, 80, 90,
                           90, 100, 110, 110, 120, 130, 130, 150, 175, 200]
        self._rentTwoHouse = [30, 60, 90, 90, 100, 150, 150, 180, 200, 200, 
                              220, 250, 250, 300, 330, 330, 360, 390, 390,
                              450, 500, 600]
        self._rentThreeHouse = [90, 180, 270, 270, 300, 450, 450, 500, 550,
                                550, 600, 700, 700, 750, 800, 800, 850, 900,
                                900, 1000, 1100, 1400]
        self._rentFourHouse = [160, 320, 400, 400, 450, 625, 625, 700, 750,
                               750, 800, 875, 875, 925, 975, 975, 1025, 1100,
                               1100, 1200, 1300, 1700]
        self._rentHotel = [250, 450, 550, 550, 600, 750, 750, 900, 950, 950,
                           1000, 1050, 1050, 1100, 1150, 1150, 1200, 1275,
                           1275, 1400, 1500, 2000]
        self._houseCost = [50, 50, 50, 50, 50, 100, 100, 100, 100, 100, 100,
                           150, 150, 150, 150, 150, 150, 200, 200, 200, 200,
                           200]
        self._color = ['purple', 'purple', 'lightblue', 'lightblue',
                       'lightblue', 'DeepPink', 'DeepPink',
                       'DeepPink', 'orange', 'orange', 'orange', 'red',
                       'red', 'red', 'yellow', 'yellow', 'yellow', 'green',
                       'green', 'green', 'blue', 'blue']
                       
    def getAttributes(self, number):
        """Returns all of one property's attributes in a list for creating
        a card"""
        return [self._properties[number], self._prices[number],
                self._rent[number], self._rentHouse[number],
                self._rentTwoHouse[number], self._rentThreeHouse[number],
                self._rentFourHouse[number], self._rentHotel[number],
                self._houseCost[number], self._color[number]]
                       
class Property(EventHandler):
    """Class for creating each street property"""
    def __init__(self, center, name, price, rent, rentHouse, rentTwoHouse, 
                 rentThreeHouse, rentFourHouse, rentHotel, houseCost,
                 color, board):
        """Creates an individual property"""
        EventHandler.__init__(self)
        width = 30
        self._width = width
        self._active = True
        self._mortgaged = False
        self._traded = False
        cx, cy = center
        self._title = name
        self._price = price
        self._rent = rent
        self._rentHouse = rentHouse
        self._rentTwoHouse = rentTwoHouse
        self._rentThreeHouse = rentThreeHouse
        self._rentFourHouse = rentFourHouse
        self._rentHotel = rentHotel
        self._houseCost = houseCost
        self._board = board
        self._base = Rectangle(width, width, center)
        self._base.setFillColor('white')
        self._base.setDepth(1)
        self._top = Rectangle(width * 9 / 10, width / 5,
                              (cx, cy - width * 7 / 20))
        self._top.setFillColor(color)
        self._top.setDepth(.5)
        self._name = Text(name, (cx, cy - width * 3 / 10), 3)
        self._name.setDepth(.5)
        self._frontDepth = .5
        self._backText = Text('-Mortgaged-', (cx, cy - 12), 3)
        self._backText.setDepth(1.5)
        self._backDepth = 1.5
        self._top.addHandler(self)
        self._name.addHandler(self)
        self._base.addHandler(self)
        
    def addTo(self, win):
        """Adds the property to a window"""
        win.add(self._base)
        win.add(self._top)
        win.add(self._name)
        win.add(self._backText)
        
    def remove(self, win):
        """Removes the property from a window"""
        win.remove(self._base)
        win.remove(self._top)
        self._name.setText(' ')
        self._backText.setText(' ')
            
    def flip(self):
        """Flips over the property"""
        self._top.setDepth(self._backDepth)
        self._name.setDepth(self._backDepth)
        self._backText.setDepth(self._frontDepth)
        self._frontDepth = self._top.getDepth()
        self._backDepth = self._backText.getDepth()
        
    def setDepth(self, depth):
        """Sets the depth of the property to a specified depth"""
        self._base.setDepth(depth)
        if self._frontDepth < self._backDepth:
            self._top.setDepth(depth - .5)
            self._name.setDepth(depth - .5)
            self._backText.setDepth(depth + .5)
            self._frontDepth = self._top.getDepth()
            self._backDepth = self._backText.getDepth()
        else:
            self._top.setDepth(depth + .5)
            self._name.setDepth(depth + .5)
            self._backText.setDepth(depth - .5)
            self._frontDepth = self._backText.getDepth()
            self._backDepth = self._top.getDepth()
                
    def moveTo(self, point):
        """Moves Property to a specified point"""
        cx, cy = point
        self._base.moveTo(point)
        self._top.moveTo((cx, cy - self._width * 7 / 20))
        self._name.moveTo((cx, cy - self._width * 3 / 10))
        self._backText.moveTo((cx, cy - 12))
        
    def getName(self):
        """Returns the name of the property"""
        return self._title
        
    def getPrice(self):
        """Returns the price of a property"""
        return self._price
    
    def getRent(self):
        """Returns the rent of the property"""
        return self._rent
        
    def getRentHouse(self):
        """Returns the rent of the property with one house"""
        return self._rentHouse
        
    def getRentTwoHouse(self):
        """Returns the rent of the property with two houses"""
        return self._rentTwoHouse
        
    def getRentThreeHouse(self):
        """Retruns the rent of the property with three houses"""
        return self._rentThreeHouse
        
    def getRentFourHouse(self):
        """Returns the rent of the property with four houses"""
        return self._rentFourHouse
        
    def getRentHotel(self):
        """Returns the rent of the property with a hotel"""
        return self._rentHotel
        
    def getHouseCost(self):
        """Returns the cost to put an additional house on the property"""
        return self._houseCost
        
    def getActive(self):
        """Returns if the property is active or not"""
        return self._active
        
    def deactivate(self):
        """"Takes the property off the market"""
        self._active = False
        
    def mortgage(self):
        """Mortgages the property"""
        self._mortgaged = True
        
    def payOff(self):
        """Pays off the property"""
        self._mortgaged = False
        
    def isMortgaged(self):
        """Returns if the property is mortgaged or not"""
        return self._mortgaged
        
    def addTrade(self):
        """Marks the property as traded"""
        self._traded = True
        
    def removeTrade(self):
        """Marks the property as not traded"""
        self._traded = False
            
    def changePossesion(self, point, num):
        """Gives you the option to buy a property"""
        cx, cy = point
        if self._active:
            while True:
                try:
                    buy = input('Would you like to buy ' + self._title + '?\
                    \n(Type y or n)')
                    if buy == 'y':
                        if num < 6:
                            self.moveTo((cx, cy + num * 8))
                        else:
                            self.moveTo((cx + 30, cy + (num - 6) * 8))
                        self.deactivate()
                        return True
                    if buy == 'n':
                        return
                except ValueError:
                    pass
                
    def handleMouseRelease(self, event):
        if Board.TRADEMODE:
            if self._traded:
                self._board.removeProp(self)
            else:
                self._board.addProp(self)
        else:
            self._board.mortgageProp(self)
        
class Railroad(EventHandler):
    """Class that creates each Railroad"""
    def __init__(self, center, name, board):
        """Creates all of the values needed for each railroad and creates the
        specified railroad"""
        EventHandler.__init__(self)
        width = 30
        cx, cy = center
        self._board = board
        self._rent = 50
        self._mortgage = 100
        self._base = Rectangle(width, width, center)
        self._base.setFillColor('white')
        self._title = name
        self._name = Text(name, (cx, cy - 10), 3)
        self._back = Text('-Mortgaged-', (cx, cy - 10), 3)
        self._base.setDepth(1)
        self._name.setDepth(.5)
        self._back.setDepth(1.5)
        self._frontDepth = .5
        self._backDepth = 1.5
        self._active = True
        self._mortgaged = False
        self._traded = False
        self._base.addHandler(self)
        self._name.addHandler(self)
                          
    def moveTo(self, point):
        """Moves the railroad by a given dx and dy"""
        cx, cy = point
        self._base.moveTo(point)
        self._name.moveTo((cx, cy - 10))
        self._back.moveTo((cx, cy - 10))
        
    def addTo(self, win):
        """Adds the railroad to a window"""
        win.add(self._base)
        win.add(self._name)
        win.add(self._back)
        
    def remove(self, win):
        """Removes the railroad from a window"""
        win.remove(self._base)
        self._name.setText('')
        self._back.setText('')
        
    def setDepth(self, depth):
        """Sets the depth of the railroad to a specified value"""
        self._base.setDepth(depth)
        if self._frontDepth < self._backDepth:
            self._name.setDepth(depth - .5)
            self._back.setDepth(depth + .5)
            self._frontDepth = self._name.getDepth()
            self._backDepth = self._back.getDepth()
        else:
            self._name.setDepth(depth + .5)
            self._back.setDepth(depth - .5)
            self._frontDepth = self._back.getDepth()
            self._backDepth = self._name.getDepth()
        
    def flip(self):
        """Flips the railroad"""
        self._name.setDepth(self._backDepth)
        self._back.setDepth(self._frontDepth)
        self._frontDepth = self._name.getDepth()
        self._backDepth = self._back.getDepth()
        
    def deactivate(self):
        """Deactivates the railroad"""
        self._active = False
        
    def getName(self):
        """Returns the name of the railroad"""
        return self._title
        
    def mortgage(self):
        """Sets the railroad to mortgaged"""
        self._mortgaged = True
        
    def payOff(self):
        """Sets the railroad to not mortgaged"""
        self._mortgaged = False
        
    def isMortgaged(self):
        """Returns if the railroad is mortgaged or not"""
        return self._mortgaged
        
    def addTrade(self):
        """Marks the railroad as added to the trade"""
        self._traded = True
        
    def removeTrade(self):
        """Mards the railroad as removed from the trade"""
        self._traded = False
    
    def changePossesion(self, point, num):
        """Creates a window where the player confirms that they want to buy
        the property, and if he/she does then possesion is given to that
        player"""
        cx, cy = point
        if self._active:
            while True:
                try:
                    buy = input('Would you like to buy ' + self._title +'?\
                    \n(Type y or n)')
                    if buy == 'y':
                        if num < 6:
                            self.moveTo((cx, cy + num * 8))
                        else:
                            self.moveTo((cx + 30, cy + (num - 6) * 8))
                        self.deactivate()
                        return True
                    if buy == 'n':
                        return
                except ValueError:
                    pass
        
    def handleMouseRelease(self, event):
        """Reports to the board when clicked"""
        if Board.TRADEMODE:
            if self._traded:
                self._board.removeProp(self)
            else:
                self._board.addProp(self)
        else:
            self._board.mortgageRail(self)
            
class Utility(EventHandler):
    """Class that creates each utility"""
    def __init__(self, center, name, board):
        """Creates all of the values needed for each utility and creates the
        specified utility"""
        EventHandler.__init__(self)
        width = 30
        cx, cy = center
        self._board = board
        self._utiity = Rectangle(width, width, center)
        self._mortgage = 75
        self._base = Rectangle(width, width, center)
        self._base.setFillColor('white')
        self._title = name
        self._name = Text(name, (cx, cy - 10), 3)
        self._back = Text('-Mortgaged-', (cx, cy - 10), 3)
        self._base.setDepth(1)
        self._name.setDepth(.5)
        self._back.setDepth(1.5)
        self._frontDepth = .5
        self._backDepth = 1.5
        self._active = True
        self._mortgaged = False
        self._traded = False
        self._base.addHandler(self)
        self._name.addHandler(self)
                          
    def moveTo(self, point):
        """Moves the utility by a given dx and dy"""
        cx, cy = point
        self._base.moveTo(point)
        self._name.moveTo((cx, cy - 10))
        self._back.moveTo((cx, cy - 10))
    
    def remove(self, win):
        """Removes the utility from a window"""
        win.remove(self._base)
        self._name.setText('')
        self._back.setText('')
        
    def addTo(self, win):
        """Adds the utility to a window"""
        win.add(self._base)
        win.add(self._name)
        win.add(self._back)
        
    def setDepth(self, depth):
        """Sets the depth of the utility to a specified value"""
        self._base.setDepth(depth)
        if self._frontDepth < self._backDepth:
            self._name.setDepth(depth - .5)
            self._back.setDepth(depth + .5)
            self._frontDepth = self._name.getDepth()
            self._backDepth = self._back.getDepth()
        else:
            self._name.setDepth(depth + .5)
            self._back.setDepth(depth - .5)
            self._frontDepth = self._back.getDepth()
            self._backDepth = self._name.getDepth()
        
    def flip(self):
        """Flips the utility"""
        self._name.setDepth(self._backDepth)
        self._back.setDepth(self._frontDepth)
        self._frontDepth = self._name.getDepth()
        self._backDepth = self._back.getDepth()
        
    def deactivate(self):
        """Deactivates the utility"""
        self._active = False
        
    def getName(self):
        """Retuns the name of the utility"""
        return self._title
        
    def mortgage(self):
        """Sets the utility to mortgaged"""
        self._mortgaged = True
        
    def payOff(self):
        """Sets the utility to not mortgaged"""
        self._mortgaged = False
        
    def isMortgaged(self):
        """Returns if the utility is mortgaged or not"""
        return self._mortgaged
        
    def addTrade(self):
        """Marks the utility as added to the trade"""
        self._traded = True
        
    def removeTrade(self):
        """Mards the utility as removed from the trade"""
        self._traded = False
    
    def changePossesion(self, point, num):
        """Creates a window where the player confirms that they want to buy
        the property, and if he/she does then possesion is given to that
        player"""
        cx, cy = point
        if self._active:
            while True:
                try:
                    buy = input('Would you like to buy ' + self._title + '?\
                    \n(Type y or n)')
                    if buy == 'y':
                        if num < 6:
                            self.moveTo((cx, cy + num * 8))
                        else:
                            self.moveTo((cx + 30, cy + (num - 6) * 8))
                        self.deactivate()
                        return True
                    if buy == 'n':
                        return
                except ValueError:
                    pass
        
    def handleMouseRelease(self, event):
        """Reports the the board when clicked"""
        if Board.TRADEMODE:
            if self._traded:
                self._board.remove(self)
            else:
                self._board.addProp(self)
        else:
            self._board.mortgageUtil(self)
            
class House(EventHandler):
    """Class for creating each house"""
    def __init__(self, center, board):
        """Creates the house"""
        EventHandler.__init__(self)
        self._board = board
        self._house = Rectangle(12, 12, center)
        self._house.setFillColor('green')
        self._house.setDepth(1)
        self._house.addHandler(self)
        self._active = True
        self._moving = False
        self._location = center
        self._startLoc = None
        self._bind = None
    
    def addTo(self, win):
        """Adds the house to a window"""
        win.add(self._house)
        
    def remove(self, win):
        """Removes the house from a window"""
        win.remove(self._house)
        
    def moveTo(self, point):
        """Moves the house to a specified point"""
        self._house.moveTo(point)
        self._location = point
        
    def deactivate(self):
        """Deactivates the house"""
        self._active = False
        
    def getActive(self):
        """Returns if the house is active or not"""
        return self._active
        
    def move(self, dx, dy):
        """Moves the house along with the mouse"""
        oldx, oldy = self._location
        newx = oldx + dx
        newy = oldy + dy
        self._location = newx, newy
        self.moveTo((newx, newy))
        
    def getLocation(self):
        """Returns the location of the house"""
        return self._location
        
    def bindTo(self, number):
        """Binds the house to a number"""
        self._bind = number
        
    def getBind(self):
        """Returns bound number"""
        return self._bind
        
    def handleMouseRelease(self, event):
        """Either makes the house follow the mouse's location or releases"""
        if not self._active:
            self._board.reportHouseClick(self)
        else:
            if self._moving:
                self._moving = False
                for cell in Board.CELLS:
                    cell.setDepth(101)
                self._board.reportHouseClick(self)
            else:
                self._moving = True
                for cell in Board.CELLS:
                    cell.setDepth(99)
                self._startLoc = event.getMouseLocation()
        
    def handleMouseMove(self, event):
        """If the house is moving, keeps the house's position the same as the
        mouse's"""
        if not self._active:
            return
        if self._moving:
            oldx, oldy = self._startLoc
            newx, newy = event.getMouseLocation()
            self.move(newx - oldx, newy - oldy)
            self._startLoc = self._location

class Hotel(EventHandler):
    """Class for creating each hotel"""
    def __init__(self, center, board):
        """Creates the hotel"""
        EventHandler.__init__(self)
        self._board = board
        self._hotel = Rectangle(13, 30, center)
        self._hotel.setFillColor('red')
        self._hotel.setDepth(0)
        self._hotel.addHandler(self)
        self._active = True
        self._moving = False
        self._location = center
        self._startLoc = None
        self._bind = None
        
    def addTo(self, win):
        """Adds the hotel to a window"""
        win.add(self._hotel)
        
    def remove(self, win):
        """Removes the hotel from a window"""
        win.remove(self._hotel)
        
    def moveTo(self, point):
        """Moves the hotel to a specified point"""
        self._hotel.moveTo(point)
        self._location = point
        
    def rotate(self, degrees):
        """Rotates the hotel by a specified degrees"""
        self._hotel.rotate(degrees)
        
    def setDepth(self, depth):
        """Gives the hotel a new depth"""
        self._hotel.setDepth(depth)
        
    def setPivot(self, point):
        """Gives the hotel a new point to rotate about"""
        self._hotel.setPivot(point)
        
    def deactivate(self):
        """Deactivates the hotel"""
        self._active = False
        
    def getActive(self):
        """Returns if the hotel is active or not"""
        return self._active
        
    def move(self, dx, dy):
        """Moves the hotel to a new location"""
        oldx, oldy = self._location
        newx = oldx + dx
        newy = oldy + dy
        self._location = newx, newy
        self.moveTo((newx, newy))
        
    def getLocation(self):
        """Returns the location of the hotel"""
        return self._location
        
    def bindTo(self, number):
        """Binds the hotel to a number"""
        self._bind = number
        
    def getBind(self):
        """Returns the number the hotel is bound to"""
        return self._bind
        
    def handleMouseRelease(self, event):
        "If the hotel is active, makes it so the hotel will follow the mouse"""
        if not self._active:
            self._board.reportHotelClick(self)
        else:
            if self._moving:
                self._moving = False
                for cell in Board.CELLS:
                    cell.setDepth(101)
                self._board.reportHotelClick(self)
            else:
                self._moving = True
                for cell in Board.CELLS:
                    cell.setDepth(99)
                self._startLoc = event.getMouseLocation()

    def handleMouseMove(self, event):
        """If the house is moving, keeps the hotel's position the same as the
        mouse's"""
        if not self._active:
            return
        if self._moving:
            oldx, oldy = self._startLoc
            newx, newy = event.getMouseLocation()
            self.move(newx - oldx, newy - oldy)
            self._startLoc = self._location


def game(win):
    """Test"""
    Board(win)
    
StartGraphicsSystem(game, 700, 700)
    
    
