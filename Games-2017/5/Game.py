"""
Creator: Anthony Reyes

File: Game.py

Date: 5-1-17

SWAGGY SCRABBLE:

RULES

#1
The first player combines two or more of his or her letters to form a word and
places it on the board to read either across or down with one letter on the
center square. Diagonal words are not allowed.

#2
Complete your turn by counting and announcing your score for that turn. Then
draw as many new letters as you played; always keep seven letters on your rack,
as long as there are enough tiles left in the bag.

#3
The second player, and then each in turn, adds one or more letters to those
already played to form new words. All letters played on a turn must be placed in
one row across or down the board, to form at least one complete word. If, at the
same time, they touch others letters in adjacent rows, those must also form
complete words, crossword fashion, with all such letters. The player gets full
credit for all words formed or modified on his or her turn.

#4
New words may be formed by:
Adding one or more letters to a word or letters already on the board.
Placing a word at right angles to a word already on the board. The new word must
use one of the letters already on the board or must add a letter to it.
Placing a complete word parallel to a word already played so that adjacent
letters also form complete words. 

#5
No tile may be shifted or replaced after it has been played and scored.

#6
The game ends when all letters have been drawn and one player uses his or her
last letter; or when all possible plays have been made.

"""
import random
from cs110graphics import *

WINWIDTH = 1000
WINHEIGHT = 1000

def reportPlayer():
    """ Makes player aware of lack of tiles """
    prompt = input("There are no more tiles... Press ok")
    return prompt

class Tile(EventHandler):
    """ one individual tile. (psudo-graohical object) """
    def __init__(self, center, letter):
        EventHandler.__init__(self)
        self._player = None
        self._space = None
        self._inBag = center
        self._home = None 
        self._center = center
        self._win = None
        
        self._letter = letter
        self._tile = Image("https://cs.hamilton.edu/~axreyes/images/" +\
                            self._letter + ".jpg", self._center, 48, 48)
        self._tile.setDepth(2)
        self._highlighter = Rectangle(50, 50, self._center)
        self._tile.addHandler(self)
        
        self._inactiveColor = 'white'
        self._activeColor = 'yellow2'
        self._highlighter.setFillColor(self._inactiveColor)
        self._highlighter.setDepth(3)
        
        self._active = False

    def addTo(self, win):
        """ adds to win """
        self._win = win
        win.add(self._tile)
        win.add(self._highlighter)
    
    def removeFrom(self, win):
        """ Removes from win """
        win.remove(self._tile)
        win.remove(self._highlighter)
    
    def setDepth(self, depth):
        """ sets depth """
        self._tile.setDepth(depth)

    def setPlayer(self, player):
        """ assigns a tile a player """
        self._player = player
        
    def getPlayer(self):
        """ returns a player """
        return self._player
        
    def setSpace(self, space):
        """ assigns a tile a space """
        self._space = space
    
    def getSpace(self):
        """ assigns a tile a space """
        return self._space
    
    def setHome(self, home):
        """ assigns a tile a home """
        self._home = home
        
    def goHome(self):
        """ moves a tile a home """
        self.moveTo(self._home)
        
    def removeFromPlayer(self):
        """ removes the tile frome the player it is assigned to """
        self._player = None
    
    def getPoints(self):
        """ returns the points (worth) of the tile """
        return pointForLetter(self._letter)
    
    def activate(self):
        """ activates tile for movment """
        self._active = True
        self._highlighter.setFillColor(self._activeColor)
    
    def deactivate(self):
        """ deactivates tile for movement """
        self._active = False
        self._highlighter.setFillColor(self._inactiveColor)
    
    def getTile(self):
        """ returns Tile """
        return self._tile
        
    def tellPlayer(self):
        """ reports to player when out of hand """
        self._player.tellPlayer(self)
    
    def moveTo(self, center):
        """ gives tile a new center """
        (dx, dy) = center
        self._center = (dx, dy)
        self._tile.moveTo(self._center)
        self._highlighter.moveTo(self._center)
    
    def handleMouseRelease(self, event):
        """ activates tile and informs all othe classes """
        if self._player != None:    
            if not self._active:
                self.activate()
                self._player.report(self, event)

class AllTiles:
    """ All the gobal tiles raoming the game """
    def __init__(self):
        self._lettersList = ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B',
                             'B', 'C', 'C', 'D', 'D', 'D', 'D', 'E', 'E', 'E', 
                             'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'F', 
                             'F', 'G', 'G', 'G', 'H', 'H', 'I', 'I', 'I', 'I',
                             'I', 'I', 'I', 'I', 'I', 'J', 'K', 'L', 'L', 'L',
                             'L', 'M', 'M', 'N', 'N', 'N', 'N', 'N', 'N', 'O',
                             'O', 'O', 'O', 'O', 'O', 'O', 'O', 'P', 'P', 'Q',
                             'R', 'R', 'R', 'R', 'R', 'R', 'S', 'S', 'S', 'S',
                             'T', 'T', 'T', 'T', 'T', 'T', 'U', 'U', 'U', 'U',
                             'V', 'V', 'W', 'W', 'X', 'Y', 'Y', 'Z']
        random.shuffle(self._lettersList)
        
        self._tileList = []
        for letters in self._lettersList:
            self._tileList.append(Tile((50, 50), letters))
            
    def getLen(self):
        """ returns deck length """
        return len(self._tileList)
    
    def topTile(self):
        """ returns the top letter """
        if len(self._tileList) > 0:
            return self._tileList[0]

    def updateTop(self):
        """ Top card is removed (CALL AFTER DRAW-topTile-) """ 
        self._tileList.pop(0)    
        
    def insertTile(self, tile):
        """ inserts a letter to the beggining of the list """
        self._tileList.insert(tile)

ALLTILES = AllTiles()

class Player:
    """ Class for each player """
    def __init__(self, win, board, number):
        self._board = board
        self._tilesAreEmpty = False
        self._scoreboard = None
        self._number = number
        self._win = win
        self._score = 0
        fx, fy = 500, 950
        self._frameCenter = (fx, fy)
        self._posTiles = [(fx, fy), (fx - 50, fy), (fx + 50, fy),\
                          (fx - 100, fy), (fx + 100, fy), (fx - 150, fy),\
                          (fx + 150, fy)]
        
        self._currentTiles = [None, None, None, None, None, None, None]
        self.draw()
            
        self._piecesNotOnBoard = []
        
    def draw(self):
        """ draws a new set of tiles """
        for i in range(len(self._posTiles)):
            if ALLTILES.getLen() > 0:
                if self._currentTiles[i] is None:
                    myTile = ALLTILES.topTile()
                    ALLTILES.updateTop()
                    myTile.moveTo(self._posTiles[i])
                    myTile.setHome(self._posTiles[i])
                    self._currentTiles[i] = myTile
                    
            elif not self._tilesAreEmpty:
                reportPlayer()
                self._tilesAreEmpty = True
                    
        for tiles in self._currentTiles:
            if tiles is not None:
                tiles.setPlayer(self)
        
    def addTo(self):
        """ adds to win """
        for pieces in self._currentTiles:
            if pieces is not None:
                pieces.addTo(self._win)
            
    def returnMyTiles(self):
        """ returns tiles to the Player """
        for tile in self._piecesNotOnBoard:
            tile.goHome()
            self._piecesNotOnBoard = []
            
    def removeFrom(self):
        """ Removes from win """
        for pieces in self._currentTiles:
            if pieces != None:
                pieces.removeFrom(self._win)

    def tellPlayer(self, piece):
        """ informs the player that a pices is not in their hand"""
        self._piecesNotOnBoard.append(piece)
    
    def getScore(self):
        """ returns score """
        return self._score
        
    def getNumber(self):
        """ returns number of player """
        return self._number
    
    def removeTiles(self):
        """ removes the pieces not in hand from the player"""
        for pieces in self._piecesNotOnBoard:
            for i in range(len(self._currentTiles)):
                if self._currentTiles[i] == pieces:
                    self._currentTiles[i] = None
            pieces.removeFromPlayer()
        self._piecesNotOnBoard = []
            
    def addToScore(self, amount):
        """ adds amount to score """
        self._score += amount

    def scoring(self):
        """ manages score for each player """
        total = 0
        
        spacesToScore = []
        for tiles in self._piecesNotOnBoard:
            for dire in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                spacesToScore.extend(spacesInTheStrip(self._board.getGrid(),\
                                     tiles.getSpace().getPosition(), dire))
        spacesToScore = list(set(spacesToScore))
        
        total = 0
        
        for spacesPos in spacesToScore:
            (x, y) = spacesPos
            spaces = self._board.getGrid()[x][y]
            total += spaces.getTile().getPoints()
        
        self.addToScore(total)
        self._scoreboard.update()
        
    def assignScoreboard(self, scoreboard):
        """ assigns a scoreboard """
        self._scoreboard = scoreboard
        
    def report(self, piece, event):
        """ calls for any active pieces to deactivate and reports the board """
        keepOneActive(self._currentTiles, piece)
        self._board.report(piece, event)

class BoardGrid:
    """ Makes a grid for the spaces to latch to """
    def __init__(self):
        self._grid = []
        for y in range(15):
            row = []
            col = 150 + y * 50
            for x in range(15):
                row.append((150 + x * 50, col))
            self._grid.append(row)

    def getGrid(self):
        """ returns the grid made """
        return self._grid

class Board:
    """ The Main functionallity is all run by this """
    def __init__(self, win):
        self._history = [[]]
        self._returnTiles = ReturnTiles(win, self)
        
        self._win = win
        background = Image(\
                    "https://cs.hamilton.edu/~axreyes/images/BGROUND.jpg",\
                    (500, 500), 1000, 1000)
        background.setDepth(1000)
        self._win.add(background)
        
        self._frame = Image("https://cs.hamilton.edu/~axreyes/images/Frame.jpg"\
                            , (500, 950), 500, 75)
        self._frame.setDepth(999)
        self._win.add(self._frame)
        
        self._nextTurnButton = NextTurn(self._win, self)
        self._endGameButton = EndGameButton(self._win, self)
        
        
        grid = BoardGrid()
        self._gridPos = grid.getGrid()
        blanks = makeBlankBoard(self._gridPos)
        self._spaces = makeBoard(blanks)
        for rows in self._spaces:
            for space in rows:
                space.addTo(self._win)
                
        for r in range(len(self._spaces)):
            for c in range(len(self._spaces)):
                pos = (r, c)
                self._spaces[r][c].setPosition(pos)
                self._spaces[r][c].setBoard(self)
        
        self._playerAmount = 4
        self._playerTurn = 0
        self._allPlayers = []
        for i in range(self._playerAmount):
            player = Player(self._win, self, i)
            self._allPlayers.append(player)
        
        indicator = Text('player ' + str(self._playerTurn + 1), (100, 950), 24)
        self._playerTurnIndication = indicator
        self._win.add(self._playerTurnIndication)
        
        self._allPlayers[self._playerTurn].addTo()
        
        self._scoreboard = ScoreBoard(self._win, self)
        
        self._awareOfTile = False
        self._activepiece = None
        
    def getGrid(self):
        """ returns the grid """
        return self._spaces
        
    def callSpace(self, r, c):
        """ returns a space """
        return self._spaces[r][c]
    
    def getAllPlayers(self):
        """ returns all the players """
        return self._allPlayers
    
    def report(self, piece, event):
        """ activates the legal spaces and becomes aware of the active tile """
        if event != None:
            self._awareOfTile = True
            self._activepiece = piece
            if not self._spaces[7][7].filled():
                self.activateCenter()
                
            elif self._spaces[7][7].filled():
                self.activateSpaces()
    
    def activateCenter(self):
        """ Makes the center piece active """
        self._spaces[7][7].activate()
        self._spaces[7][7].activePiece(self._activepiece)
    
    def activateSpaces(self):
        """ Activates the spaces """
        for rows in self._spaces:
            for space in rows:
                if space.adjacentToTile():
                    space.activate()
                    space.activePiece(self._activepiece)
                
    def returnPlayerTiles(self):
        """ returns the player's tiles"""
        self._allPlayers[self._playerTurn].returnMyTiles()
                
    def nextTurn(self):
        """ executes a new turn """
        self._allPlayers[self._playerTurn].scoring()
        self._allPlayers[self._playerTurn].removeTiles()
        self._allPlayers[self._playerTurn].removeFrom()
        self._allPlayers[self._playerTurn].draw()
        self._playerTurn = (self._playerTurn + 1) % self._playerAmount
        self._allPlayers[self._playerTurn].addTo()
        self._win.remove(self._playerTurnIndication)
        self._playerTurnIndication = Text('player ' + str(self._playerTurn + 1)\
                                          , (100, 950), 24)
        self._win.add(self._playerTurnIndication)
        
    def endGame(self):
        """ determines the end of the game """
        prompt = EndGame(self._win, self)
        prompt.addTo()

class Space(EventHandler):
    """ a space on the board """
    def __init__(self, center):
        EventHandler.__init__(self)
        self._center = center
        self._board = None
        self._position = None
        self._space = Image("https://cs.hamilton.edu/~axreyes/images/blnk.jpg"\
                            , self._center, 50, 50)
        self._space.setDepth(3)
        self._space.addHandler(self)
        self._pieceOnTop = None
        self._activePiece = None
        self._active = False
        
        self._usedInSequence = False
        
    def addTo(self, win):
        """ adds to win """
        win.add(self._space)
    
    def setNew(self, spaceType):
        """ reassign the space to its designated type """
        self._space = Image("https://cs.hamilton.edu/~axreyes/images/{}.jpg"
                            .format(spaceType), self._center, 50, 50)
        self._space.setDepth(3)
        self._space.addHandler(self)
        return self._space
        
    def getCenter(self):
        """ returns center """
        return self._center
        
    def adjacentToTile(self):
        """ Predicate to see if the space is next to a filled tile """
        (r, c) = self._position
        pred = False
        if 0 <= r + 1 < len(self._board.getGrid()):
            if self._board.callSpace(r + 1, c).getTile() is not None:
                pred = True
            
        if 0 <= r - 1 < len(self._board.getGrid()):
            if self._board.callSpace(r - 1, c).getTile() is not None:
                pred = True
                
        if 0 <= c + 1 < 15:
            if self._board.callSpace(r, c + 1).getTile() is not None:
                pred = True
                
        if 0 <= c - 1 < 15:
            if self._board.callSpace(r, c - 1).getTile() is not None:
                pred = True
        
        return pred
        
        
    def setBoard(self, board):
        """ sets position """
        self._board = board
    
    def filled(self):
        """ predicate to se if space is filled """
        if self._pieceOnTop is not None:
            return True
        
        return False
    
    def setPosition(self, pos):
        """ sets position """
        self._position = pos
        
    def getPosition(self):
        """ returns position """
        return self._position   
        
    def setPiece(self):
        """ recognizes the piece on top of it (if not None) """
        self._pieceOnTop = self._activePiece
        self._activePiece.setSpace(self)
        
    def activePiece(self, piece):
        """ recognizes the piece on top of it (if not None) """
        self._activePiece = piece
        
    def usedInSequence(self):
        """ reports that the piece was used in a sequence """
        
    def getTile(self):
        """ returns the piece on top """
        return self._pieceOnTop
    
    def activate(self):
        """ Activates leaagal spaces for placement """
        self._active = True
        
    def deactivate(self):
        """ deactivates the space """
        self._active = False
        
    def handleMouseRelease(self, event):
        """ moves pieces on top of self """
        if self._active:
            self.setPiece()
            self._pieceOnTop.moveTo(self._center)
            self._pieceOnTop.tellPlayer()

class NextTurn(EventHandler):
    """ next turn button """
    def __init__(self, win, board):
        EventHandler.__init__(self)
        self._board = board
        
        self._nextTurn = Image("https://cs.hamilton.edu/~axreyes/images/" +\
                               'NextTurn1' + ".jpg", (945, 200), 100, 100)
        self._nextTurn.addHandler(self)
        win.add(self._nextTurn)
        
    def handleMouseRelease(self, event):
        """ signals the next turn """
        self._board.nextTurn()
        
class ReturnTiles(EventHandler):
    """ next turn button """
    def __init__(self, win, board):
        EventHandler.__init__(self)
        self._board = board
        
        self._returnTiles = Image("https://cs.hamilton.edu/~axreyes/images/" +\
                                  'GiveTiles1' + ".jpg", (945, 300), 100, 100)
        self._returnTiles.addHandler(self)
        win.add(self._returnTiles)
        
    def handleMouseRelease(self, event):
        """ signals the next turn """
        self._board.returnPlayerTiles()
        
class EndGameButton(EventHandler):
    """ the end game button """
    def __init__(self, win, board):
        EventHandler.__init__(self)
        self._board = board
        
        self._endGame = Image("https://cs.hamilton.edu/~axreyes/images/" +\
                                  'EndGame' + ".jpg", (945, 400), 100, 100)
        self._endGame.setDepth(0)
        self._endGame.addHandler(self)
        win.add(self._endGame)
        
    def handleMouseRelease(self, event):
        """ signals the end of the game """
        self._board.endGame()
        
class EndGame(EventHandler):
    """ prompts the end of the game """
    def __init__(self, win, board):
        EventHandler.__init__(self)
        self._board = board
        self._win = win
        self._endGame = Image("https://cs.hamilton.edu/~axreyes/images/" +\
                              'WinningScreen' + ".jpg", (500, 500), 500, 500)
        self._endGame.setDepth(0)
        self._endGame.addHandler(self)
        
        topPlayer = topScore(self._board.getAllPlayers())
        num = str(topPlayer.getNumber() + 1)
        text = 'Player ' + num
        self._image = Text(text, (500, 450), 35)
        self._image.setDepth(0)
        
        
    def addTo(self):
        """ adds the image """
        self._win.add(self._endGame)
        self._win.add(self._image)
        
    def handleMouseRelease(self, event):
        """ look back at end game """
        self._win.remove(self._endGame)
        self._win.remove(self._image)
        
class ScoreBoard:
    """ visual representation of the score """
    def __init__(self, win, board):
        self._players = board.getAllPlayers()
        self._win = win
        self._indicators = []
        for i in range(len(self._players)):
            score = self._players[i].getScore()
            indicator = Text('p' + str(i + 1) + ' = ' +\
                             str(score), \
                             (50, 500 + (i * 50)), 24)
            self._players[i].assignScoreboard(self)
            self._indicators.append(indicator)
            win.add(indicator)
            
    def update(self):
        """ Keeps the score updated """
        for indicator in self._indicators:
            self._win.remove(indicator)
        for i in range(len(self._players)):
            score = self._players[i].getScore()
            self._indicators[i] = Text('p' + str(i + 1) + ' = ' +\
                                       str(score), \
                                       (50, 500 + (i * 50)), 24)
        for indicator in self._indicators:
            self._win.add(indicator)

def keepOneActive(lists, piece):
    """ deactivates the tiles that are active (1 at a time active) """
    nlist = []
    for pieces in lists:
        nlist.append(pieces)
    index = 0
    for i in range(len(nlist)):
        if nlist[i] == piece:
            index = i
    nlist.pop(index)
    for pieces in nlist:
        if pieces != None:
            pieces.deactivate()

def pointForLetter(letter):
    """ stores the score differentiation """
    letterToPointDictionary = {'A': 1, 'E': 1, 'I': 1, 'O': 1, 'U': 1, 'L': 1,
                               'N': 1, 'S': 1, 'T': 1, 'R': 1, 'D': 2, 'G': 2, 
                               'B': 3, 'C': 3, 'M': 3, 'P': 3, 'F': 4, 'H': 4, 
                               'V': 4, 'W': 4, 'Y': 4, 'K': 5, 'J': 8, 
                               'X': 8, 'Q': 10, 'Z': 10}
    return letterToPointDictionary[letter]
    
def makeBlankBoard(gridPos):
    """ makes a board with nothinig on it """
    boardSpaces = []
    for rows in gridPos:
        row = []
        for col in rows:
            space = Space(col)
            row.append(space)
        boardSpaces.append(row)  
    return boardSpaces

def makeBoard(spaceList):
    """ reassigns the spaces to their grid numbers """
    # Double word spaces
    dw = [(1, 1), (1, 13), (2, 2), (2, 12), (3, 3), (3, 11), (4, 4), (4, 10),
          (10, 4), (10, 10), (11, 3), (11, 11), (12, 2), (12, 12), (13, 1),
          (13, 13)]
    for i in range(len(dw)):
        x = dw[i][0]
        y = dw[i][1]
        spaceList[x][y].setNew('DW')
        
    # Triple word spaces    
    tw = [(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)]
    for i in range(len(tw)):
        x = tw[i][0]
        y = tw[i][1]
        spaceList[x][y].setNew('TW')
        
    # Double letter spaces
    dl = [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2),
          (6, 6), (6, 8), (6, 12), (7, 3), (7, 11), (8, 2), (8, 6), (8, 8), 
          (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), 
          (14, 11)]
    for i in range(len(dl)):
        x = dl[i][0]
        y = dl[i][1]
        spaceList[x][y].setNew('DL')
        
    # Triple letter spaces
    tl = [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5),
          (9, 9), (9, 13), (13, 5), (13, 9)]
    for i in range(len(tl)):
        x = tl[i][0]
        y = tl[i][1]
        spaceList[x][y].setNew('TL')
    return spaceList
    
def makeStrToList(lists):
    """ Make String into list by character"""
    newList = []
    for i in range(len(lists)):
        newList.append(lists[i])
    return newList
    
def spacesInTheStrip(grid, spacePos, direction):
    """ puts all the spaces adjacent in on direction in a list """
    (dx, dy) = direction
    (x, y) = spacePos
    lists = [(x, y)]
    for _ in range(15):
        i = 1
        if 0 < x + (i * dx) < 15 and 0 < y + (i * dy) < 15:
            if grid[x + (i * dx)][y + (i * dy)].getTile() is not None:
                lists.append((x + (i * dx), y + (i * dy)))
                i += 1

    return list(set(lists))
    
def topScore(lists):
    """ returns the top scoring player """
    topScorer = lists[0]
    for player in lists:
        for player2 in lists:
            if player.getScore() > player2.getScore():
                topScorer = player
    return topScorer
    
def main(win):
    """ The runing funtion containing the board """
    _ = Board(win)

StartGraphicsSystem(main, WINWIDTH, WINHEIGHT)
