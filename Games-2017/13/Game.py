import random
from cs110graphics import *

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
                 
    def __init__(self, board, width=25, center=(200, 35), bgcolor='white', 
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
        self._update()   ### BUG IN DIE!!!
        
    def addTo(self, win):
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
                


class RollButton(EventHandler):
    def __init__(self, board, dieOne, dieTwo, width=100, height=30, 
                 color='yellow', center=(340, 40)):
        EventHandler.__init__(self)
        self._dieOne = dieOne
        self._dieTwo = dieTwo
        self._board = board
        self._width = width
        self._height = height
        self._color = color
        self._centerX, self._centerY = center
        self._button = Rectangle(width, height, center)
        self._button.setFillColor(color)
        self._button.addHandler(self)
        self._buttonText = Text("Roll", (center[0], center[1] + 10), 30)
        
    def addTo(self, win):
        win.add(self._button)
        win.add(self._buttonText)
    
    def removeFrom(self, win):
        win.remove(self._button)
        win.remove(self._buttonText)
        
    def handleMouseRelease(self, event):
        self._dieOne.roll()
        self._dieTwo.roll()
        
class Pawn(EventHandler):
    def __init__(self, board, color, ident, pawnNum, position):
        EventHandler.__init__(self)
        self._location = (0, 0)
        self._color = color
        self._board = board
        self._ident = ident   # identifying number for this pawn
        self._pawnNum = pawnNum
        self._position = position # current logical position on the board
        self._square = Circle(10, (0, 0))
        self._square.setFillColor(color)
        self._square.addHandler(self)
    
    def addTo(self, win):
        win.add(self._square)
    
    def handleMouseRelease(self, event):
        self._board.reportPawnClick(self._ident, self._pawnNum)  # tell the                                                                      # board I was                                                                   # clicked
    
    def getPosition(self):
        return self._position
    
    def setLocation(self, pos):
        self._location = pos
        
    def moveTo(self, location):
        self._location = location
        self._square.moveTo(location)
        
    def move(self, pos):
        self._location = pos
        self._square.moveTo(pos)
    
    def getLocation(self):
        return self._location
        
class Triangles(EventHandler):
    def __init__(self, board, center, color, side):
        EventHandler.__init__(self)
        self._board = board
        self._center = center
        self._startingx = center[0]
        self._startingy = center[1]
        location = side % 2
        if location == 0:
            self._triangle = Polygon([(self._startingx, self._startingy), 
                                      (self._startingx + 28, self._startingy), 
                                      (self._startingx + 14, 
                                       self._startingy + 115)])
            self._triangle.setFillColor(color)
        else:
            self._triangle = Polygon([(self._startingx, 400 - self._startingy), 
                                      (self._startingx + 28, 
                                       400 - self._startingy), 
                                      (self._startingx + 14, 
                                       400 - self._startingy - 115)])
            self._triangle.setFillColor(color)
    def addTo(self, win):
        win.add(self._triangle)

    def handleMouseRelease(self, event):
        pass
    
    def getCenter(self):
        return (self._startingx + 14, self._startingy)



class BoardSpace:
    def __init__(self, board, center, boardWidth=360, boardHeight=260):
        self._x = center[0]
        self._y = center[1]
        self._boardWidth = boardWidth
        self._boardHeight = boardHeight
        self._board = board
        self._center = center
        self._outerboard = Rectangle(boardWidth+20, boardHeight+20, center)
        self._outerboard.setFillColor("brown")
        self._innerboard = Rectangle(boardWidth, boardHeight, center)
        self._innerboard.setFillColor("green")
        self._innerLineOne = Rectangle(12, boardHeight, 
                                       (center[0]- 6, center[1]))
        self._innerLineTwo = Rectangle(12, boardHeight, 
                                       (center[0] + 6, center[1]))
        self._innerLineOne.setFillColor("brown")
        self._innerLineTwo.setFillColor("brown")
        
    def addTo(self, win):
        win.add(self._outerboard)
        win.add(self._innerboard)
        win.add(self._innerLineOne)
        win.add(self._innerLineTwo)
        
class Board:
    def __init__(self, win):
        self._dieOne = Die(self, center=(180, 35))
        self._dieOne.addTo(win)
        self._dieTwo = Die(self, center=(220, 35))
        self._dieTwo.addTo(win)
        self._startingLocation = (34, 320)
        
        # set up some spaces
        self._spaces = []
        self._startingTri = 1
        xpos = 20
        ypos = 70
        centerx = 200
        centery = 200
        fullboard = BoardSpace(self, (centerx, centery))
        fullboard.addTo(win)
        colorList = ['red', 'white']
        for _ in range(6):
            for color in colorList:
                thisSpace = Triangles(self, (xpos, ypos), color, 
                                      self._startingTri)
                thisSpace.addTo(win)
                self._spaces.append(thisSpace)
                self._startingTri += 1
            xpos += 28
            colorList = [colorList[1], colorList[0]]
        for _ in range(6):
            for color in colorList:
                thisSpace = Triangles(self, (xpos+24, ypos), color, 
                                      self._startingTri)
                thisSpace.addTo(win)
                self._spaces.append(thisSpace)
                self._startingTri += 1
            xpos += 28
            colorList = [colorList[1], colorList[0]]    
            
        # set up two pawns
        self._pawns = []
        pawnNum = 0
        for _ in range(15):
            for color, which, pawnNum in [('black', 0, pawnNum), 
                                          ('white', 1, pawnNum)]:
                thisPawn = Pawn(self, color, which, pawnNum, 0)
                thisPawn.addTo(win)
                self._pawns.append(thisPawn)
                pawnNum += 1
        self._startingPawnLocations()
    
        # current player
        self._current = 0
        
        # roll button
        rollButton = RollButton(self, self._dieOne, self._dieTwo)
        rollButton.addTo(win)
        
        
    def reportPawnClick(self, ident, pawnNum):
        if ident == self._current:
            thePawn = self._pawns[pawnNum]
            pos = thePawn.getLocation()
            if self._current == 0:
                if pos[0] >= 200 and pos[1] >= 200:
                    pos = (pos[0] - self._dieOne.getValue() * 28 + 24, pos[1])
                if pos[0] < 200 and pos[1] >= 200:
                    pos = (pos[0] - self._dieOne.getValue() * 28, pos[1])
                if pos[0] < 200 and pos[1] < 200:
                    pos = (pos[0] + self._dieOne.getValue() * 28, pos[1])
                if pos[0] >= 200 and pos[1] < 200:
                    pos = (pos[0] + self._dieOne.getValue() * 28, pos[1])
            thePawn.setLocation(pos)
            self._updatePawnLocations()
            self.changeTurn()
    
    def changeTurn(self):
        self._current = (self._current + 1) % len(self._pawns)

        
    def _startingPawnLocations(self):
        startingX, startingY = self._startingLocation
        blackPiece = 0
        whitePiece = 0
        for i in range(5):
            if i == 0:
                startingY = self._startingLocation[1]
            self._pawns[blackPiece*2].moveTo((startingX, startingY))
            startingY -= 20
            blackPiece += 1
        for i in range(5):
            if i == 0:
                startingY = self._startingLocation[1]
            self._pawns[whitePiece*2 + 1].moveTo((startingX, startingY - 240))
            startingY += 20
            whitePiece += 1
        for i in range(3):
            if i == 0:
                startingY = self._startingLocation[1]
            self._pawns[blackPiece*2].moveTo((startingX + 28 * 4, 
                                              startingY - 240))
            startingY += 20
            blackPiece += 1
        for i in range(3):
            if i == 0:
                startingY = self._startingLocation[1]
            self._pawns[whitePiece*2 + 1].moveTo((startingX + 28 * 4, 
                                                  startingY))
            startingY -= 20
            whitePiece += 1
        for i in range(5):
            if i == 0:
                startingY = self._startingLocation[1]
            self._pawns[blackPiece*2].moveTo((startingX + 24 + 28 * 6, 
                                              startingY - 240))
            startingY += 20
            blackPiece += 1
        for i in range(5):
            if i == 0:
                startingY = self._startingLocation[1]
            self._pawns[whitePiece*2 + 1].moveTo((startingX + 24 + 28 * 6,
                                                  startingY))
            startingY -= 20
            whitePiece += 1
        for i in range(2):
            if i == 0:
                startingY = self._startingLocation[1]
            self._pawns[blackPiece*2].moveTo((startingX + 24 + 28 * 11, 
                                              startingY))
            startingY -= 20
            blackPiece += 1
        for i in range(2):
            if i == 0:
                startingY = self._startingLocation[1]
            self._pawns[whitePiece*2 + 1].moveTo((startingX + 24 + 28 * 11,
                                                  startingY - 240))
            startingY += 20
            whitePiece += 1
            
            
    def _updatePawnLocations(self):
        """ Move the two pawns to their correct locations on the window """
        for i in range(len(self._pawns)):
            pos = self._pawns[i].getLocation()
            #self._pawns[i].moveTo(pos)
            self._pawns[i].move(pos)
        
        
        
        #offsets = [-1, 1]
        #for i in range(len(self._pawns)):
        #    pos = self._pawns[i].getPosition()
        #    theSpace = self._spaces[pos]
        #    self._pawns[i].moveTo(theSpace.getCenter())
        #    self._pawns[i].move(0, offsets[i] * 10)
        
def main(win):
    Board(win)
    
StartGraphicsSystem(main)











