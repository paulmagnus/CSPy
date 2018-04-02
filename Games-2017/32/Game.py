"""
*****************************************************************************
       FILE: Game.py
     AUTHOR: Simon Newton
    PARTNER: N/A
 ASSIGNMENT: Project 6
       DATE: 05/01/17
DESCRIPTION: Creates the board game Scrabble.
*****************************************************************************
"""
import random
import math
from cs110graphics import *

#defines the size of the graphical window
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 750

def rnd(x):
    """ returns a random value in a given range """
    return random.randrange(x)

def distance(cenA, cenB):
    """ returns the value of the distance between two points """
    return math.sqrt((cenB[0] - cenA[0]) ** 2 + (cenB[1] - cenA[1]) ** 2)

class Board:
    """ creates the scrabble board """
    
    def __init__(self, win):
        """ constructs and initializes the board """
        #CITE: https://en.wikipedia.org/wiki/Scrabble
        #DETAILS: A Wikipedia page that outlines the game Scrabble
        self._url = "https://cs.hamilton.edu/~sanewton/images/scrabble_logo.png"
        self._title = Image(self._url, (650, 60), 209.25, 92.25)
        
        #creates all the center coordinates for the board tiles
        rows = 15
        columns = 15
        coords = []
        for i in range(rows):
            cx = 330
            cy = 145
            cy += 40 * i
            for _ in range(columns):
                cx += 40
                coords.append((cx, cy))
        
        #fills the boards with regular tiles
        self._board = []
        for position in coords:
            self._board.append(Tile(position, '#f5deb3', None, 0, None))
        
        #adds multiplier tiles with different colors
        orangeTiles = [0, 7, 14, 105, 119, 210, 217, 224]
        for tile in orangeTiles:
            self._board[tile] = Tile(coords[tile], 'orange', 'TW', 3, 'word')
        blueTiles = [3, 11, 36, 38, 45, 59, 92, 96, 98, 102, 108, 116, 122, 126,
                     128, 132, 165, 172, 179, 186, 188, 213, 221]
        for tile in blueTiles:
            self._board[tile] = Tile(coords[tile], 'LightBlue', 'DL', 2,
                                     'letter')
        redTiles = [16, 28, 32, 42, 48, 56, 64, 70, 154, 160, 168, 176, 182,
                    192, 196, 208]
        for tile in redTiles:
            self._board[tile] = Tile(coords[tile], 'PaleVioletRed', 'DW', 2,
                                     'word')
        greenTiles = [20, 24, 76, 80, 84, 88, 136, 140, 144, 148, 200, 204]
        for tile in greenTiles:
            self._board[tile] = Tile(coords[tile], 'LightGreen', 'TL', 3,
                                     'letter')
        
        #creates a bolder outline of the board
        self._outline = Square(600, (650, 425))
        self._outline.setBorderWidth(4)

        #creates star in the middle tile
        starCoords = [(650, 409), (639, 440), (666, 421), (634, 421),
                      (661, 440)]
        self._centerStar = Polygon(starCoords)
        self._centerStar.setFillColor('black')
        self._board[112] = Tile(coords[112], 'PaleVioletRed', None, 0, None)
        
        #initializes the panel, bag, and window
        self._panel = Panel(self)
        self._bag = Bag(self)
        self._win = win
        
        #initializes the players in the game
        player1 = Player(self, self._panel, self._bag, 175)
        player2 = Player(self, self._panel, self._bag, 1125)
        self._players = [player1, player2]
        self._current = 1
        self.changeTurn()
        
        #pieces added each turn and pieces played on the board
        self._addedPieces = []
        self._playedPieces = []
        
        self._exchanging = False
        self._validTiles = []
        self._pass = False

    def addTo(self, win):
        """ adds the tiles, outlines, star, player items, and panels to the
            window """
        win.add(self._title)
        for tile in self._board:
            tile.addTo(win)
        win.add(self._outline)
        win.add(self._centerStar)
        for player in self._players:
            player.addTo(win)
        self._panel.addTo(win)
    
    def getBoard(self):
        """ returns the board as a list of tiles """
        return self._board

    def changeTurn(self):
        """ changes the turn to the other player """
        self._players[self._current].deactivateAll()
        self._current += 1
        self._current %= 2
        self._players[self._current].activateAll()

    def addScore(self):
        """ updates the player's score when the turn ends """
        #determines the points for each added piece and then total score
        turnScore = 0
        turnMultiplier = 1
        for piece in self._addedPieces:
            pieceValue = piece.getValue()
            pieceKind = piece.getTile().getKind()
            pieceMultiplier = piece.getTile().getSize()
            if pieceKind == 'letter':
                turnScore += pieceValue * pieceMultiplier
            elif pieceKind == 'word':
                turnScore += pieceValue
                if turnMultiplier == 1:
                    turnMultiplier = pieceMultiplier
                else:
                    turnMultiplier += pieceMultiplier
            elif pieceKind is None:
                turnScore += pieceValue
        turnScore *= turnMultiplier
    
        #adds score from turn to total player score and updates the window
        totalScore = self._players[self._current].updateScore(turnScore)
        self._panel.updateScore(self._current, totalScore)
        
    def clearPieces(self):
        """ empties the list of added pieces """
        self._addedPieces = []
    
    def refill(self):
        """ gives the player a random piece for each piece they played """
        for piece in self._addedPieces:
            newPiece = self._bag.randomPiece()
            self._players[self._current].givePiece(newPiece)
            newPiece.setHome(piece.getHome())
            newPiece.returnHome()
            newPiece.setDepth(1)
            newPiece.addTo(self._win)
    
    def returnPieces(self):
        """ returns all of the player's piece to their homes """
        for piece in self._players[self._current].getPieces():
            piece.returnHome()
    
    def playPieces(self):
        """ removes pieces from the player's possession and locks them on the
            board """
        for piece in self._addedPieces:
            self._playedPieces.append(piece)
            self._players[self._current].removePiece(piece)
            piece.deactivate()
    
    def getPlayedPieces(self):
        """ returns the pieces that have been played on the board """
        return self._playedPieces
    
    def shufflePieces(self):
        """ shuffles the locations of the player's pieces """
        #gets the player's pieces and their home locations
        playerPieces = self._players[self._current].getPieces()
        currentHomes = []
        for piece in playerPieces:
            currentHomes.append(piece.getHome())
        
        #moves each of the player's pieces to a random home
        random.shuffle(playerPieces)
        for i in range(len(playerPieces)):
            playerPieces[i].setHome(currentHomes[i])
            playerPieces[i].returnHome()
    
    def exchangingActive(self):
        """ makes the player's pieces ready to be exchanged """
        self._exchanging = True
    
    def exchangingDeactive(self):
        """ stops the player's pieces from being exchanged """
        self._exchanging = False
    
    def exchanging(self):
        """ returns whether the board ready to exchange tiles """
        return self._exchanging
    
    def exchangePieces(self):
        """ exchanges tiles with random ones from the bag """
        #for each of the player's pieces, takes a random piece from the bag and
        #replaces it with the exchanged tile
        currentPlayer = self._players[self._current]
        playerPieces = currentPlayer.getPieces()
        readyPieces = []
        newPieces = []
        for piece in playerPieces:
            if piece.isReady():
                newPiece = self._bag.randomPiece()
                newPiece.addTo(self._win)
                newPiece.setHome(piece.getHome())
                newPiece.returnHome()
                newPiece.setDepth(1)
                newPieces.append(newPiece)
                readyPieces.append(piece)
                piece.removeFrom(self._win)
        
        #adds the newly exchanged pieces to the player's possession
        for newPiece in newPieces:
            currentPlayer.givePiece(newPiece)
        
        #removes the old tiles from the player's possession and puts them in the
        #bag
        for piece in readyPieces:
            currentPlayer.removePiece(piece)
            self._bag.addToBag(piece)
            
    def bothPass(self):
        """ returns whether the last player also passed """
        return self._pass
        
    def setPass(self, value):
        """ establishes whether the last turn was a pass """
        self._pass = value
    
    def endGame(self):
        """ ends the game and determines a winner """
        #deactivates all of each players items
        for player in self._players:
            player.deactivateAll()
        
        #gets the players' scores and determines who is the winner
        player1score = self._players[0].getScore()
        player2score = self._players[1].getScore()
        if player1score > player2score:
            p1Rec = Rectangle(350, 150, (650, 375))
            p1Rec.setFillColor('#ce3120')
            p1Rec.setBorderWidth(4)
            p1Rec.setDepth(1)
            p1Text = Text("Player 1 Wins!", (650, 390), 50)
            p1Text.setDepth(1)
            self._win.add(p1Rec)
            self._win.add(p1Text)
        elif player2score > player1score:
            p2Rec = Rectangle(350, 150, (650, 375))
            p2Rec.setFillColor('CornflowerBlue')
            p2Rec.setBorderWidth(4)
            p2Rec.setDepth(1)
            p2Text = Text("Player 2 Wins!", (650, 390), 50)
            p2Text.setDepth(1)
            self._win.add(p2Rec)
            self._win.add(p2Text)
        else:
            drawRec = Rectangle(350, 150, (650, 375))
            drawRec.setFillColor('white')
            drawRec.setBorderWidth(4)
            drawRec.setDepth(1)
            drawText = Text("Draw!", (650, 390), 50)
            drawText.setDepth(1)
            self._win.add(drawRec)
            self._win.add(drawText)
    
    def computeLanding(self, piece):
        """ finds the closest tile to the piece """
        #gets the centers of the given piece and all the tiles on the board
        pieceX, pieceY = piece.getLocation()
        locations = []
        for tile in self._board:
            locations.append(tile.getLocation())
            
        #computes which tile center is closest to the piece center
        count = 40
        closestTile = None
        for i in range(len(locations)):
            location = locations[i]
            if distance((pieceX, pieceY), location) < count:
                count = distance((pieceX, pieceY), location)
                closestTile = self._board[i]
        return closestTile
    
    def snapBoard(self, piece):
        """ snaps tiles to the board """
        landing = self.computeLanding(piece)
        if landing != None: 
            piece.moveTo(landing.getLocation())
            piece.setTile(landing)
            if piece not in self._addedPieces:
                self._addedPieces.append(piece)
                piece.setDepth(2)

class Tile:
    """ creates the lettered tiles """
    
    def __init__(self, center, color, letters, size, kind):
        """ constructs the tiles that make up the board """
        #creates the tile given center, color, and multiplier text
        self._center = center
        self._letters = letters
        cx, cy = center
        self._size = size
        self._kind = kind
        self._tile = Square(40, center)
        self._tile.setBorderWidth(2)
        self._tile.setFillColor(color)
        if self._letters != None:
            self._multiplierText = Text(self._letters, (cx, cy + 6), 16)
    
    def getLocation(self):
        """ returns the center coordinates of the tile """
        return self._center
        
    def getSize(self):
        """ returns the size of the multiplier the tile gives """
        return self._size
    
    def getKind(self):
        """ returns the kind of multipler the tile gives """
        return self._kind
    
    def addTo(self, win):
        """ adds the tile and the text to the window """
        win.add(self._tile)
        if self._letters != None:
            win.add(self._multiplierText)

class Panel:
    """ creates side panels for two players on either side of the board """
    
    def __init__(self, board):
        """ contructs the panels on either side of the board for each player """
        #player 1's panel graphics
        self._p1Box = Rectangle(320, 600, (175, 425))
        self._p1Box.setFillColor('#f5deb3')
        self._p1Box.setBorderWidth(4)
        self._p1LabelRec = Rectangle(290, 90, (175, 180))
        self._p1LabelRec.setFillColor('#ce3120')
        self._p1LabelRec.setBorderWidth(2)
        self._p1LabelText = Text('Player 1', (175, 192), 32)
        self._p1ScoreText = Text("Score: ", (140, 275), 30)
        self._p1 = [self._p1Box, self._p1LabelRec, self._p1LabelText,
                    self._p1ScoreText]
        
        #player 2's panel graphics
        self._p2Box = Rectangle(320, 600, (1125, 425))
        self._p2Box.setFillColor('#f5deb3')
        self._p2Box.setBorderWidth(4)
        self._p2LabelRec = Rectangle(290, 90, (1125, 180))
        self._p2LabelRec.setFillColor('CornflowerBlue')
        self._p2LabelRec.setBorderWidth(2)
        self._p2LabelText = Text('Player 2', (1125, 192), 32)
        self._p2ScoreText = Text("Score: ", (1090, 275), 30)
        self._p2 = [self._p2Box, self._p2LabelRec, self._p2LabelText,
                    self._p2ScoreText]
        
        self._board = board
        self._playerOneScore = Text('0', (220, 275), 30)
        self._playerTwoScore = Text('0', (1170, 275), 30)
    
    def addTo(self, win):
        """ adds both player's buttons and scores to the window """
        for item in self._p1:
            win.add(item)
        for item in self._p2:
            win.add(item)
        win.add(self._playerOneScore)
        win.add(self._playerTwoScore)
    
    def updateScore(self, currentPlayer, totalScore):
        """ updates the player's score """
        if currentPlayer == 0:
            self._playerOneScore.setText(str(totalScore))
        else:
            self._playerTwoScore.setText(str(totalScore))
    
    def select(self, player):
        """ highlights the panel of the current player """
        if player == 'player1':
            self._p1Box.setBorderColor('LimeGreen')
        else:
            self._p2Box.setBorderColor('LimeGreen')
    
    def deselect(self, player):
        """ removes the highlight from the panel of the current player """
        if player == 'player1':
            self._p1Box.setBorderColor('black')
        else:
            self._p2Box.setBorderColor('black')

class Slot:
    """ creates seven slots for the player's current pieces """
    
    def __init__(self, center):
        """ creates the home/spawn locations for the players' pieces """
        self._tile1 = Square(40, (center - 125, 647.5))
        self._tile2 = Square(40, (center - 41.67, 647.5))
        self._tile3 = Square(40, (center + 41.67, 647.5))
        self._tile4 = Square(40, (center + 125, 647.5))
        self._tile5 = Square(40, (center - 83.33, 695))
        self._tile6 = Square(40, (center, 695))
        self._tile7 = Square(40, (center + 83.33, 695))
        self._pieceSlots = [self._tile1, self._tile2, self._tile3, self._tile4,
                            self._tile5, self._tile6, self._tile7]
        for slot in self._pieceSlots:
            slot.setBorderWidth(2)
            slot.setDepth(5)
        
        #changes the color of the slots based on player
        for slot in self._pieceSlots:
            if center == 175:
                slot.setFillColor('#ce3120')
            elif center == 1125:
                slot.setFillColor('CornflowerBlue')

    def getLocations(self):
        """ returns the home locations of the player's piece slots """
        homeLocations = []
        for slot in self._pieceSlots:
            homeLocations.append(slot.getCenter())
        return homeLocations
        
    def addTo(self, win):
        """ adds each of the slots to the window """
        for slot in self._pieceSlots:
            win.add(slot)

class Exchange(EventHandler):
    """ creates a button to exchange player's tiles for tiles from the bag """
    
    def __init__(self, board, center):
        """ creates the button to exchanges pieces """
        EventHandler.__init__(self)
        
        self._exchangeRec = Rectangle(290, 75, (center, 335))
        self._exchangeRec.setFillColor('#f5deb3')
        self._exchangeRec.setBorderWidth(2)
        self._exchangeRec.setDepth(2)
        self._exchangeText = Text('Exchange', (center, 345), 28)
        self._exchangeText.setDepth(1.5)
        
        self._exchangeRec.addHandler(self)
        self._exchangeText.addHandler(self)
        
        self._active = False
        self._board = board

    def addTo(self, win):
        """ adds the exchange button to the window """
        win.add(self._exchangeRec)
        win.add(self._exchangeText)
    
    def activate(self):
        """ activates the button """
        self._active = True
    
    def deactivate(self):
        """ deactivates the button """
        self._active = False
        
    def handleMouseEnter(self, event):
        """ highlights the button when the mouse enters """
        if self._active:
            self._exchangeRec.setBorderColor('red')
    
    def handleMouseLeave(self, event):
        """ removes highlight from the button when the mouse leaves """
        if self._active:
            if not self._board.exchanging():
                self._exchangeRec.setBorderColor('black')

    def handleMouseRelease(self, event):
        """ the first time the button is clicked, it makes the player's
            pieces ready to be exchanged, the second time the button is clicked,
            it exchanges the pieces and changes the turn """
        if self._active:
            if not self._board.exchanging():
                self._board.exchangingActive()
            else:
                self._exchangeRec.setBorderColor('black')
                self._board.exchangingDeactive()
                self._board.exchangePieces()
                self._board.returnPieces()
                self._board.clearPieces()
                self._board.setPass(False)
                self._board.changeTurn()

class Shuffle(EventHandler):
    """ creates a button that shuffles the order of the player's tiles """
    
    def __init__(self, board, center):
        """ constructs a button the shuffles the order of the player's
            pieces """
        EventHandler.__init__(self)
        
        #creates the graphical button
        self._shuffleRec = Rectangle(290, 75, (center, 415))
        self._shuffleRec.setFillColor('#f5deb3')
        self._shuffleRec.setBorderWidth(2)
        self._shuffleRec.setDepth(2)
        self._shuffleText = Text('Shuffle', (center, 425), 28)
        self._shuffleText.setDepth(1.5)
        
        self._shuffleRec.addHandler(self)
        self._shuffleText.addHandler(self)
        
        self._board = board
        self._active = False
        
    def addTo(self, win):
        """ adds the button the window """
        win.add(self._shuffleRec)
        win.add(self._shuffleText)
    
    def activate(self):
        """ activates the button """
        self._active = True
    
    def deactivate(self):
        """ deactivates the button """
        self._active = False

    def handleMouseEnter(self, event):
        """ highlights the button when the mouse enters """
        if self._active:
            self._shuffleRec.setBorderColor('red')
    
    def handleMouseLeave(self, event):
        """ removes highlight from the button when the mouse leaves """
        if self._active:
            self._shuffleRec.setBorderColor('black')
    
    def handleMouseRelease(self, event):
        """ shuffles the player's pieces """
        self._board.shufflePieces()

class Pass(EventHandler):
    """ creates a button that ends the player's turn and awards them no points
    for their turn """
    
    def __init__(self, board, center):
        """ creates a button the allows the player to pass """
        EventHandler.__init__(self)
        
        #creates the graphical button
        self._passRec = Rectangle(290, 75, (center, 495))
        self._passRec.setFillColor('#f5deb3')
        self._passRec.setBorderWidth(2)
        self._passRec.setDepth(2)
        self._passText = Text('Pass', (center, 505), 28)
        self._passText.setDepth(1.5)
        
        self._passRec.addHandler(self)
        self._passText.addHandler(self)
        
        self._board = board
        self._active = False
        
    def addTo(self, win):
        """ adds the button to the window """
        win.add(self._passRec)
        win.add(self._passText)
    
    def activate(self):
        """ activates the button """
        self._active = True
    
    def deactivate(self):
        """ deactivates the button """
        self._active = False
    
    def handleMouseEnter(self, event):
        """ highlights the button when the mouse enters """
        if self._active:
            self._passRec.setBorderColor('red')
    
    def handleMouseLeave(self, event):
        """ removes highlight from the button when the mouse leaves """
        if self._active:
            self._passRec.setBorderColor('black')

    def handleMouseRelease(self, event):
        """ returns all the player's pieces back to their homes, clears the list
            of added pieces, and if the last player's turn was not pass, then
            change turn, otherwise, end the game """
        if self._active:
            self._passRec.setBorderColor('black')
            self._board.returnPieces()
            self._board.clearPieces()
            if not self._board.bothPass():
                self._board.setPass(True)
                self._board.changeTurn()
            else:
                self._board.endGame()

class Play(EventHandler):
    """ creates a button that ends the player's turn and updates their score """
    
    def __init__(self, board, center):
        """ constructs a button that plays pieces on the board and ends the
            player's turn """
        EventHandler.__init__(self)
        
        #creates the graphical button
        self._playRec = Rectangle(290, 75, (center, 575))
        self._playRec.setFillColor('#f5deb3')
        self._playRec.setBorderWidth(2)
        self._playRec.setDepth(2)
        self._playText = Text('Play', (center, 585), 28)
        self._playText.setDepth(1.5)

        self._playRec.addHandler(self)
        self._playText.addHandler(self)
        
        self._board = board
        self._active = False
        
    def addTo(self, win):
        """ adds the button to the window """
        win.add(self._playRec)
        win.add(self._playText)
    
    def activate(self):
        """ activates the button """
        self._active = True
    
    def deactivate(self):
        """ deactivates the button """
        self._active = False
        
    def handleMouseEnter(self, event):
        """ highlights the button when the mouse enters """
        if self._active:
            self._playRec.setBorderColor('red')
    
    def handleMouseLeave(self, event):
        """ removes highlight from the button when the mouse leaves """
        if self._active:
            self._playRec.setBorderColor('black')

    def handleMouseRelease(self, event):
        """ plays pieces to the board, counts and updates the score, refills the
            player's hand, and changes the turn """
        if self._active:
            self._playRec.setBorderColor('black')
            self._board.playPieces()
            self._board.addScore()
            self._board.refill()
            self._board.clearPieces()
            self._board.setPass(False)
            self._board.changeTurn()

class Piece(EventHandler):
    """ creates the pieces for the game """
    
    def __init__(self, letter, board):
        """ creates pieces that are played on the board """
        EventHandler.__init__(self)
        
        #lists of all letters and their corresponding score values
        self._letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                         'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                         'W', 'X', 'Y', 'Z']
        self._points = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1,
                        1, 1, 1, 4, 4, 8, 4, 10]
        
        #assigns the given letter to the corresponding score value
        self._character = letter
        for char in range(len(self._letters)):
            if self._character == self._letters[char]:
                self._value = self._points[char]
        
        #creates the piece with the given letter and score value
        cx, cy = (0, 0)
        self._face = Square(38, (cx, cy))
        self._face.setFillColor('burlywood')
        self._face.setBorderWidth(2)
        self._letter = Text(self._character, (cx - 4, cy + 11), 28)
        self._number = Text(self._value, (cx + 12, cy + 16), 10)
        
        self._face.addHandler(self)
        self._letter.addHandler(self)
        self._number.addHandler(self)
        
        self._home = (0, 0)
        self._moving = False
        self._loc = (0, 0)
        self._startPos = None
        self._active = True
        self._ready = False
        self._board = board
        self._boardList = board.getBoard()
        self._playedPieces = board.getPlayedPieces
        self._tile = None
    
    def addTo(self, win):
        """ adds graphical objects to the window """
        win.add(self._face)
        win.add(self._letter)
        win.add(self._number)
    
    def removeFrom(self, win):
        """ removes graphical objects from the window """
        win.remove(self._face)
        win.remove(self._letter)
        win.remove(self._number)
    
    def setDepth(self, depth):
        """ sets the depth of the piece """
        self._face.setDepth(depth)
        self._letter.setDepth(depth)
        self._number.setDepth(depth)
    
    def faceUp(self):
        """ makes the piece face up """
        depth = self._face.getDepth()
        self._letter.setDepth(depth - 1)
        self._number.setDepth(depth - 1)
    
    def faceDown(self):
        """ makes the piece face down """
        depth = self._face.getDepth()
        self._letter.setDepth(depth + 1)
        self._number.setDepth(depth + 1)
    
    def getLetter(self):
        """ returns the letter of the piece """
        return self._character
    
    def getValue(self):
        """ returns the value of the piece """
        return self._value
    
    def getLocation(self):
        """ returns the center value of the piece """
        return self._loc
    
    def move(self, dx, dy):
        """ moves the tile by dx, dy """
        oldx, oldy = self._loc
        newx = oldx + dx
        newy = oldy + dy
        self.moveTo((newx, newy))
        
    def moveTo(self, pos):
        """ moves the tile to a given location """
        cx, cy = pos
        self._face.moveTo(pos)
        self._letter.moveTo((cx - 4, cy + 11))
        self._number.moveTo((cx + 12, cy + 16))
        self._loc = pos
    
    def activate(self):
        """ makes the piece active """
        self._active = True
    
    def deactivate(self):
        """ makes the piece inactive """
        self._active = False
    
    def highlight(self):
        """ highlights the piece """
        self._face.setBorderColor('yellow')
    
    def deselect(self):
        """ removes highlight from the piece border """
        self._face.setBorderColor('black')
    
    def setHome(self, home):
        """ sets the home location of the piece """
        self._home = home
    
    def getHome(self):
        """ returns the location of the piece's home """
        return self._home
    
    def returnHome(self):
        """ returns the piece back to it's home location """
        cx, cy = self._home
        self._face.moveTo(self._home)
        self._letter.moveTo((cx - 4, cy + 11))
        self._number.moveTo((cx + 12, cy + 16))
        self._loc = self._home
    
    def makeReady(self):
        """ makes the piece ready to be exchanged """
        self._ready = True
    
    def notReady(self):
        """ stops the piece from being exchanged """
        self._ready = False

    def isReady(self):
        """ returns whether the piece is ready to be exchanged """
        return self._ready
    
    def setTile(self, tile):
        """ sets the board tile the piece sits on """
        self._tile = tile
    
    def getTile(self):
        """ returns the board tile the piece sits on """
        return self._tile
        
    def handleMouseRelease(self, event):
        """ if the player is exchanging tiles, clicking the pieces makes it
            ready to be exchanged, otherwise, drags the piece """
        if not self._active:
            return 
        if not self._board.exchanging():
            if self._moving:
                self._moving = False
                self._board.snapBoard(self)
                self.deselect()
            else:
                self._moving = True
                self._startPos = event.getMouseLocation()
        else:
            self.highlight()
            self.makeReady()
            
    def handleMouseMove(self, event):
        """ drags the piece as the mouse moves """
        if not self._active:
            return
        if self._moving:
            oldx, oldy = self._startPos
            newx, newy = event.getMouseLocation()
            self.move(newx - oldx, newy - oldy)
            self._startPos = newx, newy
            self.highlight()
            self._face.setDepth(0.1)
            self._letter.setDepth(0.1)
            self._number.setDepth(0.1)

class Bag:
    """ creates the bag with all the pieces """
    
    def __init__(self, board):
        """ constructs a bag with all the pieces """
        #lists all the letters and how many of them are in the bag
        self._letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                         'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                         'W', 'X', 'Y', 'Z']
        self._occurs = [9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2, 6, 8, 2, 1, 6,
                        4, 6, 4, 2, 2, 1, 2, 1]
        
        #fills the bag with pieces for given amount of occurences 
        self._board = board
        self._bag = []
        for i in range(len(self._letters)):
            for _ in range(self._occurs[i]):
                self._bag.append(Piece(self._letters[i], self._board))

    def randomPiece(self):
        """ removes a random piece from the bag and returns it """
        randomPiece = self._bag[rnd(len(self._bag))]
        self._bag.remove(randomPiece)
        return randomPiece
    
    def addToBag(self, piece):
        """ adds a piece to the bag """
        self._bag.append(piece)

class Player:
    """ creates a class with attributes of the player """
    
    def __init__(self, board, panel, bag, center):
        """ constructs players who play the game """
        self._board = board
        self._panel = panel
        self._bag = bag
        self._score = 0
        
        #creates the player's pieces
        self._pieces = []
        self._count = 7
        self._slots = Slot(center)
        self._homes = self._slots.getLocations()
        for i in range(self._count):
            newPiece = self._bag.randomPiece()
            newPiece.setDepth(1)
            self._pieces.append(newPiece)
        
        #moves each of the player's pieces to their homes locations and sets the
        #depth
        for i in range(len(self._homes)):
            self._pieces[i].setHome(self._homes[i])
            self._pieces[i].returnHome()
            self._pieces[i].setDepth(2)

        #creates the player's buttons in the side panel
        self._buttons = [Exchange(self._board, center),
                         Shuffle(self._board, center),
                         Pass(self._board, center), Play(self._board, center)]
        
        #determines the current player
        if center == 175:
            self._currentPlayer = 'player1'
        elif center == 1125:
            self._currentPlayer = 'player2'
            
    def activateAll(self):
        """ activates all the player's pieces """
        for piece in self._pieces:
            piece.activate()
            piece.faceUp()
        for button in self._buttons:
            button.activate()
        self._panel.select(self._currentPlayer)
    
    def deactivateAll(self):
        """ deactivates all the player's pieces """
        for piece in self._pieces:
            piece.deactivate()
            piece.faceDown()
            piece.notReady()
        for button in self._buttons:
            button.deactivate()
        self._panel.deselect(self._currentPlayer)
    
    def getPieces(self):
        """ returns the player's pieces """
        return self._pieces
    
    def removePiece(self, piece):
        """ removes given pieces from the player's possesion """
        pos = None        
        for i in range(len(self._pieces)):
            if self._pieces[i] == piece:
                pos = i
        if pos != None:
            self._pieces.pop(pos)
    
    def givePiece(self, piece):
        """ adds a given piece to the player's possession """
        self._pieces.append(piece)
    
    def updateScore(self, addScore):
        """ adds score from turn to player score """
        self._score += addScore
        return self._score
    
    def getScore(self):
        """ returns the player's current score """
        return self._score
    
    def addTo(self, win):
        """ adds the player's pieces, buttons, and slots to the window """
        for piece in self._pieces:
            piece.addTo(win)
        for button in self._buttons:
            button.addTo(win)
        self._slots.addTo(win)

def main(win):
    """ outputs the game to the window """
    Board(win).addTo(win)

StartGraphicsSystem(main, WINDOW_WIDTH, WINDOW_HEIGHT)
