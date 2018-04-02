"""
********************************************************************************
FILE:        Game.py

AUTHOR:      Arianna Giaramita

PARTNER:

ASSIGNMENT:  Final Project (Backgammon)

DATE:        1 May 2017

DESCRIPTION: Program that creates a Backgammon board, chips, and dice that can 
             be played by users entirely in the graphics window.

********************************************************************************
"""



import random
from cs110graphics import *

CPOSITIONS = [(200, 200), (346, 280), (321, 280), (296, 280), (271, 280), \
              (246, 280), (221, 280), (180, 280), (155, 280), (130, 280), \
              (105, 280), (80, 280), (55, 280), (55, 120), (80, 120), \
              (105, 120), (130, 120), (155, 120), (180, 120), (221, 120), \
              (246, 120), (271, 120), (296, 120), (321, 120), (346, 120), \
              (374, 200)]

class Chip(EventHandler):
    """chip class"""
    
    def __init__(self, board, position, team):
        '''initializes chip object'''
        EventHandler.__init__(self)
        self._board = board
        self._chip = Circle(8, (200, 200))
        self._team = team
        if self._team == 0:
            self._chip.setFillColor('white')
        elif self._team == 1:
            self._chip.setFillColor('red')
        self._position = position
        self._depth = 40
        self._chip.setDepth(40)
        self._active = False
        self._moveable = False
        self._chip.addHandler(self)
    
    def getCenter(self):
        '''returns center of chip'''
        return self._chip.getCenter()
    
    def getDepth(self):
        '''returns depth of chip'''
        return self._depth  
    
    def setDepth(self, newDepth):
        '''sets depth for chip'''
        self._depth = newDepth
        self._chip.setDepth(newDepth)
    
    def getTeam(self):
        '''returns current team'''
        return self._team
    
    def getPosition(self):
        '''returns position of chip'''
        return self._position
    
    def addToInit(self, win, position):
        '''sets up place to initially put chips at beginning of game'''
        win.add(self._chip)
        self._chip.moveTo(CPOSITIONS[position])
    
    def moveChip(self, dx, dy):
        '''move chips accordingly'''
        self._chip.move(dx, dy)
    
    def moveChipTo(self, point):
        '''move chips accordingly'''
        self._chip.moveTo(CPOSITIONS[point])
        self._position = point
    
    def getMoveable(self):
        '''returns if chip is moveable'''
        return self._moveable
    
    def makeMoveable(self):
        '''sets up a value if chip is able to be moved'''
        self._moveable = True
    
    def makeUnmoveable(self):
        '''sets up value if chip is unable to be moved'''
        self._moveable = False
        
    def activate(self):
        '''sets up value for chip that is able to create a move'''
        self._active = True
        #visually shows player which chips can move
        self._chip.setBorderColor('green')
        
    def deactivate(self):
        '''sets up value for chip that us unable to create a move'''
        self._active = False
        #visually shows player that chip cannot make valid move
        self._chip.setBorderColor('black')
    
    def validPoints(self):
        '''implements the direction for each team and valid points'''
        validPoints = []
        points = self._board.getPoints()
        values = self._board.getDie().getValues()
        print(values)
        #makes the direction for each team to be used in an ordered list
        if self._board.getCurrent() == 0:
            direction = 1
        elif self._board.getCurrent() == 1:
            direction = -1
        currChipPos = self.getPosition()
        for i in range(len(points)):
            validPoints.append(i)
            #removes the points that cannot be used during a particular move
            if (self._board.piecesOnPoint(i) > 1 and self._board.getCurrent() \
               != self._board.teamOnPoint(i)) or \
               self.validDieMoves(currChipPos, direction, i):
                validPoints.pop() 
        print(validPoints)
        return validPoints
    
    def validDieMoves(self, currChipPos, direction, iValue):
        '''returns True if moves indicated by die values are valid moves'''
        if currChipPos == 0 and self._board.getCurrent() == 1:
            currChipPos = 25
        values = self._board.getDie().getValues()
        countTrue = 0
        for i in range(len(values)):
            if currChipPos + (direction * values[i]) != iValue:
                countTrue += 1
        if countTrue == len(values):
            return True
        return False
    
    def handleMouseRelease(self, event):
        '''selects desired chip to be moved'''
        if self._active:
            for i in self.validPoints():
                self._board.getPoints()[i].activate()
                chips = self._board.getCurrentChips()
                for chip in chips:
                    chip.deactivate()
            self.makeMoveable()


class Point(EventHandler): 
    '''creates point on the board'''
    def __init__(self, board, start, position):
        '''initializes point object'''
        EventHandler.__init__(self)
        self._position = position
        if position == 0:
            self._tri = Rectangle(16, 170, start)
        elif position > 0 and position < 13:
            self._tri = Polygon([start, (start[0] - 25, start[1]), \
                                (start[0] - 12, start[1] - 65)])
        elif position >= 13 and position < 25:
            self._tri = Polygon([start, (start[0] + 25, start[1]), \
                                (start[0] + 12, start[1] + 65)])
        elif position == 25:
            self._tri = Rectangle(25, 174, start)
        
        if position % 2 == 1:
            self._tri.setFillColor('grey')
            self._tri.setBorderColor('black')
        elif position % 2 == 0 and position != 0:
            self._tri.setFillColor('green')
            self._tri.setBorderColor('black')
        elif position == 0:
            self._tri.setFillColor('#D2691E')
            self._tri.setBorderColor('black')
        else:
            self._tri.setBorderColor('black')
        
        if position != -1:
            self._tri.addHandler(self)
        self._tri.setDepth(45)
        
        self._board = board
        self._active = False
        
    def getTri(self):
        '''returns point'''
        return self._tri
    
    def addTo(self, win):
        '''adds point to window'''
        win.add(self._tri)
    
    def activate(self):
        '''sets up value to indicate a point is active'''
        self._active = True
        #visually shows player that a point is able to create a move
        self._tri.setBorderColor('green')

    def deactivate(self):
        '''sets up value to indicate a point is not active'''
        self._active = False
        #visually shows player that a point is unable to create a move
        self._tri.setBorderColor('black')

    def handleMouseEnter(self, event):
        '''creates red background on points when hovered over'''
        if self._active:
            self._tri.setBorderColor('red')

    def handleMouseLeave(self, event):
        '''creates black background on points that are not hovered by mouse''' 
        if self._active:
            self._tri.setBorderColor('green')
    
    def handleMouseRelease(self, event):
        """finds the moveable chip and places is it in self"""
        if self._active:    
            recent = self._board.findAndPlaceChip(self._position)
            moves = self._board.updateMoves(recent)
            points = self._board.getPoints()
            #changes turn once all moves are completed
            if moves == 0:
                for point in points:
                    point.deactivate()
                self._board.changeTurn()
            else:
                for point in points:
                    point.deactivate()
                self._board.activateValidPieces()

    def getPosition(self):
        '''returns position of point'''
        return self._position


class Board:
    '''handles points and sets up visual board for Backgammon'''
    def __init__(self, win, current=None):
        '''initializes board object'''
        self._mainBoard = Rectangle(316, 170, (200, 200))
        self._mainBoard.setDepth(50)
        self._mainBoard.setFillColor('bisque')
        self._mainBoard.setBorderColor('#D2691E')
        self._mainBoardBorder = Rectangle(316, 170, (200, 200))
        self._mainBoardBorder.setDepth(45)
        self._mainBoardBorder.setBorderColor('#D2691E')
        self._mainBoardBorder.setBorderWidth(4)
        self._current = current
        
        #the backgammon logo I drew
        url = 'https://cs.hamilton.edu/~agiarami/images/IMG_3417-2.JPG'
        self._logo = Image(url, (200, 70), 250, 55)
        win.add(self._mainBoard)
        win.add(self._logo)
        
        self._points = []
        midBar = Point(self, (200, 200), 0)
        midBar.addTo(win)
        self._points.append(midBar)
        
        for i in range(1, 7):
            addPix = (i - 1) * 25
            currPoint = Point(self, (358 - addPix, 285), i)
            currPoint.addTo(win)
            self._points.append(currPoint)
        for i in range(7, 13):
            addPix = (i - 1) * 25
            currPoint = Point(self, (342 - addPix, 285), i)
            currPoint.addTo(win)
            self._points.append(currPoint)
        for i in range(13, 19):
            addPix = (i - 13) * 25
            currPoint = Point(self, (42 + addPix, 115), i)
            currPoint.addTo(win)
            self._points.append(currPoint)
        for i in range(19, 25):
            addPix = (i - 13) * 25
            currPoint = Point(self, (58 + addPix, 115), i)
            currPoint.addTo(win)
            self._points.append(currPoint)
        endBar = Point(self, (374, 200), 25)
        self._points.append(endBar)
        endBar.addTo(win)

        #stores chips for each team
        self._redTeam = []
        self._whiteTeam = []        
    
        for i in range(1, 3):
            chipWhite = Chip(self, 1, 0)
            chipWhite.addToInit(win, 1)
            chipWhite.moveChip(0, i * -7)

            chipRed = Chip(self, 24, 1)
            chipRed.addToInit(win, 24)
            chipRed.moveChip(0, i * 7)

            self._whiteTeam.append(chipWhite)
            self._redTeam.append(chipRed)
        
        for i in range(1, 6):
            chipWhite = Chip(self, 12, 0)
            chipWhite.addToInit(win, 12)
            chipWhite.moveChip(0, i * -7)

            chipRed = Chip(self, 13, 1)
            chipRed.addToInit(win, 13)
            chipRed.moveChip(0, i * 7)
            
            self._whiteTeam.append(chipWhite)
            self._redTeam.append(chipRed)

        for i in range(1, 4):
            chipWhite = Chip(self, 17, 0)
            chipWhite.addToInit(win, 17)
            chipWhite.moveChip(0, i * 7)

            chipRed = Chip(self, 8, 1)
            chipRed.addToInit(win, 8)
            chipRed.moveChip(0, i * -7)

            self._whiteTeam.append(chipWhite)
            self._redTeam.append(chipRed)
        
        for i in range(1, 6):
            chipWhite = Chip(self, 19, 0)
            chipWhite.addToInit(win, 19)
            chipWhite.moveChip(0, i * 7)

            chipRed = Chip(self, 6, 1)
            chipRed.addToInit(win, 6)
            chipRed.moveChip(0, i * -7)

            self._whiteTeam.append(chipWhite)
            self._redTeam.append(chipRed)
            
        self._lstTeams = []
        self._lstTeams.append(self._whiteTeam)
        self._lstTeams.append(self._redTeam)
        win.add(self._mainBoardBorder)
        self._die = Die(win, self)
    
    def getCurrentChips(self):
        '''returns current team'''
        if self._current == 0:
            return self._whiteTeam
        return self._redTeam
    
    def getNoncurrentChips(self):
        '''returns noncurrent team'''
        if self._current == 1:
            return self._whiteTeam
        return self._redTeam
    
    def getPoints(self):
        '''returns point'''
        return self._points
    
    def getCurrent(self):
        '''returns team'''
        return self._current
    
    def findAndPlaceChip(self, point):
        '''finds moveable chip and places it on desired point'''
        chips = self.getNoncurrentChips()
        for i in range(len(chips)):
            chip = chips[i]
            if chip.getPosition() == point:
                chip.moveChipTo(0)
        chips = self.getCurrentChips()
        for i in range(len(chips)):
            chip = chips[i]
            if chip.getMoveable():
                start = chip.getPosition()
                chip.moveChipTo(point)
                #decides direction in which to stack chips
                if point > 12 and point < 25:
                    piecesOnPoint = self.piecesOnPoint(point)
                elif point > 0 and point < 13:
                    piecesOnPoint = -self.piecesOnPoint(point)
                else:
                    piecesOnPoint = 0
                chip.moveChip(0, (piecesOnPoint) * 7)
                chip.deactivate()
                chip.makeUnmoveable()
                chip.setDepth(chip.getDepth() - self.piecesOnPoint(point))
        return (start, point)

    def piecesOnPoint(self, point):
        '''returns the number of chips on a point'''
        chips = self._whiteTeam + self._redTeam
        count = 0
        for chip in chips:
            if chip.getPosition() == point:
                count = count + 1
        return count
    
    def teamOnPoint(self, point):
        '''returns team on a certain point'''
        chips = self._whiteTeam + self._redTeam
        for chip in chips:
            if chip.getPosition() == point:
                return chip.getTeam()
        return self._current
    
    def deactivateOffTeam(self):
        '''deactivates noncurrent team'''
        nonCurrent = (self._current + 1) % 2
        for chip in self._lstTeams[nonCurrent]:
            chip.deactivate()
            
    def changeTurn(self):
        """changes turns and color at top right"""

        self.deactivateOffTeam()
        #if self._current is 0, change to 1; if 1, do the opposite
        self._current = (self._current + 1) % 2
        self._die.activate()
    
    def getDie(self):
        '''returns dice'''
        return self._die

    def activateValidPieces(self):
        '''activates pieces that have valid moves based on die values'''
        values = self.getDie().getValues()
        if self._current == 0:
            direction = 1
        elif self._current == 1:
            direction = -1
        for chip in self.getCurrentChips():
            chipPos = chip.getPosition()
            for i in range(len(values)):
                currPoint = chipPos + (direction * values[i])
                if ((self.teamOnPoint(currPoint) == self._current) or \
                   (self.teamOnPoint(currPoint) != self._current and \
                    self.piecesOnPoint(currPoint) < 2)):
                    chip.activate()
                else:
                    chip.deactivate()
    
    def updateMoves(self, startEnd):
        '''updates dice values that are possible moves'''
        start = startEnd[0]
        end = startEnd[1]
        moveMade = abs(start - end)
        self._die.removeValue(moveMade)
        print(len(self._die.getValues()))
        return len(self._die.getValues())

class Die(EventHandler):
    '''sets up die'''
    #Taken from Professor Campbell's class notes
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
                 
    def __init__(self, win, board):
        '''initiziales visual die'''
        EventHandler.__init__(self)
        self._board = board
        self._width = 25
        self._center = (265, 200)
        center = self._center
        width = self._width
        self._square = Rectangle(width, width, center)
        self._square.setFillColor('white')
        self._square.setDepth(20)
        
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor('black')
            pip.setDepth(20)
            self._pips.append(pip)
        
        self._square2 = Rectangle(width, width, (center[0] + 35, center[1]))
        self._square2.setFillColor('white')
        self._square2.setDepth(20)
        self._square.addHandler(self) 
        self._square2.addHandler(self)
        
        self._pips2 = []
        for _ in range(Die.SIDES):
            pip2 = Circle(width / 15, (center[0] + 35, center[1]))
            pip2.setFillColor('black')
            pip2.setDepth(20)
            self._pips2.append(pip2)
    
        self._active = None
        self._used = None
        
        self.addTo(win)
        self._value = random.randrange(Die.SIDES) + 1
        self._value2 = random.randrange(Die.SIDES) + 1
        self._values = [self._value, self._value2]
        
        self._update(1)
        self._update(2)
        if self.rollDoubles():
            self._values = [self._value, self._value, self._value, \
                            self._value]
        self.deactivate()

    def handleMouseRelease(self, event):
        '''allows die to roll when clicked on'''
        if self._active:
            self.roll()
            self.deactivate
    
    def deactivate(self):
        '''deactives dice'''
        self._active = False
        self._used = False
        self._square.setBorderColor('black')
        self._square2.setBorderColor('black')
    
    def activate(self):
        '''actives dice'''
        self._active = True
        self._used = True
        self._square.setBorderColor('green')
        self._square2.setBorderColor('green')
        
    def addTo(self, win):
        '''adds pips onto die square'''
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)
        win.add(self._square2)
        for pip in self._pips2:
            win.add(pip)
    
    def roll(self):
        '''makes die have random value'''
        if self._used:
            self._value = random.randrange(Die.SIDES) + 1
            self._value2 = random.randrange(Die.SIDES) + 1
        
            self._values = [self._value, self._value2]
        
            self._update(1)
            self._update(2)
            if self.rollDoubles():
                self._values = [self._value, self._value, self._value, \
                                self._value]
            self.deactivate()
            self._board.activateValidPieces()

    def getValues(self):
        '''returns values on both die'''
        return self._values
    
    def rollDoubles(self):
        '''checks if dice values are equal'''
        if self._value == self._value2:
            return True
        return False    
    
    def _update(self, dieNum):
        '''visually changes die to match value'''
        if dieNum == 1:
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
        elif dieNum == 2:
            positions = Die.POSITIONS[self._value2]
            for i in range(len(positions)):
                if positions[i] is None:
                    self._pips2[i].setDepth(25)
                else:
                    self._pips2[i].setDepth(15)
                    cx, cy = self._center  
                    dx = positions[i][0] * self._width
                    dy = positions[i][1] * self._width  
                    self._pips2[i].moveTo((cx + dx + 35, cy + dy))
    
    def getUsed(self):
        '''returns which die values have been used'''
        return self._used

    def removeValue(self, value):
        '''removes value from possible moves that a chip can make'''
        values = self._values
        for i in range(len(values)):
            if values[i] == value:
                self._values = values[:i] + values[i + 1:]
                


def main(win):
    '''creates and starts a backgammon board game'''
    board = Board(win, 0)
    board.activateValidPieces()

StartGraphicsSystem(main)



