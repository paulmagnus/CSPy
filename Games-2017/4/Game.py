from cs110graphics import*
import random

class Board:
    def __init__(self, win):
        
        #Square
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
        
        # Chip Holder
        width = 351
        height = 23
        center = (201, 340)
        
        chipHolder = Rectangle(width, height, center)
        chipHolder.setBorderWidth(6)
        win.add(chipHolder)
        '''
        # Bottom Left
        for i in range(6):
            newX = 27 * i
                
            points = [(28.5 + newX, 321.5), (51 + newX, 321.5), (38.5 + newX,
            220)]
            
            leftUpTriangles = Polygon(points)
            win.add(leftUpTriangles)
            
            if newX % 2 == 0:
                leftUpTriangles.setFillColor('purple')
                leftUpTriangles.setBorderColor('purple')
            else:
                leftUpTriangles.setFillColor('white')
                leftUpTriangles.setBorderColor('white')
    
    
        #Bottom Right
        for i in range(6):
            newX = 27 * i
            
            points = [(214.5 + newX, 321.5), (239 + newX, 321.5), (226.5 + newX, 220)]
            
            rightUpTriangles = Polygon(points)
            win.add(rightUpTriangles)
            
            if newX % 2 == 0:
                rightUpTriangles.setFillColor('purple')
                rightUpTriangles.setBorderColor('purple')
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
                leftDownTriangles.setFillColor('purple')
                leftDownTriangles.setBorderColor('purple')
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
                rightUpTriangles.setFillColor('purple')
                rightUpTriangles.setBorderColor('purple')
            else:
                rightUpTriangles.setFillColor('white')
                rightUpTriangles.setBorderColor('white')
        '''
        points = [(25, 200), (106, 180), (187, 200), (106, 220)]
        
        # Designs
        diamondLeft = Polygon(points)
        diamondLeft.setFillColor('black')
        win.add(diamondLeft)
        
        points = [(213, 200), (294, 180), (375, 200), (294, 220)]
        
        diamondRight = Polygon(points)
        diamondRight.setFillColor('black')
        win.add(diamondRight)
    
class Die(EventHandler):
    """ A six-sided die """
    SIDES = 6
    POSITIONS = [None,
                [(0,0), None, None, None, None, None],
                [(-.25, .25), (.25, -.25), None, None, None, None],
                [(-.25, .25), (0,0), (.25, -.25), None, None, None],
                [(-.25, .25), (-.25, -.25), (.25, -.25),
                 (.25, .25), None, None],
                [(-.25, -.25), (-.25, .25), (.25, -.25),
                 (.25, .25), (0, 0), None],
                [(-.25, -.25), (-.25, .25), (.25, -.25),
                 (.25, .25), (-.25, 0), (.25, 0)]]
    
    def __init__(self, board, bgcolor = 'white',
                 fgcolor = 'black'):
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
        
        
        
        
        
        
        
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(widthA / 15, centerA)
            pip.setFillColor(fgcolor)
            pip.setDepth(20)
            self._pips.append(pip)

        self._pipsA = []
        for _ in range(Die.SIDES):
            pipA = Circle(widthA / 15, centerA)
            pipA.setFillColor(fgcolor)
            pipA.setDepth(20)
            self._pipsA.append(pipA)
        
        
        
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
        """ changes the value of this die to a random numver between 1 and
            the number of sides of a die """
        self._value = random.randrange(Die.SIDES) + 1
        self._update()
        self._valueA = random.randrange(Die.SIDES) + 1
        self._update2()
            
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
                cx, cy = self._center
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
                cxA, cyA = self._centerA # center of the die
                dxA = positions2[i][0] * self._width
                dyA = positions2[i][1] * self._width
                self._pipsA[i].moveTo((cxA +dxA, cyA +dyA))
                
    def handleMouseRelease(self, event):
        self.roll()
    
    
    
    
    
    
class Play:
    def __init__(self, win):
        self._die = Die(self)
        self._die.addTo(win)
        Board(win)
        
def main(win):
    for _ in range(1):
        Play(win)

StartGraphicsSystem(main)

    
