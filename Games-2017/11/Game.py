"""


Game.py
By Edis Levent 
04/30/17

A program that simulates a monopoly game

"""



import random
from cs110graphics import *

class Die:
    
    """Creates a Die"""
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
                 
    def __init__(self, width=25, center=(200,200), bgcolor='white', 
                 fgcolor='black'):
                     
        """ Initializes attributes of die"""
        
        
        self._value = 1
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgcolor)
        self._square.setDepth(20)
        self._center = center
        self._width = width
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgcolor)
            pip.setDepth(20)
            self._pips.append(pip)
    
    def addTo(self, win):
        
        """Adds Pips"""
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)
        
    def roll(self):
        """ change this die's current value to a random number between 1 
            and the number of sides this die has"""
        self._value = random.randrange(Die.SIDES) + 1
        self._update()
    
    def getValue(self):
        """ return this die's current value """
        return self._value
        
        
        
    def _update(self):
        """ private method.  make the appearance of the die match
            the die's value """
        #self._text.setTextString(str(self._value))
        positions = Die.POSITIONS[self._value]
        cx, cy = self._center
        for i in range(len(positions)):
            if positions[i] == None:
                self._pips[i].setDepth(25)
            else:
                self._pips[i].setDepth(15)
                dx, dy = positions[i]
                self._pips[i].moveTo((cx + dx * self._width,
                                      cy + dy * self._width)) 
                                      
class Piece:
    
    """Creates the pieces"""
    
    def __init__(self, color):
        
        """ Initiates attributes of the pieces"""
        
        self._color = color
        self._piece = Circle(10, (75, 325))
        self._piece.setFillColor(self._color)
        
        
    def addTo(self, win):
        
        """Adds the pieces"""
        win.add(self._piece)
    
    def remove(self, win):
        
        """Removes the pieces"""
        win.remove(self._piece)
        
    def getCenter(self):
        
        """Returns center of a piece"""
        self._piece.getCenter()
        
    def moveTo(self, location):
        
        """Moves a piece"""
        self._piece.moveTo(location)
        
    def findBoardSpace(self, board):
        
        """Finds what boardspce the piece is on"""
        for i in range(len(board)):
            if board[i].getCenter() == self._piece.getCenter():
                return i


class Player:
    
    """Creats Players"""
    
    def __init__(self):   
        
        """Initiates attributes of players"""
        self._players = [Piece("red"), Piece("white"), Piece("green"),\
        Piece("blue")]
        
    def getCenter(self, playerNumber):
        
        """Gets Center of a player"""
        self._players[playerNumber].getCenter()
    
    def getPlayer(self, index):
        
        """Returns a player from player list"""
        return self._players[index]
    
    

class Money:
    
    """ Creates Money"""
    
    def __init__(self):
        
        """Initiates Attributes of Money"""                                     
        self._money = [2000, 2000, 2000, 2000]
        
        #each player starts out with 2000 dollars
        
        self._text = ""
        self._textActive = False 
        
    def value(self, playerNumber):
        
        """Returns how much money a player has"""
        return self._money[playerNumber]
    
    def add(self, quantity, playerNumber, win):
        
        """Adds money to player"""
        self._money[playerNumber] += quantity
        
        if self._textActive == False:
            
            self._text = Text(self._money[playerNumber], (150, 150), 20)
            win.add(self._text)
            self._textActive = True
            
        if self._textActive == True:
            win.remove(self._text)
            self._text = Text(self._money[playerNumber], (150, 150), 20)
            win.add(self._text)
        
        #shows money every time money changes
        
    def subtract(self, quantity, playerNumber, win):
        
        """Subtracts money from player"""
        self._money[playerNumber] -= quantity
        
        if self._textActive == False:
            
            self._text = Text(self._money[playerNumber], (150, 150), 20)
            win.add(self._text)
            self._textActive = True
            
        if self._textActive == True:
            win.remove(self._text)
            self._text = Text(self._money[playerNumber], (150, 150), 20)
            win.add(self._text)
        
        #shows money every time money changes


class PropertyCard:
    
    """Creates Property Card"""
    
    def __init__(self, center, color, value, index):
        
        """ initializes attributes of property card"""
        self._houses = 0                                       
        self._value = value
        self._center = center
        self._color = color
        self._propertyCard = Rectangle(20, 40, (self._center))
        self._propertyCard.setFillColor(self._color)
        
    def moveTo(self, location):
        
        """ moves property card"""
        self._propertyCard.moveTo(location)
    
    def addTo(self, win):
        
        """adds property card to window"""
        win.add(self._propertyCard) 
        
    
    def getColor(self):
        
        """returns color of property card"""
        return self._color
    
    def getValue(self):
        
        """returns value of property card"""
        return self._value

        
    def addHouse(self):
        
        """ adds value to property card"""
        self._value += 50 
        
        #house adds value to property
        
    def addHotel(self):
        
        """adds value to property card"""
        self._value += 100
        
        #hotal adds more value to the property
   
        

class PropertyDeck:
    
    """Creates Property Deck"""
    
    def __init__(self):
        
        """ Initializes Attributes of Deck"""
        
        self._properties = []
        
        for i in range(40):
            if i == 0:
                color = "white"
                value = 0
            if i == 1:
                color = "brown" 
                value = 100
            if i == 2:
                color = "white"
                value = 0
            if i == 3:
                color = "brown"
                value = 100
            if i == 4:
                color = "white"
                value = 0
            if i == 5:
                color = "gray"
                value = 100
            if i == 6 or  i == 8 or i == 9:
                color = "blue"
                value = 150
            if i == 7:
                color = "white"
                value = 0
            if i == 10 or i == 17 or i == 20 or i == 22 or i == 30 or i == 33:
                color = "white"
                value = 0
            if i == 36 or i == 38:
                color = "white"
                value = 0
            if i == 11 or i == 13 or i == 14:
                color = "violet"
                value = 200
            if i == 16 or i == 18 or i == 19:
                color = "orange"
                value = 250
            if i == 21 or i == 23 or i == 25:
                color = "red"
                value = 300
            if i == 26 or i == 28 or i == 29:
                color = "yellow"
                value = 350
            if i == 31 or i == 33 or i == 34:
                color = "green"
                value = 400
            if i == 37 or i == 39:
                color = "indigo"
                value = 450
            if i == 15 or i == 25 or i == 35:
                color = "gray"
                value = 100
            if i == 12 or i == 28:
                color = "white"
                value = 100
            
            self._properties.append(PropertyCard((250, 200), color, value, i))
            
            #creates a list of all properties with correct colors and positions
            
        def empty(self):
            
            """checks if property deck is empty"""
            if len(self._properties) == 0:
                return True 
        
        def propertyNumber(self, index):
            
            """ returns property of the index indicated"""
            return self._properties[index]
        
        def remove(self, index, win):
            
            """removes property"""
            self._properties.remove(self._properties[index])
            win.remove(self._properties[index])
            
        


class BoardSpace:
    """ Creates a board space """
    
    def __init__(self, board, center, borderColor, number):
        
        """ Initializes attributes of Board Space"""
        self._number = number
        self._board = board
        self._center = center
        self._borderColor = borderColor
        self._tile = Rectangle(25, 25, center)
        self._tile.setFillColor(borderColor)
    
    def addTo(self, win):
        """ Adds Board Space"""
        win.add(self._tile)
    
    def getCenter(self):
        
        """ Returns Center of Board Space"""
        return self._center
        

class Board:
    """Creates Board"""
    
    def __init__(self): 
        
        """Initializes attributes of the board"""
        self._tiles = []
        
        xpos = 75
        ypos = 325
        
        
        for i in range(40):
            if i == 0:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "black", i))
                ypos -= 25
            if i == 1:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "brown", i))
                ypos -= 25
            if i == 2:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "black", i))
                ypos -= 25
            if i == 3:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "brown", i))
                ypos -= 25
            if i == 4:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "black", i))
                ypos -= 25
            if i == 5:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "gray", i))
                ypos -= 25
            if i == 6:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "blue", i))
                ypos -= 25
            if i == 7:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "black", i))
                ypos -= 25
            if i >= 8 and i <= 9:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "blue", i))
                ypos -= 25
            if i == 10:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "black", i))
                xpos += 25
            if i == 11:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "violet", i))
                xpos += 25
            if i == 12:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "white", i))
                xpos += 25
            if i >= 13 and i <= 14:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "violet", i))
                xpos += 25
            if i == 15:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "gray", i))
                xpos += 25
            if i == 16:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "orange", i))
                xpos += 25
            if i == 17:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "black", i))
                xpos += 25
            if i >= 18 and i <= 19:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "orange", i))
                xpos += 25
            if i == 20:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "black", i))
                ypos += 25
            if i == 21:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "red", i))
                ypos += 25
            if i == 22:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "black", i))
                ypos += 25
            if i >= 23 and i <= 24:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "red", i))
                ypos += 25
            if i == 25:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "gray", i))
                ypos += 25
            if i >= 26 and i <= 27:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "yellow", i))
                ypos += 25
            if i == 28:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "white", i))
                ypos += 25
            if i == 29:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "yellow", i))
                ypos += 25
            if i == 30:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "black", i))
                xpos -= 25
            if i == 31 or i == 32:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "green", i))
                xpos -= 25
            if i == 33:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "black", i))
                xpos -= 25
            if i == 34:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "green", i))
                xpos -= 25
            if i == 35:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "gray", i))
                xpos -= 25
            if i == 36:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "black", i))
                xpos -= 25
            if i == 37:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "indigo", i))
                xpos -= 25
            if i == 38:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "black", i))
                xpos -= 25
            if i == 39:
                self._tiles.append(BoardSpace(self, (xpos, ypos), "indigo", i))
                xpos -= 25
            
            #creates a list of all tiles with correct colors and positions
        
    def getSpace(self, index):
        
        """Returns specific board space"""
        return self._tiles[index]


        
        
        

class CommunityChest:
    
    """ Creates Community Chest"""

    def __init__(self):
        
        """ Initializes Attributes of Community Chest"""
        
        self._CC = [Text("Doctors Fee: Pay 50$", (150, 120), 20),\
                Text("Bank Error in your favor: Collect 200$", (150, 120), 20),\
                Text("Pay Hospital 100$", (150, 120), 20),\
                Text("Income Tax Refund: Collect 20$", (150, 120), 20),\
                Text("You inherit 100$", (150, 120), 20)]
        
        #community chest is a list of texts from real community chest cards
        
    def addTo(self, index, win):
        
        """ Adds text to window"""
        win.add(self._CC[index])
        
    def remove(self, index, win):
        
        """ removes text from window"""
        win.remove(self._CC[index])
        
        
        
class Chance:
    
    """ Creates Chance"""
    
    def __init__(self):
        """ Initializes attributes of Chance"""
        
        self._chance = [Text("Tax: Pay 50$", (150, 120), 20), \
            Text("You recieve 100$ from the bank", (150, 120), 20), \
            Text("You dropped your wallet: Lose 100$", (150, 120), 20), \
            Text("You found 10$", (150, 120), 20), \
            Text("Tax Refund: Collect 50$", (150,120),20)]
            
            #chance is a list of texts from real community chest cards
    
    def addTo(self, index, win):
        
        """ adds text to window"""
        win.add(self._chance[index])
        
    def remove(self, index, win):
        
        """removes text from window"""
        win.remove(self._chance[index])

                                     
class Controller():
    
    """ Brings all other classes together. Not an eventhandler"""
    
    def __init__(self, win):
        """ Initializes controller attributes """
        
        
        
        self._active = [True, True, True, True]
        
        self._win = win
        
        self._die1 = Die(center=(200, 175), bgcolor='red')
        self._die2 = Die(bgcolor='red')
        
        self._die1.addTo(self._win)
        self._die2.addTo(self._win)
        
        
        
        self._CommunityChest = CommunityChest()
        self._CCindex = 0
        
        
        
        self._chance = Chance()
        self._chanceIndex = 0
        
        self._chanceCCActive = False
        
        self._text = ""
        
        
        if self._CCindex > 4:
            self._CCindex = 0
            
        if self._chanceIndex > 4:
            self._chanceIndex = 0
     
        
        
        self._board = Board()
        for tile in self._board._tiles:
            tile.addTo(win)
        
        
        self._player = Player()
        for player in self._player._players:
            player.addTo(win)
        
        
        
        
        self._properties = PropertyDeck()
        for properties in self._properties._properties:
            properties.addTo(win)
        
        
        self._money = Money()
        
        
         
        self._propActive = []
        for i in range(40):
            self._propActive.append(True)
            
            # a list to keep track of what properties have been bought
        
        self._prop0 = []
        self._prop1 = []
        self._prop2 = []
        self._prop3 = []
        
        #lists to keep track of who owns what property
        
        self._xpos0 = 75
        self._ypos0 = 375
        
        self._xpos1 = 50
        self._ypos1 = 325
        
        self._xpos2 = 75
        self._ypos2 = 25
        
        self._xpos3 = 375
        self._ypos3 = 75
        
        #initial positions for property cards to be moved to once bought

        
        self._count0 = 0
        self._count1 = 0
        self._count2 = 0
        self._count3 = 0
        self._count4 = 0
        self._count5 = 0
        self._count6 = 0
        self._count7 = 0
        
        # counts number of houses and hotels
    

        
    def movePiece0(self, win):
        
        """ Makes first player move"""
        
        player0 = self._player.getPlayer(0)
         
        dieValue1 = self._die1.getValue()
        dieValue2 = self._die2.getValue()
        move = dieValue1 + dieValue2
        
        #adds values of die to know where to move
         
        location0 = player0.findBoardSpace(self._board._tiles)
         
        if self._money.value(0) > 0:
             
            if self._active[0] == True:
                 
                location0 += move
            
                if location0 > 39:
                    location0 = location0 -  40
                    self._money.add(200, 0, self._win)         #passes go 
                                                     
                property0 = self._board.getSpace(location0)
                player0.moveTo(property0.getCenter())
                
                
                for props1 in self._prop1:
                    if location0 == props1:
                        
                        self._money.add(self._properties._properties\
                        [location0].getValue() / 10, 1, self._win)
                    
                        self._money.subtract(self._properties._properties\
                        [location0].getValue() / 10, 0, self._win)
                        
                        return
                    
                #checks if current location belongs to player1
            
                for props2 in self._prop2:
                    if location0 == props2:
                        
                        self._money.add(self._properties._properties\
                        [location0].getValue() / 10, 2, self._win)
                    
                        self._money.subtract(self._properties._properties\
                        [location0].getValue() / 10, 0, self._win)
                        
                        return
                    
                    #checks if current location belongs to player2
            
                for props3 in self._prop3:
                    if location0 == props3:
                        
                        self._money.add(self._properties._properties\
                        [location0].getValue() / 10, 3, self._win)
                    
                        self._money.subtract(self._properties._properties\
                        [location0].getValue() / 10, 0, self._win)
                        
                        return
                    
                #checks if current location belongs to player3      
            
                if location0 == 10:
                    player0.moveTo(self._board._tiles[30].getCenter())
                    
                    #go to jail 
                
                if location0 == 2 or location0 == 17 or location0 == 33:
                    
                    if self._chanceCCActive == False:
                        
                        self._text = self._CommunityChest._CC[self._CCindex]
                        self._win.add(self._text)
                        self._chanceCCActive == True
                        
                        
                        
                    if self._chanceCCActive == True:
                        
                        self._win.remove(self._text)
                        self._text = self._CommunityChest._CC[self._CCindex]
                        self._win.add(self._text)
                        
                    
                    if self._CCindex == 0:
                        self._money.subtract(50, 0, self._win)
                    if self._CCindex == 1:
                        self._money.add(200, 0, self._win)
                    if self._CCindex == 2:
                        self._money.subtract(100, 0, self._win)
                    if self._CCindex == 3:
                        self._money.add(20, 0, self._win)
                    if self._CCindex == 4:
                        self._money.add(100, 0, self._win)
                    
                    self._CCindex += 1
                        
                    #community chest
                    
                    
                if location0 == 7 or location0 == 22 or location0 == 36:
                    
                    if self._chanceCCActive == False:
                        
                        self._text = self._chance._chance[self._chanceIndex]
                        self._win.add(self._text)
                        self._chanceCCActive == True
                        
                    
                    if self._chanceCCActive == True:
                        
                        self._win.remove(self._text)
                        self._text = self._chance._chance[self._chanceIndex]
                        self._win.add(self._text)
                    
                    
                    
                    if self._chanceIndex == 0:
                        self._money.subtract(50, 0, self._win)
                    if self._chanceIndex == 1:
                        self._money.add(100, 0, self._win)
                    if self._chanceIndex == 2:
                        self._money.subtract(100, 0, self._win)
                    if self._chanceIndex == 3:
                        self._money.add(10, 0, self._win)
                    if self._chanceIndex == 4:
                        self._money.add(50, 0, self._win)
                    
                    self._chanceIndex += 1
                        
                    #chance  
                    
                   
                if location0 == 4 or location0 == 38:
                    self._money.subtract(self._money.value(0)*0.1, 0, self._win)
                    
                # tax tiles
                    

                if location0 != 0 and location0 != 2 and location0 != 4\
                and location0 != 7 and location0 != 10 and location0 != 17 \
                and location0 != 20 and location0 != 22 and location0 != 30 \
                and location0 != 33 and location0 != 36 and location0 != 38 \
                and self._propActive[location0] == True and self._money.\
                value(0) > self._properties._properties[location0].getValue():
                    
                    #makes sure that the tile is a buyable property and then 
                    #checks if it has been baught and then checks if you have 
                    #enough money to buy it
                    
                    
                    ans = input("Purchase this Property?")
                    if ans == "yes":
                        
                        self._money.subtract(self._properties.\
                        _properties[location0].getValue(), 0, self._win)
                        
                        self._prop0.append(location0)
                        
                        self._propActive[location0] = False
                        
                        text = Text(0, property0.getCenter(), 10)
                        win.add(text)
                        
                        self._properties._properties[location0].moveTo\
                        ((self._xpos0, self._ypos0))
                        
                        self._xpos0 += 25
                        
                        #deactivates property and moves property card to your 
                        #side of the board
                    
                
                self._active[0] = False
                self._active[1] = True 
                
                #this next chunk of code if for houses and hotels
                
                for props in self._prop0:
                    
                    #first we check if the player has a set of properties
                    #then we ask if he would like to purchase houses
                    #if he has 4 houses he can purchase hotels
                    #he can not have more then 4 hotels
                    
                    if props == 1 and props == 3:
                        
                        if self._count0 > 8:
                            return
                            
                        
                        if self._count0 > 4:
                            
                            answer = input("Do you want to build a hotel")
                            if answer == "yes":
                                self._properties._properties[1].addHotel()
                                self._properties._properties[3].addHotel()
                                
                                self._money.subtract(100, 0, self._win)
                                
                                self._count0 += 1
                                
                                
                                
                        
                        resp = input("Do you want to build a house")
                            
                        if resp == "yes":
                            self._properties._properties[1].addHouse()
                            self._properties._properties[3].addHouse()
                            
                            self._money.subtract(50, 0, self._win)
                            
                            self._count0 += 1
                            
                            
                        
                        

                        if props == 6 and props == 8 and props == 9:
                        
                            if self._count1 > 8:
                                return
                        
                            if self._count1 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[6].addHotel()
                                    self._properties._properties[8].addHotel()
                                    self._properties._properties[9].addHotel()
                                
                                    self._money.subtract(100, 0, self._win)
                                
                                    self._count1 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[6].addHouse()
                                self._properties._properties[8].addHouse()
                                self._properties._properties[9].addHouse()
                            
                            
                                self._money.subtract(50, 0, self._win)
                            
                                self._count1 += 1
                                
                                
                            
                        if props == 11 and props == 13 and props == 14:
                        
                            if self._count2 > 8:
                                return
                        
                            if self._count2 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[11].addHotel()
                                    self._properties._properties[13].addHotel()
                                    self._properties._properties[14].addHotel()
                                
                                    self._money.subtract(100, 0, self._win)
                                
                                    self._count2 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[11].addHouse()
                                self._properties._properties[13].addHouse()
                                self._properties._properties[14].addHouse()
                            
                            
                                self._money.subtract(50, 0, self._win)
                            
                                self._count2 += 1
                                
                                
                                
                            
                        if props == 16 and props == 18 and props == 19:
                        
                            if self._count3 > 8:
                                return
                        
                            if self._count3 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[16].addHotel()
                                    self._properties._properties[18].addHotel()
                                    self._properties._properties[19].addHotel()
                                
                                    self._money.subtract(100, 0, self._win)
                                
                                    self._count3 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[16].addHouse()
                                self._properties._properties[18].addHouse()
                                self._properties._properties[19].addHouse()
                            
                            
                                self._money.subtract(50, 0, self._win)
                            
                                self._count3 += 1
                                
                                
                                
                        
                        if props == 21 and props == 23 and props == 24:
                        
                            if self._count4 > 8:
                                return
                        
                            if self._count4 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[21].addHotel()
                                    self._properties._properties[23].addHotel()
                                    self._properties._properties[24].addHotel()
                                
                                    self._money.subtract(100, 0, self._win)
                                
                                    self._count4 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[21].addHouse()
                                self._properties._properties[23].addHouse()
                                self._properties._properties[24].addHouse()
                            
                            
                                self._money.subtract(50, 0, self._win)
                            
                                self._count4 += 1
                                
                                
                        if props == 26 and props == 27 and props == 29:
                        
                            if self._count5 > 8:
                                return
                        
                            if self._count5 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[26].addHotel()
                                    self._properties._properties[27].addHotel()
                                    self._properties._properties[29].addHotel()
                                
                                    self._money.subtract(100, 0, self._win)
                                
                                    self._count5 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[26].addHouse()
                                self._properties._properties[27].addHouse()
                                self._properties._properties[29].addHouse()
                            
                            
                                self._money.subtract(50, 0, self._win)
                            
                                self._count5 += 1
                            
                            
                            
                        if props == 31 and props == 32 and props == 34:
                        
                            if self._count6 > 8:
                                return
                        
                            if self._count6 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[31].addHotel()
                                    self._properties._properties[32].addHotel()
                                    self._properties._properties[34].addHotel()
                                
                                    self._money.subtract(100, 0, self._win)
                                
                                    self._count6 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[31].addHouse()
                                self._properties._properties[32].addHouse()
                                self._properties._properties[34].addHouse()
                            
                            
                                self._money.subtract(50, 0, self._win)
                            
                                self._count6 += 1
                                
                            
                            
                            
                        if props == 37 and props == 39:
                        
                            if self._count7 > 8:
                                return
                        
                            if self._count7 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[37].addHotel()
                                    self._properties._properties[39].addHotel()
                                    
                                
                                    self._money.subtract(100, 0, self._win)
                                
                                    self._count7 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[37].addHouse()
                                self._properties._properties[39].addHouse()
                                
                            
                            
                                self._money.subtract(50, 0, self._win)
                            
                                self._count7 += 1
                                
                                
                            return
                        
                        
    
    #same as movePiece0 just using piece 1                  
                        
    def movePiece1(self, win):
        
        """ Makes second player move"""

        player1 = self._player.getPlayer(1)
        
        dieValue1 = self._die1.getValue()
        dieValue2 = self._die2.getValue()
        move = dieValue1 + dieValue2
        
        location1 = player1.findBoardSpace(self._board._tiles)
        
        if self._money.value(1) > 0:
             
            if self._active[1] == True:
                
                
                 
                location1 += move
            
                if location1 > 39:
                    location1 = location1 -  40
                    self._money.add(200, 1, self._win)  #money when passes go  
                                                   
                property1 = self._board.getSpace(location1)
                player1.moveTo(property1.getCenter())
                
                
                for props0 in self._prop0:
                    if location1 == props0:
                        
                        self._money.add(self._properties._properties\
                        [location1].getValue() / 10, 0, self._win)
                    
                        self._money.subtract(self._properties._properties\
                        [location1].getValue() / 10, 1, self._win)
                    
                        return
            
                for props2 in self._prop2:
                    if location1 == props2:
                        
                        self._money.add(self._properties._properties\
                        [location1].getValue() / 10, 2, self._win)
                    
                        self._money.subtract(self._properties._properties\
                        [location1].getValue() / 10, 1, self._win)
                    
                        return
            
                for props3 in self._prop3:
                    if location1 == props3:
                        
                        self._money.add(self._properties._properties\
                        [location1].getValue() / 10, 3, self._win)
                    
                        self._money.subtract(self._properties._properties\
                        [location1].getValue() / 10, 1, self._win)
                    
                        return
                        
            
                if location1 == 10:
                    player1.moveTo(self._board._tiles[30].getCenter())
                    #self._active[1] = False
                    #self._active[2] = True  
                
                if location1 == 2 or location1 == 17 or location1 == 33:
                    
                    if self._chanceCCActive == False:
                        
                        self._text = self._CommunityChest._CC[self._CCindex]
                        self._win.add(self._text)
                        self._chanceCCActive = True
                        
                    if self._chanceCCActive == True:
                        
                        self._win.remove(self._text)
                        self._text = self._CommunityChest._CC[self._CCindex]
                        self._win.add(self._text)
                        
                    
                    if self._CCindex == 0:
                        self._money.subtract(50, 1, self._win)
                    if self._CCindex == 1:
                        self._money.add(200, 1, self._win)
                    if self._CCindex == 2:
                        self._money.subtract(100, 1, self._win)
                    if self._CCindex == 3:
                        self._money.add(20, 1, self._win)
                    if self._CCindex == 4:
                        self._money.add(100, 1, self._win)
                    
                    self._CCindex += 1
                        
                            
                if location1 == 7 or location1 == 22 or location1 == 36:
                    
                    if self._chanceCCActive == False:
                        
                        self._text = self._chance._chance[self._chanceIndex]
                        self._win.add(self._text)
                        self._chanceCCActive = True
                    
                    if self._chanceCCActive == True:
                        
                        self._win.remove(self._text)
                        self._text = self._chance._chance[self._chanceIndex]
                        self._win.add(self._text)
                    
                    if self._chanceIndex == 0:
                        self._money.subtract(50, 1, self._win)
                    if self._chanceIndex == 1:
                        self._money.add(100, 1, self._win)
                    if self._chanceIndex == 2:
                        self._money.subtract(100, 1, self._win)
                    if self._chanceIndex == 3:
                        self._money.add(10, 1, self._win)
                    if self._chanceIndex == 4:
                        self._money.add(50, 1, self._win)
                    
                    self._chanceIndex += 1
                    
                if location1 == 4 or location1 == 38:
                    self._money.subtract(self._money.value(1)*0.1, 1, self._win)    
               

                if location1 != 0 and location1 != 2 and location1 != 4\
                and location1 != 7 and location1 != 10 and location1 != 17 \
                and location1 != 20 and location1 != 22 and location1 != 30 \
                and location1 != 33 and location1 != 36 and location1 != 38 \
                and self._propActive[location1] == True and self._money.\
                value(1) > self._properties._properties[location1].getValue():
                    
                    ans = input("Purchase this Property?")
                    if ans == "yes":
                        
                        self._money.subtract(self._properties.\
                            _properties[location1].getValue(), 1, self._win)
                        
                        self._prop1.append(location1)
                        
                        self._propActive[location1] = False
                        
                        text = Text(1, property1.getCenter(), 10)
                        win.add(text)
                        
                        self._properties._properties[location1].moveTo\
                        ((self._xpos1, self._ypos1))
                        
                        self._ypos1 -= 25
                        
                        
                self._active[1] = False
                self._active[2] = True 
                
                      
                for props in self._prop1:
                    
                    
                    
                    if props == 1 and props == 3:
                        
                        if self._count0 > 8:
                            return
                            
                        
                        if self._count0 > 4:
                            
                            answer = input("Do you want to build a hotel")
                            if answer == "yes":
                                self._properties._properties[1].addHotel()
                                self._properties._properties[3].addHotel()
                                
                                self._money.subtract(100, 1, self._win)
                                
                                self._count0 += 1
                                
                                
                                
                        
                        resp = input("Do you want to build a house")
                            
                        if resp == "yes":
                            self._properties._properties[1].addHouse()
                            self._properties._properties[3].addHouse()
                            
                            self._money.subtract(50, 1, self._win)
                            
                            self._count0 += 1
                            
                            
                        
                        

                        if props == 6 and props == 8 and props == 9:
                        
                            if self._count1 > 8:
                                return
                        
                            if self._count1 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[6].addHotel()
                                    self._properties._properties[8].addHotel()
                                    self._properties._properties[9].addHotel()
                                
                                    self._money.subtract(100, 1, self._win)
                                
                                    self._count1 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[6].addHouse()
                                self._properties._properties[8].addHouse()
                                self._properties._properties[9].addHouse()
                            
                            
                                self._money.subtract(50, 1, self._win)
                            
                                self._count1 += 1
                                
                                
                            
                        if props == 11 and props == 13 and props == 14:
                        
                            if self._count2 > 8:
                                return
                        
                            if self._count2 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[11].addHotel()
                                    self._properties._properties[13].addHotel()
                                    self._properties._properties[14].addHotel()
                                
                                    self._money.subtract(100, 1, self._win)
                                
                                    self._count2 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[11].addHouse()
                                self._properties._properties[13].addHouse()
                                self._properties._properties[14].addHouse()
                            
                            
                                self._money.subtract(50, 1, self._win)
                            
                                self._count2 += 1
                                
                                
                                
                            
                        if props == 16 and props == 18 and props == 19:
                        
                            if self._count3 > 8:
                                return
                        
                            if self._count3 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[16].addHotel()
                                    self._properties._properties[18].addHotel()
                                    self._properties._properties[19].addHotel()
                                
                                    self._money.subtract(100, 1, self._win)
                                
                                    self._count3 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[16].addHouse()
                                self._properties._properties[18].addHouse()
                                self._properties._properties[19].addHouse()
                            
                            
                                self._money.subtract(50, 1, self._win)
                            
                                self._count3 += 1
                                
                                
                                
                        
                        if props == 21 and props == 23 and props == 24:
                        
                            if self._count4 > 8:
                                return
                        
                            if self._count4 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[21].addHotel()
                                    self._properties._properties[23].addHotel()
                                    self._properties._properties[24].addHotel()
                                
                                    self._money.subtract(100, 1, self._win)
                                
                                    self._count4 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[21].addHouse()
                                self._properties._properties[23].addHouse()
                                self._properties._properties[24].addHouse()
                            
                            
                                self._money.subtract(50, 1, self._win)
                            
                                self._count4 += 1
                                
                                
                        if props == 26 and props == 27 and props == 29:
                        
                            if self._count5 > 8:
                                return
                        
                            if self._count5 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[26].addHotel()
                                    self._properties._properties[27].addHotel()
                                    self._properties._properties[29].addHotel()
                                
                                    self._money.subtract(100, 1, self._win)
                                
                                    self._count5 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[26].addHouse()
                                self._properties._properties[27].addHouse()
                                self._properties._properties[29].addHouse()
                            
                            
                                self._money.subtract(50, 1, self._win)
                            
                                self._count5 += 1
                            
                            
                            
                        if props == 31 and props == 32 and props == 34:
                        
                            if self._count6 > 8:
                                return
                        
                            if self._count6 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[31].addHotel()
                                    self._properties._properties[32].addHotel()
                                    self._properties._properties[34].addHotel()
                                
                                    self._money.subtract(100, 1, self._win)
                                
                                    self._count6 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[31].addHouse()
                                self._properties._properties[32].addHouse()
                                self._properties._properties[34].addHouse()
                            
                            
                                self._money.subtract(50, 1, self._win)
                            
                                self._count6 += 1
                                
                            
                            
                            
                        if props == 37 and props == 39:
                        
                            if self._count7 > 8:
                                return
                        
                            if self._count7 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[37].addHotel()
                                    self._properties._properties[39].addHotel()
                                    
                                
                                    self._money.subtract(100, 1, self._win)
                                
                                    self._count7 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[37].addHouse()
                                self._properties._properties[39].addHouse()
                                
                            
                            
                                self._money.subtract(50, 1, self._win)
                            
                                self._count7 += 1
                                
                                
                            return

    
        
    #same as movepiece0 just for piece 2           
        
    def movePiece2(self, win):
        
        """ Makes third player move"""
        
        player2 = self._player.getPlayer(2)
        
        dieValue1 = self._die1.getValue()
        dieValue2 = self._die2.getValue()
        move = dieValue1 + dieValue2
        
        location2 = player2.findBoardSpace(self._board._tiles)
        
        if self._money.value(2) > 0:
             
            if self._active[2] == True:
                
                
                 
                location2 += move
            
                if location2 > 39:
                    location2 = location2 -  40
                    self._money.add(200, 2, self._win)         #passes go  
                                                     
                property2 = self._board.getSpace(location2)
                player2.moveTo(property2.getCenter())
                
                
                for props1 in self._prop1:
                    if location2 == props1:
                        
                        self._money.add(self._properties._properties\
                        [location2].getValue() / 10, 1, self._win)
                    
                        self._money.subtract(self._properties._properties\
                        [location2].getValue() / 10, 2, self._win)
                    
                        return
            
                for props0 in self._prop0:
                    if location2 == props0:
                        
                        self._money.add(self._properties._properties\
                        [location2].getValue() / 10, 0, self._win)
                    
                        self._money.subtract(self._properties._properties\
                        [location2].getValue() / 10, 2, self._win)
                    
                        return
            
                for props3 in self._prop3:
                    if location2 == props3:
                        
                        self._money.add(self._properties._properties\
                        [location2].getValue() / 10, 3, self._win)
                    
                        self._money.subtract(self._properties._properties\
                        [location2].getValue() / 10, 2, self._win)
                    
                        return
            
                    
                if location2 == 10:
                    player2.moveTo(self._board._tiles[30].getCenter())
                    
                
                if location2 == 2 or location2 == 17 or location2 == 33:
                    if self._chanceCCActive == False:
                        
                        self._text = self._CommunityChest._CC[self._CCindex]
                        self._win.add(self._text)
                        self._chanceCCActive = True
                        
                    if self._chanceCCActive == True:
                        
                        self._win.remove(self._text)
                        self._text = self._CommunityChest._CC[self._CCindex]
                        self._win.add(self._text)
                    
                    if self._CCindex == 0:
                        self._money.subtract(50, 2, self._win)
                    if self._CCindex == 1:
                        self._money.add(200, 2, self._win)
                    if self._CCindex == 2:
                        self._money.subtract(100, 2, self._win)
                    if self._CCindex == 3:
                        self._money.add(20, 2, self._win)
                    if self._CCindex == 4:
                        self._money.add(100, 2, self._win)
                    
                    self._CCindex += 1
                        
                            
                if location2 == 7 or location2 == 22 or location2 == 36:
                    
                    if self._chanceCCActive == False:
                        
                        self._text = self._chance._chance[self._chanceIndex]
                        self._win.add(self._text)
                        self._chanceCCActive = True
                    
                    if self._chanceCCActive == True:
                        
                        self._win.remove(self._text)
                        self._text = self._chance._chance[self._chanceIndex]
                        self._win.add(self._text)
                    
                    if self._chanceIndex == 0:
                        self._money.subtract(50, 2, self._win)
                    if self._chanceIndex == 1:
                        self._money.add(100, 2, self._win)
                    if self._chanceIndex == 2:
                        self._money.subtract(100, 2, self._win)
                    if self._chanceIndex == 3:
                        self._money.add(10, 2, self._win)
                    if self._chanceIndex == 4:
                        self._money.add(50, 2, self._win)
                    
                    self._chanceIndex += 1
                    
                if location2 == 4 or location2 == 38:
                    self._money.subtract(self._money.value(2)*0.1, 2, self._win)
                
                    
                #for properties in self._blankProperties:

                if location2 != 0 and location2 != 2 and location2 != 4\
                and location2 != 7 and location2 != 10 and location2 != 17 \
                and location2 != 20 and location2 != 22 and location2 != 30 \
                and location2 != 33 and location2 != 36 and location2 != 38 \
                and self._propActive[location2] == True and self._money.\
                value(2) > self._properties._properties[location2].getValue():
                    
                    ans = input("Purchase this Property?")
                    if ans == "yes":
                        
                        self._money.subtract(self._properties.\
                        _properties[location2].getValue(), 2, self._win)
                        
                        self._prop2.append(location2)
                        
                        self._propActive[location2] = False
                        
                        text = Text(2, property2.getCenter(), 10)
                        win.add(text)
                        
                        self._properties._properties[location2].moveTo\
                        ((self._xpos2, self._ypos2))
                        
                        self._xpos2 += 25
                        
                
                self._active[2] = False
                self._active[3] = True 
                
                for props in self._prop2:
                    
                    
                    
                    if props == 1 and props == 3:
                        
                        if self._count0 > 8:
                            return
                            
                        
                        if self._count0 > 4:
                            
                            answer = input("Do you want to build a hotel")
                            if answer == "yes":
                                self._properties._properties[1].addHotel()
                                self._properties._properties[3].addHotel()
                                
                                self._money.subtract(100, 2, self._win)
                                
                                self._count0 += 1
                                
                                
                                
                        
                        resp = input("Do you want to build a house")
                            
                        if resp == "yes":
                            self._properties._properties[1].addHouse()
                            self._properties._properties[3].addHouse()
                            
                            self._money.subtract(50, 2, self._win)
                            
                            self._count0 += 1
                            
                            
                        
                        

                        if props == 6 and props == 8 and props == 9:
                        
                            if self._count1 > 8:
                                return
                        
                            if self._count1 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[6].addHotel()
                                    self._properties._properties[8].addHotel()
                                    self._properties._properties[9].addHotel()
                                
                                    self._money.subtract(100, 2, self._win)
                                
                                    self._count1 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[6].addHouse()
                                self._properties._properties[8].addHouse()
                                self._properties._properties[9].addHouse()
                            
                            
                                self._money.subtract(50, 2, self._win)
                            
                                self._count1 += 1
                                
                                
                            
                        if props == 11 and props == 13 and props == 14:
                        
                            if self._count2 > 8:
                                return
                        
                            if self._count2 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[11].addHotel()
                                    self._properties._properties[13].addHotel()
                                    self._properties._properties[14].addHotel()
                                
                                    self._money.subtract(100, 2, self._win)
                                
                                    self._count2 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[11].addHouse()
                                self._properties._properties[13].addHouse()
                                self._properties._properties[14].addHouse()
                            
                            
                                self._money.subtract(50, 2, self._win)
                            
                                self._count2 += 1
                                
                                
                                
                            
                        if props == 16 and props == 18 and props == 19:
                        
                            if self._count3 > 8:
                                return
                        
                            if self._count3 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[16].addHotel()
                                    self._properties._properties[18].addHotel()
                                    self._properties._properties[19].addHotel()
                                
                                    self._money.subtract(100, 2, self._win)
                                
                                    self._count3 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[16].addHouse()
                                self._properties._properties[18].addHouse()
                                self._properties._properties[19].addHouse()
                            
                            
                                self._money.subtract(50, 2, self._win)
                            
                                self._count3 += 1
                                
                                
                                
                        
                        if props == 21 and props == 23 and props == 24:
                        
                            if self._count4 > 8:
                                return
                        
                            if self._count4 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[21].addHotel()
                                    self._properties._properties[23].addHotel()
                                    self._properties._properties[24].addHotel()
                                
                                    self._money.subtract(100, 2, self._win)
                                
                                    self._count4 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[21].addHouse()
                                self._properties._properties[23].addHouse()
                                self._properties._properties[24].addHouse()
                            
                            
                                self._money.subtract(50, 2, self._win)
                            
                                self._count4 += 1
                                
                                
                        if props == 26 and props == 27 and props == 29:
                        
                            if self._count5 > 8:
                                return
                        
                            if self._count5 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[26].addHotel()
                                    self._properties._properties[27].addHotel()
                                    self._properties._properties[29].addHotel()
                                
                                    self._money.subtract(100, 2, self._win)
                                
                                    self._count5 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[26].addHouse()
                                self._properties._properties[27].addHouse()
                                self._properties._properties[29].addHouse()
                            
                            
                                self._money.subtract(50, 2, self._win)
                            
                                self._count5 += 1
                            
                            
                            
                        if props == 31 and props == 32 and props == 34:
                        
                            if self._count6 > 8:
                                return
                        
                            if self._count6 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[31].addHotel()
                                    self._properties._properties[32].addHotel()
                                    self._properties._properties[34].addHotel()
                                
                                    self._money.subtract(100, 2, self._win)
                                
                                    self._count6 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[31].addHouse()
                                self._properties._properties[32].addHouse()
                                self._properties._properties[34].addHouse()
                            
                            
                                self._money.subtract(50, 2, self._win)
                            
                                self._count6 += 1
                                
                            
                            
                            
                        if props == 37 and props == 39:
                        
                            if self._count7 > 8:
                                return
                        
                            if self._count7 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[37].addHotel()
                                    self._properties._properties[39].addHotel()
                                    
                                
                                    self._money.subtract(100, 2, self._win)
                                
                                    self._count7 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[37].addHouse()
                                self._properties._properties[39].addHouse()
                                
                            
                            
                                self._money.subtract(50, 2, self._win)
                            
                                self._count7 += 1
                                
                                
                            return
                
               
                           
                
    #same as movepiece0 just for piece 3  
    def movePiece3(self, win):
        
        """ Makes fourth player move"""
        
        player3 = self._player.getPlayer(3)
        
        dieValue1 = self._die1.getValue()
        dieValue2 = self._die2.getValue()
        move = dieValue1 + dieValue2
        
        location3 = player3.findBoardSpace(self._board._tiles)
        
        if self._money.value(3) > 0:
             
            if self._active[3] == True:
                
                 
                location3 += move
            
                if location3 > 39:
                    location3 = location3 -  40
                    self._money.add(200, 3, self._win)         #pass go 
                                                     
                property3 = self._board.getSpace(location3)
                player3.moveTo(property3.getCenter())
                
                
                for props1 in self._prop1:
                    if location3 == props1:
                        
                        self._money.add(self._properties._properties\
                        [location3].getValue() / 10, 1, self._win)
                    
                        self._money.subtract(self._properties._properties\
                        [location3].getValue() / 10, 3, self._win)
                    
                        return
            
                for props2 in self._prop2:
                    if location3 == props2:
                        
                        self._money.add(self._properties._properties\
                        [location3].getValue() / 10, 2, self._win)
                    
                        self._money.subtract(self._properties._properties\
                        [location3].getValue() / 10, 3, self._win)
                    
                        return   
            
                for props0 in self._prop0:
                    if location3 == props0:
                        
                        self._money.add(self._properties._properties\
                        [location3].getValue() / 10, 0, self._win)
                    
                        self._money.subtract(self._properties._properties\
                        [location3].getValue() / 10, 3, self._win)
                    
                        return
                    
                if location3 == 10:
                    player3.moveTo(self._board._tiles[30].getCenter())
            
                
                if location3 == 2 or location3 == 17 or location3 == 33:
                    
                    if self._chanceCCActive == False:
                        
                        self._text = self._CommunityChest._CC[self._CCindex]
                        self._win.add(self._text)
                        self._chanceCCActive = True
                        
                    if self._chanceCCActive == True:
                        
                        self._win.remove(self._text)
                        self._text = self._CommunityChest._CC[self._CCindex]
                        self._win.add(self._text)
                    
                    if self._CCindex == 0:
                        self._money.subtract(50, 3, self._win)
                    if self._CCindex == 1:
                        self._money.add(200, 3, self._win)
                    if self._CCindex == 2:
                        self._money.subtract(100, 3, self._win)
                    if self._CCindex == 3:
                        self._money.add(20, 3, self._win)
                    if self._CCindex == 4:
                        self._money.add(100, 3, self._win)
                    
                    self._CCindex += 1
                        
                            
                if location3 == 7 or location3 == 22 or location3 == 36:
                    
                    if self._chanceCCActive == False:
                        
                        self._text = self._chance._chance[self._chanceIndex]
                        self._win.add(self._text)
                        self._chanceCCActive = True
                    
                    if self._chanceCCActive == True:
                        
                        self._win.remove(self._text)
                        self._text = self._chance._chance[self._chanceIndex]
                        self._win.add(self._text)
                    
                    if self._chanceIndex == 0:
                        self._money.subtract(50, 3, self._win)
                    if self._chanceIndex == 1:
                        self._money.add(100, 3, self._win)
                    if self._chanceIndex == 2:
                        self._money.subtract(100, 3, self._win)
                    if self._chanceIndex == 3:
                        self._money.add(10, 3, self._win)
                    if self._chanceIndex == 4:
                        self._money.add(50, 3, self._win)
                    
                    self._chanceIndex += 1
                    
                if location3 == 4 or location3 == 38:
                    self._money.subtract(self._money.value(3)*0.1, 3, self._win)    
                    
                

                if location3 != 0 and location3 != 2 and location3 != 4\
                and location3 != 7 and location3 != 10 and location3 != 17 \
                and location3 != 20 and location3 != 22 and location3 != 30 \
                and location3 != 33 and location3 != 36 and location3 != 38 \
                and self._propActive[location3] == True and self._money.\
                value(3) > self._properties._properties[location3].getValue():
                    
                    ans = input("Purchase this Property?")
                    if ans == "yes":
                        
                        self._money.subtract(self._properties.\
                        _properties[location3].getValue(), 3, self._win)
                        
                        self._prop3.append(location3)
                        
                        self._propActive[location3] = False
                        
                        text = Text(3, property3.getCenter(), 10)
                        win.add(text)
                        
                        self._properties._properties[location3].moveTo\
                        ((self._xpos3, self._ypos3))
                        
                        self._ypos3 += 25
                        
                        
                self._active[3] = False
                self._active[0] = True 
               
                for props in self._prop3:
                    
                    
                    
                    if props == 1 and props == 3:
                        
                        if self._count0 > 8:
                            return
                            
                        
                        if self._count0 > 4:
                            
                            answer = input("Do you want to build a hotel")
                            if answer == "yes":
                                self._properties._properties[1].addHotel()
                                self._properties._properties[3].addHotel()
                                
                                self._money.subtract(100, 3, self._win)
                                
                                self._count0 += 1
                                
                                
                                
                        
                        resp = input("Do you want to build a house")
                            
                        if resp == "yes":
                            self._properties._properties[1].addHouse()
                            self._properties._properties[3].addHouse()
                            
                            self._money.subtract(50, 3, self._win)
                            
                            self._count0 += 1
                            
                            
                        
                        

                        if props == 6 and props == 8 and props == 9:
                        
                            if self._count1 > 8:
                                return
                        
                            if self._count1 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[6].addHotel()
                                    self._properties._properties[8].addHotel()
                                    self._properties._properties[9].addHotel()
                                
                                    self._money.subtract(100, 3, self._win)
                                
                                    self._count1 += 1 
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[6].addHouse()
                                self._properties._properties[8].addHouse()
                                self._properties._properties[9].addHouse()
                            
                            
                                self._money.subtract(50, 3, self._win)
                            
                                self._count1 += 1
                                
                                
                            
                        if props == 11 and props == 13 and props == 14:
                        
                            if self._count2 > 8:
                                return
                        
                            if self._count2 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[11].addHotel()
                                    self._properties._properties[13].addHotel()
                                    self._properties._properties[14].addHotel()
                                
                                    self._money.subtract(100, 3, self._win)
                                
                                    self._count2 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[11].addHouse()
                                self._properties._properties[13].addHouse()
                                self._properties._properties[14].addHouse()
                            
                            
                                self._money.subtract(50, 3, self._win)
                            
                                self._count2 += 1
                                
                                
                                
                            
                        if props == 16 and props == 18 and props == 19:
                        
                            if self._count3 > 8:
                                return
                        
                            if self._count3 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[16].addHotel()
                                    self._properties._properties[18].addHotel()
                                    self._properties._properties[19].addHotel()
                                
                                    self._money.subtract(100, 3, self._win)
                                
                                    self._count3 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[16].addHouse()
                                self._properties._properties[18].addHouse()
                                self._properties._properties[19].addHouse()
                            
                            
                                self._money.subtract(50, 3, self._win)
                            
                                self._count3 += 1
                                
                                
                                
                        
                        if props == 21 and props == 23 and props == 24:
                        
                            if self._count4 > 8:
                                return
                        
                            if self._count4 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[21].addHotel()
                                    self._properties._properties[23].addHotel()
                                    self._properties._properties[24].addHotel()
                                
                                    self._money.subtract(100, 3, self._win)
                                
                                    self._count4 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[21].addHouse()
                                self._properties._properties[23].addHouse()
                                self._properties._properties[24].addHouse()
                            
                            
                                self._money.subtract(50, 3, self._win)
                            
                                self._count4 += 1
                                
                                
                        if props == 26 and props == 27 and props == 29:
                        
                            if self._count5 > 8:
                                return
                        
                            if self._count5 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[26].addHotel()
                                    self._properties._properties[27].addHotel()
                                    self._properties._properties[29].addHotel()
                                
                                    self._money.subtract(100, 3, self._win)
                                
                                    self._count5 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[26].addHouse()
                                self._properties._properties[27].addHouse()
                                self._properties._properties[29].addHouse()
                            
                            
                                self._money.subtract(50, 3, self._win)
                            
                                self._count5 += 1
                            
                            
                            
                        if props == 31 and props == 32 and props == 34:
                        
                            if self._count6 > 8:
                                return
                        
                            if self._count6 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[31].addHotel()
                                    self._properties._properties[32].addHotel()
                                    self._properties._properties[34].addHotel()
                                
                                    self._money.subtract(100, 3, self._win)
                                
                                    self._count6 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[31].addHouse()
                                self._properties._properties[32].addHouse()
                                self._properties._properties[34].addHouse()
                            
                            
                                self._money.subtract(50, 3, self._win)
                            
                                self._count6 += 1
                                
                            
                            
                            
                        if props == 37 and props == 39:
                        
                            if self._count7 > 8:
                                return
                        
                            if self._count7 > 4:
                            
                                answer = input("Do you want to build a hotel")
                                
                                if answer == "yes":
                                    self._properties._properties[37].addHotel()
                                    self._properties._properties[39].addHotel()
                                    
                                
                                    self._money.subtract(100, 3, self._win)
                                
                                    self._count7 += 1
                                
                                
                                
                                
                        
                            resp = input("Do you want to build a house")
                            
                            if resp == "yes":
                                self._properties._properties[37].addHouse()
                                self._properties._properties[39].addHouse()
                                
                            
                            
                                self._money.subtract(50, 3, self._win)
                            
                                self._count7 += 1
                                
                                
                            return
                            
                            
                           
class Controller0(EventHandler):
    
    """Event Handler"""
    
    def __init__(self, center, color, piece, controller, win):
        
        """Sets up Buttons"""
        
        EventHandler.__init__(self)
        
        self._win = win
        
        self._controLLer = controller
        
        self._die1 = self._controLLer._die1
        self._die2 = self._controLLer._die2
        
        self._color = color
        self._center = center
        self._piece = piece
        
        self._button = Rectangle(25, 25, center)
        self._button.setFillColor(self._color)
        win.add(self._button)
        self._button.addHandler(self)
        
        
        #sets up buttons. One button for each player
     
        
    def handleMouseRelease(self, event):
        
        """ Handles Mouse Release"""
        if self._piece == 0:
            
            self._die1.roll()
            self._die2.roll()
            self._controLLer.movePiece0(self._win)
                
        
            
        if self._piece == 1:
            
            self._die1.roll()
            self._die2.roll()
            self._controLLer.movePiece1(self._win)
                
        
                
        if self._piece == 2:
            
            self._die1.roll()
            self._die2.roll()
            self._controLLer.movePiece2(self._win)
                
    
            
        if self._piece == 3:
            
                
            self._die1.roll()
            self._die2.roll()
            self._controLLer.movePiece3(self._win)
                
        
        #when buttons are pressed the corresponding player moves
        

       
    
def main(win):
    
    """ Plays Game"""
    
    myController = Controller(win)
    controller0 = Controller0((350, 350), "red", 0, myController, win)
    controller1 = Controller0((350, 375), "white", 1, myController, win)
    controller2 = Controller0((375, 350), "green", 2, myController, win)
    controller3 = Controller0((375, 375), "blue", 3, myController, win)
    


    
    
    
    
    
StartGraphicsSystem(main)

