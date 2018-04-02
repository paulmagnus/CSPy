"""
*****************************************************************************
FILE: Game.py

AUTHOR: Julia Opatrny

PARTNER: N/A

ASSIGNMENT: Project 6

DATE: May 1, 2017

DESCRIPTION: An interactive Scrabble game. Users can choose how many players 
are playing, can place letter pieces onto the board to form words by clicking,
and each player's points are recorded. At the end of the game, a winner is 
declared, determined by the player with the highest score.
*****************************************************************************
"""

import random
from cs110graphics import * 

class Spot(EventHandler):
    """ Creates a class for a single spot on the board. """
    def __init__(self, color, value, multiplier, text1, text2, text3, center,
                 board, pos):
        """ Names the attributes for each spot on the board, including each 
        spot's value and multiplier, what playing piece is on it, and whether 
        or not a piece can be placed on it."""
        EventHandler.__init__(self)
        self._spot = Square(40, center)
        self._spot.setBorderColor('white')
        self._spot.setFillColor(color)
        self._text1 = Text(text1, (center[0], center[1]-5), 9)
        self._text2 = Text(text2, (center[0], center[1] + 5), 9)
        self._text3 = Text(text3, (center[0], center[1] + 15), 9)
        self._spotobjects = [self._spot, self._text1, self._text2, self._text3]
        self._value = value
        self._multiplier = multiplier
        self._center = center
        self._placed = False
        self._tile = None
        self._pos = pos
        self._canPlace = True
        
        
        # adds an Event Handler to each item in the spot
        for obj in self._spotobjects:
            obj.addHandler(self)
            
        self._board = board
            
        
        
    def addTo(self, win):
        """ Adds every item in the spot to the window. """
        for obj in self._spotobjects:
            win.add(obj)
            
    def moveTo(self, pos):
        """ Moves every item in a spot to a certain position. """
        for obj in self._spotobjects:
            obj.moveTo(pos)
            
    def handleMouseRelease(self, event):
        """ Sends information to the Board class when a spot is clicked. """
        
        # sends information only if a piece can be placed on the spot
        if self._canPlace:
            
            #sends the entire spot, as well as the center of the spot
            self._board.sendSpot(self)
            self._board.sendcoordinate(self._center)
        
        
    def getValue(self):
        """ Returns the value of the spot. """
        return self._value
    
    def getMultiplier(self):
        """ Returns the multiplier of the spot. """
        return self._multiplier
        
    def pieceOn(self):
        """ Sets self._placed equal to True. """
        self._placed = True
        
    def isPieceOn(self):
        """ Returns whether or not there is a piece placed on the spot, 
        or self._placed. """
        return self._placed
        
    def setPiece(self, piece):
        """ Sets a piece on that spot, and reassigns the self._tile 
        attribute. """
        self._tile = piece
    
    def getPos(self):
        """ Returns the position of the spot. """
        return self._pos
        
    def getPiece(self):
        """ Returns self._tile, or what piece is on that spot. """
        return self._tile
        
    def makeAvailable(self):
        """ Sets self._canPlace equal to True, or makes that spot available 
        for a playing piece to be placed on. """
        self._canPlace = True
        
    def makeUnavailable(self):
        """ Makes that spot unavailable for a playing piece to be placed on. """
        self._canPlace = False
        
    def canPlace(self):
        """ Returns self._canPlace, or whether or not a piece can be placed 
        on that spot. """
        return self._canPlace
            
    
class Board:
    """ Creates a class for the board."""
    def __init__(self):
        """ Creates the spots on the board. """
        
        
        dx = 50
        dy = 50
        
        # each type of spot on the board
        r = ('#DEB887', 1, 1, "", "", "")
        dw = ('#FFB6C1', 1, 2, "DOUBLE", "WORD", "SCORE")
        tw = ('#B22222', 1, 3, "TRIPLE", "WORD", "SCORE")
        dl = ('#ADD8E6', 2, 1, "DOUBLE", "LETTER", "SCORE")
        tl = ('#4682B4', 3, 1, "TRIPLE", "LETTER", "SCORE")
        center = ('#FFB6C1', 1, 2, "", u"\u2605", "")
        
        # the board grid
        spots = [[tw, r, r, dl, r, r, r, tw, r, r, r, dl, r, r, tw],
                 [r, dw, r, r, r, tl, r, r, r, tl, r, r, r, dw, r],
                 [r, r, dw, r, r, r, dl, r, dl, r, r, r, dw, r, r,],
                 [dl, r, r, dw, r, r, r, dl, r, r, r, dw, r, r, dl],
                 [r, r, r, r, dw, r, r, r, r, r, dw, r, r, r, r],
                 [r, tl, r, r, r, tl, r, r, r, tl, r, r, r, tl, r],
                 [r, r, dl, r, r, r, dl, r, dl, r, r, r, dl, r, r],
                 [tw, r, r, dl, r, r, r, center, r, r, r, dl, r, r, tw],
                 [r, r, dl, r, r, r, dl, r, dl, r, r, r, dl, r, r],
                 [r, tl, r, r, r, tl, r, r, r, tl, r, r, r, tl, r],
                 [r, r, r, r, dw, r, r, r, r, r, dw, r, r, r, r],
                 [dl, r, r, dw, r, r, r, dl, r, r, r, dw, r, r, dl],
                 [r, r, dw, r, r, r, dl, r, dl, r, r, r, dw, r, r,],
                 [r, dw, r, r, r, tl, r, r, r, tl, r, r, r, dw, r],
                 [tw, r, r, dl, r, r, r, tw, r, r, r, dl, r, r, tw]]
        
        
        # whether or not a piece is selected         
        self._selectedpiece = None
        
        # coordinates of a spot, to be reassigned laters
        self._coordinates = None
        self._selected = False
        
        # list of spots played during each turn
        self._spots = []
        self._playedSpots = []
        
        self._spot = None
        
        # list of spots played the entire game
        self._allPlayedSpots = []
        
        for x in range(len(spots)):
            row = []
            for y in range(len(spots[x])):
                ti = Spot(spots[x][y][0], spots[x][y][1], spots[x][y][2],
                          spots[x][y][3], spots[x][y][4], spots[x][y][5], 
                          (dx, dy), self, (x, y))
                row.append(ti)
                dx += 40
            self._spots.append(row)
            dx = 50
            dy += 40
            
    def addTo(self, win):
        """ Adds each spot to the window. """
        for row in self._spots:
            for spot in row:
                spot.addTo(win)
            
    def report(self, piece):
        """ Reports the selected piece to the board. """
        self._selectedpiece = piece

        
    def sendcoordinate(self, center):
        """ Sends the coordinate of the spot to the board and moves the 
        selected piece. """
        self._coordinates = center
        self.snapTo()
        
    
    def sendSpot(self, spot):
        """ Sends the spot to the board. """
        self._spot = spot
        

    def snapTo(self):
        """ Snaps the selected piece to the coordinates of the selected spot.
        Also appends the list of pieces played the entire game, updates the
        spots that can hold a piece and deselects the piece. """
        
        # if there is a piece selected
        if self._selectedpiece:
            
            self._selectedpiece.moveTo(self._coordinates)
            self._playedSpots.append(self._spot)
            self._allPlayedSpots.append(self._spot)
            self._selectedpiece.spotPlace(self._spot)
            self._spot.setPiece(self._selectedpiece)
            self._selectedpiece.changeColorBack()
            self._selectedpiece.used()
            self.deselect()
            self._selectedpiece = None
            self.updateAvailability()
            
    def select(self):
        """ Sets self._selected equal to True, or tells the board that there 
        is a piece selected. """
        self._selected = True
        
    def isSelected(self):
        """ Returns self._selected, or whether or not there is a piece 
        selected. """
        return self._selected
        
    def deselect(self):
        """ Sets self._selected equal to False, or tells the board that there
        are no pieces selected. """
        self._selected = False
        
    def emptySpots(self):
        """ Empties the spots played that turn. """
        self._playedSpots = []
        
    def getSpots(self):
        """ Returns the spots played that turn. """
        return self._playedSpots
        
    def allSpots(self):
        """ Returns all the spots on the board. """
        return self._spots
        
    def updateAvailability(self):
        """ Updates where pieces can be placed on the board, making sure the 
        player can only place pieces next to a preexisting piece. """
        
        # makes every spot on the board unavailable
        for x in self._spots:
            for spot in x:
                spot.makeUnavailable()
        dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        
        # goes through every spot ever played, and makes the spot in all four
        # directions available
        for spot in self._allPlayedSpots:
            coorx, coory = spot.getPos()
            for dr in dirs:
                newx = coorx + dr[0]
                newy = coory + dr[1]
                
                # makes sure list does not go out of range when a piece is on
                # the edge of the board
                if newx >= 0 and newx <= 14 and newy >= 0 and newy <= 14:
                    nearspot = self._spots[newx][newy]
                    nearspot.makeAvailable()
       

class Piece(EventHandler):
    """ Creates a class for a single letter playing piece. """
    def __init__(self, letter, number, center, board):
        """ Names the attributes for a playing piece. """
        EventHandler.__init__(self)
        self._wood = Image(
            "https://cs.hamilton.edu/~jopatrny/images/wood-911002_960_720-1.jpg"
            , center, width=39, height=39)
        self._wood.setDepth(11)
        self._back = Square(40, center)
        self._back.setFillColor('#DEB887')
        self._back.setBorderColor('#DEB887')
        self._back.setDepth(12)
        self._letter = letter
        self._text = Text(letter, (center[0], center[1]+5), 20)
        self._text.setDepth(10)
        self._value = int(number)
        self._number = Text(number, (center[0] + 13, center[1] + 15), 13)
        self._number.setDepth(10)
        self._pieceobjects = [self._wood, self._back, self._text, self._number]
        for obj in self._pieceobjects:
            obj.addHandler(self)
        self._location = center
        self._board = board
        self._active = False
        self._used = False
        self._placed = False
        self._selected = False
        self._onSpot = None
        
    def remove(self, win):
        """ Removes all the parts of a piece from the window except for the wood
        and the back. """
        for obj in self._pieceobjects[2:]:
            win.remove(obj)
        
        
    def addTo(self, win):
        """ Adds all the parts of a piece to the window. """
        for obj in self._pieceobjects:
            win.add(obj)
            
    def moveTo(self, point):
        """ Moves a piece to a certain point, accounting for the text and number
        which are off-center. """
        self._wood.moveTo(point)
        self._text.moveTo((point[0], point[1]+5))
        self._number.moveTo((point[0] + 13, point[1] + 15))
        self._back.moveTo(point)
        
    def handleMouseRelease(self, event):
        """ Selects a piece when it is clicked. """
        
        # if the piece is already selected when it is clicked, it deselects it
        # and changes its border color back
        if self._selected:
            self.changeColorBack()
            self._board.deselect()
            self._selected = False
            return
        
        # returns if there is already a piece selected
        if self._board.isSelected():
            return
        
        # if the piece is active, it activates it and tells the board that there
        # is a piece selected
        if self._active:
            self._board.select()
            self._selected = True
            self._back.setBorderColor('black')
            self._board.report(self)
        else:
            return
        
    def changeColorBack(self):
        """ Sets the back color to the original color. """
        self._back.setBorderColor('#DEB887')
    
    def activate(self):
        """ Activates the piece, so that it can be played. """
        self._active = True
        
    def deactivate(self):
        """ Deactivates the piece so that it cannot be played. """
        self._active = False
        
    def used(self):
        """ Sets self._used equal to True, or tells the piece that it has been
        used. """
        self._used = True
    
    def finished(self):
        """ Returns whether or not the piece has been used. """
        return self._used
        
    def place(self):
        """ Sets self._placed equal to true, or tells the piece that it has 
        been placed. """
        self._placed = True
        
    def placed(self):
        """ Returns whether or not the piece has been placed. """
        return self._placed 
        
    def getValue(self):
        """ Returns the value of the piece. """
        return self._value
        
    def spotPlace(self, spot):
        """ Tells the piece what spot it is on. """
        self._onSpot = spot
        
    def giveSpot(self):
        """ Returns what spot the piece is on. """
        return self._onSpot
        
        
class Alphabet:
    """ Creates a class for all of the playing pieces. """
    def __init__(self, board):
        """ Creates all of the playing pieces for the game. """
        
        # all of the letters with their values and how many of them there are
        alphabet = [("A", 1, 9), ("B", 3, 2), ("C", 3, 2), ("D", 2, 4), 
                    ("E", 1, 12), ("F", 4, 2), ("G", 2, 3), ("H", 4, 2),
                    ("I", 1, 9), ("J", 8, 1), ("K", 5, 1), ("L", 1, 4),
                    ("M", 3, 2), ("N", 1, 6), ("O", 1, 8), ("P", 3, 2),
                    ("Q", 10, 1), ("R", 1, 6), ("S", 1, 4), ("T", 1, 6),
                    ("U", 1, 4), ("V", 4, 2), ("W", 4, 2), ("X", 8, 1),
                    ("Y", 4, 2), ("Z", 10, 1)]
        
        self._total = []
        self._alltiles = []
        self._board = board

        
        dx = 15
        dy = 15
        
        for x in range(len(alphabet)):
            for _ in range(alphabet[x][2]):
                piece = Piece(alphabet[x][0], alphabet[x][1], (dx, dy), board)
                self._total.append(piece)
                self._alltiles.append(piece)
                
    def drawTile(self):
        """ Draws a random playing piece. """
        randomnum = random.randrange(len(self._total))
        drawn = self._total[randomnum]
        self._total.pop(randomnum)
        return drawn
        
    
    def getTotal(self):
        """ Returns the length of the list of playing pieces. """
        return len(self._total)
        
    def getAll(self):
        """ Returns all the tiles. """
        return self._alltiles
            
class GameManager(EventHandler):
    """ Creates the Game Manager class, which sets up the game, distributes
    pieces, and keeps score. """
    def __init__(self, win):
        """ Creates the board, the buttons, determines the number of players and
        distributes pieces accordingly. """
        EventHandler.__init__(self)
        
        # determines how many players there are
        done = False
        while not done:
            self._number = int(input("Welcome to Scrabble! How many players \
are there? Please enter a number between 1 and 4."))
            if 1 <= self._number <= 4:
                done = True

        self._win = win
        
        #sets the title of the window
        self._win.setTitle("Welcome to Scrabble!")
        
        self._board = Board()
        self._tiles = Alphabet(self._board)
        
        # creates the "Next Turn" button as well as the background
        self._button = Image(
            "https://cs.hamilton.edu/~jopatrny/images/NEXT_TURN.png", 
            (815, 570), width=300, height=80)
        self._pushbutton = Image(
            "https://cs.hamilton.edu/~jopatrny/images/NEXT_TURN_pressed.png", 
            (815, 570), width=300, height=80)
        self._background = Image(
            "https://cs.hamilton.edu/~jopatrny/images/background.png", 
            (550, 350), width=1100, height=710)
        self._background.setDepth(100)
        self._parts = [self._background, self._button, self._pushbutton]
        for part in self._parts:
            self._win.add(part)
    
        for part in self._parts[1:]:
            part.addHandler(self)
            
        for x in range(1, 3):
            self._parts[x].setDepth(10 + x)
        

        # creates an instance of the pop-up instruction window
        Instruction(self._win)
        
        self._board.addTo(win)
        self._currentplayer = 0
        
        
        # creates empty lists to be appended as the game is played
        self._players = []
        self._scores = []
        self._currentSpots = []
        
        # creates the "Game Over" and "Info" buttons
        self._gameover = GameOver(self._win, self._scores, self._tiles)
        self._info = Info(self._win)
        
        # starts every player with a score of 0
        for x in range(self._number):
            self._players.append([])
            self._scores.append(0)
            
        # draws 7 tiles for every player
        for x in range(len(self._players)):
            for i in range(7):
                drawn = self._tiles.drawTile()
                self._players[x].append(drawn)
                
        dx = 700
        dy = 40
        
        # adds each player's pieces facedown to the window
        for x in range(self._number):
            playertext = Text("Player " + str(x+1), (dx, dy + 15), 25)
            playerscore = Text("Score: ", (dx + 200, dy + 15), 20)
            win.add(playertext)
            win.add(playerscore)
            for i in range(len(self._players[x])):
                self._players[x][i].addTo(win)
                self._players[x][i].place()
                self._players[x][i].moveTo((dx, dy + 50))
                self._players[x][i].remove(self._win)
                dx += 50
            dx = 700
            dy += 125
            
        # activates the current pieces and adds them to the window
        self._currentpieces = self._players[self._currentplayer]
        self.current()
        self.replace(self._win)
        self._currentscore = self._scores[self._currentplayer]
        
        # adds each player's score to a list, then adds them to the window
        self._textScores = []
        for x in range(len(self._scores)):
            self._textScores.append(Text(self._scores[x], 
                                         (970, 50 +(x * 125)), 20))
        
        for score in self._textScores:
            self._win.add(score)
        
    def current(self):  
        """ Activates the current player's pieces. """
        for obj in self._currentpieces:
            obj.activate()
         
            
                
    def changePlayer(self):
        """ The pieces that were just played are removed from the active pieces,
        the word that the player just played is found, and the score is updated.
        The pieces of the player are turned facedown and are deactivated. 
        The current player is then incremented to the next player. """
        self.removepieces()
        self.searchSpots()
        self.updateScore(self._win)
        self._board.emptySpots()
        self._currentSpots = []
        for obj in self._currentpieces:
            obj.remove(self._win)
        self.refill()
        for obj in self._currentpieces:
            obj.deactivate()
        self._currentplayer += 1
        self._currentplayer = self._currentplayer % self._number
        for obj in self._players[self._currentplayer]:
            obj.activate()
        self._currentpieces = self._players[self._currentplayer]
        self._currentscore = self._scores[self._currentplayer]
        self.replace(self._win)
        
        # if there are no more pieces left to draw and the current player has 
        # no pieces, the game is over
        if (self._tiles.getTotal == 0 and 
                len(self._players[self._currentplayer]) == 0):
            self._gameover.endgame()  
        
        
    def handleMousePress(self, event):
        """ When the "Next Turn" button is pressed, it removes itself to reveal
        a "pressed" version beneath it. """
        self._win.remove(self._button)

        
    
    def handleMouseRelease(self, event):
        """ When the mouse is released, the first "Next Turn" button reappears
        and the player is changed. """
        self._win.add(self._button)
        self.changePlayer()
        
        
    def refill(self):
        """ Draws pieces until the current player has 7 pieces. """
        while len(self._players[self._currentplayer]) != 7:
            drawn = self._tiles.drawTile()
            self._currentpieces.append(drawn)
        
    def replace(self, win):
        """ Adds the current player's pieces to the window. """
        dx = 700
        dy = 90 + (self._currentplayer * 125)
        for i in range(len(self._currentpieces)):
            self._currentpieces[i].addTo(win)
            self._currentpieces[i].moveTo((dx, dy))
            dx += 50
            
    def updateScore(self, win):
        """ Adds the updated score to the window. """
        win.remove(self._textScores[self._currentplayer])
        self.calculate()
        self._textScores[self._currentplayer] = Text(self._scores
                                                     [self._currentplayer], 
                                                     (970, 50 +
                                                      (self._currentplayer * 
                                                       125)), 20)
        win.add(self._textScores[self._currentplayer])
    
    
    def removepieces(self):
        """ Goes through all the current pieces and if a piece has been placed
        on the board, it removes it from the list of current pieces and 
        deactivates it. """
        for i in range(len(self._currentpieces)-1, -1, -1):
            if self._currentpieces[i].finished():
                spot = self._currentpieces[i].giveSpot()
                spot.pieceOn()
                self._currentSpots.append(spot)
                self._currentpieces[i].deactivate()
                self._currentpieces.pop(i)
                
    
    def getSpotsInDir(self, sp, dr):
        """ Goes in every direction from a spot and adds the spots that are 
        found to a list. """
        foundspots = []
        coorx, coory = sp.getPos()
        spots = self._board.allSpots()
        newx = coorx + dr[0]
        newy = coory + dr[1]
        if newx >= 0 and newx <= 14 and newy >= 0 and newy <= 14:
            spot = spots[coorx + dr[0]][coory + dr[1]]
            while spot.isPieceOn():
                foundspots.append(spot)
                coorx += dr[0]
                coory += dr[1]
                if coorx >= 0 and coorx <= 14 and coory >= 0 and coory <= 14:
                    spot = spots[coorx][coory]
        return foundspots
    
    
    def searchSpots(self):
        """ Searches in every direction from the spots played that turn to find
        the pieces of a word. """
        played = self._board.getSpots()
        dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for sp in played: 
            for dr in dirs:
                spotsindir = self.getSpotsInDir(sp, dr)
                for spot in spotsindir:
                    if spot not in self._currentSpots:
                        self._currentSpots.append(spot)
                        
                
                
        
    def calculate(self):
        """ Calculates the score of a players turn. """
        played = self._board.getSpots()
        turnscore = 0
        for i in range(len(self._currentSpots)):
            piece = self._currentSpots[i].getPiece()
            
            # only if the spot was played in the turn does the piece value get
            # multiplied by the spot value
            if self._currentSpots[i] in played:
                score = piece.getValue() * self._currentSpots[i].getValue()
                turnscore += score
                
            # otherwise just the piece values are added
            else:
                turnscore += piece.getValue()
        
        
        for j in range(len(self._currentSpots)):
            
            # only if the piece was just played in the turn does the word get
            # multiplied
            if self._currentSpots[j] in played:
                turnscore = turnscore * self._currentSpots[j].getMultiplier()
                
        self._scores[self._currentplayer] += turnscore
        
class GameOver(EventHandler):
    """ Creates a class for a "Game Over" button that determines the winner of
    the game. """
    def __init__(self, win, scores, tiles):
        """ Creates the "Game Over" button and the window that appears when it 
        is clicked. """
        EventHandler.__init__(self)
        self._gameover = Image(
            "https://cs.hamilton.edu/~jopatrny/images/game_over.png", 
            (1025, 570), width=70, height=70)
        self._win = win
        self._win.add(self._gameover)
        self._gameover.addHandler(self)
        self._scores = scores
        self._tiles = tiles
        self._window = Rectangle(600, 200, (550, 350))
        self._window.setDepth(8)
        self._window.setFillColor('#E0FFFF')
        self._window.setBorderColor('#B22222')
        
    def handleMouseRelease(self, event):
        """ Ends the game when the button is clicked. """
        self.endgame()
        
    def endgame(self):
        """ Determines the player with the highest score and adds a window to
        that says who won the game, as well as deactivating all the pieces.  """
        alltiles = self._tiles.getAll()
        for tile in alltiles:
            tile.deactivate()
            
        topscore = self._scores[0]
        highestplayer = 0
        for i in range(len(self._scores)):
            if self._scores[i] > topscore:
                topscore = self._scores[i]
                highestplayer = i
                
        text1 = Text("GAME OVER!", (550, 325), 50)
        text2 = Text("PLAYER " + str(highestplayer + 1) + " WINS!", 
                     (550, 400), 50)
        text1.setDepth(7)
        text2.setDepth(7)
        self._win.add(text1)
        self._win.add(text2)
        self._win.add(self._window)
        
        

class Instruction(EventHandler):
    """ Creates a class for a pop-up window with instructions. """
    def __init__(self, win):
        """ Creates a pop-up window as well as a "OK" button. """
        EventHandler.__init__(self)
        self._box = Image(
            "https://cs.hamilton.edu/~jopatrny/images/INSTRUCTIONS.png", 
            (550, 300), width=700, height=200)
        self._box.setDepth(8)
        self._win = win
        self._button = Image(
            "https://cs.hamilton.edu/~jopatrny/images/OK.png", (830, 350), 
            width=100, height=50)
        self._button.setDepth(7)
        self._button.addHandler(self)
        self._win.add(self._button)
        self._win.add(self._box)
    
    def handleMouseRelease(self, event):
        """ When the button is pressed, the window and the button are 
        removed. """
        self._win.remove(self._button)
        self._win.remove(self._box)
            
                
class Info(EventHandler):
    """ Creates a class for a button that creates an instance of the Instruction
    class. """
    def __init__(self, win):
        """ Creates the "Info" button. """
        EventHandler.__init__(self)
        self._win = win
        self._button = Image(
            "https://cs.hamilton.edu/~jopatrny/images/INFO.png", (1050, 26),
            width=50, height=50)
        self._button.addHandler(self)
        self._win.add(self._button)
        
    def handleMouseRelease(self, event):
        """ Creates an instance of the Instruction class when the button is
        pressed. """
        Instruction(self._win)

def first(win):
    """ Function that runs the game. """
    height = 700
    width = 1100
    win.setHeight(height)
    win.setWidth(width)
    _ = GameManager(win)
    
    

StartGraphicsSystem(first)
