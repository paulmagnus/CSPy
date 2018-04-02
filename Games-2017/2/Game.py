"""
********************************************************************************
Name: Annie McClanahan

Project: Game.py

Due Date: May 1, 2017

Professor: Alistair Campbell

Description: This program will run the game Monopoly and implement its rules 
             until the game is complete.
********************************************************************************
"""
import random
from cs110graphics import *

def rnd(x):
    """ return a random number between 0 (inclusive) and x (exclusive) """
    return random.randrange(x)
    
def randomColor():
    """ return a random color """
    digits = "0123456789ABCDEF"
    answer = "#"
    for _ in range(6):
        answer += digits[rnd(16)]
    return answer
    
class Dice(EventHandler):
    """ This class sets up the dice that will tell each piece how many spaces to
        move """
    
    # Used class dice demonstration (class_0405_11.py) to create base for Dice 
    # Will adjust, add, and take away elements as game develops.
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
                 
    def __init__(self, board, center, width=25, bgcolor='white', 
                 fgcolor='black'):
        EventHandler.__init__(self)
        self._board = board
        self._value = 6
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgcolor)
        self._square.setDepth(20)
        self._width = width
        self._center = center
        self._pips = []
        for _ in range(Dice.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgcolor)
            pip.setDepth(25)
            self._pips.append(pip)
        self._square.addHandler(self)
        self._update() 
        
    def addTo(self, win):
        """ adds the objects of the dice to the window """
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)

    def setDepth(self, depth):
        """ sets the depth of the elements of the dice """
        self._square.setDepth(depth)
        for pip in range(len(self._pips)):
            self._pips[pip].setDepth(depth)
    
    def getDepth(self):
        """ recieves depth of obj """
        for pip in range(len(self._pips)):
            self._pips[pip].getDepth()
            
    def roll(self):
        """ changes the value of this die to a random number between 1 and 
            the number of sides of a die """
        self._value = random.randrange(Dice.SIDES) + 1
        self._update()
    
    def getValue(self):
        """ return the current value of this die """
        return self._value
    
    def _update(self):
        """ private method: make this die's appearance match its value """
        positions = Dice.POSITIONS[self._value]
        for i in range(len(positions)):
            if positions[i] is None:
                self._pips[i].setDepth(5)
            else:
                self._pips[i].setDepth(1)
                cx, cy = self._center  # center of the die.
                dx = positions[i][0] * self._width
                dy = positions[i][1] * self._width  
                self._pips[i].moveTo((cx + dx, cy + dy))
                
    def handleMousePress(self, event):
        self.roll()
        
'''class CommunityChest:
    """ Deals with when pieces land on Community Chest sqaures """
    def __init__(self, money, board):
        ComChestCards = [advanceToGo, goToJail, happyBirthday, beautyContest, 
                         holidayFunds]
        self._player = Player(win, board, location)
        self._money = money
        
    #def advanceToGo(self):
        """ moves piece to go and collects 200 dollars """
        self._money += 200
        self._player.moveTo(50, 375)
    
    def goToJail(self):
        """ moves piece to Jail square """
        self._player.moveTo(50, 50)
        
    def happyBirthday(self):
        """ collects 10 dollars from each player for your birthday """
        #for player in 
        
    def beautyContest(self):
        """ collects 10 dollars from the bank for winning second place 
            in a  beauty contest """
        self._money += 10
        
    def holidayFunds(self):
        """ collects 100 dollars from the bank for holidays """
        self._money += 100 '''
            
'''class Chance:
    """ Deals with when pieces land on Chance squares """
    def __init__(self):
        #chanceCards = [backThree, 
         
    def backThree(self):
        """ moves the piece back three spaces """ '''


class Piece(EventHandler):
    """ This class sets up the specific piece used by the player """
    
    def __init__(self, player, location, board):
        EventHandler.__init__(self)
        self._obj = Circle(10, location)
        self._location = location
        self._obj.setFillColor(randomColor())
        self._obj.addHandler(self)
        self._player = player
        self._moving = False
        self._startPos = None    # mouse position where movement started
        self._active = False
        self._board = board
        
    def setDepth(self, depth):
        """ sets depth of obj """
        self._obj.setDepth(depth)
        
    def getCenter(self):
        """ gets the center of the circle """
        return self._obj.getCenter()
        
    def activate(self):
        """ shows which piece is acting """
        self._active = True
        self._obj.setBorderColor('green')
        
    def deactivate(self):
        """ shows which pieces are not acting """
        self._active = False
        self._obj.setBorderColor('black')
    
    def addTo(self, win):
        """ adds pieces to the window """
        win.add(self._obj)
    
    def moveTo(self, pos):
        """ moves the pieces to specific locations """
        self._obj.moveTo(pos)
        self._location = pos
    
    def handleMousePress(self, event):
        """ takes turn when click on the piece """
        self._board.takeTurn()
        
class Player(EventHandler):
    """ This class sets up the players as both a piece, their money supply, and
        their properties """
        
    def __init__(self, win, board, location, properties):
        """ constructor for player in the game """
        self._piece = Piece(self, location, board)
        EventHandler.__init__(self._piece)
        self._location = location
        self._prop = properties
        self._properties = []
        self._board = board
        self._money = 1500     # the starting amount of money for each player
        self._piece.addTo(win)
        self._window = win
        self._pos = 0
        
    def activateMyPiece(self):
        """ activates the piece on the board """
        self._piece.activate()
    
    def deactivateMyPiece(self):
        """ deactivates the piece on the board """
        self._piece.deactivate()
    
    def moveTo(self, pos):
        """ moves the piece to specific location """
        self._piece.moveTo(pos)
        
    def getCenter(self):
        """ gets current center of the piece """
        location = self._piece.getCenter()
        return location
        
    def setDepth(self, depth):
        """ sets depth of pieces """
        self._piece.setDepth(depth)
    
    def buyProperty(self, location, intPos):
        """ buys the property and reduces the money supply of the player """
        cost = self._prop[intPos].propCost(location)
        self._money -= cost 
        newprop = self._prop[intPos].propName(location)
        self.moneyUpdate()
        self._properties.append(newprop)
    
    def payRent(self):
        """ subtracts the rent from the money supply of a player """
        rent = self._location.rent()
        self._money -= rent
    
    def moneyBoxes(self):
        """ adds the money to the window """
        money = Text("Money Balances", (600, 65), size=20)
        self._window.add(money)
        for i in range(4):
            moneyBalance = Text(str(self._money), (600, 140 + 100 * i),\
            size=20)
            self._window.add(moneyBalance)
            box = Rectangle(100, 75, (600, 115 + 100 * i))
            playerName = Text("Player " + str(i + 1), (600, 110 + 100 * i), \
            size=20)
            self._window.add(playerName)
            self._window.add(box)
            
    
    def moneyUpdate(self):
        """ updates money supply """
        self._window.remove(self.moneyBoxes())
        money = Text("Money Balances", (600, 65), size=20)
        self._window.add(money)
        for i in range(4):
            box = Rectangle(100, 75, (600, 115 + 100 * i))
            playerName = Text("Player " + str(i + 1), (600, 110 + 100 * i), \
            size=20)
            self._window.add(playerName)
            self._window.add(box)
            currentBalance = self.currentMoney()
            newBalance = Text(str(currentBalance), (600, 140 + 100 * i), \
            size=20)
            self._window.add(newBalance)

    def returnPos(self):
        """ returns the position on the board """
        return self._pos
        
    def currentMoney(self):
        """ returns current money value """
        return self._money
        
class Properties:
    """ This class sets up the properties/cards aspect of Monopoly """
    
    def __init__(self, name, center, width, height):
        """ Constructor for Properties Class """
        self._bspace = Rectangle(width, height, center)
        self._centers = [(100, 380), (100, 350), (100, 320), (100, 290), 
                         (100, 260), (100, 230), (100, 200), (100, 170), 
                         (100, 140), (140, 100), (170, 100), (200, 100), 
                         (230, 100), (260, 100), (290, 100), (320, 100), 
                         (350, 100), (380, 100), (420, 140), (420, 170), 
                         (420, 200), (420, 230), (420, 260), (420, 290), 
                         (420, 320), (420, 350), (420, 380), (380, 420), 
                         (350, 420), (320, 420), (290, 420), (260, 420), 
                         (230, 420), (200, 420), (170, 420), (140, 420)]
        self._colorfam = ['red', 'orange', 'yellow', 'green', 
                          'blue', 'indigo', 'violet']
        self._names = [("Mediterranean Avenue", "Baltic Avenue"),
                       ("Oriental Avenue", "Vermont Avenue", 
                        "Conneticut Avenue"),
                       ("St. Charles Place", "States Avenue", 
                        "Virginia Avenue"),
                       ("St. James Place", "Tennessee Avenue", 
                        "New York Avenue"),
                       ("Kentucky Avenue", "Indiana Avenue", "Illinois Avenue"),
                       ("Atlantic Avenue", "Ventnor Avenue", "Marvin Gardens"),
                       ("Pacific Avenue", "North Carolina Avenue", 
                        "Pennsylvania Avenue"),
                       ("Park Place", "Boardwalk"),
                       ("Reading Railroad", "Pennsylvania Railroad", 
                        "B. & O. Railroad", "Short Line"),
                       ("Electric Company", "Water Works")]
        # simplified prices for railroads and utilities for my version
        self._price = [(60, 60), (100, 100, 120), (140, 140, 160), 
                       (180, 180, 200), (220, 220, 240), (260, 260, 280), 
                       (300, 300, 320), (350, 400), (150, 150), 
                       (200, 200, 200, 200)]
        self._rent = [(2, 4), (6, 6, 8), (10, 10, 12), (14, 14, 16), 
                      (18, 18, 20), (22, 22, 24), (26, 26, 28), (35, 50), 
                      (20, 20), (25, 25, 25, 25)]
        # creates another list of the names in their order on the board
        self._posnames = ["Meditteranean Avenue", "Community Chest", 
                          "Baltic Avenue", "Income Tax", "Reading Railroad", 
                          "Oriental Avenue", "Chance", "Vermont Avenue", 
                          "Conneticut Avenue", "St. Charles Place", 
                          "Electric Company", "States Avenue", 
                          "Virginia Avenue", "Pennsylvania Railroad", 
                          "St. James Place", "Community Chest", 
                          "Tennessee Avenue", "New York Avenue", 
                          "Kentucky Avenue", "Chance", "Indiana Avenue", 
                          "Illinois Avenue", "B. & O. Railroad", 
                          "Atlantic Avenue", "Ventnor Avenue", "Water Works", 
                          "Marvin Gardens", "Pacific Avenue", 
                          "North Carolina Avenue", 
                          "Community Chest", "Pennsylvania Avenue", 
                          "Short Line", "Chance", "Park Place", "Luxury Tax", 
                          "Boardwalk"]
        
        
    def setDepth(self, depth):
        """ sets the depth of the object so board shows """
        self._bspace.setDepth(depth)
        
    def addSpace(self, win):
        """ adds space to the board """
        win.add(self._bspace)
        
    def propName(self, location):
        """ returns the name of the property """
        for i in range(len(self._centers)):
            if self._centers[i] == location:
                return str(self._posnames[i])
        
    def propCost(self, location):
        """ returns the cost of the property the piece is on """
        # gives tuple location a name from positional names list
        for i in range(len(self._centers)):
            if location == self._centers[i]:
                location = self._posnames[i]
        # finds the positional name in the original name list
        for i in range(len(self._names)):
            for n in range(len(self._names[i])):
                if location == self._names[i][n]:
                    location = self._names[i][n]
                    return self._price[i][n]
        # searches for that name in the list
        #for i in range(len(self._price)):
            #for n in range(len(self._price[i])):
                #if self._names[i][n] == self._price[i][n]:
                    #return self._price[i][n]
            
    def rent(self):
        """ returns the rent of the property the piece is on """
        for i in range(len(self._rent)):
            for n in range(len(self._rent[i])):
                if self._names[i][n] == self._rent[i][n]:
                    return self._rent[i][n]
                    
    def getCenter(self):
        """ returns the center of the properties """
        return self._bspace.getCenter()
        
    def removeProp(self, location):
        """ removes the property from the list """
        self._posnames.remove(self._posnames[location])
        
   
class Board:
    """ This class sets up the board itself and executes the game """
    
    def __init__(self, win):
        """ Constructor for Board Class """
        # attempts to add my drawing of a monopoly board to the window
        self._win = win
        image_url = "https://cs.hamilton.edu/~amcclana/images/CS_110_Monopoly_Board.JPG"
        self._background = Image(image_url, (260, 260), 410, 410)
        self._win.add(self._background)
        self._background.setDepth(27)
        self._win.setHeight(500)
        self._win.setWidth(700)
        # adds the die to the window
        self._dice = Dice(self, center=(160, 160))
        self._dice.addTo(self._win)
        self._dice2 = Dice(self, center=(360, 360))
        self._dice2.addTo(self._win)
        self._dice.setDepth(1)
        self._dice2.setDepth(1)
        
        # adds images to the board
        #center_url = "https://cs.hamilton.edu/~amcclana/images/IMG_8932.JPG"
        #self._boardcent = Image(center_url, (260, 260), 265, 265)
        #win.add(self._boardcent)
        #self._boardcent.setDepth(27)
        
        self._go = Square(50, (100, 420))
        self._jail = Square(50, (100, 100))
        self._goToJail = Square(50, (420, 420))
        self._freeParking = Square(50, (420, 100))
        self._corners = [self._go, self._jail, self._goToJail, \
        self._freeParking]
        self._cornernames = ["Go Space", "Jail Space", "Free Parking",
                             "Go to Jail"]
        for corner in self._corners:
            self._win.add(corner)
            corner.setDepth(28)
            
        # set up spaces for first side of board
        self._spaces1 = []
        self._names1 = ["Meditteranean Avenue", "Community Chest", 
                        "Baltic Avenue", "Income Tax", "Reading Railroad", 
                        "Oriental Avenue", "Chance", "Vermont Avenue", 
                        "Conneticut Avenue"]
        xpos1 = 100
        ypos1 = 380
        for name in range(len(self._names1)):
            thisSpace = Properties(name, (xpos1, ypos1), 50, 30)
            thisSpace.addSpace(self._win)
            thisSpace.setDepth(28)
            self._spaces1.append(thisSpace)
            ypos1 -= 30
            
        # set up spaces for second side of board
        self._spaces2 = []
        self._names2 = ["St. Charles Place", "Electric Company", 
                        "States Avenue", "Virginia Avenue", 
                        "Pennsylvania Railroad", "St. James Place", 
                        "Community Chest", "Tennessee Avenue", 
                        "New York Avenue"]
        xpos2 = 140
        ypos2 = 100
        for name in self._names2:
            thisSpace = Properties(name, (xpos2, ypos2), 30, 50)
            thisSpace.addSpace(self._win)
            thisSpace.setDepth(28)
            self._spaces2.append(thisSpace)
            xpos2 += 30
            
        # set up spaces for third side of board
        self._spaces3 = []
        self._names3 = ["Kentucky Avenue", "Chance", "Indiana Avenue", 
                        "Illinois Avenue", "B. & O. Railroad", 
                        "Atlantic Avenue", "Ventnor Avenue", "Water Works", 
                        "Marvin Gardens"]
        xpos3 = 420
        ypos3 = 140
        for name in self._names3:
            thisSpace = Properties(name, (xpos3, ypos3), 50, 30)
            thisSpace.addSpace(win)
            thisSpace.setDepth(28)
            self._spaces3.append(thisSpace)
            ypos3 += 30
            
        # set up fourth side of board
        self._spaces4 = []
        self._names4 = ["Pacific Avenue", "North Carolina Avenue", 
                        "Community Chest", "Pennsylvania Avenue", "Short Line", 
                        "Chance", "Park Place", "Luxury Tax", "Boardwalk"]
        xpos4 = 380     
        ypos4 = 420
        for name in self._names4:
            thisSpace = Properties(name, (xpos4, ypos4), 30, 50)
            thisSpace.addSpace(self._win)
            thisSpace.setDepth(28)
            self._spaces4.append(thisSpace)
            xpos4 -= 30

        # creates a complete list of all the spaces as Properties on the board
        self._completeProperties = []
        #self._completeProperties.append("Go Space")
        for spaces in self._spaces1:
            self._completeProperties.append(spaces)
        #self._completeProperties.append("Jail Space")
        for spaces in self._spaces2:
            self._completeProperties.append(spaces)
        #self._completeProperties.append("Go To Jail")
        for spaces in self._spaces3:
            self._completeProperties.append(spaces)
        #self._completeProperties.append("Free Parking")
        for spaces in self._spaces4:
            self._completeProperties.append(spaces)
        
        # creates a list for centers of all the spaces on the board
        self._centers = []
        self._centers.append(self._corners[0].getCenter())
        #for i in range(len(self._corners)):
            #spaceCenter = self._corners[i].getCenter()
            #self._centers.append(spaceCenter)
        for i in range(len(self._spaces1)):
            spaceCenter = self._spaces1[i].getCenter()
            self._centers.append(spaceCenter)
        self._centers.append(self._corners[1].getCenter())
        for i in range(len(self._spaces2)):
            spaceCenter = self._spaces2[i].getCenter()
            self._centers.append(spaceCenter)
        self._centers.append(self._corners[2].getCenter())
        for i in range(len(self._spaces3)):
            spaceCenter = self._spaces3[i].getCenter()
            self._centers.append(spaceCenter)
        self._centers.append(self._corners[3].getCenter())
        for i in range(len(self._spaces4)):
            spaceCenter = self._spaces4[i].getCenter()
            self._centers.append(spaceCenter)
        
        # creates a list of the space names in order
        self._completeList = []
        self._completeList.append(self._cornernames[0])
        for names in self._names1:
            self._completeList.append(names)
        self._completeList.append(self._cornernames[1])
        for names in self._names2:
            self._completeList.append(names)
        self._completeList.append(self._cornernames[2])
        for names in self._names3:
            self._completeList.append(names)
        self._completeList.append(self._cornernames[3])
        for names in self._names4:
            self._completeList.append(names)
        
        # adds players to the window
        self._players = []
        for i in range(4):
            self._players.append(Player(win, self, \
            self._centers[0], self._completeProperties))
            location = self._players[i].returnPos()
            self._players[i].setDepth(15)
            self._players[i].moneyBoxes()
        self._current = 0
        
    def landing(self, position):
        """ buys property or identifies if it is already purchased """
        property_name = self._completeList[position]
        #if isinstance(position, str) is True:
            #return
        #else:
        reply = input("Do you want to purchase " + str(property_name) + " ?\
        Answer Yes or No")
        if reply == "Yes":
            self._completeProperties.remove(self._completeProperties[position])
            self._players[self._current].buyProperty(self._centers[position],\
            position)
    
    def checkEmpty(self):
        """ sees if all the properties have been bought, game ends when all 
            properties have been purchased """
        if self._completeProperties == []:
            return True
        return
    
    def gameOver(self):
        """ finishes the game and displays winner """
        finalMoney = []
        for i in range(4):
            playerFinalBalance = self._players[i].currentMoney()
            finalMoney.append(playerFinalBalance)
            if finalMoney[0] > finalMoney[1] and finalMoney[0] > finalMoney[2] \
            and finalMoney[0] > finalMoney[3]:
                self._win.add(Text("Player 1 wins!", (350, 300), size=50))
            if finalMoney[1] > finalMoney[0] and finalMoney[1] > finalMoney[2] \
            and finalMoney[1] > finalMoney[3]:
                self._win.add(Text("Player 2 wins!", (350, 300), size=50))
            if finalMoney[2] > finalMoney[1] and finalMoney[2] > finalMoney[0] \
            and finalMoney[2] > finalMoney[3]:
                self._win.add(Text("Player 3 wins!", (350, 300), size=50))
            if finalMoney[3] > finalMoney[1] and finalMoney[3] > finalMoney[2] \
            and finalMoney[3] > finalMoney[0]:
                self._win.add(Text("Player 4 wins!", (350, 300), size=50))
    
    def changeTurn(self):
        """ changes which piece is being moved """
        self._players[self._current].deactivateMyPiece()
        self._current += 1
        self._current %= 4
        self._players[self._current].activateMyPiece()
    
    def takeTurn(self):
        """ controls the steps of each turn and moving the pieces around 
            the board"""
        self.changeTurn()
        self._dice.roll()
        self._dice2.roll()
        
        # the minus 1 keeps it from moving to the space after the spaces rolled
        numSpaces = self._dice.getValue() + self._dice2.getValue() #-1
        position = self._players[self._current].returnPos() 
        position += numSpaces
        
        # deals with when pieces must pass the Go space
        if self._players[self._current].returnPos() < 39:
            self._players[self._current].moveTo(self._centers[position])
        else:
            spaceToEnd = 39 - self._players[self._current].returnPos()
            addedSpaces = numSpaces - spaceToEnd 
            position = 0 + addedSpaces
            self._players[self._current].moveTo(self._centers[position])
        
        # deals with landing on a space and purchasing it
        self.landing(position)
        #if self.checkEmpty() is True:
            #self.gameOver()
        
def game(win):
    Board(win)

StartGraphicsSystem(game)
