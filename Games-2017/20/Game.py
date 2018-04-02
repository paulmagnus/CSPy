"""
*****************************************************************************
FILE: Game.py
AUTHOR: Cal Reynolds
PARTNER: n/a
ASSIGNMENT: Project 6
DATE: 4/7/2017
DESCRIPTION: Scrabble!
*****************************************************************************
"""

import random
from cs110graphics import *

class Pieces:
    """ Creates group of scrabble letter pieces """
    
    def __init__(self, board):
        """ creates set amount of each letter piece each with unique value """
        self._pieceList = []
        self._cx = 500
        self._cy = 100
        
        #establishes number of each letter piece to make each with certain value
        letters = [['E', 12, 1], ['A', 9, 1], ['I', 9, 1], ['O', 8, 1],
                   ['N', 6, 1], ['R', 6, 1], ['L', 4, 1], ['U', 4, 1],
                   ['D', 4, 2], ['G', 3, 2], ['B', 2, 3], ['C', 2, 3],
                   ['M', 2, 3], ['P', 2, 3], ['F', 2, 4], ['H', 2, 4],
                   ['V', 2, 4], ['W', 2, 4], ['Y', 2, 4], ['K', 1, 5],
                   ['J', 1, 8], ['X', 1, 8], ['Q', 1, 10], ['Z', 1, 10]]
                   
        for r in range(len(letters)):
            for _ in range(letters[r][1]):
                piece = SinglePiece(letters[r][0], letters[r][2], 
                                    (self._cx, self._cy), board)
                piece.setDepth(15)
                self._pieceList.append(piece)
        self._board = board
        self._dealtPiece = None
        
    def shuffle(self):
        """ shuffles the list of pieces """
        random.shuffle(self._pieceList)

    def dealPiece(self):
        """ deals a piece from the list of pieces and removes it from list """
        self._dealtPiece = self._pieceList[0]
        self._pieceList.remove(self._pieceList[0])
        if len(self._pieceList) == 0:
            Endbutton(self._board, self._board.getWin())
        return self._dealtPiece


class SinglePiece(EventHandler):      
    """ Creates a Scrabble Letter Piece """
    
    def __init__(self, letter, value, center, board):
        """ Establishes letter, value, position, and properties of piece """
        EventHandler.__init__(self)
        self._cx, self._cy = center
        self._letter = Text(letter, (self._cx, self._cy+7), 15)
        self._value = Text(value, (self._cx + 10, self._cy + 10), 8)
        self._numberValue = value
        self._center = center
        self._piece = Square(29, (self._cx, self._cy))
        self._piece.setFillColor("beige")
        self._piece.setBorderColor("grey")
        self._letter.addHandler(self)
        self._piece.addHandler(self)
        self._value.addHandler(self)
        self._moving = False
        self._location = (0, 0)  # window location of the piece
        self._startPos = None    # mouse position where movement started
        self._active = True
        self._player = board.getPlayer()
        self._board = board

    def activate(self):
        """ Activates  piece, makes border yellow """
        self._active = True
        self._piece.setBorderColor('#FFFF00')
        self._piece.setFillColor('beige')

    def deactivate(self):
        """ Deactivates piece, makes boarder and fill color black """
        self._active = False
        self._piece.setBorderColor('black')
        self._piece.setFillColor('black')

    def placedOnBoard(self):
        """ If piece is on board, deactivates piece and sets border to black """
        self._active = False
        self._piece.setBorderColor('black')
        
    def addTo(self, win):
        """ Adds piece to window """
        win.add(self._piece)
        win.add(self._letter)
        win.add(self._value)

    def moveTo(self, position):
        """ Moves piece to certain location """
        cx, cy = position
        self._piece.moveTo(position)
        letterPosition = (cx, cy+10)
        self._letter.moveTo(letterPosition)
        valuePosition = (cx+10, cy+10)
        self._value.moveTo(valuePosition)
        self._location = position

    def move(self, dx, dy):
        """ Moves piece by a certain amount in a given direction """
        oldx, oldy = self._location
        newx = oldx + dx
        newy = oldy + dy
        self.moveTo((newx, newy))
    
    def highlight(self):
        """ Sets border color to green to signify piece is moving """
        self._piece.setBorderColor("#7FFFD4")

    def setDepth(self, depth):
        """ Sets the piece to a certain depth """
        self._piece.setDepth(depth+4)
        self._value.setDepth(depth)
        self._letter.setDepth(depth)
        
    def handleMouseRelease(self, event):
        """ if piece != active, cannot be taken. If active, can be placed """
        if not self._active:
            return 
        if self._moving:
            self.setDepth(25)
            self._piece.setBorderColor("yellow")
            self._moving = False
            self._player.report(self, event)
        else:
            self.highlight()
            self.setDepth(10)
            self._moving = True
            self._startPos = event.getMouseLocation()

    def handleMouseMove(self, event):
        """ moves the piece by mouse dragging if active, nothing if not """
        if not self._active:
            return
        if self._moving:
            oldx, oldy = self._startPos
            newx, newy = event.getMouseLocation()
            self.move(newx - oldx, newy - oldy)
            self._startPos = self._location
            
    def getLocation(self):
        """ returns location of piece """
        return self._location
    
    def getpiece(self):
        """ returns piece """
        return self._piece
        
    def getValue(self):
        """ returns number value of piece """
        return self._numberValue
        
        
class Player:
    """ Creates Scrabble Player """
    
    def __init__(self, playerNumb, win, board):
        """ Takes player number to instantiate unique player """
        self._textCenterX = 540
        self._textCenterY = 70
        self._pointList = []
        self._board = board
        playerTxt = Text(('Player ' + str(playerNumb + 1)), (self._textCenterX,\
        self._textCenterY + 110 * playerNumb), 30) 
        win.add(playerTxt)
        self._win = win
        self._playerNumb = playerNumb
        self._playerPieces = [None, None, None, None, None, None, None]
        pointTxt = Text(('Points: '), (640, self._textCenterY + 110 * \
        self._playerNumb), 10)
        win.add(pointTxt)
        self._playerPointsWin = None
        self._score = 0
        self._wordMultiplier = 1
        self._numberOfTurns = 0
        self._totalPlayerPoints = []
        self._points = 0
        self._singleWordScore = 0
        self._pieces = None
        
    def report(self, piece, event):
        """ calls the board to report whether/where a player's piece landed """
        self._board.report(piece, event)

    def replenish(self, pieces):
        """ refill pieces that have been placed on board by player """
        self._pieces = pieces
        for i in range(7):
            if self._playerPieces[i] is None:
                dealtPiece = self._pieces.dealPiece()
                self._playerPieces[i] = dealtPiece
                dealtPiece.addTo(self._win)
                dealtPiece.moveTo((self._textCenterX + i * 33, \
                self._textCenterY +  110 * self._playerNumb + 30))
                dealtPiece.deactivate()
                
    def activateAll(self):
        """ activates pieces """
        for piece in self._playerPieces:
            piece.activate()
    
    def deactivateAll(self):
        """ deactivates pieces """
        for piece in self._playerPieces:
            piece.deactivate()
    
    def removePiece(self, piece):
        """ removes piece from player's possession """
        for i in range(len(self._playerPieces)):
            if self._playerPieces[i] == piece:
                self._playerPieces[i] = None
        
    def getPlayerPieces(self):
        """ returns a player's pieces """
        return self._playerPieces
        
    def getPlayer(self):
        """ returns the player """
        return self
        
    def addValueList(self, tileInfo):
        """ Adds the value of the placed tile to a total sum of points """
        tileValue = tileInfo[0]
        tileValue *= tileInfo[1]
        self._wordMultiplier *= tileInfo[2]
        self._singleWordScore += tileValue
        self._numberOfTurns += 1

    def putOutPoints(self):
        """ determines points of player, puts then on window """
        if self._points != 0:
            self._win.remove(self._playerPointsWin) 
        self._singleWordScore *= self._wordMultiplier
        self._wordMultiplier = 1
        self._points += self._singleWordScore
        self._singleWordScore = 0
        self._playerPointsWin = Text(str(self._points), (672, 70 + 110 * \
        (self._playerNumb)), 15)
        self._win.add(self._playerPointsWin)
        
    def zeroTurns(self):
        """ zeroes the amount of turns taken by player """
        self._numberOfTurns = 0
        
    def returnTurn(self):
        """ returns how many turns the player has taken """
        return self._numberOfTurns
        
    def getPoints(self):
        """ returns a player's points """
        return self._points
        
    def getPlayerNumb(self):
        """ returns the number of the player """
        return self._playerNumb
        
        
class Changebutton(EventHandler):
    """ Button that changes player turn """
    
    def __init__(self, board, win):
        """ establishes properties of button """
        EventHandler.__init__(self)
        self._center = 300, 520
        self._button = Rectangle(150, 60, (225, 540))
        self._button.setFillColor('#FF8C00')
        self._text = Text('End Turn', (225, 547), 25)
        win.add(self._button)
        win.add(self._text)
        self._button.addHandler(self)
        self._text.addHandler(self)
        self._board = board

    def handleMouseRelease(self, event):
        """ turn changes when button is clicked """
        self._board.putPointsOut()
        self._board.getPlayer().zeroTurns()
        self._board.changeTurn()
        
        
class Endbutton(EventHandler):
    """ Button used to declare a winner + points when no more pieces left """
    
    def __init__(self, board, win):
        """ Instantiates dimensions of endbutton, color, it as EventHandler """
        EventHandler.__init__(self)
        self._board = board
        self._rectangle = Rectangle(800, 300, (450, 300))
        self._rectangle.setFillColor("#48D1CC")
        text = ("Congratulations!!!! Player " + \
        str(self._board.getWinnerPlayer()+1) + " won Scrabble with " + \
        str(self._board.getWinnerPoints()) + " points!")
        self._text = Text(text, (450, 320), 30)
        self._rectangle.setDepth(5)
        self._text.setDepth(4)
        self._rectangle.addHandler(self)
        self._text.addHandler(self)
        win.add(self._rectangle)
        win.add(self._text)
        self._win = win
        
    def handleMouseRelease(self, event):
        """ When button is pushed, the window is closed, ending the program """
        self._win.close()
        

class Tile:
    """ Tile to make up scrabble board """
    
    def __init__(self, center, tileType, board):
        """ establishes properties of tile """
        self._center = center
        self._size = 30
        self._square = Square(self._size, self._center)
        self._color = tileType[0]
        self._textLetters = tileType[1]
        self._textSize = tileType[4]
        self._wordMultiplier = tileType[3]
        self._letterMultiplier = tileType[2]
        self._text = Text(self._textLetters, self._center, self._textSize)
        self._square.setFillColor(self._color)
        self._piece = None
        self._active = False
        self._board = board
        self._scrabBoard = None
        
    def addTo(self, win):
        """ Adds tile to window """
        win.add(self._square)
        win.add(self._text)
    
    def getLocation(self):
        """ returns location of tile """
        return self._center
    
    def getPiece(self):
        """ returns tile """
        return self._piece

    def addPiece(self, piece):
        """ adds piece to tile """
        self._piece = piece
    
    def getWordMultiplier(self):
        """ returns word multiplier """
        return self._wordMultiplier

    def getLetterMultiplier(self):
        """ returns letter multiplier """
        return self._letterMultiplier
        
    def activate(self):
        """ activates tile, sets border color green to mark """
        self._active = True
        self._square.setBorderColor('#00FF7F')

    def deactivate(self):
        """ deactivates tile, sets border color black to mark """
        self._active = False
        self._square.setBorderColor('black')
        
    def getActiveStatus(self):
        """ returns whether tile is active """
        return self._active
        
    def activateIfNoPiece(self, r, c):
        """ activates tiles in all empty spaces around piece """
        self._scrabBoard = self._board.getScrabBoard()

        directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        for dir1 in directions:
            dr, dc = dir1
            
            #if first move player's turn, will count neighbor tiles' point value
            if self._board.getPlayer().returnTurn() == 0:
                if c + dc >= len(self._scrabBoard[r]) or \
                r + dr >= len(self._scrabBoard) or \
                r + dr < 0 or c + dc < 0:
                    pass
                else:
                    
                    if self._scrabBoard[r+dr][c+dc].getPiece() != None:
                        self._board.getPlayer().addValueList(\
                        ((self._scrabBoard[r+dr][c+dc].getPiece().getValue()\
                        ), 1, 1))
                    else:
                        self._scrabBoard[r+dr][c+dc].activate()
                    
            else:
                if c + dc >= len(self._scrabBoard[r]) or \
                r + dr >= len(self._scrabBoard) or \
                r + dr < 0 or c + dc < 0:
                    pass
                else: 
                    if self._scrabBoard[r+dr][c+dc].getPiece() is None:
                        self._scrabBoard[r+dr][c+dc].activate()
                        
                    else:
                        if self._scrabBoard[r+dr][c+dc].getPiece() != None:
                            self._scrabBoard[r+dr][c+dc].deactivate()
                    
                    
class Board:
    """ Creates board """
    
    def __init__(self, win):
        """ Instantiates properties of board, enables game to be played """
        #finds number of players, only allows 1-4
        playerNumb = int(input("How many players will be participating? (1-4)"))
        while playerNumb > 4 or playerNumb < 1:
            playerNumb = int(input("How many players will be participating?" + \
            " (1-4)"))
        self._playerNumb = playerNumb
        
        #instantiates attributes of each type of tile on board
        tw = ("red", "TW", 1, 3, 10)
        n = ("#DEB887", " ", 1, 1, 10)
        dl = ("#40c7ed", "DL", 2, 1, 10)
        dw = ("pink", "DW", 1, 2, 10)
        tl = ("#0066ff", "TL", 3, 1, 10)
        cnt = ("#fdffba", "*", 1, 1, 14)
        
        self._firstSquarePos = (50, 25)
        fx, fy = self._firstSquarePos
        self._current = playerNumb - 1
        self._win = win

        #creates list of players
        self._players = []
        for i in range(playerNumb):
            self._players.append(Player(i, win, self))
        
        #creates bag of letter pieces
        self._bagofpieces = Pieces(self)
        self._bagofpieces.shuffle()
        
        #distributes proper amount of pieces to however many players need
        for player in self._players:
            player.replenish(self._bagofpieces)
        
        
        #this grid represents board full of tuples with info to make tile objs.
        self._scrabBoard = [[tw, n, n, dl, n, n, n, tw, n, n, n, dl, n, n, tw], 
                            [n, dw, n, n, n, tl, n, n, n, tl, n, n, n, dw, n], 
                            [n, n, dw, n, n, n, dl, n, dl, n, n, n, dw, n, n], 
                            [dl, n, n, dw, n, n, n, dl, n, n, n, dw, n, n, dl],
                            [n, n, n, n, dw, n, n, n, n, n, dw, n, n, n, n], 
                            [n, tl, n, n, n, tl, n, n, n, tl, n, n, n, tl, n], 
                            [n, n, dl, n, n, n, dl, n, dl, n, n, n, dl, n, n], 
                            [tw, n, n, dl, n, n, n, cnt, n, n, n, dl, n, n, tw],
                            [n, n, dl, n, n, n, dl, n, dl, n, n, n, dl, n, n], 
                            [n, tl, n, n, n, tl, n, n, n, tl, n, n, n, tl, n], 
                            [n, n, n, n, dw, n, n, n, n, n, dw, n, n, n, n], 
                            [dl, n, n, dw, n, n, n, dl, n, n, n, dw, n, n, dl], 
                            [n, n, dw, n, n, n, dl, n, dl, n, n, n, dw, n, n], 
                            [n, dw, n, n, n, tl, n, n, n, tl, n, n, n, dw, n], 
                            [tw, n, n, dl, n, n, n, tw, n, n, n, dl, n, n, tw]]
                            
        #using self._tiles is work around by Prof. Campbell during office hours
        self._tiles = []
        for r in range(len(self._scrabBoard)):
            fy += 30.4
            self._tiles.append([])
            fx = self._firstSquarePos[1]
            for c in range(len(self._scrabBoard[r])):
                tile = Tile((fx, fy), self._scrabBoard[r][c], self)
                self._tiles[-1].append(tile)    #creates board as grid of tiles
                tile.addTo(win)
                tile.deactivate()
                fx += 30.4
        self._scrabBoard = self._tiles
        
        a1 = int("7") # Prof. Campbell added this to get around
        b1 = int("7") # A Pylint bug.
        self._scrabBoard[a1][b1].activate()
        
        Changebutton(self, win)
        self.changeTurn()
        
    def changeTurn(self):
        """ changes the turn, incremented by one """
        self._players[self._current].deactivateAll()
        self._current += 1
        self._current %= self._playerNumb
        self._players[self._current].activateAll()
        
    def computeLanding(self, piece):
        """ computes the landing location of the piece on the board """
        a1 = int("0") # Prof. Campbell added this to get around
        b1 = int("0") # A Pylint bug.
        tile = self._scrabBoard[a1][b1]
        x0, y0 = tile.getLocation()
        x0 -= 15
        y0 -= 15
        x1, y1 = piece.getLocation()
        col = (x1 - x0) // 30
        row = (y1 - y0) // 30
        if row < 0 or col < 0 or row > 14 or col > 14:
            return None
        if self._scrabBoard[row][col].getPiece() != None or \
        self._scrabBoard[row][col].getActiveStatus() is False:
            return None
        return row, col

    def report(self, piece, event):
        """ establishes what to do when piece is placed on board """
        if self.computeLanding(piece) != None:
            r, c = self.computeLanding(piece)
            landing = self._scrabBoard[r][c]
            
            if landing.getActiveStatus():
                self._scrabBoard[r][c].activateIfNoPiece(r, c)
                
            piece.placedOnBoard()
            landing.addPiece(piece)
            piece.moveTo(landing.getLocation()) #snaps piece to fit closest tile
            landing.deactivate()
            self._players[self._current].removePiece(piece)
            self._players[self._current].replenish(self._bagofpieces)
            self._players[self._current].addValueList((piece.getValue(),\
            landing.getLetterMultiplier(), landing.getWordMultiplier()))
            
    def getPlayer(self):
        """ returns the current player """
        return self._players[self._current]
    
    def getAllPieces(self):
        """ returns all pieces """
        return self._bagofpieces
    
    def getScrabBoard(self):
        """ returns board of tiles """
        return self._scrabBoard
        
    def putPointsOut(self):
        """ calls on player to update point score """
        self._players[self._current].putOutPoints()
        
    def getWin(self):
        """ returns the window """
        return self._win
    
    def getWinnerPlayer(self):
        """ Returns the player number of the winner """
        largestPlayerNumb = self._players[0].getPoints()
        largestPlayer = 0
        for player in self._players:
            if player.getPoints() > largestPlayerNumb:
                largestPlayerNumb = player.getPoints()
                largestPlayer = player.getPlayerNumb()
        return largestPlayer
        
    def getWinnerPoints(self):
        """ Returns the points of the winning player """
        largestPlayerNumb = self._players[0].getPoints()
        for player in self._players:
            if player.getPoints() > largestPlayerNumb:
                largestPlayerNumb = player.getPoints()
        return largestPlayerNumb


def main(win):
    """ sets window dimensions and runs program """
    win.setWidth(900)
    win.setHeight(600)
    
    Board(win)
 
StartGraphicsSystem(main)
