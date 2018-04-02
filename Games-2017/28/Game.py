"""
*****************************************************************************
FILE: Game.py

AUTHOR: Olivia Maddox

PARTNER: N/A

ASSIGNMENT: Project 6

DATE: 04/07/17

DESCRIPTION: This program builds a Hamilton-themed Monopoly game. It involves
graphics and several classes including a die, a deck, a set of Chance cards,
players, pawns, board spaces and a game board. The board is the game's manager
and controls the ending of the game. The game ends when a player runs out of
money, making the winner the player who has money left over. 

*****************************************************************************
"""
import random
from cs110graphics import *

class Die(EventHandler):
    """ Create a six-sided die """
    
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
        
                 
    def __init__(self, board, width=25, center=(291, 291), bgcolor='white', 
                 fgcolor='black'):
        # Make die the event handler
        EventHandler.__init__(self)
        
        # Initialize die attributes for creating die"
        self._value = 1
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgcolor)
        self._square.setDepth(20)
        self._center = center
        self._active = True
        self._board = board
        self._width = width
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgcolor)
            pip.addHandler(self)
            pip.setDepth(20)
            self._pips.append(pip)
        self._square.addHandler(self)

    
    def addTo(self, win):
        """Add die and pips to window""" 
        
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)
        
        
    def roll(self):
        """ Change the die's current value to a random number between 1 and 6"""
        
        if not self._active:
            return
        self._value = random.randrange(Die.SIDES) + 1
        self._active = False
        self._update()
    
    
    def getValue(self):
        """ Return this die's current value """
        
        return self._value
      
        
    def _update(self):
        """ Private method. Make the appearance of the die match the die's 
        value """
        
        positions = Die.POSITIONS[self._value]
        cx, cy = self._center
        for i in range(len(positions)):
            if positions[i] is None:
                self._pips[i].setDepth(25)
            else:
                self._pips[i].setDepth(15)
                dx, dy = positions[i]
                self._pips[i].moveTo((cx + dx * self._width,
                                      cy + dy * self._width))
                        
                                      
    def deactivate(self):
        """ Deactivate die """
        
        self._active = False
    
    
    def activate(self):
        """ Activate die """
        
        self._active = True
    
    
    def handleMouseRelease(self, event):
        """ When die is clicked, roll and report to board """
        
        self.roll()
        self._board.reportDieRoll()
        
        

class Deck:
    """A class for building a deck of cards. This class is not graphical"""
    
    def __init__(self, win, board):
        """Creates a deck of 9 Chance cards."""
        
        # Initializes deck list
        self._board = board
        self._deck = []
        self._discard = []
        
        # Sets deck activity to false 
        self._deckActive = False
        
        # Lists out possible card numbers
        nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        
        # Adds each card to the deck
        for num in nums:
            card = Card(num, num + ".png", "back.png", self)
            self._deck.append(card)
        
        # Adds each card to the window
        for c in self._deck:
            c.addTo(win)
            
                    
    def empty(self):
        """Returns True if the deck no longer contains any cards. Otherwise
        false is returned."""
        
        # Returns Boolean statement if length of deck is 0 
        return len(self._deck) == 0
    
    
    def deal(self):
        """Deals a card. A card is removed from the top of the deck and
        returned."""
        
        # CITE: Tucker Ward
        # DETAILS: The function "pop" removes a list's last item and returns it
        card = self._deck.pop()
        self._discard.append(card)
        return card
    
    
    def shuffle(self):
        """All cards currently in the deck are randomly ordered. """
        
        # Initializes a new deck for shuffled cards
        shuffled = []
        
        # Appends cards from a random position in the deck to shuffled deck
        for _ in range(9):
            shuffled.append(self._deck.pop(random.randrange(len(self._deck))))
        
        # Sets the deck equal to the shuffled deck
        self._deck = shuffled
    
        
    def activateChance(self):
        """ Activate chance cards """
        
        self._deckActive = True
        
        
    def deactivateChance(self):
        """ Deactivate chance cards """
        
        self._deckActive = False
        
        
    def getDeckActive(self):
        """ Return bool statement regarding deck activity """
        
        return self._deckActive
        
        
    def executeChanceCard(self, num):
        """ Send message to board to execute chance card """
        
        self._board.executeChanceCard(num)
        
        
    
class Card(EventHandler):
    """A class used for building graphical Chance cards"""
    
    def __init__(self, num, faceFileName, backFileName, deck):
        """Creates a Chance card with the given number."""
        
        # Set up Card as the EventHandler
        EventHandler.__init__(self)
        
        # Initialize attributes
        self._deck = deck
        self._num = num
        
        # Create image objects for card sides
        faceurl = "https://cs.hamilton.edu/~omaddox/images/" + faceFileName
        self._face = Image(faceurl, (600, 590), width=114, height=160)
        backurl = "https://cs.hamilton.edu/~omaddox/images/" + backFileName
        self._back = Image(backurl, (600, 590), width=114, height=160)
        self._back.addHandler(self)
        
        # Rotate card front and back
        self._face.rotate(45)
        self._back.rotate(45)
        
        # Assign card attributes
        self._depth = 10
        self._size = (150, 210)
        self._center = (650, 600)
        
        # List card sides and set which one is showing
        self._sides = [self._back, self._face]
        self._show = 0
        
        
    def addTo(self, win):
        """Add the card to the given graphics window."""
        
        win.add(self._face)
        win.add(self._back)
    
    
    def removeFrom(self, win):
        """Remove the card from the given graphics window. """
        
        win.remove(self._face)
        win.remove(self._face)
    
    
    def flip(self):
        """Flip the card over. This visually flips the card over as well."""
        
        # Switch card side to faced up or down. Update card.
        self._show = (self._show + 1) % 2
        self._update()


    def move(self, dx, dy):
        """Move a card by dx and dy."""
        
        self._face.move(dx, dy)
        self._back.move(dx, dy)
        
        
    def setDepth(self, depth):
        """Set the depth of graphical objects representing the card to depth"""
        
        self._depth = depth
        self._update()
        
        
    def handleMouseRelease(self, event):
        """Handle mouse release event from the button"""
        
        # Deal card, flip card and move it to pile if deck isn't empty
        if self._deck.empty() != True:
            card = self._deck.deal()
            card.flip()
            card.move(90, 0)
            
            # Send card num to the deck to execute chance card
            if self._deck.getDeckActive() is True:
                self._deck.executeChanceCard(card.getNum())
            
            
    def _update(self):
        """Recieve calls from other functions, and adjust image depths to
        represent which card side should be showing"""
        
        # Locate the correct side from card sides list and adjust the depth
        for i in range(len(self._sides)):
            if i == self._show:
                self._sides[i].setDepth(self._depth)
            else:
                self._sides[i].setDepth(self._depth + 1)
                
                
    def getNum(self):
        """ Returns num value """
        
        return self._num
 
      
        
class Player:
    """ A class used the players in the game  """
    
    def __init__(self, board, player, value):
        self._board = board
        self._player = player
        self._money = value
        self._props = []
        colors = ["black", "white"]
        self._color = colors[player]
        
        # Create pawn piece for corresponding player
        self._pawn = Pawn(self._board, self._color, self._player)
        
        # Create text to display each player's money
        self._monText = Text(("Player {} money left: ${}".
                              format(self._player + 1, self._money)),
                             (1000, 30 + player * 225), 14)
        
        # Create text to display each player's properties
        self._propText = Text(("Properties: {}".format(self._props)),
                              (1000, 50 + player * 225), 14)
        
        # Create color indicator to match player with its pawn color
        self._tellColor = Rectangle(30, 30, (1130, 20 + player * 225))
        self._tellColor.setFillColor(self._color)
        
        # Initialize jail statements as false
        self._isInJail = False
        self._isJustFreed = False
        
        
    def addTo(self, win):
        """ Add pawn, money text and color indicator to window """
        
        self._pawn.addTo(win)
        win.add(self._monText)
        win.add(self._propText)
        win.add(self._tellColor)
        
        
    def moveTo(self, position):
        """ Move pawn to given position """
         
        self._pawn.moveTo(position) 
    
    
    def setPosition(self, pos):
        """ Set pawn position to given position """
        
        self._pawn.setPosition(pos)
        
        
    def addMoney(self, value):
        """ Add money to current value """
        
        self._money += value
        self._monText.setTextString("Player {} money left: ${}".
                                    format(self._player + 1, self._money))
        
        
    def loseMoney(self, value):        
        """ Subtract money from current value """

        self._money -= value
        self._monText.setTextString("Player {} money left: ${}".
                                    format(self._player + 1, self._money))
        
        # If player's money is less than or equal to 0, game ends and they lose
        if self._money <= 0:
            self._board.gameOver()
        
        
    def propOwn(self, prop):
        """ method docstring """
        
        for prp in self._props:
            if prp == prop:
                return True
        return False
           

    def addProperty(self, prop):
        """ Append property to player's property list """
        
        self._props.append(prop)
        self._propText.setTextString(("Properties: {}".format(self._props)))
     
    
    def getPawn(self):
        """ Return pawn """
        
        return self._pawn
        
        
    def activate(self):
        """ Activate pawn to allow moving """
        
        self._pawn.activate()
        
        
    def deactivate(self):
        """ Deactivate pawn to prohibit moving """
        
        self._pawn.deactivate()
        
    
    def passedGo(self):
        """ Add 200 when player has passed Go """
            
        self.addMoney(200)
        
        
    def goToJail(self):
        """ Player is sent to jail """
        
        self._board.goToJail()
        
        
    def setJustFreed(self, val):
        """ Set value to either true or false """
        
        self._isJustFreed = val
        
        
    def getJustFreed(self):
        """ Return bool statement regarding player's release from jail """
        
        return self._isJustFreed
    
    
    def getPosition(self):
        """ Return pawn position """
        
        return self._pawn.getPosition()
        
        
    def isInJail(self):
        """ Return bool statement of whether player is in jail or not """
        
        return self._isInJail
        
    
    def stuckInJail(self):
        """ Player is stuck in jail. Returns true. """
        
        self._isInJail = True
        
        
    def outOfJail(self):
        """ Player is out of jail. Returns false. """
        
        self._isInJail = False
        
        
    def getMoney(self):
        """ Return a player's money"""
        
        return self._money
        
        
    
class Pawn(EventHandler):
    """ A class dedicated to each player's pawn """
    
    def __init__(self, board, color, ident):
        # Set pawn as event handler
        EventHandler.__init__(self)
        
        # Initialize attributes
        self._color = color
        self._board = board
        
        # Set identifying number for this pawn
        self._ident = ident   
        
        # Establish current logical position on the board
        self._position = 0    
        
        # Create pawn
        self._square = Rectangle(30, 30, (829, 824))
        self._square.setFillColor(color)
        self._square.addHandler(self)
        
        # Set pawn to inactive
        self._pawnActive = False

    
    def activate(self):
        """ Set pawn to active. Create a green thick border to show activity."""

        self._pawnActive = True
        self._square.setBorderColor('green')
        self._square.setBorderWidth(5)
        
        
    def deactivate(self):
        """Set pawn to inactive. Create a black border to show inactivity """

        self._pawnActive = False
        self._square.setBorderColor('black')
        self._square.setBorderWidth(1)
        
        
    def handleMouseRelease(self, event):
        """ Tell board that the active pawn was clicked """

        if not self._pawnActive:
            return
        self._board.reportPawnClick(self._ident)


    def addTo(self, win):
        """ Add pawn piece to window """
        
        win.add(self._square)
    
    
    def getPosition(self):
        """ Return pawn position """

        return self._position
    
    
    def moveTo(self, position):
        """ Move pawn to given position """
        
        self._square.moveTo(position)
    
    
    def setPosition(self, pos):
        """ Set pawn position to given position """
        
        self._position = pos


    def move(self, dx, dy):
        """ Move pawn by dx and dy """

        self._square.move(dx, dy)



class BoardSpace:
    """ A class dedicated to the spaces on the board and their corresponding 
    kind"""
    
    def __init__(self, board, center, kind):
        self._board = board
        self._center = center
        self._kind = kind
    
    
    def getCenter(self):
        """ Return the board space's center """
        
        return self._center
        
        
    def getKind(self):
        """ Return the board space's kind """
        
        return self._kind
    
    
    def implementAction(self):
        """ Implement action for the space's designated kind """
        
        # Chance:
        if self._kind == "Chance":
            self._board.activateChance()
        
        # Properties:       
        if self._kind == "Prop":
            self._board.landedOnProp(self._center)
            
        # Utilities:
        if self._kind == "Utility":
            self._board.landedOnProp(self._center)
        
        # Go:
        if self._kind == "Go":
            self._board.passedGo()
            self._board.changeTurn()
            
        # Tax:
        if self._kind == "Tax":
            self._board.taxes()
            
        # Free parking
        if self._kind == "Park":
            self._board.changeTurn()
        
        # Just visiting jail
        if self._kind == "Visit":
            self._board.changeTurn()
            
        # Go to jail
        if self._kind == "ToJail":
            self._board.goToJail()
            self._board.changeTurn()



class Board:
    """ This class is the game's controller site. Creates board spaces. Keeps
    track of pawn movement and changing turns. Implements actions from board
    space class. Controls game ending. """
    
    def __init__(self, win):
        # Set image as game board
        self._board = Image("https://cs.hamilton.edu/~omaddox/images/yes.png",
                            (585, 450), 1170, 900)
        
        # Add board and die to the window
        win.add(self._board)
        self._die = Die(self)
        self._die.addTo(win)
        self._win = win
        
        # Initialize pawn movement to false
        self._pawnMoved = False

        # Set up space positions and kinds
        self._positions = [((831, 832), "Go"), ((714, 876), "Prop"), 
                           ((625, 874), "Prop"), ((541, 871), "Chance"),
                           ((447, 873), "Prop"), ((357, 874), "Prop"),
                           ((272, 877), "Tax"), ((182, 878), "Prop"),
                           ((25, 872), "Visit"), ((24, 716), "Chance"),
                           ((21, 628), "Prop"), ((18, 535), "Prop"),
                           ((20, 448), "Utility"), ((20, 362), "Prop"),
                           ((20, 271), "Prop"), ((20, 187), "Prop"),
                           ((21, 62), "Park"), ((179, 23), "Prop"),
                           ((269, 20), "Prop"), ((360, 22), "Chance"),
                           ((446, 21), "Utility"), ((537, 16), "Prop"),
                           ((625, 21), "Utility"), ((712, 20), "Prop"),
                           ((869, 23), "ToJail"), ((873, 175), "Prop"),
                           ((873, 270), "Utility"), ((873, 354), "Prop"),
                           ((873, 445), "Prop"), ((874, 533), "Prop"),
                           ((873, 626), "Tax"), ((871, 716), "Prop"), 
                           ((86, 810), "Jail")]
           
        # Set up properties with price and statement if bought and center  
        self._props = [(1, "Bundy", 60, False, (714, 876)), 
                       (2, "Dunham", 60, False, (625, 874)), 
                       (4, "North", 100, False, (447, 873)),
                       (5, "South", 100, False, (357, 874)),
                       (7, "Wertimer", 120, False, (182, 878)),
                       (10, "Keehn", 140, False, (21, 628)),
                       (11, "Major", 140, False, (18, 535)),
                       (12, "McEwen", 200, False, (20, 448)),
                       (13, "Minor", 180, False, (20, 362)),
                       (14, "Babbitt", 180, False, (20, 271)),
                       (15, "Milbank", 200, False, (20, 187)),
                       (17, "Carnegie", 220, False, (179, 23)),
                       (18, "Macintosh", 220, False, (269, 20)),
                       (20, "Commons", 200, False, (446, 21)), 
                       (21, "Root", 260, False, (537, 16)), 
                       (22, "Diner", 200, False, (625, 21)),
                       (23, "Kirkland", 260, False, (712, 20)), 
                       (25, "Morris", 300, False, (873, 175)),
                       (26, "Opus", 200, False, (873, 270)),
                       (27, "Ferguson", 300, False, (873, 354)),
                       (28, "Rogers", 320, False, (873, 445)), 
                       (29, "Farmhouse", 350, False, (874, 533)),
                       (31, "Co-op", 400, False, (871, 716))]      
        
        # Set up property rent 
        self._rent = [(1, 10), (2, 10), (4, 17), (5, 17), (7, 20), (10, 23),
                      (11, 23), (12, 33), (13, 30), (14, 30), (15, 33), 
                      (17, 37), (18, 37), (20, 33), (21, 43), (22, 33), 
                      (23, 47), (25, 50), (26, 33), (27, 50), (28, 53), 
                      (29, 58), (31, 67)]

        # Set up board spaces
        self._spaces = []
        for i in range(len(self._positions)):
            space = BoardSpace(self, self._positions[i][0], 
                               self._positions[i][1])
            self._spaces.append(space)
                           
        # Set up players
        self._players = []
        for player in range(int(input("How many players? (1-2)"))):
            thisPlayer = Player(self, player, 1500)
            thisPlayer.addTo(win)
            self._players.append(thisPlayer)
        self._updatePawnLocations()
    
        # Set current player
        self._current = len(self._players) - 1
        self.changeTurn()
        
        # Create and shuffle deck
        self._deck = Deck(win, self)
        self._deck.shuffle()
       
        
    def reportPawnClick(self, ident):
        """ Report to board that current player has been clicked """
        
        if self._pawnMoved:
            return
        if ident == self._current:
            self._pawnMoved = True
            thePawn = self._players[ident].getPawn()
            pos = thePawn.getPosition()
            
            # If current player is in jail, change turns unless die value is 6
            if self._players[ident].isInJail():
                if self._die.getValue() != 6:
                    self.changeTurn()
                
                # If player in jail rolls a 6, they are released from jail
                else:
                    self._players[ident].outOfJail()
                    self.changeTurn()
                    self._players[ident].setJustFreed(True)
            
            # Current player is out of jail, value of freedom reinitializes 
            else:
                if self._players[ident].getJustFreed():
                    pos += 8
                    self._players[ident].setJustFreed(False)
                pos += self._die.getValue()
                
                # Call passed go
                if pos > (len(self._positions) - 1):
                    self.passedGo()
                
                # Create pathway for pawns around the board. 
                pos = pos % (len(self._positions) - 1)
                thePawn.setPosition(pos)
                self._updatePawnLocations()
                
                # Get player position to tell board space to implement action
                playerPos = self._players[self._current].getPosition()
                self._spaces[playerPos].implementAction()
            
    
    def landedOnProp(self, center):
        """ Player either has choice to buy if untaken, or has to pay rent if 
        taken """
        
        # Ask player if they want to buy untaken property
        if self.propTaken(center) is False:
            if input("Do you want to buy this property? Yes or No:") == "Yes":
                self.buyProperty()
            else:
                self.changeTurn()
        
        # Check if bought property is landed on by owner
        else:
            for i in range(len(self._props)):
                if self._props[i][4] == center:
                    # If true, change turn
                    if self._players[self._current].propOwn(self._props[i][1]):
                        self.changeTurn()
                    # if false, player pay rent
                    else:
                        self.payRent()
            
          
    def propTaken(self, center):
        """ Check whether the property has been bought or not """
        
        pos = 0
        for i in range(len(self._positions)):
            if self._positions[i][0] == center:
                pos = i
                
        # Return bool statement of whether property has been bought
        for j in range(len(self._props)):
            if self._props[j][0] == pos:
                return self._props[j][3]
            
        
    def buyProperty(self):
        """ Player buys property. Spends money and takes away availability """
        
        for i in range(len(self._props)):
            if self._props[i][0] == self._players[self._current].getPosition():
                
                # Player loses money when buying
                self._players[self._current].loseMoney(self._props[i][2])
                self._players[self._current].addProperty(self._props[i][1])
                
                # Change property availability from False to True
                self._props[i][3] = True
        self.changeTurn()
        
    
    def payRent(self):
        """ Player pays rent when landing on other player's properties """
        
        for i in range(len(self._rent)):
            if self._rent[i][0] == self._players[self._current].getPosition():
                
                # Gives owner money and loses own money
                self.givePlayMon(self._rent[i][1], self._players[self._current])
                self.changeTurn()
            

    def passedGo(self):
        """ Current player passes go """
        
        self._players[self._current].passedGo()
        
        
    def goToJail(self):
        """ Current player goes to jail """
        
        self._players[self._current].stuckInJail()
        self._players[self._current].setPosition(32)
        self._updatePawnLocations()
        self.changeTurn()
        
            
    def reportDieRoll(self):
        """ Reports whether the die has been rolled and pawn has moved """
        
        self._pawnMoved = False
    
    
    def changeTurn(self):
        """ Switch turn of players. Activate die."""
        
        # Deactivate current player and activate other player
        self._players[self._current].deactivate()
        self._current = (self._current + 1) % len(self._players)
        self._players[self._current].activate()
        self._die.activate()
    
                
    def givePlayMon(self, value, player):
        """ Give other player money, current player loses own money """
        
        if self._players[0] != player:
            self._players[0].addMoney(value)
            player.loseMoney(value)
        else:
            player.addMoney(value)
            self._players[0].loseMoney(value)
                
                
    def _updatePawnLocations(self):
        """ Move the two pawns to their correct locations on the window """
        
        offsets = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for i in range(len(self._players)):
            self._pawn = self._players[i].getPawn()
            pos = self._pawn.getPosition()
            self._pawn.moveTo(self._spaces[pos].getCenter())
            self._pawn.move(offsets[i][0] * 10, offsets[i][1] * 10)
    
    
    def taxes(self):
        """ Take money away from player and change turns"""
        
        self._players[self._current].loseMoney(200)
        self.changeTurn()
        
    
    def activateChance(self):
        """ Activate chance cards """
        
        self._deck.activateChance()

    
    def executeChanceCard(self, num):
        """ Execute the chance card and its each specific function"""
        
        if num == "1":
            # Pay each player $100
            self.givePlayMon(100, self._players[self._current])
            self.changeTurn()
            self._deck.deactivateChance()
        
        if num == "2":
            # Advance to go
            self._players[self._current].setPosition(0)
            self._updatePawnLocations()
            self.passedGo()
            self.changeTurn()
            self._deck.deactivateChance()
            
        if num == "3":
            # Go to jail
            self.goToJail()
            self._deck.deactivateChance()
            
        if num == "4":
            # Pay bank $150
            self._players[self._current].loseMoney(150)
            self.changeTurn()
            self._deck.deactivateChance()

        if num == "5":
            # Advance to free parking
            self._players[self._current].setPosition(16)
            self._updatePawnLocations()
            self.changeTurn()
            self._deck.deactivateChance()
            
        if num == "6":
            # Move back 3 spaces
            currentPos = self._players[self._current].getPosition()
            self._players[self._current].setPosition(currentPos - 3)
            self._updatePawnLocations()
            self.changeTurn()
            self._deck.deactivateChance()
            
        if num == "7":
            # Move forward 4 spaces
            currentPos = self._players[self._current].getPosition()
            self._players[self._current].setPosition(currentPos + 4)
            self._updatePawnLocations()
            self.changeTurn()
            self._deck.deactivateChance()
        
        if num == "8":
            # Collect $150
            self._players[self._current].addMoney(150)
            self.changeTurn()
            self._deck.deactivateChance()
            
        if num == "9":
            # Move to opus
            self._players[self._current].setPosition(26)
            self._updatePawnLocations()
            self.changeTurn()
            self._deck.deactivateChance()
            
            
    def gameOver(self):
        """ End game """
        
        # Deactivate players and die
        for i in range(len(self._players)):
            self._players[i].deactivate()
        self._die.deactivate()
        
        # Print and add game-over text to window
        gameOverText = Text("Game over!", (500, 230), 48)
        self._win.add(gameOverText)
        
        # Calculate winner
        for i in range(len(self._players)):
            if self._players[i].getMoney() > 0:
                winner = i + 1
        winnerText = Text("Player {} wins!".format(winner), (500, 270), 32)
        self._win.add(winnerText)


def play(win):
    """ function docstring """
    
    _ = Board(win)

StartGraphicsSystem(play, width=1170, height=900)
