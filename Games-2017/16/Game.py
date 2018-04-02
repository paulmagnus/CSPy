"""
FILE: Game.py
AUTHOR:  Henry Cohen
PARTNER: Sterling Bray
ASSIGNMENT: Project 6
DATE: 4-13-17
DESCRIPTION: The game of Monopoly

"""

import random
from cs110graphics import *

class Board:
    """Sets up Board and all necessary functions the board performs"""  
    def __init__(self, win):

        backgroundURL = "https://cs.hamilton.edu/~hcohen/images/BoardFinal.JPG"
        self._board = Image(backgroundURL, width=500, height=500)
        lampURL = "https://cs.hamilton.edu/~hcohen/images/genie1.png"
        self._lamp = Image(lampURL, width=25, height=25)
        self._lamp.setDepth(20)
        horseURL = "https://cs.hamilton.edu/~hcohen/images/horse1.png"
        self._horse = Image(horseURL, width=25, height=25)
        self._horse.setDepth(20)
        carpetURL = "https://cs.hamilton.edu/~hcohen/images/magic_carpet1.png"
        self._carpet = Image(carpetURL, width=25, height=25)
        self._carpet.setDepth(20)
        roseURL = "https://cs.hamilton.edu/~hcohen/images/rose1.png"
        self._rose = Image(roseURL, width=25, height=25)
        self._rose.setDepth(20)
        sleighURL = "https://cs.hamilton.edu/~hcohen/images/sleigh1.png"
        self._sleigh = Image(sleighURL, width=20, height=25)
        self._sleigh.setDepth(20)
        pumpkinURL = "https://cs.hamilton.edu/~hcohen/images/pump1.png"
        self._pumpkin = Image(pumpkinURL, width=25, height=25)
        self._pumpkin.setDepth(20)
        
        self.current = 0 
        self.win = win
        self._numPlayers = int(input("How many players? (2-6)"))
        colorList = ['black', 'green', 'red', 'blue', 'purple', 'yellow']
        
        
        #List of space locations
        self._locations = [(89.68181610107422, 513.9090881347656),
                           (84.68181610107422, 455.9090881347656),
                           (86.68181610107422, 415.9090881347656),
                           (84.68181610107422, 377.9090881347656),
                           (84.68181610107422, 337.9090881347656),
                           (85.68181610107422, 299.9090881347656),
                           (85.68181610107422, 259.9090881347656),
                           (82.68181610107422, 223.90908813476562),
                           (83.68181610107422, 184.90908813476562),
                           (83.68181610107422, 144.90908813476562),
                           (62.68181610107422, 67.90908813476562),
                           (144.68181610107422, 84.90908813476562),
                           (182.68181610107422, 84.90908813476562),
                           (222.68181610107422, 82.90908813476562),
                           (261.6818161010742, 81.90908813476562),
                           (299.6818161010742, 84.90908813476562),
                           (339.6818161010742, 84.90908813476562),
                           (379.6818161010742, 86.90908813476562),
                           (416.6818161010742, 85.90908813476562),
                           (455.6818161010742, 84.90908813476562),
                           (513.6818161010742, 84.90908813476562),
                           (520.6818161010742, 143.90908813476562),
                           (522.6818161010742, 184.90908813476562), 
                           (520.6818161010742, 223.90908813476562),
                           (519.6818161010742, 260.9090881347656),
                           (519.6818161010742, 300.9090881347656),
                           (520.6818161010742, 337.9090881347656),
                           (518.6818161010742, 380.9090881347656),
                           (518.6818161010742, 416.9090881347656),
                           (518.6818161010742, 455.9090881347656),
                           (515.6818161010742, 511.9090881347656),
                           (455.6818161010742, 518.9090881347656),
                           (417.6818161010742, 513.9090881347656), 
                           (376.6818161010742, 521.9090881347656),
                           (339.6818161010742, 519.9090881347656),
                           (299.6818161010742, 514.9090881347656),
                           (262.6818161010742, 518.9090881347656), 
                           (220.68181610107422, 520.9090881347656),
                           (182.68181610107422, 515.9090881347656),
                           (142.68181610107422, 518.9090881347656),
                           (102.68181610107422, 100.90908813476562)] 
        
        self.dice = DieController(win, self)
        
        #Creates a piece for each player
        self.pieces = []
        for i in range(self._numPlayers):
            thisPiece = Piece(self, colorList[i], i, 0)
            thisPiece.addTo(win)
            self.pieces.append(thisPiece)
        self.updatePieceLocations()
        
        #Creates bank for each player
        self.banks = []
        for i in range(self._numPlayers):
            thisBank = PlayerBank()
            self.banks.append(thisBank)
        self._postPlayerBanks(win)
        
        
        self._properties = PropertiesList()
        
        self._utilities = UtilitiesList()
        
        self._rr = RRList()
        
        #Creates a ownership tracker for each player
        self._owned = []
        for i in range(self._numPlayers):
            thisPlayer = PlayersOwn(self._properties, self._utilities,\
                self._rr)
            self._owned.append(thisPlayer)
        
        self._postOwnings(win)
        
        
    def spaceAction(self, pos, value):
        """Filters designated function based on piece's location"""
        
        propertyPositions = [1, 3, 6, 8, 9, 11, 13, 14, 16, 18, 19,\
                             21, 23, 24, 26, 27, 29, 31, 32, 34, 37, 39]
            
        if pos in propertyPositions:
            self.dice.dice1.deactivate()
            self.dice.dice2.deactivate()
            self.propertyAction(pos)
            
        utilityPositions = [12, 28]
            
        if pos in utilityPositions:
            self.dice.dice1.deactivate()
            self.dice.dice2.deactivate()
            self.utilityActions(pos, value)
            
        rrPositions = [5, 15, 25, 35]
        
        if pos in rrPositions:
            self.dice.dice1.deactivate()
            self.dice.dice2.deactivate()
            self.rrActions(pos)
            
        chancePositions = [7, 22, 36]
        
        if pos in chancePositions:
            self.dice.dice1.deactivate()
            self.dice.dice2.deactivate()
            ChanceActions(self)
        
        treasurePositions = [2, 17, 33]
        
        if pos in treasurePositions:
            self.dice.dice1.deactivate()
            self.dice.dice2.deactivate()
            TreasureActions(self)
        
                        

        
        
            
    def rrActions(self, pos):
        """Actions taken for a railroad property"""
        
        rrIndex = self._rr.whichProperty(pos)
        
        #If already bought. Calculates Rent and pays it.
        if not self._rr.checkBought(rrIndex):
            
            i = 0
            for item in self._owned:
                if item.isOwned(pos):
                    owner = i 
                i += 1
        
            rents = [25, 50, 100, 200]
        
            rrnumber = self._owned[owner].numRROwned()
            rent = rents[rrnumber - 1]
            
        
            self.banks[self.current].removeMoney(rent)
            
            self.banks[owner].addMoney(rent)
            
            self.dice.dice1.activate()
            self.dice.dice2.activate()
            
        #If player has enough money to buy railroad. 
        #Runs buy option function.   
        elif self.banks[self.current].getBank() >=\
            self._rr.getPrice(rrIndex):
            
            BuyingRR(self.win, self._rr,\
            pos, self._owned, self.current, self.banks, self.dice, self)
        
        
        else:
            
            self.dice.dice1.activate()
            self.dice.dice2.activate()
            

    def utilityActions(self, pos, value):
        """Actions taken for a utility"""
        
        
        utilityindex = self._utilities.whichProperty(pos)
        #If already bought. Calculates rent.
        if not self._utilities.checkBought(utilityindex):
            
            i = 0
            for item in self._owned:
                if item.isOwned(pos):
                    owner = i
                i += 1    
            if self._owned[owner].numUtilitiesOwned() == 1:
                rent = int(value * 4)
            
            else:
                rent = int(value * 10)
            
            self.banks[self.current].removeMoney(rent)
            
            self.banks[owner].addMoney(rent)
            
            self.dice.dice1.activate()
            self.dice.dice2.activate()
        
        #If player can afford utility.  Runs buy option function.
        elif self.banks[self.current].getBank() >=\
            self._utilities.getPrice(utilityindex):
                
            BuyingUtility(self.win, self._utilities,\
                pos, self._owned, self.current, self.banks, self.dice, self)
                
        else:
            
            self.dice.dice1.activate()
            self.dice.dice2.activate()
    
    
    
    
    def propertyAction(self, pos):
        """Actions taken for a property"""
        
        propertyIndex = self._properties.whichProperty(pos)
        
        #If already bought. Calculates rent.
        if not self._properties.checkBought(propertyIndex):
            
            
            rent = self._properties.getRent(propertyIndex)
            self.banks[self.current].removeMoney(rent)
            i = 0
            for item in self._owned:
                if item.isOwned(pos):
                    owner = i 
                i += 1
            self.banks[owner].addMoney(rent)
            
            self.dice.dice1.activate()
            self.dice.dice2.activate()
        
        #If player can afford property.  Runs buy option function.    
        elif self.banks[self.current].getBank() >=\
            self._properties.getPrice(propertyIndex):
            
                
            BuyingProperty(self.win, self._properties,\
                pos, self._owned, self.current, self.banks, self.dice, self)
        else:
            self.dice.dice1.activate()
            self.dice.dice2.activate()
        
        
    def playerEliminate(self):
        """Eliminates player when it runs out of money"""
        
        
        #Calculates which player is out of money. 
        #Removes all of that players data
        i = 0 
        for bank in self.banks:
            if bank.getBank() <= 0:
                player = i
                
                del self.banks[player]
                
                self.win.remove(self._bankTexts[player])
                
                del self._bankTexts[player]
        
                self.pieces[player].removeFrom(self.win)
        
                del self.pieces[player]
        
                self._numPlayers = len(self.pieces)
                
                rR = self._owned[player].returnRR()
                
                
                
                #Makes that players ownings available again
                for posRR in rR:
                    
                    indexRR = self._rr.whichProperty(posRR)
                    
                    self._rr.makeAvailable(indexRR)
                
                util = self._owned[player].returnUtility()
                
                for posU in util: 
                    
                    indexU = self._utilities.whichProperty(posU)
                    
                    self._utilities.makeAvailable(indexU)


                
                props = self._owned[player].returnProperty()
                
                for posP in props:
                    
                    indexP = self._properties.whichProperty(posP)
                    
                    self._properties.makeAvailable(indexP)
                    
                del self._owned[player]
                    
                
                
            i += 1
        
        
    def endGame(self):
        """If only one player is left, ends game"""
        
        if self._numPlayers == 1:
            
            newRect = Rectangle(600, 600, (300, 300))
            newRect.setFillColor('purple')
            newRect.setDepth(2)
            self.win.add(newRect)
            newText = Text('YOU WIN!!!', (300, 300), 26)
            newText.setDepth(1)
            self.win.add(newText)
        
    
    def reportDieRoll(self, value, doubles):
        """The functions taken when the die is rolled"""
        
        
        pos = self.pieces[self.current].getPosition()
        
        
        if pos == 30:
            
            self._jail(value, doubles)
            
       
        
        
        
        
        else: 
            #Adds $200 as player passes go
            newpos = pos + value
            
            if newpos > 39:
                
                self.banks[self.current].addMoney(200)
                
            newPosition = (pos + value) % 40
            
            
            #Tax positions on board
            if newPosition == 4:
                self.banks[self.current].removeMoney(200)
                
            if newPosition == 38:
                self.banks[self.current].removeMoney(75)
            
            
            
            self.pieces[self.current].changePosition(newPosition)
        
            self.updatePieceLocations()
            
            #Runs action to see if further action 
            #is needed for current location
            self.spaceAction(newPosition, value)
            
            self.updatePieceLocations()
            self.updatePlayerBanks()
            self.playerEliminate()
            self.endGame()
            
            #Changes turn of player if they did not roll doubles
            if doubles:
                pass
    
            else:
                
                self.changeTurn()
        
        
    
    def _jail(self, tValue, doubles):
        """The function when a piece is in jail"""
        
        #Different functionality for each turn piece has been in jail
        if self.pieces[self.current].getJailCounter() == 0:
            self.pieces[self.current].addJailCounter()
            self.updatePieceLocations()
            self.changeTurn()
            
            
        if self.pieces[self.current].getJailCounter() == 1 or\
            self.pieces[self.current].getJailCounter() == 2:
            if doubles:
                pos = 10 + tValue
                self.pieces[self.current].changePosition(pos)
                self.pieces[self.current].resetJailCounter()
                self.spaceAction(pos, tValue)
                self.updatePlayerBanks()
                self.updatePieceLocations()
                
                self.changeTurn()
                
                
            else:
                self.pieces[self.current].addJailCounter()
                self.changeTurn()
                
        if self.pieces[self.current].getJailCounter() == 3:
            if doubles:
                pos = 10 + tValue
                self.pieces[self.current].changePosition(pos)
                self.pieces[self.current].resetJailCounter()
                self.updatePieceLocations()
                self.spaceAction(pos, tValue)
                self.changeTurn()
            else:    
                pos = 10 + tValue
                self.pieces[self.current].changePosition(pos)
                self.pieces[self.current].resetJailCounter()
                self.updatePieceLocations()
                self.banks[self.current].removeMoney(50)
                self.spaceAction(pos, tValue)
                self.updatePlayerBanks()
                self.changeTurn()
        
    def _postOwnings(self, win):
        """Posts the current players ownings"""
        
        
        properties = self._owned[self.current].propOwned()
        
        utilities = self._owned[self.current].utilOwned()
        
        rr = self._owned[self.current].rrOwned()
        self._owningTexts = []
        propText = Text('Player ' + str(self.current+1) + ' properties: '+\
            str(properties), (300, 570), 12)
                    
        utilText = Text('Player ' + str(self.current+1) + ' utilities: '+\
            str(utilities), (300, 580), 12)
            
        rrText = Text('Player ' + str(self.current+1) + ' railroads: '+\
            str(rr), (300, 590), 12)
        self._owningTexts.append(propText)
        self._owningTexts.append(utilText)
        self._owningTexts.append(rrText)
        
        win.add(propText)
        win.add(utilText)
        win.add(rrText)
        
    def _updateOwnings(self):
        """Updates the current players ownings"""
        
        
        properties = self._owned[self.current].propOwned()
        
        utilities = self._owned[self.current].utilOwned()
        
        rr = self._owned[self.current].rrOwned()
        
        self._owningTexts[0].setText('Player ' + str(self.current+1) +\
            ' properties: ' + str(properties))
        
        self._owningTexts[1].setText('Player ' + str(self.current+1) +\
            ' utilities: ' + str(utilities))
        
        self._owningTexts[2].setText('Player ' + str(self.current+1) +\
            ' railroads: ' + str(rr))
            
    def _postPlayerBanks(self, win):
        """Post the players' bank totals"""
        
        #Posts bank numbers across top of window 
        dx = 0
        self._bankTexts = []
        for i in range(self._numPlayers):
            bankText = Text('Player ' + str(i + 1) + ': $' +\
                str(self.banks[i].getBank()), (50 + dx, 20), 12)
            self._bankTexts.append(bankText)
            win.add(bankText)
            dx += 90
            
    def updatePlayerBanks(self):
        """Updates the players' bank totals"""
        
        i = 0
        for text in self._bankTexts:
            text.setText('Player ' + str(i + 1) + ': $' +\
                str(self.banks[i].getBank()))
            i += 1
            
            
    def completeBoard(self, win):
        """Adds extra images to the window to complete board"""
        
        win.add(self._board)
        self._board.move(300, 300)
        win.add(self._lamp)
        self._lamp.move(520, 418.6)
        win.add(self._horse)
        self._horse.move(300, 520)
        win.add(self._carpet)
        self._carpet.move(522.7, 302)
        win.add(self._rose)
        self._rose.move(183.7, 82)
        win.add(self._sleigh)
        self._sleigh.move(74, 303)
        win.add(self._pumpkin)
        self._pumpkin.move(302, 105)
        
    def changeTurn(self):
        """Changes the current turn and highlights 
           the piece of current turn"""
        
        #Unhighlights previous piece and highlights current turns piece
        self.pieces[self.current].unhighlight()
        self.pieces[self.current].setWidthSmall()
        self.current = (self.current + 1) % len(self.pieces)
        self._updateOwnings()
        self.pieces[self.current].highlight()
        self.pieces[self.current].setWidthBig()
        
        
        
    def updatePieceLocations(self):
        """ Move the pieces to their correct locations on the window """
        
        for i in range(self._numPlayers):
            pos = self.pieces[i].getPosition()
            

            #Offsets each piece based on its location                
            if pos == 30:
                pos = 40
                offsets = [(-7.5, 0), (7.5, 0), (7.5, 7.5), (-7.5, 7.5), 
                           (7.5, -7.5), (-7.5, -7.5)]
            if pos >= 0 and pos <= 9 or pos >= 21 and pos < 30:
                offsets = [(17, -8.5), (17, 8.5), (0, -8.5), (0, 8.5),
                           (-17, -8.5), (-17, 8.5)]
            if pos == 10:
                offsets = [(51, 0), (0, 0), (0, 17), (0, 34), (17, 0), \
                           (34, 0)]  
                           
            if pos >= 11 and pos <= 20 or pos >= 31 and pos <= 39:
                offsets = [(-8.5, 17), (8.5, 17), (-8.5, 0), (8.5, 0), 
                           (-8.5, -17), (8.5, -17)] 

            
            self.pieces[i].moveTo(self._locations[pos])
            cx, cy = offsets[i]
            self.pieces[i].move(cx, cy)
        
        
    
        
        
class ChanceActions(EventHandler):
    """Creates chance cards and contains each card's actions"""
        
    def __init__(self, board):
        
        
        EventHandler.__init__(self)
        
        self._board = board
        
        self._pos = self._board.pieces[self._board.current].getPosition()
        self._chance = [['Advance to Go', self.chance0],
                        ['Found your Lost Ring. Collect $50',\
                            self.chance5],
                        ['You\'ve been Cursed. Lose $150',\
                            self.chance1],
                        ['Lost the Magic Lamp. Lose $100', self.chance6],
                        ['Lost a Necklace. Pay $15', self.chance7],
                        ['Host a Tea Party. Pay Each Player $50',\
                            self.chance10],
                        ['You win the Prince\'s Heart. Collect $150',\
                            self.chance11]]
        
        self._chanceCard = Rectangle(350, 150, (300, 300))
        self._chanceCard.setFillColor('orange')
        self._cardText = ''
        self.run()
        

        
    def chance0(self):
        """Chance card function"""
        
        self._board.pieces[self._board.current].changePosition(0)
        self._board.banks[self._board.current].addMoney(200)
        
    
    def chance1(self):        
        """Chance card function"""
        
        self._board.banks[self._board.current].removeMoney(150)
            
    def chance5(self):
        """Chance card function"""
        
        self._board.banks[self._board.current].addMoney(50)
        
    def chance6(self):
        """Chance card function"""  
            
        self._board.banks[self._board.current].removeMoney(100)
            
                
            
            
    def chance7(self):
        """Chance card function"""
        
        self._board.banks[self._board.current].removeMoney(15)
            
            
            
    def chance10(self):
        """Chance card function"""
            
        for bank in self._board.banks:
            bank.addMoney(50)
                
        number = len(self._board.banks)
        self._board.banks[self._board.current].removeMoney(50 * number)
        
    def chance11(self):
        """Chance card function""" 
            
        self._board.banks[self._board.current].addMoney(150)
        
    def run(self):
        """Runs correct function for the card and adds card to window"""
        
        
        self._x = random.randrange(len(self._chance)) #Random card
        text = self._chance[self._x][0]
        self._cardText = Text(text, (300, 300), 18)
        self._board.win.add(self._chanceCard)
        self._board.win.add(self._cardText)
        self._cardText.addHandler(self)
        self._chanceCard.addHandler(self)
        self._chance[self._x][1]() #Runs the function specified in list
        self._board.updatePieceLocations()
        self._board.updatePlayerBanks()
        
        
    def handleMouseRelease(self, event):
        """Removes card from window when clicked"""
        
        
        
        self._board.updatePieceLocations()
        self._board.updatePlayerBanks()
        
        self._board.win.remove(self._chanceCard)
        self._board.win.remove(self._cardText)
        
        
        self._board.dice.dice1.activate()
        self._board.dice.dice2.activate()
        
        
class TreasureActions(EventHandler):
    """Creates Treasure Cards and contains all related functions"""
    
    def __init__(self, board):
        
        
        EventHandler.__init__(self)
        
        self._board = board
        self._pos = self._board.pieces[self._board.current].getPosition()
        
        self._treasure = [['Advance to Go', self.treasure0],
                          ['Found a Crown. Collect $200', self.treasure1],
                          ['Ate a Poison Apple. Pay $50', self.treasure2],
                          ['A Present from the Prince. Recieve $50',\
                              self.treasure3],
                          ['Host a Feast. Collect $50 from each Player',\
                              self.treasure4],
                          ['It is your Birthday. Collect $10 from each Player',\
                              self.treasure5],
                          ['Rapunzel Let Down her Hair. Collect $100',\
                              self.treasure6],
                          ['You Lost your Glass Slippers.  Lose $150',\
                              self.treasure7],
                          ['The Flying Carpet is in the Shop . Pay $75',\
                              self.treasure8],
                          ['The Clock Strikes 12. Pay $25',\
                              self.treasure9]]

                          
        self._treasureCard = Rectangle(350, 150, (300, 300))
        self._treasureCard.setFillColor('blue')  
        self._x = 0    
        self._treasureText = ''
        self.run()

    


    def treasure0(self):
        """Function for treasure card"""
        
        self._board.pieces[self._board.current].changePosition(0)
        self._board.banks[self._board.current].addMoney(200)
    
    def treasure1(self):
        """Function for treasure card"""
        
        self._board.banks[self._board.current].addMoney(200)
        
    def treasure2(self):
        """Function for treasure card"""
        
        self._board.banks[self._board.current].removeMoney(50)
        
    def treasure3(self):
        """Function for treasure card"""
        
        self._board.banks[self._board.current].addMoney(50)
        
    def treasure4(self):
        """Function for treasure card"""
        
        for player in self._board.banks:
            
            player.removeMoney(50)
            
        multiplier = len(self._board.banks)
        
        self._board.banks[self._board.current].addMoney(50 * multiplier)
    
    def treasure5(self):
        """Function for treasure card"""
        
        for player in self._board.banks:
            
            player.removeMoney(10)
            
        multiplier = len(self._board.banks)
        
        self._board.banks[self._board.current].addMoney(10 * multiplier)

    def treasure6(self): 
        """Function for treasure card"""
        
        self._board.banks[self._board.current].addMoney(100)


    def treasure7(self):
        """Function for treasure card"""
        
        self._board.banks[self._board.current].removeMoney(150)
        
    def treasure8(self):
        """Function for treasure card"""
        
        self._board.banks[self._board.current].removeMoney(75)
        
    def treasure9(self):
        """Function for treasure card"""
        
        self._board.banks[self._board.current].removeMoney(75)
        

    def run(self):
        """Runs the correct function for the card and 
           adds card to window"""
           
        self._x = random.randrange(len(self._treasure)) #Random Card
        text = self._treasure[self._x][0]
        self._treasureText = Text(text, (300, 300), 18)
        self._board.win.add(self._treasureCard)
        self._board.win.add(self._treasureText)
        self._treasureText.addHandler(self)
        self._treasureCard.addHandler(self)
        self._treasure[self._x][1]()  #Runs the specified function
        self._board.updatePieceLocations()
        self._board.updatePlayerBanks()
        
    def handleMouseRelease(self, event):
        """Removes card when clicked"""
        
        
        self._board.updatePieceLocations()
        self._board.updatePlayerBanks()
        self._board.win.remove(self._treasureCard)
        self._board.win.remove(self._treasureText)
        
        
        self._board.dice.dice1.activate()
        self._board.dice.dice2.activate()


class PlayersOwn():
    """Tracks which properties players own"""
    
    def __init__(self, properties, utilities, rr):
        
        #List for each type of possible ownership
        self._propertiesOwned = []
        self._utilitiesOwned = []
        self._rrOwned = []
        
        self._properties = properties
        self._utilities = utilities
        self._rr = rr
        
        
    def returnRR(self):
        """Returns railroads owned"""
        
        return self._rrOwned
        
    def returnProperty(self):
        """Returns properties owned"""
        
        return self._propertiesOwned
        
    def returnUtility(self):
        """Returns utilities owned"""
        
        return self._utilitiesOwned
        
    def addProperty(self, pos):
        """Adds property to the list of properties"""
        
        self._propertiesOwned.append(pos)
        
    def addUtility(self, pos):
        """Adds utility to list of utilities"""
        
        self._utilitiesOwned.append(pos)
        
    def addRR(self, pos):
        """Adds railroad to list of railroads"""
        
        self._rrOwned.append(pos)
        
    def isOwned(self, pos):
        """Returns True if property is owned by player, False if not"""
        
        return pos in self._propertiesOwned or pos in self._utilitiesOwned\
            or pos in self._rrOwned
    
    
    def numRROwned(self):
        """Returns number of railroads owned"""
        
        return len(self._rrOwned)
        
    def numUtilitiesOwned(self):
        """Returns number of utilities owned"""
        
        return len(self._utilitiesOwned)
        
    def propOwned(self):
        """Returns a list of the names of the properties owned"""
        
        owned = []
        for item in self._propertiesOwned:
            x = self._properties.getName(item)
            owned.append(x)
        return owned
        
    def utilOwned(self):
        """Returns a list of the names of the utilities owned"""
        owned = []
        for item in self._utilitiesOwned:
            x = self._utilities.getName(item)
            owned.append(x)
        return owned
        
        
    def rrOwned(self):
        """"Returns a list of the names of the railroads owned"""
        owned = []
        for item in self._rrOwned:
            x = self._rr.getName(item)
            owned.append(x)
        return owned
        
    
        
    


class BuyingRR:
    """Creates items that can be clicked in response to
       landing on a railroad that can be bought"""
       
    def __init__(self, win, rr, pos, owned, current, bank, dice, board):
        
        self._win = win
        self._index = rr.whichProperty(pos)
        
        
        self._buyRect = Rectangle(90, 90, (200, 300))
        self._buyRect.setFillColor('white')
        self._buyText = Text('Buy Railroad', (200, 300), 16)
        win.add(self._buyRect)
        win.add(self._buyText)
        #Sets handler for buying rectangle and text
        self._buyRect.addHandler(BuyRController(self, pos, owned,\
            current, bank, rr, win, dice, board))
        self._buyText.addHandler(BuyRController(self, pos, owned,\
            current, bank, rr, win, dice, board))
        
        
        self._passRect = Rectangle(90, 90, (400, 300))
        self._passRect.setFillColor('white')
        self._passText = Text("Do Not Buy", (400, 300), 16)
        win.add(self._passRect)
        win.add(self._passText)
        #Sets handler for passing rectangle and text
        self._passRect.addHandler(PassRController(self, win, dice))
        self._passText.addHandler(PassRController(self, win, dice))
        
        self._viewRect = Rectangle(90, 90, (300, 300))
        self._viewRect.setFillColor('white')
        self._viewText = Text("View Card", (300, 300), 16)
        win.add(self._viewRect)
        win.add(self._viewText)
        #Sets handler for view card rectangle and text
        self._viewRect.addHandler(ViewRCardController(self, self._win,\
            self._index, rr))
        self._viewText.addHandler(ViewRCardController(self, self._win,\
            self._index, rr))
            
            
    
    def removeAll(self, win):
        """Removes all graphic items"""
        
        win.remove(self._buyRect)
        win.remove(self._buyText)
        win.remove(self._passRect)
        win.remove(self._passText)
        win.remove(self._viewText)
        win.remove(self._viewRect)



class BuyRController(EventHandler):
    """Controller for the buy option"""
    
    def __init__(self, buyingRR, pos, owned, current,\
        bank, rr, win, dice, board):
        
        EventHandler.__init__(self)
        self._board = board
        self._buyingRR = buyingRR
        self._dice = dice
        
        self._pos = pos
        
        self._owned = owned
        
        self._current = current
        self._win = win
        self._bank = bank
        self._rr = rr
        
    def handleMouseRelease(self, event):
        """Assigns property to player and makes appropriate 
           bank changes"""
        
        self._owned[self._current].addRR(self._pos)  #Adds it to ownership
        index = self._rr.whichProperty(self._pos)  #Finds number in list
        self._rr.makeBought(index)  #Assigns as bought
        price = self._rr.getPrice(index)  #Gets price
        self._bank[self._current].removeMoney(price) #Removes price from bank
        self._buyingRR.removeAll(self._win)
        self._board.updatePlayerBanks()
        
        self._dice.dice1.activate()
        self._dice.dice2.activate()


class PassRController(EventHandler):
    """Controller for pass option"""
    
    def __init__(self, buyingRR, win, dice):
        
        EventHandler.__init__(self)
        self._dice = dice
        self._buyingRR = buyingRR
        self._win = win
        
    def handleMouseRelease(self, event):
        """"Removes all when button is clicked and activates die"""
        
        self._buyingRR.removeAll(self._win)
        self._dice.dice1.activate()
        self._dice.dice2.activate()


class ViewRCardController(EventHandler):
    """Controller for viewing card"""
    
    def __init__(self, buyingRR, win, index, rr):
        
        EventHandler.__init__(self)
        
        self._buyingRR = buyingRR
        self._win = win
        self.card = Rectangle(300, 300, (300, 300))
        self.card.setFillColor('white')
        self.textName = Text('Name: '+ str(rr.getData(index, 0)),\
            (300, 205), 16)
        self.textPrice = Text('Price: '+ str(rr.getData(index, 1)),\
            (300, 225), 16)
        self.textRent = Text('Rent: $'+ str(rr.getData(index, 2)),\
            (300, 245), 16)
        self.textRentTwo = Text('If 2 Railroads are owned: $'+\
            str(rr.getData(index, 3)), (300, 265), 16)
        self.textRentThree = Text('If 3 Railroads are owned: $'+\
            str(rr.getData(index, 4)), (300, 285), 16)
        self.textRentFour = Text('If 4 Railroads are owned: $'+\
            str(rr.getData(index, 5)), (300, 305), 16)
        self.textMortgage = Text('Mortgage Value: ' +\
            str(rr.getData(index, 8)), (300, 325), 16)
        
        #Assigns card a handler
        self.card.addHandler(RCardUpController(self._win, self))
    
    
    def handleMouseRelease(self, event):
        """Adds every graphic of card"""
        
        self._win.add(self.card)
        self._win.add(self.textName)
        self._win.add(self.textPrice)
        self._win.add(self.textRent)
        self._win.add(self.textRentTwo)
        self._win.add(self.textRentThree)
        self._win.add(self.textRentFour)
        self._win.add(self.textMortgage)


class RCardUpController(EventHandler):
    """Controller for once card is up"""
    
    def __init__(self, win, view):
        EventHandler.__init__(self)
        self._view = view
        self._win = win
        
    def handleMouseRelease(self, event):
        """Removes aspects of card from window"""
        
        self._win.remove(self._view.card)
        self._win.remove(self._view.textName)
        self._win.remove(self._view.textPrice)
        self._win.remove(self._view.textRent)
        self._win.remove(self._view.textRentTwo)
        self._win.remove(self._view.textRentThree)
        self._win.remove(self._view.textRentFour)
        self._win.remove(self._view.textMortgage)


        
        
class BuyingUtility():
    """Class that sets up graphics for when a buyable
       utility is landed on"""
       
    def __init__(self, win, utilities, pos, owned, current, bank, dice,\
        board):
        
    
        
        self._win = win
        self._index = utilities.whichProperty(pos)
        
        self._buyRect = Rectangle(90, 90, (200, 300))
        self._buyRect.setFillColor('white')
        self._buyText = Text('Buy Utility', (200, 300), 16)
        win.add(self._buyRect)
        win.add(self._buyText)
        self._buyRect.addHandler(BuyUController(self, pos, owned,\
            current, bank, utilities, win, dice, board))
        self._buyText.addHandler(BuyUController(self, pos, owned,\
            current, bank, utilities, win, dice, board))
        
        self._passRect = Rectangle(90, 90, (400, 300))
        self._passRect.setFillColor('white')
        self._passText = Text("Do Not Buy", (400, 300), 16)
        win.add(self._passRect)
        win.add(self._passText)
        self._passRect.addHandler(PassUController(self, win, dice))
        self._passText.addHandler(PassUController(self, win, dice))
        
        self._viewRect = Rectangle(90, 90, (300, 300))
        self._viewRect.setFillColor('white')
        self._viewText = Text("View Card", (300, 300), 16)
        win.add(self._viewRect)
        win.add(self._viewText)
        self._viewRect.addHandler(ViewUCardController(self, self._win,\
            self._index, utilities))
        self._viewText.addHandler(ViewUCardController(self, self._win,\
            self._index, utilities))
            
            
    
    def removeAll(self, win):
        """Removes all graphics from window"""
        
        win.remove(self._buyRect)
        win.remove(self._buyText)
        win.remove(self._passRect)
        win.remove(self._passText)
        win.remove(self._viewText)
        win.remove(self._viewRect)
            
class BuyUController(EventHandler):
    "Controller for buying utility"""
    
    def __init__(self, buyingUtility, pos, owned, current,\
        bank, utilities, win, dice, board):
        
        EventHandler.__init__(self)
        
        self._board = board
        
        self._buyingUtility = buyingUtility
        
        self._dice = dice
        self._pos = pos
        
        self._owned = owned
        
        self._current = current
        self._win = win
        self._bank = bank
        self._utilities = utilities
        
    def handleMouseRelease(self, event):
        """Adds utility to players ownings and makes appropriate
            bank changes"""
            
        self._owned[self._current].addUtility(self._pos)
        
        index = self._utilities.whichProperty(self._pos)
        self._utilities.makeBought(index)
        price = self._utilities.getPrice(index)
        self._bank[self._current].removeMoney(price)
        self._buyingUtility.removeAll(self._win)
        self._board.updatePlayerBanks()
        self._dice.dice1.activate()
        self._dice.dice2.activate()
    
class PassUController(EventHandler):
    "Controller for passing"""
    
    def __init__(self, buyingUtility, win, dice):
        
        EventHandler.__init__(self)
        self._dice = dice
        self._buyingUtility = buyingUtility
        self._win = win
        
    def handleMouseRelease(self, event):
        """Removes all graohics from window and activates die"""
        
        self._buyingUtility.removeAll(self._win)
        self._dice.dice1.activate()
        self._dice.dice2.activate()
        

        

class ViewUCardController(EventHandler):
    "Controller for the view card button"""
    
    def __init__(self, buyingUtilities, win, index, utilities):
        
        EventHandler.__init__(self)
        
        self._buyingUtilities = buyingUtilities
        self._win = win
        self.card = Rectangle(300, 300, (300, 300))
        self.card.setFillColor('white')
        self.textName = Text('Name: '+ str(utilities.getData(index, 0)),\
            (300, 205), 16)
        self.textPrice = Text('Price: '+ str(utilities.getData(index, 6)),\
            (300, 225), 16)
        self.textRent = Text('If one utility is owned, rent is 4 times' +\
            'amount shown on die', (300, 245), 16)
        self.textRentTwo = Text('If two utilities is owned, rent is 10 times'+\
            'amount shown on die', (300, 265), 16)

        self.textMortgage = Text('Mortgage Value: ' +\
            str(utilities.getData(index, 4)), (300, 285), 16)
        
        
        self.card.addHandler(UCardUpController(self._win, self))
    
    
    def handleMouseRelease(self, event):
        """Adds all aspect of card to window"""
        
        self._win.add(self.card)
        self._win.add(self.textName)
        self._win.add(self.textPrice)
        self._win.add(self.textRent)
        self._win.add(self.textRentTwo)
        self._win.add(self.textMortgage)
        
        
class UCardUpController(EventHandler):
    """Controller for once card is up"""
    
    def __init__(self, win, view):
        EventHandler.__init__(self)
        self._view = view
        self._win = win
    
    def handleMouseRelease(self, event):
        """Removes all aspects of cards"""
        
        self._win.remove(self._view.card)
        self._win.remove(self._view.textName)
        self._win.remove(self._view.textPrice)
        self._win.remove(self._view.textRent)
        self._win.remove(self._view.textRentTwo)
        self._win.remove(self._view.textMortgage)

    
        
class BuyingProperty:
    """Sets up options for buying a property if it buyable"""
    
    def __init__(self, win, properties, pos, owned, current, bank, dice, board):
        
        self._win = win
        self._index = properties.whichProperty(pos)
        
        self._buyRect = Rectangle(90, 90, (200, 300))
        self._buyRect.setFillColor('white')
        self._buyText = Text('Buy Property', (200, 300), 16)
        win.add(self._buyRect)
        win.add(self._buyText)
        self._buyRect.addHandler(BuyController(self, pos, owned,\
            current, bank, properties, win, dice, board))
        self._buyText.addHandler(BuyController(self, pos, owned,\
            current, bank, properties, win, dice, board))
        
        self._passRect = Rectangle(90, 90, (400, 300))
        self._passRect.setFillColor('white')
        self._passText = Text("Do Not Buy", (400, 300), 16)
        win.add(self._passRect)
        win.add(self._passText)
        self._passRect.addHandler(PassController(self, win, dice))
        self._passText.addHandler(PassController(self, win, dice))
        
        self._viewRect = Rectangle(90, 90, (300, 300))
        self._viewRect.setFillColor('white')
        self._viewText = Text("View Card", (300, 300), 16)
        win.add(self._viewRect)
        win.add(self._viewText)
        self._viewRect.addHandler(ViewCardController(self, self._win,\
            self._index, properties))
        self._viewText.addHandler(ViewCardController(self, self._win,\
            self._index, properties))
        
        
        
        
    
    def removeAll(self, win):
        """Removes all graphics"""
        
        
        win.remove(self._buyRect)
        win.remove(self._buyText)
        win.remove(self._passRect)
        win.remove(self._passText)
        win.remove(self._viewText)
        win.remove(self._viewRect)
        

        
        
        
class BuyController(EventHandler):
    """Controller for buying property"""
    
    def __init__(self, buyingProperty, pos, owned, current,\
        bank, properties, win, dice, board):
        
        EventHandler.__init__(self)
        
        self._board = board
        self._buyingProperty = buyingProperty
        
        self._dice = dice
        self._pos = pos
        
        self._owned = owned
        
        self._current = current
        self._win = win
        self._bank = bank
        self._properties = properties
        
    def handleMouseRelease(self, event):
        """Adds property to player's ownings and makes
           changes to bank"""
        
        self._owned[self._current].addProperty(self._pos)
        
        index = self._properties.whichProperty(self._pos)
        self._properties.makeBought(index)
        price = self._properties.getPrice(index)
        self._bank[self._current].removeMoney(price)
        self._buyingProperty.removeAll(self._win)
        self._board.updatePlayerBanks()
        self._dice.dice1.activate()
        self._dice.dice2.activate()
        

        
class PassController(EventHandler):
    """Controller for passing option"""
    
    def __init__(self, buyingProperty, win, dice):
        
        EventHandler.__init__(self)
        
        self._buyingProperty = buyingProperty
        self._win = win
        self._dice = dice
    def handleMouseRelease(self, event):
        """Removes all graphics and activates die"""
        
        self._buyingProperty.removeAll(self._win)
        self._dice.dice1.activate()
        self._dice.dice2.activate()
        
        
class ViewCardController(EventHandler):
    """Controller for viewing card"""
    
    def __init__(self, buyingProperty, win, index, properties):
        
        EventHandler.__init__(self)
        
        self._buyingProperty = buyingProperty
        self._win = win
        self.card = Rectangle(300, 300, (300, 300))
        self.card.setFillColor('white')
        self.textName = Text('Name: '+ str(properties.getData(index, 0)),\
            (300, 205), 16)
        self.textPrice = Text('Price: '+ str(properties.getData(index, 1)),\
            (300, 225), 16)
        self.textRent = Text('Rent: '+ str(properties.getData(index, 3)),\
            (300, 245), 16)
        self.textRentOne = Text('Rent with 1 Houses: '+\
            str(properties.getData(index, 4)), (300, 265), 16)
        self.textRentTwo = Text('Rent with 2 Houses: '+\
            str(properties.getData(index, 5)), (300, 285), 16)
        self.textRentThree = Text('Rent with 3 Houses: '+\
            str(properties.getData(index, 6)), (300, 305), 16)
        self.textRentFour = Text('Rent with 4 Houses: '+\
            str(properties.getData(index, 7)), (300, 325), 16)
        self.textRentHotel = Text('Rent with Hotel: '+\
            str(properties.getData(index, 8)), (300, 345), 16)
        self.textMortgage = Text('Mortgage Value: ' +\
            str(properties.getData(index, 9)), (300, 365), 16)
        self.textHouse = Text('House Price: ' +\
            str(properties.getData(index, 10)), (300, 385), 16)
        self.card.addHandler(CardUpController(self._win, self))
    def handleMouseRelease(self, event):
        """Adds all aspects of card to window"""
        
        self._win.add(self.card)
        self._win.add(self.textName)
        self._win.add(self.textPrice)
        self._win.add(self.textRentOne)
        self._win.add(self.textRentTwo)
        self._win.add(self.textRentThree)
        self._win.add(self.textRentFour)
        self._win.add(self.textRentHotel)
        self._win.add(self.textMortgage)
        self._win.add(self.textHouse)
        
class CardUpController(EventHandler):
    """Controller for when card is up"""
    
    def __init__(self, win, view):
        EventHandler.__init__(self)
        self._view = view
        self._win = win
        
    def handleMouseRelease(self, event):
        self._win.remove(self._view.card)
        self._win.remove(self._view.textName)
        self._win.remove(self._view.textPrice)
        self._win.remove(self._view.textRentOne)
        self._win.remove(self._view.textRentTwo)
        self._win.remove(self._view.textRentThree)
        self._win.remove(self._view.textRentFour)
        self._win.remove(self._view.textRentHotel)
        self._win.remove(self._view.textMortgage)
        self._win.remove(self._view.textHouse)
    
    
    
    
class PlayerBank:
    """Holds the money numbers for each player"""
    
    def __init__(self):
        
        self._totalMoney = 1500
        
    def getBank(self):
        """Returns money total"""
        
        return self._totalMoney 
        
    def removeMoney(self, value):
        """Removes money from a player's bank"""
        
        self._totalMoney -= value
        
    def addMoney(self, value):    
        """Adds money to a player's bank"""
        
        self._totalMoney += value


class PropertiesList:
    """List of Property Values
    0: Name
    1: Price
    2: Location on Board
    3: Rent Price
    4: Rent 1 House
    5: Rent 2 House
    6: Rent 3 House
    7: Rent 4 House
    8: Rent with Hotel
    9: Mortgage Value
    10: House Cost Each
    11: Total Cost for Hotel
    12: Available or Not
    13: Current Hotels
    """
    
    def __init__(self):
        
        
        self._properties = [['Mother Goethel', 60, 1, 2, 10, 30, 90, 160, 250,\
            30, 50, 250, True], 
                            ['Rapunzel', 60, 3, 4, 20, 60, 180, 320,\
                                450, 30, 50, 250, True, 0],
                            ['Seven Dwarves', 100, 6, 6, 30, 90, 270, 400,\
                                550, 50, 50, 250, True, 0],
                            ['The Evil Queen', 100, 8, 6, 30, 90, 270, 400,\
                                550, 50, 50, 250, True, 0],
                            ['Snow White', 120, 9, 8, 40, 100, 300,\
                                450, 600, 60, 50, 250, True, 0],
                            ['Genie', 140, 11, 10, 50, 150, 450,\
                                625, 750, 70, 100, 500, True, 0], 
                            ['Jafar', 140, 13, 10, 50, 150, 450,\
                                625, 750, 70, 100, 500, True, 0], 
                            ['Jasmine', 160, 14, 12, 60, 180, 500,\
                                700, 900, 80, 100, 500, True, 0],
                            ['Olaf', 180, 16, 14, 70, 200, 550,\
                                750, 950, 90, 100, 500, True, 0],
                            ['Anna', 180, 18, 14, 70, 200, 550,\
                                750, 950, 90, 100, 500, True, 0],
                            ['Elsa', 200, 19, 16, 80, 220, 600,\
                                800, 1000, 100, 100, 500, True, 0],
                            ['Sebastian', 220, 21, 18, 90, 250, 700,\
                                875, 1050, 110, 150, 750, True, 0],
                            ['Ursula', 220, 23, 220, 21, 18, 90, 250,\
                                700, 875, 1050, 110, 150, 750, True, 0], 
                            ['Ariel', 240, 24, 20, 100, 300, 750,\
                                925, 1100, 120, 150, 750, True, 0],
                            ['Mrs. Potts', 260, 26, 22, 110, 330, 800,\
                                975, 1150, 130, 150, 750, True, 0],
                            ['Gustan', 260, 27, 260, 26, 22, 110, 330,\
                                800, 975, 1150, 130, 150, 750, True, 0],
                            ['Belle', 280, 29, 24, 120, 360, 850,\
                                1025, 1200, 140, 150, 750, True, 0],
                            ['Fairy Godmothers', 300, 31, 26, 130, 390,\
                                900, 1100, 1275, 150, 200, 1000, True, 0],
                            ['Maleficent', 300, 32, 26, 130, 390,\
                                900, 1100, 1275, 150, 200, 1000, True, 0],
                            ['Sleeping Beauty', 320, 34, 28, 150, 450,\
                                1000, 1200, 1400, 160, 200, 1000, True, 0],
                            ['Ugly Stepsisters', 350, 37, 35, 175, 500,\
                                1100, 1300, 1500, 175, 200, 1000, True, 0],
                            ['Cinderella', 400, 39, 50, 200, 600,\
                                1400, 1700, 2000, 200, 200, 1000, True, 0]]
        
        
        
    def checkBought(self, prop):
        """Returns True if property is available. False if Not"""
        
        return self._properties[prop][12]
        
        
    def numberHotels(self, prop):
        """Returns number of hotels on a given property"""
        
        return self._properties[prop][13]
        
    def addHotel(self, index, numHotels):
        """Adds hotels to property"""
        
        self._properties[index][13] += numHotels
        
    def makeBought(self, prop):
        """Sets a given property to bought"""
        
        self._properties[prop][12] = False
        
    def makeAvailable(self, prop):
        """Sets a given property to available"""
        
        self._properties[prop][12] = True
        
    def getPrice(self, index):
        """Gets price of a given property"""
        
        return self._properties[index][1]
        
    def whichProperty(self, index):
        """Takes the number space on the board and returns what
           number that property is in the property list"""
           
        for item in self._properties:  
            if item[2] == index:         # matches location on board
                return self._properties.index(item)  #Finds number in list
                
    def getRent(self, index):
        """Returns the rent of a property"""
        
        return self._properties[index][3]
        
    def getData(self, index, other):
        """Returns any data point of a property"""
        
        return self._properties[index][other]
        
    def getName(self, loc):
        """Returns name of property given its space"""
        
        for item in self._properties:
            if item[2] == loc:                
                index = self._properties.index(item)
        return self.getData(index, 0)


class UtilitiesList():
    """
    List of Utilities
    0: Name
    1: Location on Board
    2: Rent multiplier with One Owned
    3: Rent multiplier with Two Owned
    4: Mortgage Value
    5: Available or not
    6: Price
    """
    
    def __init__(self):

        
        self._utilities = [['Enchanted Rose', 12, 4, 10, 75, True, 150],
                           ['The Lamp', 28, 4, 10, 75, True, 150]]
        
        
    def getData(self, index, other):
        """Returns any data point of given utility"""
        
        return self._utilities[index][other]
        
            
    def checkBought(self, prop):
        """Checks if utility is bought"""
        
        return self._utilities[prop][5]
            
    def whichProperty(self, index):
        """Given the space of a utility on the board, returns the 
           number property in the list"""
           
        for item in self._utilities:
            if item[1] == index:
                return self._utilities.index(item)
        
    def getPrice(self, index):
        """Returns price of a given utility"""
        return self._utilities[index][6]
            
    def makeBought(self, index):
        """Sets a given utility to bought"""
        
        self._utilities[index][5] = False
        
    def makeAvailable(self, index):
        """Sets a a given utility to available"""
         
        self._utilities[index][5] = True
    
    def getName(self, loc):
        """Returns name of utility given space on board"""
        
        for item in self._utilities:
            if item[1] == loc:
                index = self._utilities.index(item)
        return self.getData(index, 0)
            

class RRList():
    """
    List of Railroads
    0: Name
    1: Price
    2: Rent
    3: Rent with 2 owned
    4: Rent with 3 owned
    5: Rent with 4 owned
    6: Location on board
    7: Available or Not
    8: Mortgage Value
    """
        
    def __init__(self):

        
        self._rr = [['Reindeer Pulled Slay', 200, 25, 50, 100, 200,\
                        5, True, 100],
                    ['Pumpkin Coach', 200, 25, 50, 100, 200, 15,\
                        True, 100],
                    ['Flying Carpet', 200, 25, 50, 100, 200, 25,\
                        True, 100],
                    ['Samson The Horse', 200, 25, 50, 100, 200, 35,\
                        True, 100]]
                        
    def getData(self, index, other):
        """ Returns any data of given railroad"""
        
        return self._rr[index][other]
            
    def makeBought(self, index):
        """Makes a given railroad bought"""
        
        self._rr[index][8] = False
        
    def makeAvailable(self, index):
        """Makes a given railroad available"""
        
        self._rr[index][8] = True
            
    def whichProperty(self, index):
        """Given a railroad's space on the board, returns
           number in list"""
           
        for item in self._rr:
            if item[6] == index:
                return self._rr.index(item)
        
    def checkBought(self, index):
        """Checks if railroad is bought"""
        
        return self._rr[index][8]
            
    def getPrice(self, index):
        """Returns price of railroad"""
        
        return self._rr[index][1]
    
    def getName(self, loc):
        """Given space location of a railroad, returns railroad name"""
        
        for item in self._rr:
            if item[6] == loc:
                index = self._rr.index(item)
        return self.getData(index, 0)

class Die():
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
                  
                 
    def __init__(self, board, width=25, center=(425, 425), bgcolor='white', 
                 fgcolor='black'):
        
        self._board = board
        self._value = 6
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgcolor)
        self._square.setBorderWidth(2)
        self._square.setDepth(20)
        self._width = width
        self._center = center
        self._active = False
        
        
            
        
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgcolor)
            pip.setDepth(20)
            self._pips.append(pip)
        
        
        self._update()
        
    def addTo(self, win):
        """Adds die to window"""
        
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)

        
    
    

    def roll(self):
        """ changes the value of this die to a random number between 1 and 
            the number of sides of a die """
            
        self._value = random.randrange(Die.SIDES) + 1
        self._update()
    
    def getValue(self):
        """ return the current value of this die """
        
        return self._value
        
    def _update(self):
        """ private method: make this die's appearance match its value """
        
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
    
    def activate(self):
        """Activates Die"""
        
        self._active = True
        self._square.setBorderColor('green')
        
    def deactivate(self):
        """Deactivates Die"""
        
        self._active = False
        self._square.setBorderColor('black')
    
    def isActive(self):
        """Returns True if die is active, false if not"""
        
        return self._active
        
    
                

        
class Piece:
    """Creates the game piece"""
    
    def __init__(self, board, color, ident, position):
        
        self._color = color
        self._board = board
        self._ident = ident   # identifying number for this pawn
        self._position = position # current logical position on the board
        self._square = Rectangle(15, 15, (92, 504))
        self._square.setDepth(1)
        self._square.setFillColor(color)
        self._jailCounter = 0
        
    def changePosition(self, value):
        """Chnages Position of Die"""
        
        self._position = value
    
    
    def getJailCounter(self):
        """Returns the jail counter"""
        
        return self._jailCounter
    
    def addJailCounter(self):
        """Adds to jail counter"""
        
        self._jailCounter += 1
        
    def resetJailCounter(self):
        """Resets the jail counter"""
        
        self._jailCounter = 0   
    
    def addTo(self, win):
        """Adds the piece to the window"""
        
        win.add(self._square)
        
    def removeFrom(self, win):
        """Removes piece from window"""
        
        win.remove(self._square)
        
    def getPosition(self):
        """Returns position of piece"""
        
        return self._position
        
    def moveTo(self, location):
        """Moves piece to a location"""
        
        self._square.moveTo(location)
        
    def move(self, dx, dy):
        """Moves piece"""
        
        self._square.move(dx, dy)
        
    def highlight(self):
        """Highlight Piece"""
        
        self._square.setBorderColor('green')
        
    def unhighlight(self):
        """Changes border of piece to black"""
        
        self._square.setBorderColor('black')
        
    def setWidthBig(self):
        """Sets border width large"""
        
        self._square.setBorderWidth(2)
        
    def setWidthSmall(self):
        """Sets the border width small"""
        
        self._square.setBorderWidth(.5)
        
    
        
class DieController(EventHandler):
    """Creates two Die and tracks their values and when
       they are rolled"""
       
    def __init__(self, win, board):
        
        EventHandler.__init__(self)
        self._board = board
        
        #Creates the two dice
        self.dice1 = Die(self)
        self.dice1.addTo(win)
        self.dice1.activate()
        self.dice2 = Die(self, center=(450, 450))
        self.dice2.addTo(win)
        self.dice2.activate()
        
        
        #Creates the button and text that rolls dice  
        self._button = Rectangle(57, 35, (406, 458))
        self._button.setFillColor('pink')
        self._button.setDepth(20)
        win.add(self._button)
        self._text = Text('Roll Dice', (406, 458), 14)
        win.add(self._text)
        self._text.setDepth(20)
        
        #Assigns self handler
        self._button.addHandler(self)
        self._text.addHandler(self)
        self._tValue = self.dice1.getValue() + self.dice2.getValue()
        
    def returnValue(self):
        """Returns total value of both die"""
        
        return self._tValue
        
    def isDoubles(self):
        """Returns true if the die values are the same,
           false if not"""
           
        return self.dice1.getValue() == self.dice2.getValue()
        
        
    def handleMouseRelease(self, event):
        
        if self.dice1.isActive():
            self.dice1.roll()
            self.dice2.roll()
            doubles = self.dice1.getValue() == self.dice2.getValue()
            self._tValue = self.dice1.getValue() + self.dice2.getValue()
            self._board.reportDieRoll(self._tValue, doubles)

def main(win):
    """Runs board and sets window up"""
    
    board = Board(win)
    win.setHeight(600)
    win.setWidth(600)
    board.completeBoard(win)

    
StartGraphicsSystem(main)
    
