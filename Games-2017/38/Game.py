"""
******************************************************************************
FILE: Game.py

AUTHOR: Tucker Ward

PARTNER: N/A

ASSIGNMENT: Project 6

DATE: 5/1/17

DESCRIPTION: This is a game of scrabble. Game over and Trade Button are slightly
buggy

***************************************************************************** 
"""

import random
from cs110graphics import *
#from wordParser2 import DICTIONARY

class Tile:
    """This class represents a single space on the board. It is a 
    pseudographical object that stores information about word multipliers"""
    def __init__(self, center, multLetter, multWord,
                 color, value, text, position):
        """Create a constructor for the object Tile"""
        
        # Store location and drawing information
        self._center = center
        self._dim = 40
        self._value = value
        self._letterMult = multLetter
        self._wordMult = multWord
        self._adjacentToLetter = False
        self._boardPos = position
        
        # Store the information that gives the tile a particular purpose 
        self._manager = None
        self._multLetter = multLetter
        self._multWord = multWord
        
        # Store graphical objects for tile
        self._tile = Rectangle(self._dim, self._dim, center)
        self._tile.setFillColor(color)
        self._tile.setBorderWidth(2)
        self._tile.setBorderColor('white')
        cx, cy = center
        self._bounds = ((cx - 20, cy - 20), (cx + 20, cy + 20))
        self._text = Text(text, (cx, cy + 5), 18)
        self._tile.setDepth(100)
        self._text.setDepth(100)
        
    def addTo(self, win):
        """Add a tile to a window"""
        
        win.add(self._tile)
        win.add(self._text)
        
    def setManager(self, obj):
        """Tell a tile who its GameManager is"""
        
        self._manager = obj
        
    def getCenter(self):
        """Return the center location of a tile"""
        
        return self._center
    
    def getValue(self):
        """Return the value of the letter object on the tile"""
        
        return self._value
        
    def getLetterMult(self):
        """Return the letter multiplier of the tile"""
        
        return self._letterMult
        
    def getWordMult(self):
        """Return the word multiplier of the tile"""
        
        return self._wordMult
        
    def setLetterMult(self, val):
        """Sets the letter multiplier of the tile"""
        
        self._letterMult = val
        
    def setWordMult(self, val):
        """Sets the word multiplier of the tile"""
        
        self._wordMult = val
        
    def setValue(self, val):
        """Sets the value attribute of the tile"""
        
        self._value = val
        
    def update(self, letter):
        """Responsible for setting a value of the tile to allow scoring"""
        
        self._value = letter
        
    def getBoardPos(self):
        """Return the position on the board of a tile"""
        
        return self._boardPos
        
    def highlight(self):
        """Change the appearance of the tile to look highlighted"""
        
        self._tile.setBorderWidth(3)
        self._tile.setBorderColor('red')
        
    def unhighlight(self):
        """Undo the appearance changes of the highligh() function"""
        
        self._tile.setBorderWidth(1)
        self._tile.setBorderColor('black')
        
class Board():
    """This class holds a list of tiles in a board as well as the graphical
    construction for the board. Acts as a middle man between Tiles and
    GameManager"""
    
    def __init__(self, win):
        """Create a graphical board of tiles to play the game"""
        self._border = Square(600, (600, 300))
        self._border.setBorderWidth(2)
        self._manager = None
        
        # Set up space values for board: mt = "empty" or no special multiplier
        # tw and tl are triple word and letter dw and dl are double word and
        # letter ctr is the center special tile
        mt = (1, 1, '#C6C0A7', None, '')
        tw = (1, 3, '#FA6B50', None, 'TW')
        tl = (3, 1, '#3E9DB4', None, 'TL')
        dw = (1, 2, '#F1B3A4', None, 'DW')
        dl = (2, 1, '#BBD6D1', None, 'DL')
        # CITE: http://stackoverflow.com/questions/3215168/how-to-get-character
        # -in-a-string-in-python, http://www.fileformat.info/info/unicode/char
        # /2605/index.htm
        # DESC: Learning how to put a unicode character in to a string as well
        # as the unicode value for a star
        ctr = (1, 2, '#F1B3A4', None, u'\u2605')
        
        # Create a grid to represent board
        self._board = []
        brd = [[tw, mt, mt, dl, mt, mt, mt, tw, mt, mt, mt, dl, mt, mt, tw],
               [mt, dw, mt, mt, mt, tl, mt, mt, mt, tl, mt, mt, mt, dw, mt],
               [mt, mt, dw, mt, mt, mt, dl, mt, dl, mt, mt, mt, dw, mt, mt],
               [dl, mt, mt, dw, mt, mt, mt, dl, mt, mt, mt, dw, mt, mt, dl],
               [mt, mt, mt, mt, dw, mt, mt, mt, mt, mt, dw, mt, mt, mt, mt],
               [mt, tl, mt, mt, mt, tl, mt, mt, mt, tl, mt, mt, mt, tl, mt],
               [mt, mt, dl, mt, mt, mt, dl, mt, dl, mt, mt, mt, dl, mt, mt],
               [tw, mt, mt, dl, mt, mt, mt, ctr, mt, mt, mt, dl, mt, mt, tw],
               [mt, mt, dl, mt, mt, mt, dl, mt, dl, mt, mt, mt, dl, mt, mt],
               [mt, tl, mt, mt, mt, tl, mt, mt, mt, tl, mt, mt, mt, tl, mt],
               [mt, mt, mt, mt, dw, mt, mt, mt, mt, mt, dw, mt, mt, mt, mt],
               [dl, mt, mt, dw, mt, mt, mt, dl, mt, mt, mt, dw, mt, mt, dl],
               [mt, mt, dw, mt, mt, mt, dl, mt, dl, mt, mt, mt, dw, mt, mt],
               [mt, dw, mt, mt, mt, tl, mt, mt, mt, tl, mt, mt, mt, dw, mt],
               [tw, mt, mt, dl, mt, mt, mt, tw, mt, mt, mt, dl, mt, mt, tw]]
                     
                     
        startX = 320
        startY = 20
        for i in range(15):
            self._board.append([])
            for j in range(15):
                # Create tiles with values specified in grid
                mLetter, mWord, col, val, txt = brd[i][j]
                tile = Tile((startX + i * 40, startY + j * 40),
                            mLetter, mWord, col, val, txt, (i, j))
                self._board[-1].append(tile)
                tile.addTo(win)
        win.add(self._border)        
                
    def setManager(self, obj):
        """Tells each tile who their GameManager is"""
        
        self._manager = obj
        for row in self._board:
            for tile in row:
                tile.setManager(obj)
        
    def getTileAt(self, piece):
        """Returns the tile at the position clicked"""
        
        x0, y0 = self._board[0][0].getCenter()
        x0 -= 20
        y0 -= 20
        x1, y1 = piece.getCenter()
        row = int((x1 - x0) // 40)
        col = int((y1 - y0) // 40)
        
        # Check if the row and col returned by the calculations are valid
        # indicies on the board
        if row < 0 or col < 0 or row > 14 or col > 14:
            return None
        if self._board[row][col].getValue() != None:
            return None
        return self._board[row][col]
    
    def findTile(self, tile):
        """Find the row and col positions of a given letter on the board grid"""
        
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                if self._board[i][j] == tile:
                    return i, j
    
    def clearSpace(self, space):
        """Sets the value of the space on the board to None"""
        
        row, col = self.findTile(space)
        self._board[row][col].setValue(None)
    
    def checkContinuity(self, heading, anchor):
        """Using a heading and anchor specified by the game manager, this
        function makes sure that all the letters are places in the correct row
        and col and that they touch the rest of the word"""
        
        i = 0
        dx, dy = heading
        moves = self._manager.getMove()
        letters = []
        for move in moves:
            
            # Appends letter component of move
            letters.append(move[0])
        sx, sy = self.findTile(anchor)
        length = len(moves)
        
        # Step through the board for the length of the word number of times
        while i < length:
            tile = self.getSpace(sx, sy)
            letter = tile.getValue()
            
            # Means that tiles are not continguous
            if letter is None:
                return False
                
            # If the letter is already in the crossword add to length
            if letter.checkPartOfCrossword():
                i += 1
                length += 1
            elif letter in letters:
                i += 1
            sx += dx
            sy += dy
        return True
    
    def additionalWordFind(self, heading, anchor):
        """This function is responsible for finding the scores of words that 
        are formed by branching off of the letters placed in the main word"""
        
        dx, dy = heading
        row, col = self.findTile(anchor)
        
        # Back up to beginning of word
        while self._board[row][col].getValue() != None:
            if row - 1 == 0 or col - 1 == 0:
                break
            row -= dx
            col -= dy
        row += dx
        col += dy
        score = 0
        wordMult = 1
        
        # Step through all letters until you get to a blank space
        while self._board[row][col].getValue() != None:
            letterMult = self._board[row][col].getLetterMult()
            score += self._board[row][col].getValue().getValue() * letterMult
            
            # Set already used letter multiplier to 1
            self._board[row][col].setLetterMult(1)
            wM = self._board[row][col].getWordMult()
            if wM != 1:
                wordMult = wM
            self._board[row][col].setWordMult(1)
            if row + 1 == len(self._board) or col + 1 == len(self._board[row]):
                break
            row += dx
            col += dy
        score *= wordMult
        return score
    
    def score(self, heading, anchor):
        """This is the main scoring function that calculates a score for a 
        word placed by a player"""
        
        dx, dy = heading
        row, col = self.findTile(anchor)
        
        # Step back to beginning of word
        while self._board[row][col].getValue() != None:
            if row != 0:
                row -= dx
            else:
                break
            if col != 0:
                col -= dy
            else:
                break
        row += dx
        col += dy
        score = 0
        wordMult = 1
        
        # Step through the word adding the values of the letters*multipliers
        while self._board[row][col].getValue() != None:
            letterMult = self._board[row][col].getLetterMult()
            score += self._board[row][col].getValue().getValue() * letterMult
            wM = self._board[row][col].getWordMult()
            if wM != 1:
                wordMult = wM
            if not self._board[row][col].getValue().checkPartOfCrossword():
                try:
                    if (self._board[row + dy][col + dx].getValue() != None or
                            self._board[row - dy][col - dx].getValue() != None):
                        score += self.additionalWordFind(heading, anchor)
                except IndexError:
                    pass
            self._board[row][col].setWordMult(1)
            self._board[row][col].setLetterMult(1)
            if row + 1 == len(self._board) or col + 1 == len(self._board[row]):
                break
            row += dx
            col += dy
        score *= wordMult
        return score
    
    def getValidTiles(self, tile):
        """This function gets all adjacent tiles to a particular space"""
        
        tiles = []
        row, col = self.findTile(tile)
        
        # Check to avoid indexing errors then add space
        if row - 1 >= 0:
            tiles.append(self._board[row - 1][col])
        if row + 1 < len(self._board):
            tiles.append(self._board[row + 1][col])
        if col - 1 >= 0:
            tiles.append(self._board[row][col - 1])
        if col + 1 < len(self._board[row]):
            tiles.append(self._board[row][col + 1])
                        
        return tiles
        
    def getSpace(self, row, col):
        """This function returns a board space at a specific row/col"""
        
        return self._board[row][col]
                
class Letter(EventHandler):
    """This class represents a letter piece. It can handle its own mouse 
    events and moves with a mouse."""
    
    def __init__(self, manager, owner, letter, value, position, center):
        """This initializes the pieces of a letter"""
        
        # Establishes information about location in the window
        EventHandler.__init__(self)
        self._owner = owner
        self._letter = letter
        self._value = value
        self._position = position
        self._manager = manager
        self._depth = 50
        self._origin = center
        self._center = center
        
        # Initialize information to move at the right times
        self._clicked = False
        self._exchanging = False
        self._marked = False
        self._active = False
        self._placed = False
        self._isInCrossword = False
        self._location = center
        
        # Create graphical components of project
        cx, cy = center
        self._rect = Rectangle(40, 40, center)
        self._back = Rectangle(40, 40, center)
        self._rect.setFillColor('#efcca2')
        self._back.setFillColor('#efcca2')
        self._rect.setDepth(self._depth + 2)
        self._lText = Text(letter, (cx, cy + 10), 30)
        self._vText = Text(value, (cx + 13, cy + 12), 12)
        self._lText.setDepth(self._depth + 1)
        self._vText.setDepth(self._depth + 1)
        self._back.setDepth(self._depth)
        self._rect.addHandler(self)
        self._lText.addHandler(self)
        self._vText.addHandler(self)
        self._pieces = [self._rect, self._back, self._lText, self._vText]
        
    def addTo(self, win):
        """Adds all pieces to a win"""
        
        win.add(self._rect)
        win.add(self._back)
        win.add(self._lText)
        win.add(self._vText)
        
    def removeFrom(self, win):
        """Remove graphical components from win"""
        
        win.remove(self._rect)
        win.remove(self._back)
        win.remove(self._lText)
        win.remove(self._vText)
        
        # Returns the letter value of the tile to the letter pool in manager
        self._manager.returnLetter(self._value)
        
    def setManager(self, obj):
        """set the GameManager class for the letter"""
        
        self._manager = obj
        
    def highlight(self):
        """Graphical adjustment to indicate clicked letters"""
        
        self._rect.setBorderWidth(3)
        self._rect.setBorderColor('red')
        
    def unhighlight(self):
        """Function designed to undo tweaks of highlight function"""
        
        self._rect.setBorderWidth(1)
        self._rect.setBorderColor('black')
        
    def getValue(self):
        """Return the letter value of the letter tile"""
        
        return self._value
    
    def getPosition(self):
        """Return Position of letter"""
        
        return self._position
        
    def getCenter(self):
        """Returns the center of the letter piece"""
        
        return self._center
        
    def getOwner(self):
        """Return player number of who the letter belongs to"""
        
        return self._owner
        
    def setExchanging(self, val):
        """Sets the self._exchanging attribute to a certain val"""
        
        self._exchanging = val
        
    def isMarked(self):
        """Returns if a letter has been marked to exchange"""
        
        return self._marked
        
    def moveTo(self, pos):
        """move a letter to a specified tile"""
        
        cx, cy = pos
        self._rect.moveTo(pos)
        self._back.moveTo(pos)
        self._vText.moveTo((cx + 13, cy + 12))
        self._lText.moveTo((cx, cy + 10))
        self._center = pos
        
    def moveToTile(self, tile):
        """Using move to, center tile on the center of a Tile on the board"""
        
        self.moveTo(tile.getCenter())
        tile.update(self)
        
    def move(self, dx, dy):
        """move tile by a dx, dy"""
        
        self._rect.move(dx, dy)
        self._lText.move(dx, dy)
        self._vText.move(dx, dy)
        cx, cy = self._center
        self._center = (cx + dx, cy + dy)
        
    def activate(self):
        """activates letters so they can be clicked"""
        
        if self._placed:
            return
        self._active = True
        self._back.setDepth(self._depth + 2)
        self._rect.setDepth(self._depth + 1)
        self._lText.setDepth(self._depth)
        self._vText.setDepth(self._depth)
        
    def deactivate(self):
        """Deactivates letters so they can't be clicked"""
        
        self._active = False
        self._back.setDepth(self._depth)
        self._rect.setDepth(self._depth + 2)
        self._lText.setDepth(self._depth + 1)
        self._vText.setDepth(self._depth + 1)
        
    def finalize(self):
        """This method identifies the letter as a part of the crossword"""
        
        self._isInCrossword = True
    
    def checkPartOfCrossword(self):
        """Returns tiles isInCrossword attribute"""
        
        return self._isInCrossword
        
    def undoClick(self, space=None):
        """return Tile to rack optionally takes a space if the letter was on 
        the board in order to clear that space logicically so other tiles can 
        be placed"""
        
        self._clicked = False
        self._placed = False
        self.unhighlight()
        cx, cy = self._origin
        self._rect.moveTo(self._origin)
        self._manager.takeBackTile(self, self._owner)
        
        # If a space is given clear it
        if space != None:
            self._manager.clearBoardSpace(space)
        self._back.moveTo(self._origin)
        self._vText.moveTo((cx + 13, cy + 12))
        self._lText.moveTo((cx, cy + 10))
        
        
    def setDepth(self, depth):
        """function designed to bring clicked tile to the front of the layers"""
        
        self._depth = depth
        self._rect.setDepth(self._depth + 1)
        self._lText.setDepth(self._depth)
        self._vText.setDepth(self._depth)
        
        
    def handleMouseRelease(self, event):
        """Handles a click depending on factors like if the tile is
        active or already clicked """
        
        if not self._active:
            return
        if self._placed:
            return
        
        # Special action if the player is exchanging 
        if self._exchanging:
            if not self._marked:
                self._marked = True
                self.highlight()
            else:
                self._marked = False
                self.unhighlight()
        else:
            # Actions of the letter has not already been clicked
            if not self._clicked:
                self.highlight()
                self._clicked = True
                self.setDepth(10)
                self._manager.setLetter(self)
            
            # Actions if the letter has been clicked
            else:
                self._clicked = False
                self._placed = True
                self.unhighlight()
                self.setDepth(50)
                self._manager.report()
    
    def handleMouseMove(self, event):
        """Makes the tile follow the mouse position after it has been clicked"""
        
        if not self._clicked:
            return
        newX, newY = event.getMouseLocation()
        self.moveTo((newX, newY))
        self._location = (newX, newY)

class SubmitButton(EventHandler):
    """This class is a sumbit putton to advance turns after a player has placed
    their word"""
    
    def __init__(self, center, player, win):
        """Initialize variables and graphical objects of button"""
        EventHandler.__init__(self)
        cx, cy = center
        self._player = player
        self._doneButton = Rectangle(75, 25, (cx - 75, cy - 40))
        self._doneButton.setFillColor('green')
        self._text = Text('Submit', (cx - 75, cy - 35), 14)
        self._text.addHandler(self)
        self._doneButton.addHandler(self)
        win.add(self._doneButton)
        win.add(self._text)
        
    def handleMousePress(self, event):
        """Visual change to let user know they clicked the button"""
        self._doneButton.setFillColor('#cccccc')
    
    def handleMouseRelease(self, event):
        """Reports the click to it's player"""
        self._player.submitReport()
        self._doneButton.setFillColor('green')
        
class PassButton(EventHandler):
    """This class is a button which allows the player to simply pass their
    turn"""
    
    def __init__(self, center, player, win):
        """Initialize logical and graphical attributes of button"""
        
        EventHandler.__init__(self)
        cx, cy = center
        self._player = player
        self._doneButton = Rectangle(75, 25, (cx + 10, cy - 40))
        self._doneButton.setFillColor('#add8e6')
        self._text = Text('Pass', (cx + 10, cy - 35), 14)
        self._text.addHandler(self)
        self._doneButton.addHandler(self)
        win.add(self._doneButton)
        win.add(self._text)
        
    def handleMousePress(self, event):
        """Visual change to let user know mouse has been pressed"""
        
        self._doneButton.setFillColor('#cccccc')
    
    def handleMouseRelease(self, event):
        """Sends report of being clicked to its player"""
        
        self._player.submitPass()
        self._doneButton.setFillColor('#add8e6')

class TradeButton(EventHandler):
    """This is a button that allows players to exchange tiles in their rack 
    with random tiles from the pool. It is slightly buggy."""
    def __init__(self, center, player, win):
        """Initialize logical and graphical attributes of button"""
        
        EventHandler.__init__(self)
        cx, cy = center
        self._final = False
        self._player = player
        self._doneButton = Rectangle(75, 25, (cx + 85, cy - 40))
        self._doneButton.setFillColor('#efb956')
        self._text = Text('Exchange', (cx + 85, cy - 35), 14)
        self._text.addHandler(self)
        self._doneButton.addHandler(self)
        win.add(self._doneButton)
        win.add(self._text)
        
    def handleMousePress(self, event):
        """Visual change to let user know mouse has been pressed"""
        
        self._doneButton.setFillColor('#cccccc')
    
    def handleMouseRelease(self, event):
        """Sends report to its player that it has been clicked and indicates 
        if it is the first or second time it has been clicked"""
        
        if self._final is False:
            self._player.submitTrade(False)
            self._final = True
        else:
            self._player.submitTrade(True)
            self._final = False
        
        self._doneButton.setFillColor('#efb956')
    

class PlayerUI():
    """This class manages the players and acts as a middle man for the letters
    and the GameManager. It also has other buttons and UI features that a 
    player may need"""
    
    def __init__(self, win, manager, player, letters, center):
        """Initialize the players with their letters and a button to indicate
        that they have finished placing their pieces"""
        
        # Allows players to select their names
        name = input('Enter name') or ('Player ' + str(player + 1))
        self._letters = []
        self._manager = manager
        self._score = 0
        self._win = win
        self._player = player
        self._active = False
        self._center = center
        cx, cy = center
        self._rack = Rectangle(250, 30, center)
        self._nameTxt = Text(name, (cx - 85, cy - 60), 20)
        self._scoreText = Text("Score: {}".format(str(self._score)), 
                               (cx, cy - 60), 16)
        SubmitButton(center, self, win)
        PassButton(center, self, win)
        #TradeButton(center, self, win)
        win.add(self._rack)
        win.add(self._nameTxt)
        win.add(self._scoreText)
        
        # List correlating letters and values to create letter tiles with
        #appropriate letters and values
        self._letterVals = [('A', 1), ('B', 3), ('C', 3), ('D', 2), ('E', 1), 
                            ('F', 4), ('G', 2), ('H', 4), ('I', 1), ('J', 8), 
                            ('K', 5), ('L', 1), ('M', 3), ('N', 1), ('O', 1), 
                            ('P', 3), ('Q', 10), ('R', 1), ('S', 1), ('T', 1), 
                            ('U', 1), ('V', 4), ('W', 4), ('X', 8), ('Y', 4), 
                            ('Z', 10)]
        
        for i in range(len(letters)):
            for val in self._letterVals:
                if letters[i] == val[0]:
                    ltr = Letter(self._manager, player, letters[i], val[1], i, 
                                 (cx - 130 + i * 40, cy - 5))
                    self._letters.append(ltr)
                    ltr.addTo(win)
                    
    def setManager(self, obj):
        """Indicate the player's GameManager"""
        
        for ltr in self._letters:
            ltr.setManager(obj)
            
    def submitReport(self):
        """Handle end of turn button press to allow class to tell manager to
        changeTurns"""

        if not self._active:
            return
        
        # Check if move was valid
        if self._manager.checkValidMove():
            self._manager.score(self._player)
            self._manager.changeTurn()
            if self._manager.isInFinalMoves():
                self._manager.deductMove()
                if self._manager.getRemainingMoves() <= 0:
                    self._manager.gameOver()
        
        # If the move is not valid pull all pieces off the board    
        else:
            for move in self._manager.getMove():
                move[0].undoClick(move[1])
                self._manager.resetMove()
                
    def submitPass(self):
        """Called if the player passes. Simply changes the move """
        
        for move in self._manager.getMove():
            move[0].undoClick(move[1])
        self._manager.changeTurn()
        if self._manager.isInFinalMoves():
            self._manager.deductMove()
            if self._manager.getRemainingMoves() <= 0:
                self._manager.gameOver()
                
    def getLetters(self):
        """Return list of letters"""
        
        return self._letters
    
    def getScore(self):
        """Return player's score"""
        
        return self._score
        
    def submitTrade(self, done):
        """Deals with letter exchanges. comes in two parts, the first and 
        second click"""
        
        for move in self._manager.getMove():
            move[0].undoClick(move[1])
            
        # On the first click just set all the letters so they can be exchanged
        if not done:
            for ltr in self._letters:
                ltr.setExchanging(True)
                
        # On the second click loop through all letters and remove letter 
        # if it is marked
        else:
            for ltr in self._letters:
                if ltr.isMarked():
                    self.relinquish(ltr)
                    ltr.removeFrom(self._win)
            self.replaceTiles()
            for ltr in self._letters:
                ltr.setExchanging(False)
            self._manager.changeTurn()
            
            
            
    def activateAll(self):
        """Activate all letters in the letter rack presumably when it is a
        specific player's turn"""
        
        self._active = True
        for letter in self._letters:
            if letter != None:
                letter.activate()
            
    def deactivateAll(self):
        """Deactivate all letters in a player's rack presumably at the end of
        their turn"""
        
        self._active = False
        for letter in self._letters:
            if letter != None:
                letter.deactivate()
            
    def relinquish(self, letter):
        """This method removes a letter from the player's list of letters and
        replaces it with the value None"""
        
        position = 0
        for i in range(len(self._letters)):
            if self._letters[i] == letter:
                position = i
        self._letters.pop(position)
        self._letters.insert(position, None)
        return position
        
    def takeBack(self, letter):
        """Returns a letter from the board to its player"""
        
        self._letters[letter.getPosition()] = letter
        
    def addLetter(self, pos, letter):
        """Adds a letter with a given value to a position"""
        
        cx, cy = self._center
        for val in self._letterVals:
            if letter == val[0]:
                ltr = Letter(self._manager, self._player, letter, val[1], pos, 
                             (cx - 130 + pos * 40, cy - 5))
                ltr.addTo(self._win)
        self._letters[pos] = ltr
        
    def replaceTiles(self):
        """Replace all tiles with a None value in the letter list"""
        
        for i in range(len(self._letters)):
            if self._letters[i] is None:
                self.addLetter(i, self._manager.requestLetter())
                
    def addScore(self, score):
        """Adds to a player's score"""
        
        self._score += score
        self._scoreText.setTextString('Score: {}'.format(str(self._score)))
            
class GameManager(EventHandler):
    """This class manages the game and creates the board and players. It
    communicates messages between disconnected objects"""
    
    def __init__(self, win):
        """Create board and players"""
        
        EventHandler.__init__(self)
        self._board = Board(win)
        self._board.setManager(self)
        self._requiredSpaces = [self._board.getSpace(7, 7)]
        self._currentMove = []
        self._heading = (0, 0)
        self._valid = False
        self._isInFinalMoves = False
        self._movesLeft = 0
        self._moves = []
        self._state = 1
        self._toReplace = []
        self._win = win
        self._letterClicked = None
        self._spaceClicked = None
        self._players = []
        self._ltrPool = ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
                         'E', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'I', 
                         'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'O', 'O', 'O', 
                         'O', 'O', 'O', 'O', 'O', 'N', 'N', 'N', 'N', 'N', 'N', 
                         'R', 'R', 'R', 'R', 'R', 'R', 'T', 'T', 'T', 'T', 'T',
                         'T', 'L', 'L', 'L', 'L', 'S', 'S', 'S', 'S', 'U', 'U', 
                         'U', 'U', 'D', 'D', 'D', 'D', 'G', 'G', 'G', 'B', 'B', 
                         'C', 'C', 'M', 'M', 'P', 'P', 'F', 'F', 'H', 'H', 'V', 
                         'V', 'W', 'W', 'Y', 'Y', 'K', 'J', 'X', 'Q', 'Z']
        players = input("How many players (up to 4)")
        random.shuffle(self._ltrPool)
        
        # Create the right number of players with letter lists
        for i in range(int(players)):
            letters = []
            for _ in range(7):
                r = random.randrange(len(self._ltrPool))
                
                letters.append(self._ltrPool.pop(r))
            player = PlayerUI(win, self, i, letters, (160, 100 + i * 150))
            player.setManager(self)
            self._players.append(player)
            
        self._turn = int(players) - 1
        self.changeTurn()
            
    def setLetter(self, letter):
        """Tells GameManager which letter is being manipulated"""
        
        self._letterClicked = letter
        
    def resetMove(self):
        """Blanks the current move"""
        
        self._currentMove = []
        
    def isInFinalMoves(self):
        """Returns whether the game is reaching the end""" 
        
        return self._isInFinalMoves
        
    def deductMove(self):
        """Subtracts one from the remaining moves left"""
        
        self._movesLeft -= 1
        
    def getRemainingMoves(self):
        """Return how many moves are left in a game"""
        
        return self._movesLeft
        
        
    def changeTurn(self):
        """change turn between players by telling players to activate and
        deactivate letters also replenishes the letters in the new player's
        rack"""
        
        self._players[self._turn].deactivateAll()
        self.updateRequiredSpaces()
        self.makePartOfCrossword()
        self._moves.append((self._currentMove, self._currentMove))
        self._currentMove = []
        self._turn += 1
        self._turn %= len(self._players)
        self._valid = False
        self._players[self._turn].replaceTiles()
        self._players[self._turn].activateAll()
    
    def returnLetter(self, letter):
        """Returns a letter to the letter pool"""
        
        self._ltrPool.append(letter)
    
    def makePartOfCrossword(self):
        """Finalizes move and makes it a part of the crossword"""
        
        for moves in self._currentMove:
            moves[0].finalize()
    
    def updateRequiredSpaces(self):
        """Add tiles that are adjacent to the letters places and that have 
        a value of None to the list of required spaces"""
        
        for moves in self._currentMove:
            letters = self._board.getValidTiles(moves[1])
            for i in range(len(letters)):
                if letters[i].getValue() is None:
                    self._requiredSpaces.append(letters[i])
            for space in self._requiredSpaces:
                space.highlight()
        
    def report(self):
        """Called when a letter is dropped. Either snaps to a space or returns
        to rack then sets the value of the board space if an actual space was
        selected"""
        
        place = self._board.getTileAt(self._letterClicked)
        if place is None:
            self._letterClicked.undoClick()
            return
        if place in self._requiredSpaces:
            self._valid = True
        self._toReplace.append(self._players[self._turn].
                               relinquish(self._letterClicked))
        self._letterClicked.moveToTile(place)
        place.update(self._letterClicked)
        self._currentMove.append((self._letterClicked, place))
        
        # Special case for the second move to determine the heading of a word
        if len(self._currentMove) == 2:
            rowZero, colZero = self._board.findTile(self._currentMove[0][1])
            rowOne, colOne = self._board.findTile(self._currentMove[1][1])
            dRow, dCol = (rowOne - rowZero, colOne - colZero)
            
            # Normalize heading to either (1, 0) or (0, 1)
            try:
                dRow /= dRow
            except ZeroDivisionError:
                pass
            try:
                dCol /= dCol
            except ZeroDivisionError:
                pass
            self._heading = (dRow, dCol)
        
    def getAnchorTile(self):
        """Returns the space with the lowest row or col index depending on
        the heading"""
        
        minX, minY = self._board.findTile(self._currentMove[0][1])
        anchor = self._currentMove[0][1]
        
        # Finds min values and sets anchor equal to space with those values 
        if self._heading[0] != 0:
            for move in self._currentMove:
                row, col = self._board.findTile(move[1])
                if row < minX:
                    minX = row
                    anchor = move[1]
        if self._heading[1] != 0:
            for move in self._currentMove:
                row, col = self._board.findTile(move[1])
                if col < minY:
                    minY = col
                    anchor = move[1]
        return anchor
        
    def clearBoardSpace(self, space):
        """Tells the board to clear the value of a board space"""
        
        self._board.clearSpace(space)
                        
    def checkValidMove(self):
        """Checks if word played is legal"""
        
        connectsToCrossword = False
        connectsToMove = False
        for moves in self._currentMove:
            place = moves[1]
            
            #If the word played touches at least one of the existing words
            if place in self._requiredSpaces:
                connectsToCrossword = True
        
        # If each letter in the word touches at least one other in the 
        #correct heading    
        connectsToMove = self._board.checkContinuity(self._heading, 
                                                     self.getAnchorTile())
        return connectsToCrossword and connectsToMove
    
    def takeBackTile(self, tile, player):
        """Tells a player to take back a tile"""
        
        self._players[player].takeBack(tile)
            
    
    def score(self, player):
        """Calculate the score of the placed word"""
        self._players[player].addScore(self._board.score(self._heading, 
                                                         self.getAnchorTile()))
    
    def requestLetter(self):
        """Returns a random letter from the letter pool and sets endgame 
        into motion if the letter pool is empty"""
        
        if len(self._ltrPool) > 0:
            r = random.randrange(len(self._ltrPool))
            letter = self._ltrPool.pop(r)
            return letter
            
        # Case for if the pool is empty and we need to end the game soon
        else:
            for player in self._players:
                if player.getLetters() == [None] * 7:
                    self.gameOver()
            if not self._inFinalMoves:
                self._isInFinalMoves = True
                self._movesLeft = len(self._players)
            return None
        
    def getMove(self):
        """Return the current move"""
        
        return self._currentMove
        
        
    def gameOver(self):
        """Ends the game and determines a winner"""
        
        rect = Rectangle(1200, 600, (600, 300))
        rect.setFillColor('white')
        self._win.add(rect)
        self._win.add(Text("Game Over", (600, 150), 50))
        maxScore = self._players[0].getScore()
        player = 0
        for i in range(len(self._players)):
            if self._players[i].getScore() > maxScore:
                maxScore = self._players[i].getScore()
                player = i 
        self._win.add(Text("Winner: Player {} with {} points!".
                           format(player + 1, maxScore), (600, 450), 50))

def main(win):
    """Function to create a GameManager"""
    _ = GameManager(win)
    

StartGraphicsSystem(main, width=1200, height=600)
