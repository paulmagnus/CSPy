'''
********************************************************************************
Author:       Kyle Canelli

Partner:      Henry Golden 

Date:         05/01/17

File:         Monoply.py

Description:  This program enables the user(s) to play monopoly. 
********************************************************************************
'''

import random
from cs110graphics import *

SPACELIST = ['go', 'med', 'cc1', 'bal', 'intax', 'rr2', 'orient', 
             'cha1', 'vt', 'ct', 'jail', 'st.cha', 'elc', 'stat', 'va', 
             'rr2', 'st.jam', 'cc2', 'tn', 'nyave', 'freepark', 'ky',
             'cha2', 'in', 'il', 'rr3', 'atl', 'vet', 'ww', 'marv',
             'gotojail', 'pac', 'nc', 'cc3', 'pa', 'rr4', 'cha3', 
             'park', 'lux', 'board']
                 
SIZE = 800
WIDTH = SIZE / 13
HEIGHT = SIZE / 6.5
PRICES = [60, 60, 100, 100, 120, 140, 140, 160, 180, 180, 200, 220, 220,   
          240, 260, 260, 280, 300, 300, 320, 350, 400]
RENT = [2, 4, 6, 6, 8, 10, 10, 12, 14, 14, 16, 18, 18, 20, 22, 22, 24, 26, 
        26, 28, 35, 50]
POS = [1, 3, 6, 8, 9, 11, 13, 14, 16, 18, 19, 21, 23, 24, 26, 28, 29, 31, 
       32, 34, 37, 39]
MONEYPOS = [(200, 620), (300, 620), (400, 620), (500, 620), (600, 620)]
RRDPOS = [5, 15, 25, 35]
UTILPOS = [12, 28]
CHANCEPOS = [7, 22, 36]
CHESTPOS = [2, 17, 33]
PLAYERPOS = [(200, 600), (300, 600), (400, 600), (500, 600), (600, 600)]

MONOPLOIES = [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 
              8, 8]

SPACEPOS = [(SIZE - WIDTH, SIZE - WIDTH), (SIZE - 2.5*WIDTH, SIZE - WIDTH),
            (SIZE - 3.5*WIDTH, SIZE - WIDTH), (SIZE - 4.5*WIDTH, 
            SIZE - WIDTH), (SIZE - 5.5*WIDTH, SIZE - WIDTH),  
            (SIZE - 6.5*WIDTH, SIZE - WIDTH), (SIZE - 7.5*WIDTH, 
            SIZE - WIDTH), (SIZE - 8.5*WIDTH, SIZE - WIDTH), (SIZE - 9.5*WIDTH,
            SIZE - WIDTH), (SIZE - 10.5*WIDTH, SIZE - WIDTH),
            (WIDTH, SIZE - WIDTH), (WIDTH, 10.5*WIDTH), (WIDTH, 9.5*WIDTH), 
            (WIDTH, 8.5*WIDTH), (WIDTH, 7.5*WIDTH), 
            (WIDTH, 6.5*WIDTH), (WIDTH, 5.5*WIDTH), (WIDTH, 4.5*WIDTH),
            (WIDTH, 3.5*WIDTH), (WIDTH, 2.5*WIDTH), (WIDTH, WIDTH),
            (WIDTH*2.5, WIDTH), (WIDTH*3.5, WIDTH), (WIDTH*4.5, WIDTH),
            (WIDTH*5.5, WIDTH), (WIDTH*6.5, WIDTH), (WIDTH*7.5, WIDTH),
            (WIDTH*8.5, WIDTH), (WIDTH*9.5, WIDTH), (WIDTH*10.5, WIDTH),
            (SIZE - WIDTH, WIDTH), (SIZE - WIDTH, 2.5*WIDTH), (SIZE - WIDTH,\
            3.5*WIDTH), (SIZE - WIDTH, 4.5*WIDTH), (SIZE - WIDTH, 5.5*WIDTH),
            (SIZE - WIDTH, 6.5*WIDTH), (SIZE - WIDTH, 7.5*WIDTH), (SIZE -
            WIDTH, 8.5*WIDTH), (SIZE - WIDTH, 9.5*WIDTH), \
            (SIZE - WIDTH, 10.5*WIDTH)]

PROPNAMES = ['Mediterranean', 'Baltic', 'Oriental', 'Vermont',
             'Connecticut', 'St. Charles', 'States', 'Virgina', 
             'St. James', 'Tennessee', 'New York', 'Kentucky', 
             'Indiana', 'Illinois', 'Atlantic', 'Ventnor', 
             'Marvin Garden', 'Pacific', 'North Carolina', 
             'Pennsylvania', 'Park Place', 'Boardwalk']
RRDNAMES = ['Reading', 'Pennsylvania', 'B & O', 'Short Line']
UTILNAMES = ['Electric Company', 'Water Works']


class Board:
    '''Creates a board on which game pieces can move'''
    def __init__(self, win):
        '''initializes the attributes of the object, namely the self._tile 
       attributes'''
        width = SIZE / 13
        height = SIZE / 6.5
        kinds1 = ['prop1', 'chest', 'prop1', 'tax', 'rrd', 'prop2', 'chance',\
                  'prop2', 'prop2']
        kinds2 = ['prop3', 'prop3', 'rrd', 'prop4', 'chest', \
                  'prop4', 'prop4']
        kinds3 = ['prop5', 'chance', 'prop5', 'prop5', 'rrd', 'prop6', 'util', \
                  'prop6', 'prop6']
        kinds4 = ['prop7', 'prop7', 'chest', 'prop7', 'rrd', 'chance', 'prop8',\
                  'tax', 'prop8']
        corners = ['go', 'jail', 'freepark', 'gotojail']
        cornerMoves = [(SIZE - width, SIZE - width), (width, SIZE - width), \
                       (width, width), (SIZE - width, width)]
        xpos = 2.5
        ypos = 4.5
        self._tiles = []
        #Places the first fow of rectangular tiles
        for i in range(9):
            tile = Tiles(kinds1[i], width, height)
            tile.moveTo((SIZE - xpos * width, SIZE - width))
            self._tiles.append(tile)
            tile.addTo(win)
            xpos += 1.0
            #customizes each tile in the row
            if kinds1[i] == 'prop1':
                x = xpos - 1
                rect = Rectangle(width, height / 4)
                win.add(rect)
                rect.moveTo((SIZE - x * width, SIZE + height / 8 - height))
                rect.setFillColor("#6600cc")
            if kinds1[i] == 'prop2':
                x = xpos - 1
                rect = Rectangle(width, height / 4)
                win.add(rect)
                rect.moveTo((SIZE - x * width, SIZE + height / 8 - height))
                rect.setFillColor("#b3d1ff")
            if kinds1[i] == 'chest':
                text1 = Text('Community', (SIZE - 3.5*WIDTH, SIZE - WIDTH - 25))
                text2 = Text('Chest', (SIZE - 3.5*WIDTH, SIZE - WIDTH - 10))
                win.add(text1)
                win.add(text2)
            if kinds1[i] == 'tax':
                text1 = Text('Income Tax', (SIZE - 5.5*WIDTH, SIZE - WIDTH))
                text2 = Text('Pay $200', (SIZE - 5.5*WIDTH, SIZE - WIDTH + 15))
                win.add(text1)
                win.add(text2)
            if kinds1[i] == 'rrd':
                text1 = Text('Reading', (SIZE - 6.5*WIDTH, SIZE - WIDTH - 25))
                text2 = Text('Railroad', (SIZE - 6.5*WIDTH, SIZE - WIDTH - 10))
                win.add(text1)
                win.add(text2)
            if kinds1[i] == 'chance':
                text1 = Text('Chance', (SIZE - 8.5*WIDTH, SIZE - WIDTH - 35))
                win.add(text1)
        #Places second row of tiles
        rect1 = Tiles('prop3', height, width)
        rect1.moveTo((WIDTH, 10.5*width))
        rect2 = Tiles('util', height, width)
        rect2.moveTo((WIDTH, 9.5*width))
        rect1.addTo(win)
        rect2.addTo(win)
        self._tiles.append(rect1)
        self._tiles.append(rect2)
        
        for i in range(7):
            tile = Tiles(kinds2[i], height, width)
            tile.moveTo((width, SIZE - ypos * width))
            self._tiles.append(tile)
            tile.addTo(win)
            ypos += 1.0
            #Customizes the tiles in the row
            if kinds2[i] == 'prop3':
                y = ypos - 1
                rect = Rectangle(height / 4, width)
                win.add(rect)
                rect.moveTo((height - height / 8, SIZE - y * width))
                rect.setFillColor("#cc0099")
            if kinds2[i] == 'prop4':
                y = ypos - 1
                rect = Rectangle(height / 4, width)
                win.add(rect)
                rect.moveTo((height - height / 8, SIZE - y * width))
                rect.setFillColor("#ff8533")
            if kinds2[i] == 'util':
                text1 = Text('Electric Company', (WIDTH, 9.5*WIDTH + 25))
                win.add(text1)
            if kinds2[i] == 'rrd':
                text1 = Text('Penn Railroad', (WIDTH +8.5, 6.5*WIDTH + 25), 9.5)
                win.add(text1)
            if kinds2[i] == 'chest':
                text1 = Text('Community Chest', (WIDTH + 20, 4.5*WIDTH - 20), 9)
                win.add(text1)

        xpos = 2.5
        #Place third row of tiles
        for i in range(9):
            tile = Tiles(kinds3[i], width, height)
            tile.moveTo((xpos * width, width))
            self._tiles.append(tile)
            tile.addTo(win)
            xpos += 1.0
             #Customizes the tiles in the row
            if kinds3[i] == 'prop5':
                x = xpos - 1
                rect = Rectangle(width, height / 4)
                win.add(rect)
                rect.moveTo((x * width, height - height / 8))
                rect.setFillColor("#ff0000")
            if kinds3[i] == 'prop6':
                x = xpos - 1
                rect = Rectangle(width, height / 4)
                win.add(rect)
                rect.moveTo((x * width, height - height / 8))
                rect.setFillColor("#ffff4d")
            if kinds3[i] == 'chance':
                text1 = Text('Chance', (WIDTH * 3.5, WIDTH + 35))
                win.add(text1)
            if kinds3[i] == 'rrd':
                text1 = Text('B & O', (WIDTH*6.5, WIDTH + 15))
                text2 = Text('Raildroad', (WIDTH*6.5, WIDTH + 30))
                win.add(text1)
                win.add(text2)
            if kinds3[i] == 'util':
                text1 = Text('Water', (WIDTH*8.5, WIDTH + 15))
                text2 = Text('Works', (WIDTH*8.5, WIDTH + 30))
                win.add(text1)
                win.add(text2)
            
        ypos = 2.5
        #Place the first part of the fourt row of tiles
        for i in range(2):
            tile = Tiles(kinds4[i], height, width)
            tile.moveTo((SIZE - width, ypos * width))
            self._tiles.append(tile)
            tile.addTo(win)
            ypos += 1.0
            #Customizes the tiles in the row
            if kinds4[i] == 'prop7':
                y = ypos - 1
                rect = Rectangle(height / 4, width)
                win.add(rect)
                rect.moveTo((SIZE + height / 8 - height, y * width))
                rect.setFillColor("#00b300")
        cc = Tiles('chest', height, width)
        cc.moveTo(SPACEPOS[33])
        cc.addTo(win)
        self._tiles.append(cc)
        ypos = 5.5 
        #Place second part of the fourth row of tiles
        for i in range(3,9):
            tile = Tiles(kinds4[i], height, width)
            tile.moveTo((SIZE - width, ypos * width))
            self._tiles.append(tile)
            tile.addTo(win)
            ypos += 1.0
            #Customizes the tiles in the row
            if kinds4[i] == 'prop7':
                y = ypos - 1
                rect = Rectangle(height / 4, width)
                win.add(rect)
                rect.moveTo((SIZE + height / 8 - height, y * width))
                rect.setFillColor("#00b300")
            if kinds4[i] == 'prop8':
                y = ypos - 1
                rect = Rectangle(height / 4, width)
                win.add(rect)
                rect.moveTo((SIZE + height / 8 - height, y * width))
                rect.setFillColor("#0000e6")
            if kinds4[i] == 'chest':
                text1 = Text('Community Chest', 
                            (SIZE - WIDTH - 20, 4.5*WIDTH + 20), 9)
                win.add(text1)
            if kinds4[i] == 'rrd':
                text1 = Text('Short Line', (SIZE - WIDTH - 35, 6.5*WIDTH - 20))
                win.add(text1)
            if kinds4[i] == 'chance':
                text1 = Text('Chance', (SIZE - WIDTH, 7.5*WIDTH - 20))
                win.add(text1)
            if kinds4[i] == 'tax':
                text1 = Text('Luxary Tax', 
                            (SIZE - WIDTH - 32, 9.5*WIDTH - 10), 9.5)
                text2 = Text('Pay $100', (SIZE - WIDTH - 30, 9.5*WIDTH + 10), 
                             9.5)
                win.add(text1)
                win.add(text2)
        #Places down the corner pieces
        for i in range(4):
            tile = Tiles(corners[i], height, height)
            tile.moveTo(cornerMoves[i])
            tile.addTo(win)
        #Puts down the free parking text
        freepark = Text("Free Parking", (WIDTH, WIDTH + 30), 16)
        win.add(freepark)
            
        # PICTURES
        monopoly = Image("https://cs.hamilton.edu/~hgolden/images/title.PNG", 
                         (400, 400), 500, 500)
        win.add(monopoly)
        monopoly.rotate(220)
        rrdLocs = [(SIZE - 6.5 * width, SIZE - width), (width, SIZE - 6.5 *\
                   width), (6.5 * width, width), (SIZE - width, 6.5 * width)]
        deg = 0
        #Lays down the railroad pictues
        for i in range(4):
            rrd = Image("https://cs.hamilton.edu/~hgolden/images/rrd.PNG",    
                        rrdLocs[i], width + 15, height - 3)
            win.add(rrd)
            rrd.rotate(deg)
            deg += 90
        chanLocs = [(3.2 * width, width), (SIZE - width, 7.2 * width), 
                    (SIZE - 8.2 * width, SIZE - width)]
        deg = 180
        #Lays down the chance pictures
        for i in range(3):
            chan = Image("https://cs.hamilton.edu/~hgolden/images/chance.PNG",
                         chanLocs[i], height, width * 2)
            win.add(chan)
            chan.rotate(deg)
            deg += 90
        chestLocs = [(SIZE - width, 4.5 * width), (SIZE - 3.5 * width, SIZE -
                     width), (width, SIZE - 8.5 * width)]
        deg = 270
        #Places down the community chest pictues 
        for i in range(3):
            chest = Image("https://cs.hamilton.edu/~hgolden/images/chest.PNG", 
                          chestLocs[i], width + 15, height + 15)
            win.add(chest)
            chest.rotate(deg)
            deg += 90
        misLocs = [(width, SIZE - 3.35 * width), (8.5 * width, width), 
                   (SIZE - width, 9.4 * width)]
        mispics = ["https://cs.hamilton.edu/~hgolden/images/light.PNG", 
                   "https://cs.hamilton.edu/~hgolden/images/water.PNG", 
                   "https://cs.hamilton.edu/~hgolden/images/ring.PNG"]
        missize = [height - 15, width * 2, width + 20, height - 3, 
                   width * 2, height * 2]
        deg = 90
        x = 0
        y = 1
        #Places the untility and luxary tax pictue
        for i in range(3):
            pic = Image(mispics[i], misLocs[i], missize[x], missize[y])
            win.add(pic)
            pic.rotate(deg)
            x += 2
            y += 2
            deg += 90
        cornLocs = [(SIZE - width, SIZE - width - 20), 
                    (width + 12, SIZE - width - 25), (width, width + 20), 
                    (SIZE - width - 15, width)]
        cornPics = ["https://cs.hamilton.edu/~hgolden/images/go.PNG", 
                    "https://cs.hamilton.edu/~hgolden/images/injail.PNG", 
                    "https://cs.hamilton.edu/~hgolden/images/freepark.PNG",
                    "https://cs.hamilton.edu/~hgolden/images/gotojail.PNG"]
        cornDeg = [0, 0, 180, 225]
        cornSize = [height + 15, height + 15, height, height, height, height, 
                    height, height]
        x = 0
        y = 1
        #Places down the pictures in the corner
        for i in range(4):
            corn = Image(cornPics[i], cornLocs[i], cornSize[x], cornSize[y])
            win.add(corn)
            corn.rotate(cornDeg[i])
            x += 2
            y += 2
        proplocs = [SPACEPOS[1], SPACEPOS[3], SPACEPOS[6], SPACEPOS[8],
                    SPACEPOS[9], SPACEPOS[11], SPACEPOS[13], SPACEPOS[14],
                    SPACEPOS[16], SPACEPOS[18], SPACEPOS[19], SPACEPOS[21],
                    SPACEPOS[23], SPACEPOS[24], SPACEPOS[26], SPACEPOS[28],
                    SPACEPOS[29], SPACEPOS[31], SPACEPOS[32], SPACEPOS[34],
                    SPACEPOS[37], SPACEPOS[39]]
        
        #Puts down the property names
        for i in range(22):
            name = Text(PROPNAMES[i], proplocs[i], 9.4)
            win.add(name)
    def getList(self):
        '''Returns the tiles list'''
        return self._tiles
class Tiles:
    '''Creates a template for making rectangular board tiles'''
    def __init__(self, kind, width, height):
        '''Initiate the attributes'''
        self._kind = kind
        self._tile = Rectangle(width, height)
        self._center = (0, 0)
        
    def getCenter(self):
        '''Returns the center of the tile'''
        return self._center
        
    def getKind(self):
        '''Returns the 'kind' of the tile'''
        return self._kind
    
    def getRect(self):
        '''Returns the rectangle object attribute'''
        return self._tile
        
    def addTo(self, win):
        '''Add the tiles to the window and set the background color'''
        win.setWidth(SIZE)
        win.setHeight(SIZE)
        win.setBackgroundColor('#ccffdd')
        win.add(self._tile)

    def moveTo(self, pos):
        '''Move the tile to the given location'''
        self._tile.moveTo(pos)
        self._center = pos
       
        
        
class Player:
    '''Creates players that dictate the actions of the piece and have a 
       net worth'''
    def __init__(self, piece, win, num, color):
        '''Initializes the attributes of the player's piece'''
        self._worth = 1500
        self._props = []
        self._rr = []
        self._rrrent = [25, 50, 100, 200]
        self._piece = Piece(piece)
        self._win = win
        self._num = num
        #Creates the text on the board that tracks the players' money
        self._title = Text(color + " Player", PLAYERPOS[self._num])
        self._money = Text("Net Worth: " + str(self._worth), 
                           MONEYPOS[self._num])
        win.add(self._title)
        win.add(self._money)
    
    def getWorth(self):
        '''Returns the players worth'''
        return self._worth
    
    def spend(self, price):
        '''Lowers the player's money when they spend'''
        self._worth -= price
        self._money.setTextString("Net Worth: " + str(self._worth))
        
    def earn(self, price):
        '''Raises the player's money when they earn'''
        self._worth += price
        self._money.setTextString("Net Worth: " + str(self._worth))
            
    def getPiece(self):
        '''Returns the piece'''
        return self._piece
   
    def getRailroad(self, rrd):
        '''Adds a railroad to the railroad list'''
        self._rr.append(rrd)
    
    def getProp(self, prop):
        '''Adds a property to the property list'''
        self._props.append(prop)
    
    def getRrdRent(self):
        '''Returns the railroads rent based on how many railroads are owned'''
        rent = self._rrrent[len(self._rr) - 1]
        return rent
    
    def lose(self):
        '''If a player runs out of money they are out of the game'''
        self._worth = 'LOSER'
        self._money.setTextString("Net Worth: " + str(self._worth))
        win = self._win 
        self._piece.lose(win)
        
    def getProps(self):
        '''Returns the property'''
        return self._props
        
    def conquer(self, player):
        '''The conquering player takes the losers properties'''
        newProps = player.getProps()
        self._props.extend(newProps)
    
    def canAfford(self, price):
        '''Determines if a player can afford a property'''
        return self._worth >= price

    def buyHouse(self, prop):
        '''Buys a house for a monopoly'''
        pass
    
    def buyHotel(self, prop):
        '''Buys a hotel for a monopoly'''
        pass
    
class Piece:
    '''Creates a piece for the player'''
    def __init__(self, color):
        '''Initializes the attributes of the piece'''
        width = SIZE / 13
        self._circ = Circle(20, (SIZE - width, SIZE - width))
        self._circ.setDepth(0)
        self._location = (SIZE - width, SIZE -width)
        self._circ.setFillColor(color)
        self._color = color
        self._active = False
    
    def getLoc(self):
        '''Returns the location of the piece'''
        return self._location
    
    def getColor(self):
        '''Returns the color of the piece'''
        return self._color
    
    def lose(self, win):
        '''Removes the piece from the window if the player loses'''
        win.remove(self._circ)
    
    def activate(self):
        '''Turns the border of a player's piece green if it's their turn'''
        self._active = True
        self._circ.setBorderColor('green')
        self._circ.setDepth(50)
        
    def deactivate(self):
        '''Turns the border of a player's piece black if it isn't their turn'''
        self._active = False
        self._circ.setBorderColor('black')
        self._circ.setBorderWidth(5)
    def addTo(self, win):
        '''Adds a piece to the window'''
        win.add(self._circ)
    
    def move(self, roll):
        '''Moves the piece around the board'''
        for i in range(40):
            if SPACEPOS[i] == self._location:
                current = i
        x = current + roll
        #Keeps x in range
        if x >= 40:
            x %= 40
        #Sends a piece to jail
        if x == 30:
            x = 10
        self._circ.moveTo(SPACEPOS[x])
        self._location = SPACEPOS[x]
        
class Die:
    '''Creates two die that determine how far the pieces move'''
    #CITE: PROFESSOR CAMPBELL'S COMPSCI CLASS
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
        '''Initializes the attributes of the die'''
        self._value = 1
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgcolor)
        self._square.setDepth(20)
        self._center = center
        self._width = width
        #self._text = Text("1", center, 18)
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgcolor)
            pip.setDepth(20)
            self._pips.append(pip)
    
    def addTo(self, win):
        '''Adds the die to the window'''
        win.add(self._square)
        #win.add(self._text)
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

class Controller(EventHandler):
    def __init__(self, win):
        """ set up objects with events on a window """
        board = Board(win)
        self._tiles = board.getList()
        self._ownedRR = []
        self._rrds = []
        for i in range(4):
            rrd = Railroads(SPACEPOS[RRDPOS[i]], RRDNAMES[i])
            self._rrds.append(rrd)
        EventHandler.__init__(self)   # set up the EventHandler properly
        self._ownedProps = []
        self._props = []
        #Creates dice and roll button'''
        self._die1 = Die(center = (200, 200))
        self._die1.addTo(win)
        self._die2 = Die(center = (230, 200))
        self._die2.addTo(win)
        self._button = Square(50, (215, 250))
        self._button.setFillColor('white')
        win.add(self._button)
        self._button.addHandler(self) # register the controller as the handler
                                      # for button's events
        self._roll = Text("Roll!", (215, 250))
        win.add(self._roll)
        #Free Parking
        self._parkText = Text('Free Parking Pot', (600, 200), 16)
        self._parkVal = 0
        self._parkText2 = Text('$' + str(self._parkVal), (600, 225), 16)
        win.add(self._parkText)
        win.add(self._parkText2)
        for i in range(22):
            prop = Props(MONOPLOIES[i], PRICES[i], RENT[i], SPACEPOS[POS[i]], 
                   PROPNAMES[i])
            self._props.append(prop)
        self._quant = int(input("Input the number of players (2 through 5)"))
        self._pieces = ['#BC8DA7', '#ffffff', '#1DD3B0', '#FFD23F', '#4392F1']
        self._names = ['Purple', 'White', 'Turquoise', 'Gold', 'Blue']
        self._players = []
        self._current = 0
        for i in range(self._quant):
            player = Player(self._pieces[i], win, i, self._names[i])
            self._players.append(player)
        for i in range(len(self._players)):
            self._players[(len(self._players) - 1) - i].getPiece().addTo(win)
        self._players[self._current].getPiece().activate()
    
    
    def changeTurn(self):
        '''Change whose turn it is'''
        self._players[self._current].getPiece().deactivate()
        self._current += 1
        self._current %= self._quant
        self._players[self._current].getPiece().activate()
    
    def handleMouseRelease(self, event):
        '''Dice roll when the mouse is released moving the piece around the 
           board'''
        self._die1.roll()
        self._die2.roll()
        num = self._die1.getValue() + self._die2.getValue()
        start = self._players[self._current].getPiece().getLoc()
        self._players[self._current].getPiece().move(num)
        finish = self._players[self._current].getPiece().getLoc()
        self._tiles[16].moveTo((61.53846153846154, 215.3846153846154))
        self._tiles[17].moveTo((61.53846153846154, 153.84615384615384))
        #Checks if the player landed on a chance
        for i in range(len(CHANCEPOS)):
            if finish == SPACEPOS[CHANCEPOS[i]]:
                self._players[self._current].getPiece()\
                .move(random.randrange(40))
        #Checks if the player lands on a community chest
        for i in range(len(CHESTPOS)):
            if finish == SPACEPOS[CHESTPOS[i]]:
                self._players[self._current].earn(random.randrange(-200,200))
        #Checks if a player landed on an available property
        for i in range(len(self._props)):
            if finish == self._props[i].getLoc():
                land = True
                prop = self._props[i]
        if land:
            if self._players[self._current].canAfford(prop.getPrice()):
                if prop.offerProp():
                    self.buyProp(prop, self._players[self._current])
        #Checks if a player landed on a railroad
        for i in range(len(self._rrds)):
            if finish == self._rrds[i].getLoc():
                onrrd = True
                rrd = self._rrds[i]
        if onrrd:
            if self._players[self._current].canAfford(200):
                if rrd.offerRR():
                    self.buyRR(rrd, self._players[self._current])
        #Checks if rent needs to be payed
        for i in range(len(self._ownedProps)):
            if finish == self._ownedProps[i].getLoc():
                rent = True
                prop = self._ownedProps[i]
        if rent:
            if self._players[self._current].canAfford(prop.getRent()):
                self.payRent(prop, prop.getOwner(), \
                self._players[self._current])
            else:
                self._players[self._current].lose()
                prop.getOwner().conquer(self._players[self._current])
                self._players.remove(self._players[self._current])
                for item in self._players[self._current].getProps():
                    self.buyProp(item, prop.getOwner())
                    prop.getOwner().earn(item.getPrice())
        #Free Parking
        if finish == SPACEPOS[20]:
            self._players[self._current].earn(self._parkVal)
            self._parkVal = 0
            self._parkText2.setTextString("$" + str(self._parkVal))
        #Adds money to the free parking pot
        if finish == SPACEPOS[4]:
            self._parkVal += 200
            self._parkText2.setTextString("$" + str(self._parkVal))
            self._players[self._current].spend(200)
        if finish == SPACEPOS[39]:
            self._parkVal += 100
            self._parkText2.setTextString("$" + str(self._parkVal))
            self._players[self._current].spend(100)
        #Checks if a player passed go
        for i in range(40):
            if SPACEPOS[i] == start:
                start = i
        for i in range(40):
            if SPACEPOS[i] == finish:
                finish = i
        if start > finish:
            self._players[self._current].earn(200)
        #Changes the turn
        if self._die1.getValue() != self._die2.getValue():
            self.changeTurn()
    
    def buyRR(self, rr, player):
        '''Transfers possesion of a railroad from the contorller to 
           the player'''
        player.getRailroad(rr)
        player.spend(200)
        self._rrds.remove(rr) 
        rr.assignOwner(player)
        self._ownedRR.append(rr)
        for i in range(len(self._tiles)):
            if self._tiles[i].getCenter() == rr.getLoc():
                num = i
        rect = self._tiles[num].getRect()
        rect.setFillColor(player.getPiece().getColor())
        rect.setDepth(100)
        
    
    def buyProp(self, prop, player): 
        '''Transfers possession of a property from the controller to 
           the player'''
        player.getProp(prop)
        player.spend(prop.getPrice())
        self._props.remove(prop)
        prop.assignOwner(player)
        for i in range(len(self._tiles)):
            if self._tiles[i].getCenter() == prop.getLoc():
                num = i
        rect = self._tiles[num].getRect()
        rect.setFillColor(player.getPiece().getColor())
        rect.setDepth(100)
        self._ownedProps.append(prop)
    
    def payRent(self, prop, owner, renter):
        '''Transfers rent money between players'''
        rent = prop.getRent()
        owner.earn(rent)
        renter.spend(rent)
    
            
class Props:
    '''Creates and object that holds all information of a property'''
    def __init__(self, monopoly, price, rent, loc, name):
        '''Initializes the attributes of a property'''
        self._monopoly = monopoly
        self._price = price
        self._loc = loc
        self._rent = rent
        self._name = name
        self._owner = None
        
    def assignOwner(self, player):
        '''Give the property to a player'''
        self._owner = player
    
    def getOwner(self):
        '''Returns the owner of the property'''
        return self._owner
        
    def getPrice(self):
        '''Returns the price of the property'''
        return self._price
    
    def getRent(self):
        '''Returns the rent of the property'''
        return self._rent
        
    def getLoc(self):
        '''Returns the location of the property'''
        return self._loc
    
    def getMonopoly(self):
        '''Returns what monoploy the property belongs to'''
        return self._monopoly
        
    def getName(self):
        '''Returns the name of the property'''
        return self._name
    
    def offerProp(self):
        '''Creates and input window for a player to buy a property'''
        wantProp = input('Would you like to purchase ' + str(self._name) + \
                         ' for $' + str(self._price) + '? Type yes/no')
        return wantProp == 'yes'
class Railroads:
    '''Creates and object that holds all information about a railroad'''
    def __init__(self, loc, name):
        '''Initializes the attributes of the railroads'''
        self._loc = loc
        self._name = name
        self._owner = None
    
    def assignOwner(self, player):
        '''Assigns an owner to the railroad'''
        self._owner = player
    
    def getOwner(self):
        '''Returns the owner of the railroad'''
        return self._owner
    
    def getLoc(self):
        '''Returns the location of the railroad'''
        return self._loc
    
    def getName(self):
        '''Returns the name of the railroad'''
        return self._name
        
    def offerRR(self):
        '''Creats and input window for a player to buy a property'''
        wantRR = input('Would you like to purchase ' + str(self._name) + \
                       ' Railroad for $200? Type yes/no')
        return wantRR == 'yes'

def main(win):
    _ = Controller(win)
    
    
StartGraphicsSystem(main)
    
    
