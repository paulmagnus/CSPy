"""
********************************************************************************
FILE: Game.py
AUTHOR: Zack Weinstein
PARTNER: N/A
ASSIGNMENT: Game
DATE: 5/1/2017
DESCRIPTION: A program designed to create an (almost) fully functional game of
Scrabble.
********************************************************************************
"""

from random import shuffle
from cs110graphics import *

class UndoButton(EventHandler):
    """ An undo button that redos the player's last move """
    
    def __init__(self, board, win, width, height, center):
        """ Initializae the undo button """
        EventHandler.__init__(self)
        self._board = board
        self._rect = Rectangle(width, height, center)
        self._rect.setFillColor("burlywood")
        self._rect.addHandler(self)
        self._text = Text("Undo", center, 15)
        win.add(self._rect)
        win.add(self._text)
        
    def handleMouseRelease(self, event):
        """" Undo the last move when the mouse is released """
        self._board.undo()
        
class EndTurnButton(EventHandler):
    """ An end turn button to change turns and see if a winner has occured """
    
    def __init__(self, board, win, width, height, center):
        """ Initialize end turn button """
        EventHandler.__init__(self)
        self._board = board
        self._rect = Rectangle(width, height, center)
        self._rect.setFillColor("tan")
        self._text = Text("End", center, 15)
        self._rect.addHandler(self)
        win.add(self._rect)
        win.add(self._text)
        
    def handleMouseRelease(self, event):
        """ End turn when the mouse is released """
        self._board.endTurn()
        
class Tile(EventHandler):
    """ Set up tiles that are the pieces for the game """
    
    def __init__(self, letter, player):
        """ Initialize the tiles """
        EventHandler.__init__(self)
        self._letter = letter
        self._player = player
        self._back = Rectangle(17, 17)
        self._front = Text(letter)
        self._back.setFillColor("khaki")
        self._back.addHandler(self)
        self._moving = False
        self._location = (0, 0)
        self._home = (0, 0)
        self._startPos = None    # mouse position where movement started
        self._active = False
        self._depth = 0
        self._back.setDepth(0)
        self._front.setDepth(0)
        self._scored = False
        
    def getDepth(self):
        """ Return the depth of the tile """
        return self._depth
        
    def setDepth(self, depth):
        """ Set the depth of the tile """
        self._depth = depth
        self._back.setDepth(depth)
        self._front.setDepth(depth)
    
    def activate(self):
        """ Activate a tile so it can be used """
        self._active = True
        self._back.setBorderColor('green')
        
    def deactivate(self):
        """ Deactivate a tile so it cannot be used """
        self._active = False
        self._back.setBorderColor('black')
    
    def highlight(self):
        """ Highlight a tile to acknowledge that it has been activated """
        self._back.setBorderColor('yellow')
    
    def addTo(self, win):
        """ Add a tile to the window """
        win.add(self._back)
        win.add(self._front)
        
    def remove(self, win):
        """ Remove a tile from the window """
        win.remove(self._back)
        win.remove(self._front)
    
    def moveTo(self, pos):
        """ Move a tile to a given location """
        self._back.moveTo(pos)
        self._front.moveTo(pos)
        self._location = pos
        
    def getHome(self):
        """ Return the home location of a tile """
        return self._home
        
    def setHome(self, home):
        """ Set the home location of a tile """
        self._home = home
    
    def moveToHome(self):
        """ Move a tile to its home location """
        self.moveTo(self._home)
    
    def move(self, dx, dy):
        """ Move a tile by dx, dy units """
        oldx, oldy = self._location
        newx = oldx + dx
        newy = oldy + dy
        self.moveTo((newx, newy))
        
    def getPlayer(self):
        """ Return the player who controls the tile """
        return self._player
        
    def setPlayer(self, player):
        """ Set what player controls the tile """
        self._player = player
    
    def getLocation(self):
        """ Return the location of a tile """
        return self._location
        
    def getLetter(self):
        """ Return the letter of a tile """
        return self._letter
        
    def score(self):
        """ Set scored to True to show the tile has been scored """
        self._scored = True
        
    def scored(self):
        """ Return if the tile has been scored """
        return self._scored
    
    def handleMouseRelease(self, event):
        """ Report to the player when a tile is placed """
        if not self._active:
            return 
        if self._moving:
            self._moving = False
            self._player.report(self, event)
        else:
            self._moving = True
            self._startPos = event.getMouseLocation()
    
    def handleMouseMove(self, event):
        """ Moves a tile around when the mouse moves """
        if not self._active:
            return
        if self._moving:
            oldx, oldy = self._startPos
            newx, newy = event.getMouseLocation()
            self.move(newx - oldx, newy - oldy)
            self._startPos = newx, newy

class TileBag:
    """ A bag of tiles that the board will use """
    
    def __init__(self):
        """ Initialize the tile bag """
        self._tiles = []
        letters = ["E", "A", "O", "T", "I", "N", "R", "S", "D", "L", "U", "C",
                   "M", "G", "H", "B", "P", "F", "W", "Y", "V", "K", "J", "X",
                   "Q", "Z"]
        times = [24, 16, 15, 15, 13, 13, 13, 10, 8, 7, 7, 6, 6, 5, 5, 4, 4, 4,
                 4, 4, 3, 2, 2, 2, 2, 2]
        for i in range(len(letters)):
            for _ in range(times[i]):
                self._tiles.append(Tile(letters[i], None))
        shuffle(self._tiles)
                
    def getItem(self, i):
        """ Return a tile from the tile bag """
        return self._tiles[i]
        
    def isEmpty(self):
        """ Return True if the tile bag is empty """
        return len(self._tiles) == 0
    
    def drawTile(self, tile, location):
        """ Draw and remove a tile from the bag and move it to a location """
        tile.moveTo(location)
        tile.setHome(location)
        self._tiles.remove(tile)
            
class Cell:
    """ Cells that are the spots for tiles to be placed on. Have different 
        values depending on if they are double word, etc. """
        
    def __init__(self, win, pos, color, score):
        """ Initialize a cell """
        self._win = win
        self._location = pos
        self._color = color
        self._rect = Rectangle(20, 20, pos)
        self._rect.setFillColor(color)
        self._front = None
        self._score = score
        win.add(self._rect)
        self._tile = None
        self._depth = 1
        self._rect.setDepth(2)
        self._isDL = False
        self._isDW = False
        self._isTL = False
        self._isTW = False
        
    def isDL(self):
        """ Return if a cell is a double letter spot """
        return self._isDL
        
    def isDW(self):
        """ Return if a cell is a double word spot """
        return self._isDW
        
    def isTL(self):
        """ Return if a cell is a triple letter spot """
        return self._isTL
        
    def isTW(self):
        """ Return if a cell is a triple word spot """
        return self._isTW
        
    def getDepth(self):
        """ Return the depth of a cell """
        return self._rect.getDepth()
        
    def setDepth(self, depth):
        """ Set the depth of a cell """
        self._depth = depth
        self._rect.setDepth(depth)
        
    def addTo(self, win):
        """ Add a cell to the window """
        win.add(self._rect)
    
    def getLocation(self):
        """ Get the location of a cell """
        return self._location
    
    def getTile(self):
        """ Return the tile that is on the cell """
        return self._tile
        
    def isEmpty(self):
        """ Return True if the cell does not have a tile on it """
        return self._tile is None
        
    def addTile(self, tile):
        """ Add a tile to the cell """
        self._tile = tile
        
    def removeTile(self):
        """ Remove a tile from the cell """
        self._tile = None
        
    def setFillColor(self, color):
        """ Set the fill color of a cell. Red indicates a triple word cell, blue
            indicates a triple letter cell, cyan indicates a double letter cell,
            and pink indicates a double word cell. All other colors (white) do
            not have special values """
        self._rect.setFillColor(color)
        if color == "red":
            self._isTW = True
        elif color == "blue":
            self._isTL = True
            self._front = Text("TL")
        elif color == "cyan":
            self._isDL = True
        elif color == "pink":
            self._isDW = True
        
    def getFillColor(self):
        """ Return the fill color of a cell """
        return self._rect.getFillColor
        
class Player:
    """ Create a player (numbered 0 or 1) to play the game """
    
    def __init__(self, win, num, board):
        """ Initialize a player """
        
        self._tiles = []
        self._win = win
        self._num = num
        self._board = board
        self._tileBag = TileBag()
        self._score = 0
        
        # Draw initial tiles for the player that are put in that player's tray
        for i in range(7):
            tile = self._tileBag.getItem(i)
            tile.setPlayer(self)
            tile.addTo(win)
            self._tileBag.drawTile(tile, ((60 + i * 20 + num * 160), 375))
            tile.setHome(((60 + i * 20 + num * 160), 375))
            self._board.getTrays()[i + 7 * num].addTile(tile)
            self._tiles.append(tile)
    
    def getNum(self):
        """ Return which number (0 or 1) the player is """
        return self._num
        
    def report(self, tile, event):
        """ Report an event to the board """
        self._board.report(tile, event)
    
    def activateAll(self):
        """ Activate all of a player's tiles """
        for tile in self._tiles:
            tile.activate()
    
    def removeTile(self, tile):
        """ Remove a tile from the player's control """
        pos = None        
        for i in range(len(self._tiles)):
            if self._tiles[i] == tile:
                pos = i
        if pos != None:
            self._tiles.pop(pos)
                
    def addTile(self, tile):
        """ Add a tile to the player's control """
        self._tiles.append(tile)
    
    def deactivateAll(self):
        """ Deactivate all of a player's tiles """
        for tile in self._tiles:
            tile.deactivate()
            
    def getScore(self):
        """ Return how many points the player has """
        return self._score
        
    def addScore(self, score):
        """ Add points to the player's current score """
        self._score += score

            
class Board:
    """ Create the board for the game to be played on """
    
    def __init__(self, win):
        """ Initialize the board """
        
        self._win = win
        
        # Set up a history for the undo button
        self._history = []
        
        # Set up the tile bag to be used for a given game
        self._tileBag = TileBag()
            
        # Set up the board in the form of a grid, kept in self._cells
        self._cells = []
        ypos = 60
        for rows in range(15):
            xpos = 60
            self._cells.append([])
            for cols in range(15):
                color = "white"
                if rows == cols or rows == (14 - cols):
                    if rows == 0 or rows == 14:
                        color = "red"
                    elif cols == 5 or cols == 9:
                        color = "blue"
                    elif cols == 6 or cols == 8:
                        color = "cyan"
                    elif cols == 7:
                        color = "black"
                    else:
                        color = "pink"
                thisCell = Cell(win, (xpos, ypos), color, None)
                thisCell.addTo(win)
                self._cells[-1].append(thisCell)
                xpos += 20
            ypos += 20
        
        # Establish which cells have special values
        self._dls = [self._cells[3][0], self._cells[11][0], self._cells[6][2], 
                     self._cells[8][2], self._cells[0][3], self._cells[7][3], 
                     self._cells[14][3], self._cells[2][6], self._cells[6][6], 
                     self._cells[8][6], self._cells[12][6], self._cells[3][7], 
                     self._cells[11][7], self._cells[2][8], self._cells[6][8], 
                     self._cells[8][8], self._cells[12][8], self._cells[0][11], 
                     self._cells[7][11], self._cells[14][11], 
                     self._cells[6][12], self._cells[8][12], self._cells[3][14],
                     self._cells[11][14]]
        self._dws = [self._cells[1][1], self._cells[2][2], self._cells[3][3],
                     self._cells[4][4], self._cells[7][7], self._cells[10][10],
                     self._cells[11][11], self._cells[12][12],
                     self._cells[13][13], self._cells[13][1], 
                     self._cells[12][2], self._cells[11][3], self._cells[10][4],
                     self._cells[4][10], self._cells[3][11], self._cells[2][12],
                     self._cells[1][13]]
        self._tls = [self._cells[5][1], self._cells[9][1], self._cells[1][5],  
                     self._cells[5][5], self._cells[9][5], self._cells[13][5],  
                     self._cells[1][9], self._cells[5][9], self._cells[9][9], 
                     self._cells[13][9], self._cells[5][13], self._cells[9][13]]
        self._tws = [self._cells[0][0], self._cells[0][7], self._cells[0][14],
                     self._cells[7][0], self._cells[7][14], self._cells[14][0],
                     self._cells[14][7], self._cells[14][14]]
        
        # Fill in the colors (and hence give values) to each special cell
        for dl in self._dls:
            dl.setFillColor("cyan")
        for dw in self._dws:
            dw.setFillColor("pink")
        for tl in self._tls:
            tl.setFillColor("blue")
        for tw in self._tws:
            tw.setFillColor("red")
                
        # Create trays for the players to keep their pieces
        self._trays = []
        for player in [0, 1]:
            for i in range(7):
                xpos = 60 + i * 20 + player * 160
                thisCell = Cell(win, (xpos, 375), "white", None)
                thisCell.addTo(win)
                self._trays.append(thisCell)
                
        # Create a list of tiles that have been added to the board/trays
        self._tiles = []
                
        # Set up and add two players to the game 
        self._players = []
        for num in range(2):
            self._players.append(Player(win, num, self))
        
        # Create a background
        self._background = Rectangle(400, 400, (200, 200))
        self._background.setFillColor("cornsilk")
        self._background.setDepth(100)
        self._win.add(self._background)
        
        # Create a scoreboard
        self._scoreList = []
        self._playerNames = []
        for i in range(len(self._players)):
            self._scoreboard = Rectangle(50, 50, (175 + i * 50, 25))
            self._scoreboard.setDepth(1)
            self._scoreboard.setFillColor("wheat")
            self._scoreDisplay = Text('0', (175 + i * 50, 25), 15)
            self._scoreDisplay.setDepth(0)
            self._player = Text("Player " + str(i + 1), (120 + i * 160, 25), 15)
            self._player.setDepth(0)
            self._playerBox = Rectangle(60, 50, (120 + i * 160, 25))
            self._playerBox.setFillColor("burlywood")
            self._playerBox.setDepth(5)
            self._scoreList.append(self._scoreDisplay)
            self._playerNames.append(self._player)
            self._playerNames.append(self._playerBox)
            self._win.add(self._scoreboard)
            self._win.add(self._scoreDisplay)
            self._win.add(self._player)
            self._win.add(self._playerBox)

        # Create Undo and End Turn buttons
        UndoButton(self, win, 40, 50, (70, 25))
        EndTurnButton(self, win, 40, 50, (330, 25))
        
        # Set the current player to 1 and change turn
        self._current = 1
        self.changeTurn()
     
    def scoreBoard(self):
        """Determine the scores of each turn played and update the scoreboard
            accordingly """
        
        # Hold each letter and its value
        scores = {"A": 1, "C": 3, "B": 3, "E": 1, "D": 2, "G": 2, "F": 4, 
                  "I": 1, "H": 4, "K": 5, "J": 8, "M": 3, "L": 1, "O": 1, 
                  "N": 1, "Q": 10, "P": 3, "S": 1, "R": 1, "U": 1, "T": 1, 
                  "W": 4, "V": 4, "Y": 4, "X": 8, "Z": 10}
                  
        # Initialize necessary variables
        total = 0
        tilesScored = 0
        doubleWord = False
        tripleWord = False
        multiplier = 1
        
        # Calculates total score for the turn based off of special keys
        for tile in self._tiles:
            if not tile.scored():
                for row in range(15):
                    for col in range(15):
                        if tile.getLocation() == \
                        self._cells[row][col].getLocation():
                            if self._cells[row][col].isDW():
                                doubleWord = True
                            if self._cells[row][col].isTW():
                                tripleWord = True
                            if self._cells[row][col].isDL():
                                multiplier = 2
                            elif self._cells[row][col].isTL():
                                multiplier = 3
                            else:
                                multiplier = 1
                            total += multiplier * scores[tile.getLetter()] 
                            tile.score()
                            tilesScored += 1
        if doubleWord:
            total *= 2
        if tripleWord:
            total *= 3
        if tilesScored >= 7:
            total += 50
        
        # Add up the player's score and update them on the screen
        self._players[self._current].addScore(total)
        for i in range(len(self._players)):
            self._scoreList[i].setText(self._players[i].getScore())
    
    def getTrays(self):
        """ Return a list of tiles that are in the player's trays """
        return self._trays
        
    def changeTurn(self):
        """ Change the player whose turn it currently is """
        self._players[self._current].deactivateAll()
        self._current += 1
        self._current %= 2
        self._players[self._current].activateAll()
        
    def computeLanding(self, tile):
        """ Determine the cell where a piece was placed, as long as that cell is
        legal. Otherwise, None """
        x0, y0 = self._cells[0][0].getLocation()
        x0 -= 10
        y0 -= 10
        x1, y1 = tile.getLocation()
        row = (y1 - y0) // 20
        col = (x1 - x0) // 20
        if row < 0 or col < 0 or row > 14 or col > 14:
            return None
        if self._cells[row][col].getTile() != None:
            return None
            
        # The first move of the game must be on the center of the board
        if len(self._history) == 0:
            row = 7
            col = 7
            return self._cells[row][col]
        
        # All other moves must be touching a tile that is already on the board
        else:
            if row > 0:
                if not self._cells[row - 1][col].isEmpty():
                    return self._cells[row][col] 
            if row < 14:
                if not self._cells[row + 1][col].isEmpty():
                    return self._cells[row][col] 
            if col > 0:
                if not self._cells[row][col - 1].isEmpty():
                    return self._cells[row][col] 
            if col < 14:
                if not self._cells[row][col + 1].isEmpty():
                    return self._cells[row][col] 
        return None
        
    def getWinnerScore(self):
        """ Return a score when the tile bag is empty and a winner has occurred,
            otherwise None """
        if self._tileBag.isEmpty():
            if self._players[0].getScore() > self._players[1].getScore():
                self._playerNames[0].setText("Winner!")
                return self._players[0].getScore()
            elif self._players[0].getScore() < self._players[1].getScore():
                self._playerNames[2].setText("Winner!")
                return self._players[1].getScore()
            else:
                self._playerNames[0].setText("Tie!")
                self._playerNames[2].setText("Tie!")
                return self._players[0].getScore()
        return None
    
    def undo(self):
        """ Undo the last move made by either player, reactivating a tile sent
            back to the tray """
        if len(self._history) != 0:
            tile, cell, player = self._history.pop()
            tile.moveToHome()
            cell.removeTile()
            player.addTile(tile)
            for i in range(len(self._trays)):
                if self._trays[i].getLocation() == tile.getHome():
                    self._trays[i].addTile(tile)
            tile.activate()
            
    def endTurn(self):
        """ End the current player's turn. Update the scoreboard, and if the 
            tile bag is not empty, draw tiles to replenish the trays, else get
            winner score """
        if not self._tileBag.isEmpty():
            for i in range(len(self._trays)):
                if self._trays[i].isEmpty():
                    tile = self._tileBag.getItem(0)
                    self._tileBag.drawTile(tile, self._trays[i].getLocation())
                    self._trays[i].addTile(tile)
                    tile.addTo(self._win)
                    tile.setPlayer(self._players[self._current])
                    self._players[self._current].addTile(tile)
            self.scoreBoard()
            self.changeTurn()
        else:
            self.scoreBoard()
            self.getWinnerScore()
            
    
    def report(self, tile, event):
        """ When a tile has been placed,  if the movement was valid, finalize
            the movement, append the history for the undo button, and remove
            the tile from its tray """
        landing = self.computeLanding(tile)
        if landing != None:
            tile.deactivate()
            player = self._players[self._current]
            player.removeTile(tile)
            landing.addTile(tile)
            tile.moveTo(landing.getLocation())
            self._history.append((tile, landing, player))
            self._tiles.append(tile)
            for i in range(len(self._trays)):
                if self._trays[i].getLocation() == tile.getHome():
                    self._trays[i].removeTile(tile)

def play(win):
    """ Play Scrabble! """
    Board(win)
    
StartGraphicsSystem(play)