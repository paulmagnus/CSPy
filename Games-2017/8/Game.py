""" ****************************************************************************
FILE: Game.py

AUTHOR: Chengqi Guo

PARTNER: None

ASSIGNMENT: Project 6

DATE: 04/06/2017

DESCRIPTION: Scrabble.

The followings are what makes it different from a real game:

It checks for words added, but only following the rules below:
1 consonant following 1 vowel, or
1 vowel following 1 consonant

Each player gets 6 tiles each turn. This is a pure misunderstanding of the 
rules. Lol

Instead of shuffling the word rack each turn, the letters in this game that
are not moved to the board are preserved and new tiles are added to the blank
spaces. Again, this is another misunderstanding.

If we only add 1 tile at a time, there might be some bugs with the score 
calculating algorithms. 

It is always illegal to form two words at the same time. The word with be taken
by the word in the directions the tiles in this turn are added to the 
board. This is exactly what makes 1-tile at a time algorithm difficult and I 
chose not to do that.

*******************************************************************************
"""
import random
from cs110graphics import *


class BoardSpace(EventHandler):
    """The class of the BoardSpace"""
    def __init__(self, board, center, color):
        """set up all the attributes."""
        EventHandler.__init__(self)
        self._board = board 
        self._center = center 
        self._tileCenter = None
        self._tile = Rectangle(20, 20, center)
        self._tile.setFillColor(color)
        self._tile.setDepth(1)
        self._tile.addHandler(self)
        self._onto = False
        self._active = False 
    
    def getOnto(self):
        """Return if the mouse is on itself."""
        return self._onto
    
    def addTo(self, win):
        """Adds every board space to the window."""
        win.add(self._tile)
        
    def getCenter(self):
        """This gets the center of the board space."""
        return self._center
    
    def setFillColor(self, color):
        """Changes the fill color of the board space."""
        self._tile.setFillColor(color)
        
    def handleMouseRelease(self, event):
        """When clicked on, several things happen."""
        if self._active is False:
            self._board.failToAddTiles(self)
        else:
            self._board.reportBoardSpaceClick(self, event)

    def handleMouseMove(self, event):
        """If the mouse is on the space."""
        self._onto = True
        self._board.reportBoardSpaceMove(self, event)
            
    def handleMouseLeave(self, event):
        """IF the mouse leaves the space."""
        self._onto = False
        self._board.reportBoardSpaceMove(self, event)
        
    def getTileCenter(self):
        """Gets the center of the tile."""
        return self._tileCenter
    
    def setBorderColor(self, color):
        """Sets the border color of itself."""
        self._tile.setBorderColor(color)
    
    def restoreBorder(self):
        """Makes the border color go back to the original."""
        self._tile.setBorderColor('black')
        
    def activate(self):
        """Activates the space"""
        self._active = True
    
    def deactivate(self):
        """Deactivates the space."""
        self._active = False
        
    def getActivity(self):
        """Returns the activity of the space."""
        return self._active

class Words(EventHandler):
    """The class of the word tiles."""
    def __init__(self, board, wordBag, letter, color, value):
        """set up all the attributes."""
        EventHandler.__init__(self)
        self._mousePos = (0, 0)
        self._center = (0, 0)
        self._board = board
        self._letter = letter
        self._value = value 
        self._front = Text(letter, (0, 0))
        self._back = Rectangle(18, 18, (0, 0))
        self._front.setDepth(0)
        self._back.setDepth(0)
        self._back.setFillColor(color)
        self._back.addHandler(self)
        self._wordBag = wordBag
        #self._moving = False 
        self._secondClick = False 
        #self._startPos = None     # mouse position where movement started
        self._active = False
    
    def addTo(self, win):
        """Adds the word tiles to the window."""
        win.add(self._back)
        win.add(self._front)
        
    def removeFrom(self, win):
        """Remove from the window."""
        win.remove(self._front)
        win.remove(self._back)
    
    def move(self, dx, dy):
        """Moves the word tile by (dx, dy)."""
        self._front.move(dx, dy)
        self._back.move(dx, dy)
        x, y = self._center
        #update the change
        self._center = (x + dx, y + dy)
    
    def setBorderColor(self, color):
        """Sets the border color."""
        self._back.setBorderColor(color)
    
    def moveTo(self, x, y):
        """Moves the word tile to (x, y)."""
        newLoc = (x, y)
        self._front.moveTo(newLoc)
        self._back.moveTo(newLoc)
        self._center = newLoc
    
     
    def getLetter(self):
        """Returns the letter of the word tile."""
        return self._letter
        
    def getCenter(self):
        """Returns the center of the word tile."""
        return self._center
        
    def getValue(self):
        """Gets the letter's value."""
        return self._value 
    
    def activate(self):
        """Activates the word tile."""
        self._active = True
        self._back.setBorderColor('green')
     
    def deactivate(self):
        """Deactivates the word tile."""
        self._active = False
        self._back.setBorderColor('black')
        
    def getActivity(self):
        """See if the tile is active or not."""
        return self._active
    
    def handleMouseRelease(self, event):
        """The following things happen."""
        if not self._active:
            return
        else:
            self._board.wordTileReport(self)
            
   
class WordRack:
    """This creates a rack that contains the unplaced words."""
    def __init__(self, board, kind, win):
        self._kind = kind
        # it now changes to a nested list, with each sublist the word object
        # first, and its index (may be the fixed position in the list!
        self._wordRack = []
        self._removedWordsIndices = []
        self._board = board
        self._homesForTiles = []
        #self._wordRack is a list of pseudo-graphical objects wordTile.
        if self._kind == 0:
            self._bigWordBag = WordBag(self, 'yellow', self._board)
            self._wordbaglist = self._bigWordBag.getWordBag()
            for i in range(6):
                self._wordRack.append([self._wordbaglist[0], i])
                self._wordbaglist = self._wordbaglist[1 :]
            for i in range(6):
                self._wordRack[i][0].addTo(win)
                self._wordRack[i][0].moveTo(50 + i * 20, 50)
                self._homesForTiles.append((50 + i * 20, 50))
        if self._kind == 1:
            self._bigWordBag = WordBag(self, 'violet', self._board)
            self._wordbaglist = self._bigWordBag.getWordBag()
            for i in range(6):
                self._wordRack.append([self._wordbaglist[0], i])
                self._wordbaglist = self._wordbaglist[1 :]
            for i in range(6):
                self._wordRack[i][0].addTo(win)
                self._wordRack[i][0].moveTo(50 + i * 20, 550)
                self._homesForTiles.append((50 + i * 20, 550))
        self._empty = False
        self._win = win
        #self.addNewTilesTo(self._win)
    
    def getRemovedWordsIndices(self):
        """Gets the removed words' indices."""
        return self._removedWordsIndices
        
    def getKind(self):
        """Gets the kind of itself."""
        return self._kind
        
    def getWordBag(self):
        """For debugging."""
        return self._wordbaglist
    
    def getWordRack(self):
        """For debugging."""
        return self._wordRack
    
    def wordsRemove(self, word):
        """To remove the word from the wordBag."""
        for i in range(len(self._wordRack)):
            if self._wordRack[i][0] == word:
                self._removedWordsIndices.append(self._wordRack[i])
    
    def getHomes(self):
        """Returns the homeList for the tiles."""
        return self._homesForTiles
        
    def insertTiles(self):
        """Inserts tiles to the empty postions on the word rack."""
        newWordTiles = []
        for j in range(len(self._removedWordsIndices)):
            newWordTiles.append([self._wordbaglist[0],
                                 self._removedWordsIndices[j][1]])
            self._wordbaglist = self._wordbaglist[1 :]
        self._wordRack.extend(newWordTiles)    
        self._wordRack = sorted(self._wordRack, key=getKey)
        self._removedWordsIndices = []
        
    def isEmpty(self):
        """Returns true when it is empty."""
        if self._wordRack == []:
            self._empty = True
    
    def activateAll(self):
        """Activates all the words in the wordbag."""
        for each in self._wordRack:
            each[0].activate()
        
    def deactivateAll(self):
        """Deactivates all the words in the wordbag."""
        for each in self._wordRack:
            each[0].deactivate()
    
    def haveFun(self, lst):
        """hahahaha!"""
        self._wordbaglist.extend(lst)
        
    def wordBagisEmpty(self):
        """Returns True if the word bag is empty"""
        return self._wordbaglist == []
    
def getKey(item):
    """This is a function only for sorting."""
    return item[1]
    
def getKey0(item):
    """Also a function only for sorting."""
    return item[0]
        
class WordBag:
    """This is a class that creates the wordBags for players."""
    def __init__(self, wordRack, color, board):
        """set up all the attributes."""
        # The tuples in the follwing nested lists contains the letter and the
        # score of the letter.
        listOfLetters = [[[('E', 12), ('A', 9), ('I', 9), ('O', 8), ('N', 6),
                           ('R', 6), ('T', 6), ('L', 4), ('S', 4), ('U', 4)],
                          1],
                         [[('D', 4), ('G', 3)], 2],
                         [[('B', 2), ('C', 2), ('M', 2), ('P', 2)], 3],
                         [[('F', 2), ('H', 2), ('V', 2), ('W', 2), ('Y', 2)],
                          4],
                         [[('K', 1)], 5],
                         [[('J', 1), ('X', 1)], 8],
                         [[('Q', 1), ('Z', 1)], 10]]
        self._board = board
        self._wordRack = wordRack
        self._wordBag = []
        for valueSet in listOfLetters:
            letterAndNumber = valueSet[0]
            value = valueSet[1]
            for eachTuple in letterAndNumber:
                for _ in range(eachTuple[1]):
                    letterTile = Words(self._board, self, eachTuple[0], 
                                       color, value)
                    self._wordBag.append(letterTile)
        # In each round there are only 6 tiles displayed.            
        self.shuffle()
        
    def getWordBag(self):
        """Gets the wordBag."""
        return self._wordBag
        
    def shuffle(self):
        """Shuffles the wordBag."""
        random.shuffle(self._wordBag)
        return self._wordBag
    

class EndRoundButton(EventHandler):
    """The changeTurn Button."""
    def __init__(self, board, win, position, wordRack):
        """set up all the attributes."""
        EventHandler.__init__(self)
        self._endRoundButton = Rectangle(50, 20, position)
        self._endRoundButton.setFillColor('pink')
        self._endRoundButton.addHandler(self)
        self._text = Text("End Turn")
        win.add(self._endRoundButton)
        win.add(self._text)
        self._text.moveTo(position)
        self._board = board
        self._wordRack = wordRack
    
    def handleMouseRelease(self, event):
        """Reports to the board as the mouse clicks on the object."""
        # The controller reports to the board so that objects in Board can
        # be called.
        self._board.report(self, event)
    
    def handleMousePress(self, event):
        """When it is pressed."""
        self._board.reportButtonPressed(self)
    
    def setFillColor(self, color):
        """This sets the color of the button."""
        self._endRoundButton.setFillColor(color)
    
    def restoreColor(self):
        """It restores the color of the button."""
        self._endRoundButton.setFillColor('pink')

class GoBackButton(EventHandler):
    """This is the button that can help you go back."""
    def __init__(self, board, win, position):
        EventHandler.__init__(self)
        self._button = Rectangle(50, 20, position)
        self._button.addHandler(self)
        self._button.setFillColor('red')
        self._text = Text('Go Back', position)
        win.add(self._button)
        win.add(self._text)
        self._board = board
    
    def handleMouseRelease(self, event):
        """When it is clicked, it reports to the board."""
        self._board.goBack(self)


class Board:
    """This is the class of the interface between the player 
       and the computer."""
    def __init__(self, win):
        """Set up and initialize the important attributes."""
        self._win = win
        self._grid = []
        self._lastWordLastTime = None
        self._lastWordThisTime = None
        print("self._grid")
        #Nested list with each first sublist as [Word, letter, wordValue, 
        #                                        spaceLocation, spaceValue
        #                                        kind]
        self._scoreCurrentTurn = 0
        self._scoreSum0 = 0
        self._scoreSum1 = 0
        self._score0 = Text('Total Score of player 0: ' + str(self._scoreSum0))
        self._score1 = Text('Total Score of player 1: ' + str(self._scoreSum1))
        win.add(self._score0)
        win.add(self._score1)
        self._score0.moveTo((75, 25))
        self._score1.moveTo((75, 575))
        self._vocabThisTurn = []
        self._history = []
        self._hint = Text('Welcome To scrabble!')
        win.add(self._hint)
        self._hint.moveTo((300, 590))
        self._boardSpaceMoved = None
        self._wordClicked = None
        self._goBackBarrier = None
        self._wordsRemovedEachTurn = []
        # Two endRoundButton, each controls one wordbag.
        # Two wordBags
        self._wordRacks = [WordRack(self, 0, win), 
                           WordRack(self, 1, win)]
        self._current = 1
        self._homeIndex = []
        print(self._wordRacks[self._current])
        wordRack = self._wordRacks[self._current]
        self._goBackButton = GoBackButton(self, win, (550, 280))
        self._endRoundButton = EndRoundButton(self, win, (550, 320), wordRack)
        self._board = []
        for r in range(15):
            thisRow = []
            for c in range(15):
                eachTile = BoardSpace(self, 
                                      (130 + 20 + r * 20, 130 + 20 + c * 20),
                                      '#eee4d7')
                thisRow.append(eachTile)
            self._board.append(thisRow)
        # The important tiles 
        self._redTiles = [(0, 0), (0, 7), (0, 14),
                          (7, 0), (7, 14),
                          (14, 0), (14, 7), (14, 14)]
        self._pinkTiles = [(1, 1), (2, 2), (3, 3), (4, 4), (10, 10), (11, 11), 
                           (12, 12), (13, 13), (13, 1), (12, 2), 
                           (11, 3), (10, 4), (7, 7), (4, 10), (3, 11), 
                           (2, 12), (1, 13)]
        self._darkBlueTiles = [(1, 5), (1, 9), (5, 5), (5, 9),
                               (9, 5), (9, 9), (13, 5), (13, 9),
                               (9, 13), (5, 13), (5, 1), (9, 1)]
        self._skyBlueTiles = [(0, 3), (0, 11),
                              (2, 6), (2, 8),
                              (3, 0), (3, 7), (3, 14),
                              (6, 2), (6, 6), (6, 8), (6, 12),
                              (7, 3), (7, 11),
                              (8, 2), (8, 6), (8, 8), (8, 12),
                              (11, 0), (11, 7), (11, 14),
                              (12, 6), (12, 8),
                              (14, 3), (14, 11)]
        for i in range(15):
            for j in range(15):
                self._board[i][j].addTo(win)
        self._addSpecial()
        self._board[7][7].activate()
        self.changeTurn()
        self._redTiles1 = [self._redTiles, [(3, 1)]]
        self._pinkTiles1 = [self._pinkTiles, [(2, 1)]]
        self._darkBlueTiles1 = [self._darkBlueTiles, [(3, 0)]]
        self._skyBlueTiles1 = [self._skyBlueTiles, [(2, 0)]]
        self._colorWithValue = [self._redTiles1, self._pinkTiles1,
                                self._darkBlueTiles1, self._skyBlueTiles1]
        
    def _addSpecial(self):
        """This private method adds all special tiles on the board."""
        #red tiles
        for each in self._redTiles:
            self._board[each[0]][each[1]].setFillColor('#ff4d4d')
        #pink tiles
        for each in self._pinkTiles:
            self._board[each[0]][each[1]].setFillColor('#ffb4b4')
        #dark blue tiles 
        for each in self._darkBlueTiles:
            self._board[each[0]][each[1]].setFillColor('#005bb5')
        #sky blue tiles
        for each in self._skyBlueTiles:
            self._board[each[0]][each[1]].setFillColor('#4fc4ff')
    
    def reportButtonPressed(self, endRoundButton):
        """When the button is pressed, it shortly turns to red."""
        self._endRoundButton.setFillColor('green')
    
    def wordTileReport(self, word):
        """This reports the word clicked."""
        self._wordClicked = word
    
    def failToAddTiles(self, boardSpace):
        """IF the first tile is not added to the center of the board."""
        if self._history == []:
            self._hint.setText('Please place your tile at the center of\
                                the board.')
        else:
            self._hint.setText('You cannot add any tile there!')

    def reportBoardSpaceMove(self, boardSpace, event):
        """This function reports when the mouse is on the top of each 
           boardSpace."""
        onto = boardSpace.getOnto()
        x, y = boardSpace.getCenter()
        x1, y1 = (x - 130) // 20 - 1, (y - 130) // 20 - 1
        self._boardSpaceMoved = (x1, y1)
        if onto:
            self._board[x1][y1].setBorderColor('red')
        if not onto:
            self._board[x1][y1].restoreBorder()
            
    def reportBoardSpaceClick(self, boardSpace, event):
        """This function reports as the boardSpace is becomes clicked."""
        if self._wordClicked is None:
            return
        wordActive = self._wordClicked.getActivity()
        if not wordActive:
            return
        else:
            x_0, y_0 = self._wordClicked.getCenter()
            #if self.wordRacks[self._current].getKind() == 0:
            self._homeIndex.append((x_0 - 50) / 20)
            
            #if self.wordRacks[self._current].getKind() == 1:
            x, y = self._boardSpaceMoved
            
            posx, posy = 130 + x * 20 + 20, 130 + y * 20 + 20
            self._wordClicked.moveTo(posx, posy)
            if x < 14 and x > 0 and y < 14 and y > 0:
                self._board[x - 1][y].activate()
                self._board[x][y - 1].activate()
                self._board[x][y + 1].activate()
                self._board[x + 1][y].activate()
            
            if x == 14 and y < 14 and y > 0:
                self._board[x - 1][y].activate()
                self._board[x][y - 1].activate()
                self._board[x][y + 1].activate()
            
            if x == 0 and y < 14 and y > 0:
                self._board[x + 1][y].activate()
                self._board[x][y - 1].activate()
                self._board[x][y + 1].activate()
                
            if y == 14 and x < 14 and x > 0:
                self._board[x - 1][y].activate()
                self._board[x][y - 1].activate()
                self._board[x + 1][y].activate()
                
            if y == 0 and x < 14 and x > 0:
                self._board[x - 1][y].activate()
                self._board[x][y + 1].activate()
                self._board[x + 1][y].activate()
                
            letter = self._wordClicked.getLetter()
            value = self._wordClicked.getValue()
            self._history.append([self._wordClicked, letter, value, (x, y)])
            #boardSpaceValue: (x, y): x is the scalar,
            #                         y = 0: score = x * letterValue
            #                         y = 1: score = x * wordValue
            for i in range(len(self._colorWithValue)):
                for each in self._colorWithValue[i][0]:
                    if each == (x, y):
                        spaceValue = self._colorWithValue[i][1]
                        break
            self._history[-1].append(spaceValue)
            self._wordClicked.deactivate()
            self._wordsRemovedEachTurn.append(self._wordClicked)
            self._hint.setText('Good move! Now please place another tile\
                                or end your turn if there is no tile to\
                                place.')
            self._lastWordThisTime = self._history[-1]
    
    def addNewTilesTo(self, win):
        """This adds New Tiles to the window after the endRoundButton is 
           clicked."""
        if self._lastWordThisTime is None:
            x = input("No move detected. Enter '0' for replacing all the\
                       current tiles to a new set. Enter '1' to continue.")
            if x == '0':
                x = self._wordRacks[self._current].getRemovedWordsIndices()
                for each in self._wordRacks[self._current].getWordRack():
                    self._wordsRemovedEachTurn.append(each)
                    x.append(each)
                self._wordRacks[self._current].haveFun(x)
     
        for each in self._wordsRemovedEachTurn:
            self._wordRacks[self._current].wordsRemove(each)
        wordRack = self._wordRacks[self._current].getWordRack()
        removedWordsIndices = self._wordRacks[self._current]\
                              .getRemovedWordsIndices()
        #print(removedWordsIndices)
        kind = self._wordRacks[self._current].getKind()
        #for each in wordRack:
            #each.removeFrom(win)
        for each in removedWordsIndices:
            for item in wordRack:
                if item == each:
                    wordRack.remove(item)
        self._wordRacks[self._current].insertTiles()
        for i in range(6):
            wordRack[i][0].addTo(win)
            if kind == 0:
                wordRack[i][0].moveTo(50 + i * 20, 50)
            else:
                wordRack[i][0].moveTo(50 + i * 20, 550)
            
    def report(self, endRoundButton, event):
        """This this the report function when the endRound Button is hit."""
        endRoundButton.restoreColor()
        self.addNewTilesTo(self._win)
        self._wordsRemovedEachTurn = []
        self.changeTurn()
     
    def goBack(self, goBackButton):
        """This is what the goBack Button does."""
        if self._history == [] or self._history[-1] == self._goBackBarrier:
            self._hint.setText('You cannot go further back than this!')
        else:
            word = self._history[-1][0]
            word.activate()
            lstOfHomes = self._wordRacks[self._current].getHomes()
            x, y = lstOfHomes[self._homeIndex[-1]]
            word.moveTo(x, y)
            self._history.pop(-1) 
            self._homeIndex.pop(-1)
    
    def calculateScore(self):
        """Calculate the score of the current player, called only after the 
           changeTurn button is clicked."""
        if self._history != []:
            self.makeBlankGrid()
            for i in range(len(self._history)):
                x, y = self._history[i][3]   #boardSpace clicked on
                self._grid[y][x] = self._history[i][1]
                
            if self._lastWordLastTime != None:
                firstIndex = self._history.index(self._lastWordLastTime)
                secondIndex = self._history.index(self._lastWordThisTime)
            else: 
                firstIndex = -1
                secondIndex = self._history.index(self._lastWordThisTime)
            historyOfTheTurn = self._history[firstIndex + 1: secondIndex + 1]
            
            wordsLocation = []
            for i in range(len(historyOfTheTurn)):
                wordsLocation.append(historyOfTheTurn[i][3])
            
            wordsLocation = sorted(wordsLocation)
            findingOnGrid = findLetters(self._grid)
            print('the Words and locations on the grid is =', findingOnGrid)
            print('words locations this turn =', wordsLocation)
            
            missingTiles = []
            if len(wordsLocation) == 1:
                x, y = wordsLocation[0]
                for each in findingOnGrid:
                    if (x, y + 1) == each[1]:
                        missingTiles.append((x, y + 1))
                    if (x + 1, y) == each[1]:
                        missingTiles.append((x + 1, y))
                    if (x, y - 1) == each[1]:
                        missingTiles.append((x, y - 1))
                    if (x - 1, y) == each[1]:
                        missingTiles.append((x - 1, y))
            ###############################################
                    
            else:
                if goingRight(wordsLocation):
                    distance = wordsLocation[-1][0] - wordsLocation[0][0]
                    for i in range(distance + 2):
                        missingTiles.append((wordsLocation[0][0] + i, \
                                            wordsLocation[0][1]))
                    missingTiles.insert(0, (wordsLocation[0][0] - 1, \
                                            wordsLocation[0][1]))
                else:
                    wordsLocation = sorted(wordsLocation, key=getKey)
                    distance = wordsLocation[-1][1] - wordsLocation[0][1]
                    for i in range(distance + 2):
                        missingTiles.append((wordsLocation[0][0], \
                                            wordsLocation[0][1] + i,))
                    missingTiles.insert(0, (wordsLocation[0][0], \
                                            wordsLocation[0][1] - 1))
                
                print('The complete words should look like:', missingTiles)
            
            for each in missingTiles:
                for every in self._history:
                    if each == every[3]:
                        self._vocabThisTurn.append(every)
            
            print('So this is what we use to calculate the score: ', \
                  self._vocabThisTurn)
            
            if self._vocabThisTurn != []:
                isWord = self.isAWord()
                print('Test for isAWord:', isWord)
                if isWord:
                    for each in self._vocabThisTurn:
                        each[0].setBorderColor('blue')
                    self.calculateSmallerScore()
                    print('the current score is: ', self._scoreCurrentTurn)
                else:
                    self._hint.setText("This is not a 'word'! \
                                        No score will be added")
                        
            if self._current == 0:
                self._scoreSum1 += self._scoreCurrentTurn
            else:
                self._scoreSum0 += self._scoreCurrentTurn
            
            self._score0.setText('Total Score of player 0: ' +\
                                  str(self._scoreSum0))
            self._score1.setText('Total Score of player 1: ' +\
                                str(self._scoreSum1))
            
            print('***********************************************************')
            self._lastWordLastTime = self._lastWordThisTime
            self._lastWordThisTime = None
            #printGrid(self._grid)
        else:
            return
        
    def calculateSmallerScore(self):
        ######################
        """This is a subfunction of the last function."""
        scalar0 = 1
        scalar1 = 1
        for each in self._vocabThisTurn:
            if each[-1] == [(3, 1)]:
                self._scoreCurrentTurn += each[2]
                scalar = 3
            elif each[-1] == [(2, 1)]:
                self._scoreCurrentTurn += each[2]
                scalar1 = 2
            elif each[-1] == [(3, 0)]:
                self._scoreCurrentTurn += each[2] * 3
            elif each[-1] == [(2, 0)]:
                self._scoreCurrentTurn += each[2] * 2
            elif each[-1] is None:
                self._scoreCurrentTurn += each[2]
        self._scoreCurrentTurn = self._scoreCurrentTurn * scalar0 * scalar1
    
    def isAWord(self):
        """This returns True if the vocabThisTurn is a word."""
        aListOfLetters = []
        for each in self._vocabThisTurn:
            aListOfLetters.append(each[1])
        return wordFind(aListOfLetters)
    
                
    def changeTurn(self):
        """Changes turn when it is called."""
        self._wordRacks[self._current].deactivateAll()
        self._current += 1
        self._current %= 2
        #if self._current == 1:
            #self._wordRacks[self._current].activateAll()
        #else:
        self._wordRacks[self._current].activateAll()
        self.calculateScore()
        if self._history != []:
            self._goBackBarrier = self._history[-1]
        
        print('__________________________________________________________')
        self._vocabThisTurn = []
        self._scoreCurrentTurn = 0
        if not self._wordRacks[self._current].wordBagisEmpty():
            pass
        else:
            x = max(self._scoreSum0, self._scoreSum1)
            if x == self._scoreSum0:
                self._hint.setText('Congratulations!!!!!, player 0 wins!!!!!')
            if x == self._scoreSum1:
                self._hint.setText('Congratulations!!!!!, player 1 wins!!!!!')
        #For debugging 
        #t = []
        #for each in (self._wordRacks[self._current]).getWordRack():
            #t.append(each.getLetter())
        #print(t)
        
        #x = (self._wordRacks[self._current]).getWordBag()
        #y = []
        #for each in x:
            #y.append(each.getLetter())
        #print(y)
        
    def makeBlankGrid(self):
        """Makes a blank grid."""
        grid = []
        for i in range(15):
            grid.append([])
            for j in range(15):
                grid[-1].append('_')
        self._grid = grid

            
def printGrid(grid):
    """Only prints the grid (self._grid) in a prettier format."""
    numRows = len(grid)  
    numCols = len(grid[0]) 
    for r in range(numRows):
        for c in range(numCols):
            print(grid[r][c], end=' ')
        print()


def goingRight(tupleList):
    """Takes in a list of tuples and return True if it has a trend of going
       right."""
    return tupleList[0][0] < tupleList[1][0]
            

def findLetters(grid):
    """Find every letter that is on the grid. Returns a list of letters and
       their positions. """
    words = []
    j = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != '_':
                words.append([grid[i][j], (j, i)])
    return words

def wordFind(lstOfLetters):
    """The function that returns True if words that are in the 'words' file """
    vowels = ['A', 'E', 'I', 'O', 'U']
    consonants = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', \
                  'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
    letterType = [consonants, vowels]
    startValue = 0
    #0: true 
    #1: false
    lstOfTruthValues = []
    if lstOfLetters[0] in letterType[startValue]:
        for i in range(1, len(lstOfLetters)):
            value = (startValue + i) % 2
            if lstOfLetters[i] in letterType[value]:
                lstOfTruthValues.append(0)
            else:
                lstOfTruthValues.append(1)
    else:
        for i in range(1, len(lstOfLetters)):
            value = (startValue + i + 1) % 2
            if lstOfLetters[i] in letterType[value]:
                lstOfTruthValues.append(0)
            else:
                lstOfTruthValues.append(1)
    
    print('the List of Truth Values: ', lstOfTruthValues)            
    for each in lstOfTruthValues:
        if each != 0:
            return False
    return True

def main(win):
    """The main function."""
    Board(win)


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

StartGraphicsSystem(main, WINDOW_WIDTH, WINDOW_HEIGHT)
