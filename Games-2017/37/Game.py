"""
*****************************************************************************
FILE: Game.py
AUTHOR: Sterling Bray
PARTNER: Henry Cohen
ASSIGNMENT: Project 6
DATE: 4/10/17
DESCRIPTION: Program that creates the game of monopoly
*****************************************************************************
"""
import random
from cs110graphics import *


class Board:
    """Contains the board and all of the methods performed
       within the board class."""
    
    def __init__(self, win):
        
        #locations from Go to in jail(Jail space is just visiting) 
        self._locations = [(513, 508),
                           (459, 523),
                           (418, 523),
                           (381, 523),
                           (341, 523),
                           (300, 517),
                           (260, 523),
                           (218, 523),
                           (177, 523),
                           (138, 523),
                           (62, 537), 
                           (78, 458),
                           (78, 421),
                           (78, 376),
                           (78, 336),
                           (78, 297),
                           (78, 256),
                           (78, 214),
                           (78, 174),
                           (78, 133),
                           (84, 80.89582824707031),
                           (137.4375, 76),
                           (178.4375, 76),
                           (220.4375, 76),
                           (259.4375, 76),
                           (297.4375, 76),
                           (339.4375, 76),
                           (379.4375, 76),
                           (418.4375, 76),
                           (458.4375, 76),
                           (509.4375, 75.89582824707031),
                           (523, 132.8958282470703),
                           (523, 174.8958282470703),
                           (523, 215.8958282470703),
                           (523, 255.8958282470703),
                           (523, 298.8958282470703),
                           (523, 335.8958282470703),
                           (523, 375.8958282470703),
                           (523, 417.8958282470703),
                           (523, 456.8958282470703),
                           (93, 501)]
        
        #gives board access to properties
        self._propertyaccess = Properties()
        '''self._propertycards = []
        for pos in self._allPropSpaces:
            card = PropertyCards(pos)
            self._propertycards.append(card)'''
            
        #gives board access to utilties
        self._utilitiesaccess = Utilities()
        
        #gives board access to railroads
        self._railroadsaccess = RailRoads()
        
        self._win = win
        
        #adds prize cards to board
        prizeurl = "https://cs.hamilton.edu/~stbray/images/pulitzer_prze.png"
        self._prize = Image(prizeurl, width=70, height=40)
        self._prize.setDepth(20)
        win.add(self._prize)
        self._prize.move(200, 175)
        self.dice = DieController(win, self)
        
        #adds chance cards to board
        chanceurl = "https://cs.hamilton.edu/~stbray/images/chance.png"
        self._chance = Image(chanceurl, width=70, height=40)
        self._chance.setDepth(20)
        win.add(self._chance)
        self._chance.move(400, 400)
        
        self._NumPlayers = int(input('How many players?'))
        
        #creates pieces
        self._pawnlist = []
        colorlist = ['blue', 'green', 'purple', 'yellow',\
            'orange', 'red']
        for i in range(self._NumPlayers):
            thispawn = Pawn(self, colorlist[i], i, 0)
            self._pawnlist.append(thispawn)
            thispawn.addTo(win)
        self.updatePawnLocations()
        
        #creates player banks
        self._playerBanks = []
        for i in range(self._NumPlayers):
            thisbank = PlayerBank()
            self._playerBanks.append(thisbank)
        self.banksOnBoard(win)
        
        #creates player ownings
        self._playerassets = []
        for i in range(self._NumPlayers):
            assets = PlayerOwnings()
            self._playerassets.append(assets)
            
        #creates board
        bGurl = "https://cs.hamilton.edu/~stbray/images/Board.JPG"
        self._boardBG = Image(bGurl, width=500, height=500)
        
        self._current = 0 
        
    def banksOnBoard(self, win):
        """adds banks to the window to be displayed."""
        
        start = 0 
        self._banksTexts = []
        for i in range(self._NumPlayers):
            bank = Text("Player " + str(i + 1) + ": $" +\
            str(self._playerBanks[i].returnBank()), (50 + start, 25), 12)
            start += 100
            self._banksTexts.append(bank)
            win.add(bank)
        
    def updateBanks(self):
        """Updates the banks to have the correct values."""
        
        banknum = 0 
        for bank in self._banksTexts:
            bank.setText("Player " + str(banknum + 1) + ": $" +\
            str(self._playerBanks[banknum].returnBank()))
            banknum += 1
            
    def changeTurn(self):
        """Changes the current player, changing the turn."""
      
        self._current = (self._current + 1) % len(self._pawnlist)
        
    def reportDieRoll(self, value, doubles):
        """Reports the die roll and calls functions based on the 
           new position of the pawn."""
        
        #checks the position of the current pawn
        pos = self._pawnlist[self._current].getPosition()
        if pos == 30:
            self.injail(value, doubles)
        else:
            pos = pos + value
            if pos > 39:
                self._playerBanks[self._current].addMoney(200)
            pos = pos % 40
            if pos == 4:
                self._playerBanks[self._current].loseMoney(200)
            if pos == 38:
                self._playerBanks[self._current].loseMoney(75)
            self._pawnlist[self._current].setPosition(pos)
            self.updatePawnLocations()
            self.landedOn(pos, value)
            self.updatePawnLocations()
            self.updateBanks()
            self.playerElim()
            self.endGame()
            if doubles is False:
                self.changeTurn()
            else:
                pass
            
    def playerElim(self):
        """Checks to see if any players have negative banks and removes
           the pawn and its bank from the window. The player's assets
           are made available again."""
        
        i = 0
        for banks in self._playerBanks:
            if banks.returnBank() <= 0:
                owner = i
                self._pawnlist[owner].removePawn(self._win)
                
                del self._playerBanks[owner]
                
                self._win.remove(self._banksTexts[owner])
                del self._banksTexts[owner]
                
                del self._pawnlist[owner]
                
                self._NumPlayers = len(self._pawnlist)
                
                railroads = self._playerassets[owner].getrR()
                for railpos in railroads:
                    
                    railInList = self._railroadsaccess.railInList(railpos)
                    self._railroadsaccess.unbought(railInList)
                
                utilities = self._playerassets[owner].getUtil()
                for utilpos in utilities:
                    
                    utilInList = self._utilitiesaccess.utilityInList(utilpos)
                    self._utilitiesaccess.unbought(utilInList)
                    
                properties = self._playerassets[owner].getProps()
                for proppos in properties:
                    
                    propInList = self._propertyaccess.propertyInList(proppos)
                    self._propertyaccess.unbought(propInList)
                
                del self._playerassets[owner]
            i += 1
            
    def endGame(self):
        """Ends the game if there's only one player remaining in the game."""
        
        if self._NumPlayers == 1:
            
            rect = Rectangle(600, 600, (300, 300))
            rect.setFillColor('green')
            rect.setDepth(2)
            recttext = Text('You win!', (300, 300), 18)
            recttext.setDepth(1)
            self._win.add(rect)
            self._win.add(recttext)
        
    def addBoard(self, win):
        """Adds the board to the window."""
        
        #adds board to window
        win.add(self._boardBG)
        self._boardBG.move(300, 300)

    def updatePawnLocations(self):
        """Moves pawns to their current locations on the window"""

        for i in range(self._NumPlayers):
            pos = self._pawnlist[i].getPosition()
            if pos == 30:
                offsets = [(2, 10), (-14, 10), (-14, -10), (2, -10),\
                (18, 10), (18, -10)]
                pos = 40
            if pos > 0 and pos < 10 or pos > 20 and pos < 30:
                offsets = [(-7, 17), (-7, 0), (-7, -17), (12, -17),\
                (12, 0), (12, 17)]
            if pos > 10 and pos < 20 or pos > 30 and pos < 40:
                offsets = [(17, -7), (0, -7), (-17, -7), (-17, 12),\
                (0, 12), (17, 12)]
            if pos == 10:
                offsets = [(0, 0), (0, -15), (0, -30), (15, 0), (30, 0),\
                (45, 0)]
            if pos == 0 or pos == 20:
                offsets = [(20, -10), (20, 10), (0, -10), (0, 10),\
                (-20, 10), (-20, -10)]
            #theSpace = self._spaces[pos]
            self._pawnlist[i].moveTo(self._locations[pos])
            cx, cy = offsets[i]
            self._pawnlist[i].move(cx, cy)
            
    def injail(self, value, doubles):
        """This is called when a pawn is in jail. It requires the 
           player to either roll doubles or wait three turns to get 
           out of jail."""
        
        jailcount = self._pawnlist[self._current].getjailcount()
        if jailcount == 0:
            self._pawnlist[self._current].jailAdder()
            self.updatePawnLocations()
            self.changeTurn()
        elif jailcount == 1:
            if doubles:
                position = value + 10
                self._pawnlist[self._current].setPosition(position)
                self.landedOn(position, value)
                self.updatePawnLocations()
                self.updateBanks()
                self._pawnlist[self._current].resetcount()
                self.changeTurn()
            else:
                self._pawnlist[self._current].jailAdder()
                self.changeTurn()
        elif jailcount == 2:
            if doubles:
                position = value + 10
                self._pawnlist[self._current].setPosition(position)
                self.landedOn(position, value)
                self.updatePawnLocations()
                self.updateBanks()
                self._pawnlist[self._current].resetcount()
                self.changeTurn()
            else:
                position = value + 10
                self._playerBanks[self._current].loseMoney(50)
                self._pawnlist[self._current].setPosition(position)
                self.landedOn(position, value)
                self.updatePawnLocations()
                self.updateBanks()
                self._pawnlist[self._current].resetcount()
                self.changeTurn()
                
    def landedOn(self, pos, value):
        '''This contains lists of different types of spaces and calls
           a separate function based on the current location of the pawn.'''
        
        #locations of properties on the board
        propertypositions = [1, 3, 6, 8, 9, 11, 13, 14, 16, 18, 19,\
            21, 23, 24, 26, 27, 29, 31, 32, 34, 37, 39]
            
        if pos in propertypositions:
            self.propertyOps(pos)
            
        #locations of utilities on the board
        utilitypositions = [12, 28]
        
        if pos in utilitypositions:
            self.utilityOps(pos, value)
         
        #locations of the railroads on the board   
        rRpositions = [5, 15, 25, 35]
        
        if pos in rRpositions:
            self.rROps(pos)
        
        #locations of pulitzer prize on the board
        chestpositions = [2, 17, 33]
        
        if pos in chestpositions:
            CommunityChest(self._playerBanks, self._pawnlist,\
                self._win, self._current, self)
        
        #locations of chance on the board
        chancepositions = [7, 22, 36]
        
        if pos in chancepositions:
            ChanceCards(self._playerBanks, self, self._pawnlist,\
                self._playerassets, self._win, self._current, self)
        
    def rROps(self, pos):
        """When you land on a railroad, this function is called."""
        
        rRInList = self._railroadsaccess.railInList(pos)
        if self._railroadsaccess.railroadOwned(rRInList):
            i = 0
            for asset in self._playerassets:
                if asset.owned(pos):
                    owner = i
                i += 1
            numOwned = self._playerassets[owner].numRailRoads()
            rentList = [25, 50, 100, 200]
            rent = rentList[numOwned - 1]
            self._playerBanks[owner].addMoney(rent)
            self._playerBanks[self._current].loseMoney(rent)
    
        elif self._railroadsaccess.getRRInfo(rRInList, 2) <=\
            self._playerBanks[self._current].returnBank():
                
            BuyRR(self._win, pos, self._railroadsaccess,\
                self._playerassets, self._current, self._playerBanks, self)
        
        else:
            pass
            
    def utilityOps(self, pos, value):
        """When a pawn lands on a utility, this function is called."""
        
        #checks if the utility is owned
        utilityInList = self._utilitiesaccess.utilityInList(pos)
        if self._utilitiesaccess.utilityOwned(utilityInList):
            i = 0
            for asset in self._playerassets:
                if asset.owned(pos):
                    owner = i
                i += 1
            numOwned = self._playerassets[owner].numUtils()
            if numOwned == 1:
                rent = value * 4
                self._playerBanks[owner].addMoney(rent)
                self._playerBanks[self._current].loseMoney(rent)
            else:
                rent = value * 10
                self._playerBanks[owner].addMoney(rent)
                self._playerBanks[self._current].loseMoney(rent)

                
        elif self._utilitiesaccess.getUInfo(utilityInList, 2) <=\
            self._playerBanks[self._current].returnBank():
                
            BuyUtility(self._win, pos, self._utilitiesaccess,\
                self._playerassets, self._current, self._playerBanks, self)
                    
        else:
            pass
            
    def propertyOps(self, pos):
        """When a pawn lands on a property, this function is called."""
        
        #checks if the property is owned
        propertyInList = self._propertyaccess.propertyInList(pos)
        if self._propertyaccess.propertyOwned(propertyInList):
            rent = self._propertyaccess.getInfo(propertyInList, 3)
            self._playerBanks[self._current].loseMoney(rent)
            i = 0
            for asset in self._playerassets:
                if asset.owned(pos):
                    self._playerBanks[i].addMoney(rent)
                i += 1
            i = 0
           
        elif self._propertyaccess.getInfo(propertyInList, 2) <=\
                self._playerBanks[self._current].returnBank():
                    
            BuyProperty(self._win, pos, self._propertyaccess,\
                self._playerassets, self._current, self._playerBanks, self)
        
        else:
            pass

class CommunityChest(EventHandler):
    """This class contains the community chest cards and adds an individual
       card to the window when it is called. It also contains the actions 
       that are executed when each card is called."""
    
    def __init__(self, playerbank, pawnlist, win, turn, board):
        
        #assigns variables to parameters
        EventHandler.__init__(self)
        self._pawnlist = pawnlist
        self._current = turn
        self._board = board
        self._win = win
        self._topcard = 1
        self._playerbank = playerbank
        
        #list of Pulitzer prize cards
        self._chestCards = [["Writer's block! Pay $50", 0],
                            ['Win the National Book Award! Collect $150',\
                                1],
                            ['Happy Birthday! Collect $10 from each player',\
                                2],
                            ['Sponsor a public library. Pay $50', \
                                3],
                            ['Editing Fee. Pay $20', 4]]
        
        self._cardrect = Rectangle(400, 100, (300, 300))
        self._cardrect.setFillColor('blue')
        self._topcard = self.drawCard()
        self._cardrect.setDepth(14)
        self._cardtext = Text(self.drawCard(), (300, 300), 16)
        self._cardtext.setDepth(14)
        self._win.add(self._cardrect)
        self._win.add(self._cardtext)
        self._cardrect.addHandler(self)
        self._cardtext.addHandler(self)
        
    def drawCard(self):
        """Draws a random card from the community chest list and returns
           it."""
        
        #updates self._cardlist in order to remove the random card
        self._topcard = self._chestCards[random.randrange(5)]
        self._chestCards = self._chestCards[1:]
        self._chestCards.append(self._topcard)
        return self._topcard[0]
        
    def chestOps(self):
        """Contains each action executed by a card and uses if statements
           to determine which actions should be executed."""
        
        if self._topcard[1] == 0 or self._topcard[1] == 3:
        
            self._playerbank[self._current].loseMoney(50)
    
        if self._topcard[1] == 1:
            
            self._playerbank[self._current].addMoney(150)
    
        if self._topcard[1] == 2:
            
            for i in range(len(self._playerbank)):
        
                self._playerbank[self._current].addMoney(10)
                self._playerbank[i].loseMoney(10)
    
        if self._topcard[1] == 4:
        
            self._playerbank[self._current].loseMoney(20)
        
    def handleMouseRelease(self, event):
        """When the card is clicked, this method calls the chest options
           and updates the player banks. Then it removes the card and
           its text from the window."""
        
        self.chestOps()
        self._board.updateBanks()
        self._win.remove(self._cardrect)
        self._win.remove(self._cardtext)
        
class ChanceCards(EventHandler):
    """This class contains the chance cards and adds an individual
       card to the window when it is called. It also contains the actions 
       that are executed when each card is called."""
    
    def __init__(self, playerbank, boardclass, pawnlist,\
        playerassets, win, turn, board):
            
        EventHandler.__init__(self)
        self._board = board
        self._pawnlist = pawnlist
        self._playerassets = playerassets
        self._board = boardclass
        self._current = turn
        self._win = win
        self._topcard = 0
        self._playerbank = playerbank
        self._chanceCards = [['You inherit an antique quill pen. Collect $100'\
                                , 0],
                             ['Ebooks are limiting your sales. Pay $100', \
                                1],
                             ['Literacy rates are declining, Pay $25',\
                                2],
                             ['Book rights sold for a movie! Collect $75', \
                                3],
                             ['Missed a deadline. Pay $15', 4]]
        
        self._cardrect = Rectangle(400, 100, (300, 300))
        self._cardrect.setFillColor('orange')
        self._topcard = self.drawCard()
        self._cardrect.setDepth(14)
        self._cardtext = Text(self.drawCard(), (300, 300), 16)
        self._cardtext.setDepth(14)
        self._win.add(self._cardrect)
        self._win.add(self._cardtext)
        self._cardrect.addHandler(self)
        self._cardtext.addHandler(self)
        
    def drawCard(self):
        """Draws a random card from the chance list and returns it."""
        
        #updates self._cardlist in order to remove the random card
        self._topcard = self._chanceCards[random.randrange(5)]
        self._chanceCards = self._chanceCards[1:]
        self._chanceCards.append(self._topcard)
        
        return self._topcard[0]
        
    def chanceOps(self):
        """Contains the actions to be executed by each chance card and 
           uses if statements to determine which action to execute."""

        if self._topcard[1] == 0:
            
            self._playerbank[self._current].addMoney(100)
            
        if self._topcard[1] == 1:
        
            self._playerbank[self._current].loseMoney(100)
    
        if self._topcard[1] == 2:
        
            self._playerbank[self._current].loseMoney(25)
        
        if self._topcard[1] == 3:
        
            self._playerbank[self._current].addMoney(75)
        
        if self._topcard[1] == 4:
            
            self._playerbank[self._current].loseMoney(15)

    def handleMouseRelease(self, event):
        """When the chance card is clicked, this fuctions calls chance
           options and updates the player banks. Then the card and it
           text is removed from the window."""
        
        self.chanceOps()
        self._board.updateBanks()
        self._win.remove(self._cardrect)
        self._win.remove(self._cardtext)
        
class BuyRR:
    """This class creates the buy card rectangle, view card rectangle,
       and the pass rectangle. This class is used when a pawn has landed 
       on a railroad."""
    
    def __init__(self, win, rawpos, RRList, owned, turn, banks, board):
        
        #assigns variable to parameters
        self._win = win
        self._board = board
        self._owned = owned
        self._rawpos = rawpos
        self._RailRoads = RRList
        self._RRInList = self._RailRoads.railInList(rawpos)
        self._banks = banks
        self._current = turn
        
        #creates the 3 cards and adds them to the window
        self._buycard = Rectangle(100, 100, (225, 200))
        self._viewcard = Rectangle(100, 100, (330, 200))
        self._Pass = Rectangle(100, 100, (435, 200))
        self._buycard.setFillColor('white')
        self._buycard.setDepth(19)
        self._viewcard.setFillColor('white')
        self._Pass.setFillColor('white')
        self._buytext = Text("Buy Railroad", (225, 235), 14)
        self._buytext.setDepth(19)
        self._viewcardtext = Text("View Card", (330, 235), 14)
        self._PassText = Text("Pass", (435, 235), 14)
        win.add(self._buycard)
        win.add(self._viewcard)
        win.add(self._Pass)
        win.add(self._buytext)
        win.add(self._viewcardtext)
        win.add(self._PassText)
        
        #assigns handlers to the cards
        self._buycard.addHandler(BuyRRController(self, self._rawpos,\
            self._RailRoads, self._owned, self._banks, self._current,\
            self._win, self._board))
        self._buytext.addHandler(BuyRRController(self, self._rawpos,\
            self._RailRoads, self._owned, self._banks, self._current,\
            self._win, self._board))
        self._viewcard.addHandler(ViewRRCard(self, self._rawpos, \
            self._RailRoads, self._win))
        self._viewcardtext.addHandler(ViewRRCard(self, self._rawpos, \
            self._RailRoads, self._win))
        self._Pass.addHandler(PassController(self, self._win))
        self._PassText.addHandler(PassController(self, self._win))
        
    def removeAll(self, win):
        """Removes the 3 rectangles and their text from the window
           once one has been clicked."""
        
        win.remove(self._buycard)
        win.remove(self._viewcard)
        win.remove(self._Pass)
        win.remove(self._buytext)
        win.remove(self._viewcardtext)
        win.remove(self._PassText)

class BuyRRController(EventHandler):
    """This class serves as an event handler for the buy railroad 
       card."""
    
    def __init__(self, buyRRClass, rawpos, railroads, owned, banks,\
        turn, win, board):
            
        EventHandler.__init__(self)
        
        #assigns variables to the parameters
        self._board = board
        self._rawpos = rawpos
        self._win = win
        self._railroads = railroads
        self._buyRRClass = buyRRClass
        self._RRInList = self._railroads.railInList(rawpos)
        self._owned = owned
        self._banks = banks
        self._current = turn
        
    def handleMouseRelease(self, event):
        """When the buy railroad card is clicked, the necessary functions
           are called through this method."""
        
        price = self._railroads.getRRInfo(self._RRInList, 2)
        self._banks[self._current].loseMoney(price)
        self._board.updateBanks()
        self._railroads.bought(self._RRInList)
        self._owned[self._current].addUtil(self._rawpos)
        self._buyRRClass.removeAll(self._win)
        
class ViewRRCard(EventHandler):
    """This class serves as an event handler for the view railroad card."""
    
    def __init__(self, buyrrclass, rawpos, railroads, win):
        
        EventHandler.__init__(self)
        self._buyRRClass = buyrrclass
        
        #initilizes the view cards for railroad
        self._cardrect = Rectangle(400, 400, (300, 300))
        self._cardrect.setFillColor('white')
        self._cardrect.setDepth(14)
        self._win = win
        self._railroads = railroads
        self._rawpos = rawpos
        self._RailInList = self._railroads.railInList(rawpos)
        railImages = ['https://cs.hamilton.edu/~stbray/images/Type.png'\
            , 'https://cs.hamilton.edu/~stbray/images/Untitled.jpg',\
            'https://cs.hamilton.edu/~stbray/images/pen_.jpg', \
            'https://cs.hamilton.edu/~stbray/images/feather_and_ink.png']
        self._Title = Image(railImages[self._RailInList], width=40,\
            height=70)
        self._Title.setDepth(14)
        self._textName = Text(str(self._railroads.getRRInfo(self._RailInList,\
            0)), (300, 200), 18)
        self._textName.setDepth(14)
        self._textPrice = Text('Price : $' + str(self._railroads.getRRInfo\
            (self._RailInList, 2)), (300, 225), 18)
        self._textPrice.setDepth(14)
        self._textRent = Text('Rent: $25', (300, 265), 18)
        self._textRent.setDepth(14)
        self._textRentone = Text("If 2 R.R's are owned: $50", \
            (300, 305), 18)
        self._textRentone.setDepth(14)
        self._textRenttwo = Text('If 3 " " ": $100', \
            (300, 345), 18)
        self._textRenttwo.setDepth(14)
        self._textRentthree = Text('If 4 " " ": $200',\
            (300, 385), 18)
        self._textRentthree.setDepth(14)
        
        #adds handlers to the card
        self._cardrect.addHandler(ViewRRUp(self, self._win))
        self._Title.addHandler(ViewRRUp(self, self._win))
        self._textName.addHandler(ViewRRUp(self, self._win))
        self._textPrice.addHandler(ViewRRUp(self, self._win))
        self._textRent.addHandler(ViewRRUp(self, self._win))
        self._textRentone.addHandler(ViewRRUp(self, self._win))
        self._textRenttwo.addHandler(ViewRRUp(self, self._win))
        self._textRentthree.addHandler(ViewRRUp(self, self._win))
        
    def handleMouseRelease(self, event):
        """When the view card rectangle is clicked, the card's information
           is displayed on a new rectangle that appears in the window."""
        
        self._win.add(self._cardrect)
        self._win.add(self._Title)
        self._Title.moveTo((300, 150))
        self._win.add(self._textName)
        self._win.add(self._textPrice)
        self._win.add(self._textRent)
        self._win.add(self._textRentone)
        self._win.add(self._textRenttwo)
        self._win.add(self._textRentthree)
    
    def remove(self, win):
        """Removes the card and its text when it is called."""
        
        win.remove(self._Title)
        win.remove(self._textName)
        win.remove(self._textPrice)
        win.remove(self._textRent)
        win.remove(self._textRentone)
        win.remove(self._textRenttwo)
        win.remove(self._textRentthree)
        win.remove(self._cardrect)
        
class ViewRRUp(EventHandler):
    """Serves as an event handler for the railroad information card."""
    
    def __init__(self, viewclass, win):
        
        EventHandler.__init__(self)
        self._win = win
        self._viewcardclass = viewclass
        
    def handleMouseRelease(self, event):
        """When the info card is clicked, it is removed from the window."""
            
        self._viewcardclass.remove(self._win)
        
class BuyUtility:
    """This class creates the buy card rectangle, view card rectangle,
       and the pass rectangle. This class is used when a pawn has landed 
       on a utility."""
    
    def __init__(self, win, rawpos, utilList, owned, turn, banks, board):
        
        #assigns variables to the parameters
        self._win = win
        self._owned = owned
        self._board = board
        self._rawpos = rawpos
        self._utilities = utilList
        self._utilityInList = self._utilities.utilityInList(rawpos)
        self._banks = banks
        self._current = turn
        
        #initializes the 3 cards
        self._buycard = Rectangle(100, 100, (225, 200))
        self._viewcard = Rectangle(100, 100, (330, 200))
        self._Pass = Rectangle(100, 100, (435, 200))
        self._buycard.setFillColor('white')
        self._buycard.setDepth(19)
        self._viewcard.setFillColor('white')
        self._Pass.setFillColor('white')
        self._buytext = Text("Buy Utility", (225, 235), 14)
        self._buytext.setDepth(19)
        self._viewcardtext = Text("View Card", (330, 235), 14)
        self._PassText = Text("Pass", (435, 235), 14)
        win.add(self._buycard)
        win.add(self._viewcard)
        win.add(self._Pass)
        win.add(self._buytext)
        win.add(self._viewcardtext)
        win.add(self._PassText)
        
        #assigns handlers to the 3 cards
        self._buycard.addHandler(BuyUtilController(self, self._rawpos,\
            self._utilities, self._owned, self._banks, self._current,\
            self._win, self._board))
        self._buytext.addHandler(BuyUtilController(self, self._rawpos,\
            self._utilities, self._owned, self._banks, self._current,\
            self._win, self._board))
        self._viewcard.addHandler(ViewUtilCard(self, self._rawpos,\
            self._utilities, self._win))
        self._viewcardtext.addHandler(ViewUtilCard(self, self._rawpos,\
            self._utilities, self._win))
        self._Pass.addHandler(UtilPassController(self, self._win))
        self._PassText.addHandler(UtilPassController(self, self._win))
        
    def removeAll(self, win):
        """This method removes all 3 rectangles from the window when 
           it's called."""
        
        win.remove(self._buycard)
        win.remove(self._viewcard)
        win.remove(self._Pass)
        win.remove(self._buytext)
        win.remove(self._viewcardtext)
        win.remove(self._PassText)
        
class ViewUtilCard(EventHandler):
    """Serves as an event handler for the view card rectangle."""
    
    def __init__(self, buyUtilClass, rawpos, utilities, win):
        
        EventHandler.__init__(self)
        self._buyUtilClass = buyUtilClass
        
        #initializes the view utility cards
        self._cardrect = Rectangle(400, 400, (300, 300))
        self._cardrect.setFillColor('white')
        self._cardrect.setDepth(14)
        self._win = win
        self._utilities = utilities
        self._rawpos = rawpos
        self._utilInList = self._utilities.utilityInList(rawpos)
        utilityImages = ['https://cs.hamilton.edu/~stbray/images/penguin.png'\
            , 'https://cs.hamilton.edu/~stbray/images/book.png']
        self._Title = Image(utilityImages[self._utilInList], width=40,\
            height=70)
        self._Title.setDepth(14)
        self._textName = Text(str(self._utilities.getUInfo(self._utilInList,\
            0)), (300, 200), 18)
        self._textName.setDepth(14)
        self._textPrice = Text('Price : $' + str(self._utilities.getUInfo\
            (self._utilInList, 2)), (300, 225), 18)
        self._textPrice.setDepth(14)
        self._textRent = Text('If one "Utility" is owned', (300, 265), 18)
        self._textRent.setDepth(14)
        self._textRentone = Text("rent is 4 times amount shown", \
            (300, 305), 18)
        self._textRentone.setDepth(14)
        self._textRenttwo = Text('on dice. If both are owned', \
            (300, 345), 18)
        self._textRenttwo.setDepth(14)
        self._textRentthree = Text('rent is 10 times amount shown on dice',\
            (300, 385), 18)
        self._textRentthree.setDepth(14)
        
        #assigns handlers to the card and the text
        self._cardrect.addHandler(ViewUtilUp(self, self._win))
        self._Title.addHandler(ViewUtilUp(self, self._win))
        self._textName.addHandler(ViewUtilUp(self, self._win))
        self._textPrice.addHandler(ViewUtilUp(self, self._win))
        self._textRent.addHandler(ViewUtilUp(self, self._win))
        self._textRentone.addHandler(ViewUtilUp(self, self._win))
        self._textRenttwo.addHandler(ViewUtilUp(self, self._win))
        self._textRentthree.addHandler(ViewUtilUp(self, self._win))
        
    def handleMouseRelease(self, event):
        """When the view card rectangle is clicked, the utility information
           card appears in the window."""
        
        self._win.add(self._cardrect)
        self._win.add(self._Title)
        self._Title.moveTo((300, 150))
        self._win.add(self._textName)
        self._win.add(self._textPrice)
        self._win.add(self._textRent)
        self._win.add(self._textRentone)
        self._win.add(self._textRenttwo)
        self._win.add(self._textRentthree)
    
    def remove(self, win):
        """Removes the utility information card from the window when 
           the function is called."""
        
        win.remove(self._Title)
        win.remove(self._textName)
        win.remove(self._textPrice)
        win.remove(self._textRent)
        win.remove(self._textRentone)
        win.remove(self._textRenttwo)
        win.remove(self._textRentthree)
        win.remove(self._cardrect)

class UtilPassController(EventHandler):
    """This class serves as an event handler for the utility pass card."""
    
    def __init__(self, buyclass, win):
        
        EventHandler.__init__(self)
        
        self._buyclass = buyclass
        self._win = win
        
    def handleMouseRelease(self, event):
        """When the pass card is clicked, all 3 cards are removed from the
           window."""
        
        self._buyclass.removeAll(self._win)

class ViewUtilUp(EventHandler):
    """This class serves as an event handler for the utility information
       card."""
    
    def __init__(self, viewclass, win):
        
        EventHandler.__init__(self)
        self._win = win
        self._viewcardclass = viewclass
        
    def handleMouseRelease(self, event):
        """When the info card is clicked, it is removed from the window."""
            
        self._viewcardclass.remove(self._win)

class BuyUtilController(EventHandler):
    """This class is the event handler for the buy utility card.
       It allows for the card to react to events."""
    
    def __init__(self, buyUtilClass, rawpos, utilities, owned, banks,\
        turn, win, board):
            
        EventHandler.__init__(self)
        
        #assigns variables to the parameters
        self._rawpos = rawpos
        self._board = board
        self._win = win
        self._utilities = utilities
        self._buyUtilClass = buyUtilClass
        self._utilInList = self._utilities.utilityInList(rawpos)
        self._owned = owned
        self._banks = banks
        self._current = turn
        
    def handleMouseRelease(self, event):
        """This method calls the necessary functions after the buy utility
           card has been clicked."""
        
        price = self._utilities.getUInfo(self._utilInList, 2)
        self._banks[self._current].loseMoney(price)
        self._board.updateBanks()
        self._utilities.bought(self._utilInList)
        self._owned[self._current].addUtil(self._rawpos)
        self._buyUtilClass.removeAll(self._win)
        
class BuyProperty:
    """This class creates the buy card rectangle, view card rectangle,
       and the pass rectangle. This class is used when a pawn has landed 
       on a property."""
    
    def __init__(self, win, rawpos, proplist, owned,\
    turn, banks, board):
    
        #assigns variables to the parameters
        self._win = win
        self._board = board
        self._owned = owned
        self._properties = proplist
        self._rawpos = rawpos
        self._propInList = self._properties.propertyInList(rawpos)
        self._banks = banks
        self._current = turn
        
        #initializes the 3 cards
        self._buycard = Rectangle(100, 100, (225, 200))
        self._viewcard = Rectangle(100, 100, (330, 200))
        self._Pass = Rectangle(100, 100, (435, 200))
        self._buycard.setFillColor('white')
        self._buycard.setDepth(19)
        self._viewcard.setFillColor('white')
        self._Pass.setFillColor('white')
        self._buytext = Text("Buy Property", (225, 235), 14)
        self._buytext.setDepth(19)
        self._viewcardtext = Text("View Card", (330, 235), 14)
        self._PassText = Text("Pass", (435, 235), 14)
        
        #assigns handlers to the cards and their text
        win.add(self._buycard)
        win.add(self._viewcard)
        win.add(self._Pass)
        win.add(self._buytext)
        win.add(self._viewcardtext)
        win.add(self._PassText)
        self._buycard.addHandler(BuyController(self, self._rawpos,\
            self._properties, self._owned, self._banks, self._current,\
            self._win, self._board))
        self._buytext.addHandler(BuyController(self, self._rawpos,\
            self._properties, self._owned, self._banks, self._current,\
            self._win, self._board))
        self._viewcard.addHandler(ViewController(self, self._rawpos,\
            self._properties, self._win))
        self._viewcardtext.addHandler(ViewController(self, self._rawpos,\
            self._properties, self._win))
        self._Pass.addHandler(PassController(self, self._win))
        self._PassText.addHandler(PassController(self, self._win))
        
    def removeAll(self, win):
        """Removes the 3 cards and their text from the window."""
        
        win.remove(self._buycard)
        win.remove(self._viewcard)
        win.remove(self._Pass)
        win.remove(self._buytext)
        win.remove(self._viewcardtext)
        win.remove(self._PassText)

class ViewCardUpController(EventHandler):
    """This class handles the events for the property info card."""
    
    def __init__(self, viewclass, win):
        
        EventHandler.__init__(self)
        self._win = win
        self._viewcardclass = viewclass
        
    def handleMouseRelease(self, event):
        """When the info card is clicked, it is removed from the window."""
            
        self._viewcardclass.remove(self._win)
        
class ViewController(EventHandler):
    """This card handles the events for the view card rectangle."""
    
    def __init__(self, buyingclass, rawpos, props, win):
        
        EventHandler.__init__(self)
        self._buyingclass = buyingclass
        
        #initializes view cards for property
        self._cardrect = Rectangle(400, 400, (300, 300))
        self._cardrect.setFillColor('white')
        self._cardrect.setDepth(14)
        self._win = win
        self._properties = props
        self._rawpos = rawpos
        self._propinlist = self._properties.propertyInList(rawpos)
        self._textTitle = Text('Title Deed', (300, 125), 14)
        self._textTitle.setDepth(14)
        self._textName = Text(str(self._properties.getInfo(self._propinlist,\
            0)), (300, 150), 18)
        self._textName.setDepth(14)
        self._textPrice = Text('Price : $' + str(self._properties.getInfo\
            (self._propinlist, 2)), (300, 175), 18)
        self._textPrice.setDepth(14)
        self._textRent = Text('Rent: $' + str(self._properties.getInfo\
            (self._propinlist, 3)), (300, 200), 18)
        self._textRent.setDepth(14)
        self._textRentone = Text("With 1 House: $" + str(self.\
            _properties.getInfo(self._propinlist, 4)), (300, 225), 18)
        self._textRentone.setDepth(14)
        self._textRenttwo = Text('With 2 Houses: $' + str(self.\
            _properties.getInfo(self._propinlist, 5)), (300, 250), 18)
        self._textRenttwo.setDepth(14)
        self._textRentthree = Text('With 3 Houses: $' + str(self.\
            _properties.getInfo(self._propinlist, 6)), (300, 275), 18)
        self._textRentthree.setDepth(14)
        self._textRentfour = Text('With 4 Houses: $' + str(self.\
            _properties.getInfo(self._propinlist, 7)), (300, 300), 18)
        self._textRentfour.setDepth(14)
        self._textRenthotel = Text('With Hotel: $' + str(self.\
            _properties.getInfo(self._propinlist, 8)), (300, 325), 18)
        self._textRenthotel.setDepth(14)
        self._textHousecost = Text('Houses cost $' + str(self.\
            _properties.getInfo(self._propinlist, 9)) + ' each', (300, 350), 18)
        self._textHousecost.setDepth(14)
        
        #adds handlers tp the card and the text
        self._cardrect.addHandler(ViewCardUpController(self, self._win))
        self._textTitle.addHandler(ViewCardUpController(self, self._win))
        self._textName.addHandler(ViewCardUpController(self, self._win))
        self._textPrice.addHandler(ViewCardUpController(self, self._win))
        self._textRent.addHandler(ViewCardUpController(self, self._win))
        self._textRentone.addHandler(ViewCardUpController(self, self._win))
        self._textRenttwo.addHandler(ViewCardUpController(self, self._win))
        self._textRentthree.addHandler(ViewCardUpController(self, self._win))
        self._textRentfour.addHandler(ViewCardUpController(self, self._win))
        self._textRenthotel.addHandler(ViewCardUpController(self, self._win))
        self._textHousecost.addHandler(ViewCardUpController(self, self._win))
            
    def handleMouseRelease(self, event):
        """When the view card rectangle is clicked, an info card appears
           containing all of the property's information."""
        
        self._win.add(self._cardrect)
        self._win.add(self._textTitle)
        self._win.add(self._textName)
        self._win.add(self._textPrice)
        self._win.add(self._textRent)
        self._win.add(self._textRentone)
        self._win.add(self._textRenttwo)
        self._win.add(self._textRentthree)
        self._win.add(self._textRentfour)
        self._win.add(self._textRenthotel)
        self._win.add(self._textHousecost)
    
    def remove(self, win):
        """Removes the info card and its text."""
        
        win.remove(self._textTitle)
        win.remove(self._textName)
        win.remove(self._textPrice)
        win.remove(self._textRent)
        win.remove(self._textRentone)
        win.remove(self._textRenttwo)
        win.remove(self._textRentthree)
        win.remove(self._textRentfour)
        win.remove(self._textRenthotel)
        win.remove(self._textHousecost)
        win.remove(self._cardrect)
        
class PassController(EventHandler):
    """Serves as the event handler for the pass card."""
    
    def __init__(self, buyclass, win):
        
        EventHandler.__init__(self)
        
        self._buyclass = buyclass
        self._win = win
        
    def handleMouseRelease(self, event):
        """When the pass card is clicked, all 3 rectangles are removed from
           the window."""
        
        self._buyclass.removeAll(self._win)
        
class BuyController(EventHandler):
    """Handles the events for the buy property card."""
    
    def __init__(self, buyingclass, rawpos, props, owned, banks,\
        turn, win, board):
        
        EventHandler.__init__(self)
        
        self._win = win
        self._board = board
        self._properties = props
        self._buyingclass = buyingclass
        self._propinlist = self._properties.propertyInList(rawpos)
        self._rawposition = rawpos
        self._owned = owned
        self._banks = banks
        self._current = turn
        
    def handleMouseRelease(self, event):
        """When the buy property card is clicked, the necessary functions are
           called."""
        
        price = self._properties.getInfo(self._propinlist, 2)
        self._banks[self._current].loseMoney(price)
        self._board.updateBanks()
        self._properties.bought(self._propinlist)
        self._owned[self._current].addProp(self._rawposition)
        self._buyingclass.removeAll(self._win)
        
class PlayerBank:
    """Creates the template for a player bank"""
    
    def __init__(self):
        
        #starting money is 1500
        self._money = 1500
    
    def returnBank(self):
        """Returns the amount of money in the player bank."""
        
        return self._money
    
    def addMoney(self, value):
        """Adds a given value to the player bank."""
        
        self._money += value
        
    def loseMoney(self, value):
        """Subtracts a given value from the player bank."""
        
        self._money -= value
        
class RailRoads:
    """creates a class for the railroads, containing a list that holds
       the pertinent information for each railroad. In the list, 
       postion 0=name, 1=position, 2=price, 3=owned(true or false)"""
    
    def __init__(self):
        
        #list of railroads
        self._allRailRoads = [['Typewriter', 5, 200, False],\
            ['Pencil', 15, 200, False], ['Pen', 25, 200, False],\
            ['Feather & Ink', 35, 200, False]]
        
    def getRRInfo(self, pos, index):
        """Returns the information that is asked for based on the 
        position and index."""
            
        return self._allRailRoads[pos][index]
        
    def railroadOwned(self, pos):
        """Returns whether the railroad is owned is not"""
            
        return self._allRailRoads[pos][3]
        
    def railInList(self, rawpos):
        """Returns the railroad's place in the list."""
            
        for item in self._allRailRoads:
            if item[1] == rawpos:
                return self._allRailRoads.index(item)
                
    def bought(self, pos):
        """Sets an individual railroad in the list to bought."""
            
        self._allRailRoads[pos][3] = True
        
    def unbought(self, pos):
        """Sets an individual railroad in the list to unbought."""
        
        self._allRailRoads[pos][3] = False
            
class Utilities:
    """creates a class for the utilities. In the list for utilities,
       0=name, 1=position, 2=price, 3=owned(true or false)"""
    
    def __init__(self):
        
        #list of utilities
        self._allUtilities = [['Penguin Classics', 12, 150, False],\
            ['Random House Publishing', 28, 150, False]]
            
    def getUInfo(self, pos, index):
        """Returns the requested information based on the given
          position and index."""
            
        return self._allUtilities[pos][index]
        
    def utilityOwned(self, pos):
        """Returns whether the utility is owned or not"""
    
        return self._allUtilities[pos][3]
    
    def utilityInList(self, rawpos):
        """Returns the location of the utility in the list"""
            
        for item in self._allUtilities:
            if item[1] == rawpos:
                return self._allUtilities.index(item)
                
    def bought(self, pos):
        """Sets an individual utility to bought."""
        
        self._allUtilities[pos][3] = True
    
    def unbought(self, pos):
        """Sets an individual utility to unbought."""
        
        self._allUtilities[pos][3] = False
    
class Properties:
    """creates a class for the properties
    0. name
    1. position
    2.price
    3. rent
    4. rent with 1 house
    5. rent with 2 houses
    6. rent with 3 houses
    7. rent with 4 houses
    8. rent with hotel
    9. cost per house
    10. owned(True or False)
    11. houses on property"""
    
    def __init__(self):
    
        #list of properties
        self._allproperties = [['To Kill a Mockingbird', 1, 60, 2, 10, 30,\
            90, 160, 250, 50, False, 0],
                               ['Catcher in the Rye', 3, 60, 4, 20, 60,\
            180, 320, 450, 50, False, 0],
                               ['Lord of the Flies', 6, 100, 6, 30, 90,\
            270, 400, 550, 50, False, 0],
                               ['Lord of the Rings', 8, 100, 6, 30, 90,\
            270, 400, 550, 50, False, 0],
                               ['The Sun Also Rises', 9, 120, 8, 40, 100,\
            300, 450, 600, 50, False, 0],
                               ['Animal Farm', 11, 140, 10, 50, 150, 450,\
            625, 750, 100, False, 0],
                               ['1984', 13, 140, 10, 50, 150, 450, 625, 750,\
            100, False, 0],
                               ['Infinite Jest', 14, 160, 12, 60, 180, 500,\
            700, 900, 100, False, 0],
                               ['Atlas Shrugged', 16, 180, 14, 70, 200,\
            550, 750, 950, 100, False, 0],
                               ['Of Mice and Men', 18, 180, 14, 70, 200, 550,\
            750, 950, 100, False, 0],
                               ['Grapes of Wrath', 19, 200, 16, 80, 220, 600,\
            800, 1000, 100, False, 0],
                               ["All the King's Men", 21, 220, 18, 90, 250,\
            700, 875, 1050, 150, False, 0],
                               ['On the Road', 23, 220, 18, 90, 250,\
            700, 875, 1050, 150, False, 0],
                               ['Gone With the Wind', 24, 240, 20, 100, 300,\
            750, 925, 1100, 150, False, 0], 
                               ['Catch-22', 26, 260, 22, 110, 330, 800, 975,\
            1150, 150, False, 0], 
                               ['Moby Dick', 27, 260, 22, 110, 330, 800, 975,\
            1150, 150, False, 0], 
                               ['The Giver', 29, 280, 24, 120, 360, 850, 1025,\
            1200, 150, False, 0],
                               ['Brave New World', 31, 300, 26, 130, 390,\
            900, 1100, 1275, 200, False, 0],
                               ['Lucky Jim', 32, 300, 26, 130, 390, 900,\
            1100, 1275, 200, False, 0],
                               ['Hamlet', 34, 320, 28, 150, 450, 1000,\
            1200, 1400, 200, False, 0],
                               ['Pride and Prejudice', 37, 350, 35, 175, 500,\
            1100, 1300, 1500, 200, False], 
                               ['The Great Gatsby', 39, 400, 50, 200, 600,\
            1400, 1700, 2000, 200, False, 0]]
            
    def getInfo(self, pos, index):
        """Returns requested information based on the given
           position and index"""
            
        return self._allproperties[pos][index]
            
    def propertyOwned(self, pos):
        """Returns whether the property is owned or not"""
    
        return self._allproperties[pos][10]
    
    def propertyInList(self, rawpos):
        """Returns the location in the list of a given property."""
        
        for item in self._allproperties:
            if item[1] == rawpos:
                return self._allproperties.index(item)
        
    def bought(self, pos):
        """Sets an individual property to bought."""
        
        self._allproperties[pos][10] = True
    
    def unbought(self, pos):
        """Sets an individual property to unbought"""
        
        self._allproperties[pos][10] = False
        
class PlayerOwnings:
    """Creates a class for what a player owns."""
    
    def __init__(self):
        
        #creates empty lists for the original player ownings
        self._utilsOwned = []
        self._RROwned = []
        self._propsOwned = []
        
    def addProp(self, pos):
        """Appends a property to a player's ownings."""
        
        self._propsOwned.append(pos)
        
    def getrR(self):
        """Returns the list of a player's owned railroads."""
        
        return self._RROwned
    
    def getUtil(self):
        """Returns the list of a player's owned utilities"""
        
        return self._utilsOwned
        
    def getProps(self):
        """Returns the list of a player's owned properties."""
        
        return self._propsOwned
        
    def addRR(self, pos):
        """Appends a railroad into a player's railroad ownings."""
        
        self._RROwned.append(pos)
        
    def addUtil(self, pos):
        """Appends a railroad into a player's utility ownings."""
        
        self._utilsOwned.append(pos)
    
    def numRailRoads(self):
        """Returns the length of the list of railroads in a player's
           ownings."""
        
        return len(self._RROwned)
        
    def numUtils(self):
        """Returns the length of the list of utilities in a player's
           ownings."""
        
        return len(self._utilsOwned)
        
    def owned(self, pos):
        """Returns whether an asset is part of a player's ownings."""
        
        return pos in self._utilsOwned or pos in self._RROwned\
            or pos in self._propsOwned
            
class Die:
    """Initializes the die that is used to determine the movement of the
       pawns."""

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

    def __init__(self, board, width=25, center=(170, 260), bgcolor='white',
                 fgcolor='black'):

        #creates the attributes for the die
        self._board = board
        self._value = 6
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgcolor)
        self._square.setDepth(20)
        self._square.setBorderWidth(2)
        self._width = width
        self._center = center
        self._pips = []
        self._active = False
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgcolor)
            pip.setDepth(20)
            self._pips.append(pip)
        self._update()
    
    def addTo(self, win):
        """Adds the die to the window"""
        
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)
        
    def activate(self):
        """Activates the die."""
        
        self._active = True
        self._square.setBorderColor('green')
        
    def isActive(self):
        """Returns whether the die is active or not"""
        
        return self._active
        
    def roll(self):
        """Rolls the die"""
        
        self._value = random.randrange(Die.SIDES) + 1
        self._update()

    def getValue(self):
        """Returns the value of the die."""
        
        return self._value
        
    def _update(self):
        """Updates the die"""

        #self._text.setTextString(str(self._value))
        positions = Die.POSITIONS[self._value]
        for i in range(len(positions)):
            if positions[i] is None:
                self._pips[i].setDepth(25)
            else:
                self._pips[i].setDepth(15)
                cx, cy = self._center  # center of the die.
                dx = positions[i][0] * self._width
                dy = positions[i][1] * self._width  
                self._pips[i].moveTo((cx + dx, cy + dy))
    
class Pawn:
    """Creates the template for the pawns."""
    
    def __init__(self, board, color, ident, position):

        self._color = color
        self._board = board
        
        #identifying number for this pawn
        self._ident = ident   
        self._position = position 
        self._square = Rectangle(15, 15, (0, 0))
        self._square.setFillColor(color)
        self._square.setDepth(20)
        self._jailturns = 0
        
    def getjailcount(self):
        """Returns how many turns a pawn has spend in jail."""
        
        return self._jailturns
    
    def jailAdder(self):
        """Adds 1 to the amount of turns in jail."""
        
        self._jailturns += 1
    
    def resetcount(self):
        """Resets the jail count to zero."""
        
        self._jailturns = 0

    def addTo(self, win):
        """Adds the pawn to the window."""
        
        win.add(self._square)
    
    def removePawn(self, win):
        """Removes the pawn from the window"""
        
        win.remove(self._square)
    
    def getPosition(self):
        """Returns the position of the pawn"""
        
        return self._position
    
    def setPosition(self, pos):
        """Sets the position of the pawn"""
        
        self._position = pos
        
    def moveTo(self, location):
        """Moves the pawn to a specific location"""
        
        self._square.moveTo(location)
        
    def move(self, dx, dy):
        """Moves the pawn by an x and y value"""
        
        self._square.move(dx, dy)

class DieController(EventHandler):
    """Handles events for the die"""
    
    def __init__(self, win, board):
        
        EventHandler.__init__(self)
        self._board = board
        
        #Initializes the roll button that will handle the die's events
        self._rollbutton = (Rectangle(60, 40, (190, 300)))
        self._rollbutton.addHandler(self)
        
        #Initizalizes the die and activates them
        self._die1 = Die(self)
        self._die2 = Die(self, width=25, center=(200, 260),\
            bgcolor='white', fgcolor='black')
        self._die1.addTo(win)
        self._die2.addTo(win)
        self._die1.activate()
        self._die2.activate()
        rolltext = Text("Roll", (190, 308), 25)
        rolltext.addHandler(self)
        rolltext.setDepth(20)
        self._rollbutton.setDepth(20)
        self._rollbutton.setFillColor('Orange')
        win.add(self._rollbutton)
        win.add(rolltext)
        self._addeddie = 0
        
    def getValue(self):
        """returns added value of both die"""
        
        return self._die2.getValue() + self._die1.getValue()
        
    def handleMouseRelease(self):
        """Calls the necessary functions when the roll button is clicked"""
        
        if self._die1.isActive():
            self._die1.roll()
            self._die2.roll()
            die2val = int(self._die2.getValue())
            die1val = int(self._die1.getValue())
            doubles = die2val == die1val
            self._addeddie = die2val + die1val
            self._board.reportDieRoll(self._addeddie, doubles)

def main(win):
    """Runs board and sets the window"""
    
    run = Board(win)
    win.setHeight(600)
    win.setWidth(600)
    run.addBoard(win)

StartGraphicsSystem(main)
