"""
Alex Schluter is my partner and has a more up-to-date version of the program.
"""


import random
from cs110graphics import *

class Die(EventHandler):
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
    
    def __init__(self, board, bgcolor='white', 
                 fgcolor='black'):
        EventHandler.__init__(self)
        self._board = board
        
        self._dx = 200
        self._dy = 30
        center = (self._dx, self._dy)
        width = 25
        self._value = 6
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgcolor)
        self._square.setDepth(20)
        self._width = width
        self._center = center
        
        self._dxA = 250
        self._dyA = 30
        centerA = (self._dxA, self._dyA)
        widthA = 25
        self._valueA = 6
        self._square2 = Rectangle(widthA, widthA, centerA)
        self._square2.setFillColor(bgcolor)
        self._square2.setDepth(20)
        self._widthA = widthA
        self._centerA = centerA
        
        self._dxB = 100
        self._dyB = 30
        centerB = (self._dxB, self._dyB)
        widthB = 100
        heightB = 25
        self._rollButton = Rectangle(widthB, heightB, centerB)
        self._rollButton.setFillColor('MediumSeaGreen')
        self._rollButton.setBorderColor('MediumSeaGreen')
        self._rollButton.setDepth(20)
        
        self._widthB = widthB
        self._centerB = centerB
        
        self._dxC = 100.5
        self._dyC = 35
        centerC = (self._dxC, self._dyC)
        size = 18
    
        self._text = Text('Click To Roll', centerC, size)
        self._text.setDepth(10)
        
        
        
        #newText = Text('hello', center=(200,399), size=12)
        #newText.setTextString('Hello')
        #win.add(newText)
        
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgcolor)
            pip.setDepth(20)
            self._pips.append(pip)
            
        
        self._pipsA = []
        for _ in range(Die.SIDES):
            pipA = Circle(widthA / 15, centerA)
            pipA.setFillColor(fgcolor)
            pipA.setDepth(20)
            self._pipsA.append(pipA)
            
        #self._square.addHandler(self)
        #self._square2.addHandler(self)
        self._rollButton.addHandler(self)
        self._text.addHandler(self)
        self._update()
        
        
        
    def addTo(self, win):
        
        win.add(self._square)
        win.add(self._square2)
        win.add(self._rollButton)
        win.add(self._text)
        for pip in self._pips:
            win.add(pip)
        
        for pipA in self._pipsA:
            win.add(pipA)
            

    
    def roll(self):
        """ changes the value of this die to a random number between 1 and 
            the number of sides of a die """
        #dieValue = []    
        self._value = random.randrange(Die.SIDES) + 1
        self._update()
        #dieValue.append(self._value)
        #print(dieValue)
        #print(self._value)
        self._valueA = random.randrange(Die.SIDES) + 1
        #self._update2()
        #print(self._valueA)
        
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
                
    def _update2(self):
        positions2 = Die.POSITIONS[self._valueA]       
        for i in range(len(positions2)):
            if positions2[i] is None:
                self._pipsA[i].setDepth(25)
            else:
                self._pipsA[i].setDepth(15)
                cxA, cyA = self._centerA  # center of the die.
                dxA = positions2[i][0] * self._width
                dyA = positions2[i][1] * self._width  
                self._pipsA[i].moveTo((cxA + dxA, cyA + dyA))

    def handleMouseRelease(self, event):
        self.roll()
        





class Board:
    def __init__(self, win):
        self._die = Die(self)
        self._die.addTo(win)
        
class Piece(EventHandler):
    def __init__(self, color, player):
        EventHandler.__init__(self)
        self._color = color
        self._player = player
        self._back = Circle(10)
        #self._front = Text(kind)
        self._back.setFillColor(color)
        self._back.addHandler(self)
        self._moving = False
        self._location = (0, 0)  # window location of the piece
        self._startPos = None    # mouse position where movement started
        self._active = False
        self._back.setDepth(0)
    
    def activate(self):
        self._active = True
        self._back.setBorderColor('green')
        
    def deactivate(self):
        self._active = False
        self._back.setBorderColor('black')
    
    def addTo(self, win):
        win.add(self._back)
        #win.add(self._front)
        
    
    def moveTo(self, pos):
        self._back.moveTo(pos)
        #self._front.moveTo(pos)
        self._location = pos
    
    def move(self, dx, dy):
        oldx, oldy = self._location
        newx = oldx + dx
        newy = oldy + dy
        self.moveTo((newx, newy))
    
    def handleMouseRelease(self, event):
        if not self._active:
            return 
        if self._moving:
            self._moving = False
            self._player.report(self, event)
        else:
            self._moving = True
            self._startPos = event.getMouseLocation()
    
    def handleMouseMove(self, event):
        if not self._active:
            return
        if self._moving:
            oldx, oldy = self._startPos
            newx, newy = event.getMouseLocation()
            self.move(newx - oldx, newy - oldy)
            self._startPos = newx, newy
            
    

class Player:
    def __init__(self, win, color, board):
        self._pieces = []
        self._board = board
        count = 15
        if color == 'Yellow':
            count = 15
           
            #Piece.changeColor('blue')
        for i in range(count):
            piece = Piece(color, self)
            piece.addTo(win)
            if color == 'LightBlue':
                piece.moveTo((300,375))#50 + i * 25, 50 + (count+15) * 200))
            else:
                piece.moveTo((200,375))
            self._pieces.append(piece)
            
        self._dxC = 100.5
        self._dyC = 35
        centerC = (self._dxC, self._dyC)
        size = 50
        
        self._aList = []
        
        for i in range(count):
            self._aList.append(i+1)
            
        self._largest = self._aList[0]
        for large in self._aList:
            if large > self._largest:
                self._largest = large
            self._text = Text(str(self._largest), centerC, size)
            self._text.setDepth(10)
        #win.add(self._text)
    
    def removeLargest(self):    
        
        self._aList.remove(self._largest)
        
    
    def reduceNumber(self):
        if self.deactivateAll():
            self._aList.remove(self._largest)
            print('this ran')
        #self._text = Text(str(largest), centerC, size)
        #self._text.setDepth(10)
            
                
        
        
    def listIt(self):
        return self._aList
            
    
    def report(self, piece, event):
        self._board.report(piece, event)
    
    def activateAll(self):
        for piece in self._pieces:
            piece.activate()
    
    def deactivateAll(self):
        for piece in self._pieces:
            piece.deactivate()
      
class Board2:
    def __init__(self, win):
        self._players = []
        for color in ['Yellow', 'LightBlue']:
            self._players.append(Player(win, color, self))
        self._current = 1
        self.changeTurn()
        #self.showNumber()
        """
        self._chipNum = []
        for i in range(15):
            self._chipNum.append(Player(win, 

        self._players2 = []
        for  in [Player.]:
            self._players.append(Player(win, kind, self))
        x, y = 55, 100  # center of the upperleft cell
        self._cells = []
        for row in range(3):
            self._cells.append([])
            for col in range(3):
                newCell = Cell(win, (x + 30 * row, y + 30 * col))
                self._cells[-1].append(newCell)
        self._current = 1
        self.changeTurn()
        """
        
        
    
    def changeTurn(self):
        self._players[self._current].deactivateAll()
        self._current += 1
        self._current %= 2
        self._players[self._current].activateAll()
    
    
        
    def report(self, piece, event):
        print("Something happened with {}".format(piece))
        self.changeTurn()

#def play(win):
#    Board2(win)
    


        
        
        
        
def main(win):
    Board2(win)
    
    for _ in range(1):
        Board(win)
    
    
    # Square 
    width = 351
    height = 250
    center = (201, 200)
    
    nice = Rectangle(width, height, center)
    nice.setBorderWidth(6)
    nice.setFillColor('LightSlateGrey')
    win.add(nice)
    
    # Divider
    width = 26
    height = 273
    center = (200, 215)
    
    centrr = Rectangle(width, height, center)
    centrr.setFillColor('black')
    win.add(centrr)
    
    # Chip holder
    width = 351
    height = 23
    center = (201, 340)
    
    chipHolder = Rectangle(width, height, center)
    chipHolder.setBorderWidth(6)
    win.add(chipHolder)
    
    # Bottom Left
    for i in range(6):
        newX = 27 * i
        
        points = [(28.5 + newX, 321.5), (51 + newX, 321.5), (38.5 + newX, 220)]
    
        leftUpTriangles = Polygon(points)
        win.add(leftUpTriangles)

        if newX % 2 == 0:
            leftUpTriangles.setFillColor('red')
            leftUpTriangles.setBorderColor('red')
        else:
            leftUpTriangles.setFillColor('white')
            leftUpTriangles.setBorderColor('white')
        
        
    # Bottom Right
    for i in range(6):
        newX = 27 * i
        
        points = [(214.5 + newX, 321.5), (239 + newX, 321.5), (226.5 + newX, 220)]
    
        rightUpTriangles = Polygon(points)
        win.add(rightUpTriangles)
        
        if newX % 2 == 0:
            rightUpTriangles.setFillColor('red')
            rightUpTriangles.setBorderColor('red')
        else:
            rightUpTriangles.setFillColor('white')
            rightUpTriangles.setBorderColor('white')
        
    # Top Left
    for i in range(6):
        newX = 27 * i
        
        points = [(28.5 + newX, 78.5), (51 + newX, 78.5), (38.5 + newX, 180)]
    
        leftDownTriangles = Polygon(points)
        win.add(leftDownTriangles)
        
        if newX % 2 == 0:
            leftDownTriangles.setFillColor('red')
            leftDownTriangles.setBorderColor('red')
        else:
            leftDownTriangles.setFillColor('white')
            leftDownTriangles.setBorderColor('white')
        
    # Top Right
    for i in range(6):
        newX = 27 * i
        
        points = [(214.4 + newX, 78.5), (239 + newX, 78.5), (226.5 + newX, 180)]
    
        rightUpTriangles = Polygon(points)
        win.add(rightUpTriangles)
        
        if newX % 2 == 0:
            rightUpTriangles.setFillColor('red')
            rightUpTriangles.setBorderColor('red')
        else:
            rightUpTriangles.setFillColor('white')
            rightUpTriangles.setBorderColor('white')
            
    points = [(25, 200), (106, 180), (187, 200), (106, 220)]
    
    # Designs
    diamondLeft = Polygon(points)
    diamondLeft.setFillColor('black')
    win.add(diamondLeft)
    
    points = [(213, 200), (294, 180), (375, 200), (294, 220)]
    
    diamondRight = Polygon(points)
    diamondRight.setFillColor('black')
    win.add(diamondRight)
    
    
    
    



StartGraphicsSystem(main)

