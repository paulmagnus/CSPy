""" 
*****************************************************************************
FILE:           Game.py

AUTHOR:         Griffin Kearns

ASSIGNMENT:     Project 6: Board Game (v2)

DATE:           05/01/2017

DESCRIPTION:    The backgammon set is now complete and usable for gameplay.
                There is a board, with pieces and dice. However, no rules are   
                enforced yet. Also, additional features like wagering or the    
                doubling cube have not yet been implemented.  
*****************************************************************************
"""
import random

from cs110graphics import *

            
    
class Board:
    """ Serves as background for game and underlying platform for all other             classes (i.e. objects of class Die, Piece, etc. are built here"""
    
    def __init__(self, win):
        self._mainBoard = Rectangle(650, 500, (325, 250))
        self._mainBoard.setFillColor("green")
        win.add(self._mainBoard)
        
        self._allPoints = [None, None, None, None, None, None, \
                           None, None, None, None, None, None, \
                           None, None, None, None, None, None, \
                           None, None, None, None, None, None]
        
        self._allPoints[0] = Point((625, 400), "maroon", 0)
        self._allPoints[1] = Point((575, 400), "black", 1)
        self._allPoints[2] = Point((525, 400), "maroon", 2)
        self._allPoints[3] = Point((475, 400), "black", 3)
        self._allPoints[4] = Point((425, 400), "maroon", 4)
        self._allPoints[5] = Point((375, 400), "black", 5)
        
        self._allPoints[6] = Point((275, 400), "maroon", 6)
        self._allPoints[7] = Point((225, 400), "black", 7)
        self._allPoints[8] = Point((175, 400), "maroon", 8)
        self._allPoints[9] = Point((125, 400), "black", 9)
        self._allPoints[10] = Point((75, 400), "maroon", 10)
        self._allPoints[11] = Point((25, 400), "black", 11)
        
        self._allPoints[12] = Point((25, 100), "maroon", 12)
        self._allPoints[13] = Point((75, 100), "black", 13)
        self._allPoints[14] = Point((125, 100), "maroon", 14)
        self._allPoints[15] = Point((175, 100), "black", 15)
        self._allPoints[16] = Point((225, 100), "maroon", 16)
        self._allPoints[17] = Point((275, 100), "black", 17)
        
        self._allPoints[18] = Point((375, 100), "maroon", 18)
        self._allPoints[19] = Point((425, 100), "black", 19)
        self._allPoints[20] = Point((475, 100), "maroon", 20)
        self._allPoints[21] = Point((525, 100), "black", 21)
        self._allPoints[22] = Point((575, 100), "maroon", 22)
        self._allPoints[23] = Point((625, 100), "black", 23)
        
        for i in range(12):
            self._allPoints[i].rotate(180.0)
            
        for point in self._allPoints:
            point.addTo(win)
            
            
        self._bar = Rectangle(50, 500, (325, 250))
        self._bar.setFillColor("tan")
        win.add(self._bar)
    
        
        
        die1 = Die((425, 250))
        die1.addTo(win)
    
        die2 = Die((475, 250))
        die2.addTo(win)
        
    
        whitePieces = []
        brownPieces = []
        for i in range(15):
            whitePiece = Piece(win, "ivory")
            whitePieces.append(whitePiece)
            brownPiece = Piece(win, "SaddleBrown")
            brownPieces.append(brownPiece)
       
       
       #moving the pieces to starting positions     
        whitePieces[0].moveTo((25, 20))
        whitePieces[1].moveTo((25, 60))
        whitePieces[2].moveTo((25, 100))
        whitePieces[3].moveTo((25, 140))
        whitePieces[4].moveTo((25, 180))
        whitePieces[5].moveTo((625, 20))
        whitePieces[6].moveTo((625, 60))
        whitePieces[7].moveTo((225, 480))
        whitePieces[8].moveTo((225, 440))
        whitePieces[9].moveTo((225, 400))
        whitePieces[10].moveTo((375, 480))
        whitePieces[11].moveTo((375, 440))
        whitePieces[12].moveTo((375, 400))
        whitePieces[13].moveTo((375, 360))
        whitePieces[14].moveTo((375, 320))
        
        brownPieces[0].moveTo((25, 480))
        brownPieces[1].moveTo((25, 440))
        brownPieces[2].moveTo((25, 400))
        brownPieces[3].moveTo((25, 360))
        brownPieces[4].moveTo((25, 320))
        brownPieces[5].moveTo((625, 480))
        brownPieces[6].moveTo((625, 440))
        brownPieces[7].moveTo((225, 20))
        brownPieces[8].moveTo((225, 60))
        brownPieces[9].moveTo((225, 100))
        brownPieces[10].moveTo((375, 20))
        brownPieces[11].moveTo((375, 60))
        brownPieces[12].moveTo((375, 100))
        brownPieces[13].moveTo((375, 140))
        brownPieces[14].moveTo((375, 180))
        

    
    
#    def restrictMovement(self, die1, die2, piece, pointList):
#        currentPoint = computeLandingOnPoint(piece, pointList)
#        valDie1 = die1.getValue()
#        valDie2 = die2.getValue()
#        if valDie1 != currentPoint and valDie2 != currentPoint
        
        
class Piece(EventHandler):
    """ Class for the gamepieces. They are moveable (handle their own events)"""
    def __init__(self, win, color):
        EventHandler.__init__(self)
        self._checker = Circle(20)
        self._checker.setFillColor(color)
        self._checker.addHandler(self)
        win.add(self._checker)
        self._color = color
        
        #CITE: Professor Campbell 4/14 class code
        #DESC: self._active, self._moving method of moving piece
        self._active = True
        self._moving = False
        self._location = (0, 0)
        self._startLoc = None
        self._pointOn = None
        
        
        
    
    def addTo(self, win):
        """adds the piece to the window. """
        win.add(self._checker)
    
    def moveTo(self, position):
        """ moves a piece to a position """
        self._checker.moveTo(position)
        self._location = position
        
    def move(self, dx, dy):
        """moves a piece in a direction"""
        x0, y0 = self._location
        self.moveTo((x0 + dx, y0 + dy))
        self._location = (x0 + dx, y0 + dy)
        
    def getLocation(self):
        """ returns the current location of the piece"""
        return self._location
        
    def getColor(self):
        """returns the color of the piece"""
        return self._color
    
    #def activate(self):
    #    self._active = True 
        
        
    def handleMouseRelease(self, event):
        
        if self._moving:
            self._moving = False
            #self._active = False
            
        else:
            self._moving = True
            self._startLoc = event.getMouseLocation()

            
    def handleMouseMove(self, event):
        if self._active is False:
            return
        if self._moving:
            oldx, oldy = self._startLoc
            newx, newy = event.getMouseLocation()
            self.move(newx - oldx, newy - oldy)
            self._startLoc = self._location
            

    



#CITE: Prof. Campbell, class code 3/29
#DESC: code for class Die. However, I have modified it so that the die handles 
#      its own events, instead of using a separate controller.
class Die(EventHandler):
    """ class used to make two dice that can be rolled. Handle their own
        events"""
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
                 
    def __init__(self, center, width=25, bgcolor='white', 
                 fgcolor='black'):
        EventHandler.__init__(self)
        self._value = 6
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgcolor)
        self._square.setDepth(20)
        self._square.addHandler(self)
        self._width = width
        self._center = center
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgcolor)
            pip.setDepth(20)
            self._pips.append(pip)
        self._active = True
        
    def addTo(self, win):
        """adds the dice components to the window"""
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)
    
#   The roll function was placed directly under handleMouseRelease 
    
    def getValue(self):
        """ return the current value of a die """
        return self._value
        
    def _update(self):
        """ updates appearance of the die to match the value """
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
        #self._active = False
        
                
    def handleMouseRelease(self, event):
        #if self._active is False:
        #    return
        #else:
        self._value = random.randrange(Die.SIDES) + 1
        self._update()
   
   
class Point:
    """ similar to Cell in the tic-tac-toe demo. It is an area of the board             around one of the triangular points within which landing can be                 computed."""
    def __init__(self, loc, color, value):
        self._location = loc
        self._zone = Rectangle(50, 250, loc)
        self._zone.setBorderColor(None)
        self._vis = Polygon([(loc[0] - 25, loc[1] - 125),\
            (loc[0] + 25, loc[1] - 125), (loc[0], loc[1] + 125)])
        self._vis.setPivot(loc)
        self._vis.setFillColor(color)
        self.piecesOn = []
        self._value = value
        
    def rotate(self, degrees):
        """rotates a point"""
        self._vis.rotate(degrees)
    
    def addTo(self, win):
        """adds components of a point to the window"""
        win.add(self._zone)
        win.add(self._vis)
    
    def getLocation(self):
        """ returns the location of a point"""
        return self._location
        
    def getValue(self):
        """ each point is assigned a value for the purpose of keeping track of 
            the pieces' movement. This returns that value """
        return self._value
        
    def addPiece(self, piece):
        """ adds piece to list of pieces on point """
        self.piecesOn.append(piece)    



def computeLandingOnPoint(piece, pointList):
    """ determines whether a piece has landed on a point. If it has, then the 
    piece is added to the point, and the value of the point is returned so that 
    this information can be stored in the point. This function also enforces the     rule for "hitting" where if a point with a single piece of one color becomes     occupied by a piece of the opposite color, that original piece is sent to 
    the bar"""
    for point in pointList:
        pointLoc = point.getLocation()
        pieceLoc = piece.getLocation()
        if pieceLoc[0] >= pointLoc[0] - 25 and \
            pieceLoc[0] <= pointLoc[0] + 25 and \
            pieceLoc[1] >= pointLoc[1] - 125 and \
            pieceLoc[1] <= pointLoc[1] + 125:
            if len(point.piecesOn) == 1 and \
                piece.getColor() != point.piecesOn[0].getColor():
                point.piecesOn[0].moveTo(325, 250)
            point.addPiece(piece)
            return point.getValue()

def main(win):
    """function that produces the board in the graphics window """
    Board(win)
    
    
    
    
#window size altered to accomodate board plus side vanishing area for pieces    
StartGraphicsSystem(main, 750, 500)
