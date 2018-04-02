"""
 *****************************************************************************
   FILE:           Game.py
   
   AUTHOR:         Michelle Chung
   
   PARTNER:        N/A
   
   ASSIGNMENT:     Project 6
   
   DATE:           04.07.17
   
   DESCRIPTION:    Allows user to play board game similar to Monopoly

 *****************************************************************************
"""
import random
from cs110graphics import *

WINDOW_HEIGHT = 900
WINDOW_WIDTH = 900

# Asks for how many total players and remembers each player's color piece
NUMPLAYERS = int(input("How many players would you like?"))
PLAYERIDENTITY = []
for numId in range(NUMPLAYERS):
    colorPlayer = str(input("What color for Player " + str(numId) + "?"))
    PLAYERIDENTITY.append((colorPlayer, numId, 1500))

class Die(EventHandler):
    """Creates a six-sided die that rolls"""
    
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
    DICE = 2
                  
    def __init__(self, board, width=25, center=(25, 25),
                 bgcolor='LightSteelBlue', fgcolor='DarkBlue'):
        """Establishes characteristics of a single die"""
        
        # Establishes that die will handle an event
        EventHandler.__init__(self)
        
        # Sets up characteristics of the die itself
        self._board = board
        self._value = 6
        self._square = Rectangle(width, width, center)
        self._square.setFillColor(bgcolor)
        self._square.setDepth(20)
        self._width = width
        self._center = center
        
        # Creates the individual pips that make up the value of the die
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(width / 15, center)
            pip.setFillColor(fgcolor)
            pip.setDepth(20)
            self._pips.append(pip)
        
        # Specifies square as the object that should handle event
        self._square.addHandler(self)
        self._totalPips()
        
        # Says that the die is active and ready to be used
        self._active = True
        
    def addTo(self, win):
        """Adds individual pips to square"""
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)
            
    def roll(self):
        """Changes value of die to random number between 1 and 6"""
        self._value = random.randrange(Die.SIDES) + 1
        self._totalPips()
        
    def getValue(self):
        """Returns current value of die"""
        return self._value
        
    def _totalPips(self):
        """Makes die's appearance match the value of roll"""
        
        # Sets up pips depending on the value of the roll
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
                
    def handleMouseRelease(self, event):
        """Establishes that click causes roll"""
        if self._active is True:
            self.roll()
            self.deactivate()
        
    def activate(self):
        """Activates who can use die"""
        self._active = True
        
    def deactivate(self):
        """Deactivates who can use die"""
        self._active = False

class BoardTile(EventHandler):
    """Creates a single board tile"""
    
    def __init__(self, board, center):
        """Establishes the characteristics of a single board tile"""
        
        # Establishes that tile will handle an event
        EventHandler.__init__(self)
        
        # Sets up characteristics of the tile itself
        self._board = board
        self._center = center
        self._square = Rectangle(10, 10, center)
        
    def addTo(self, win):
        """Adds individual tile"""
        win.add(self._square)
        
    def handleMouseRelease(self, event):
        pass
    
    def getCenter(self):
        """Gives center of the tile"""
        return self._center

class Pawn(EventHandler):
    """Creates single pawn"""
    
    def __init__(self, board, color, ident, money, position):
        """Establishes characteristics of a single pawn"""
        
        EventHandler.__init__(self)
        self._color = color
        self._board = board
        self._ident = ident
        self._money = money
        self._position = position
        self._square = Rectangle(10, 10, (759, 694))
        self._square.setFillColor(color)
        self._square.addHandler(self)
        
    def addTo(self, win):
        """Adds pawns to board"""
        win.add(self._square)
    
    def handleMouseRelease(self, event):
        """Notifies board that the pawn has been clicked"""
        self._board.reportPawnClick(self._ident)  # tell the board I was clicked
    
    def getPosition(self):
        """Returns position of pawn at that time"""
        return self._position
    
    def setPosition(self, pos):
        """Establishes position of pawn at that time"""
        self._position = pos
        
    def moveTo(self, location):
        """Moves pawn to a certain location"""
        self._square.moveTo(location)
        
    def move(self, dx, dy):
        """Moves pawn by certain amount"""
        self._square.move(dx, dy)

class Board(EventHandler):
    """Creates board with all necessary pieces and parts"""
    
    def __init__(self, win):
        """Establishes characteristics of the board"""

        # Adds dice to the board
        self._die = Die(self)
        self._die.addTo(win)
        
        # Adds cards to the board
        self._communityChest = CommunityChest(self)
        self._communityChest.addTo(win)
        self._chanceCard = ChanceCard(self)
        self._chanceCard.addTo(win)
        
        # Adds picture of board to board
        EventHandler.__init__(self)
        self._board = \
        Image("https://cs.hamilton.edu/~mchung/images/Monopoly_Board.png", \
              (450, 450), 800, 800)
        self._board.addHandler(self)
        win.add(self._board)
        
        # Centers of spaces on board; comments below match numbers above
        self._centers = [(759, 694), (683, 696), (627, 696), (569, 695),
                         # Go, Wertimer, Community Chest, Wallace Johnson 
                         (511, 693), (455, 693), (393, 693), (336, 689),
                         # Laundry, Bus, Major, Chance
                         (278, 693), (221, 696), (155, 698), (151, 620),
                         # Keehn, Opus 1, Campus Police, Kirner-Johnson
                         (152, 567), (150, 514), (148, 461), (148, 409),
                         # Bon Appetit, McEwen, Diner, Jitney
                         (148, 353), (147, 302), (145, 249), (147, 194),
                         # Sadove Center, Community Chest, Wellin, Commons
                         (149, 129), (223, 124), (282, 124), (339, 124),
                         # Free Parking, Dunham, Chance, South
                         (397, 124), (456, 124), (513, 125), (571, 124),
                         # North, Zip Car, Benedict Hall, CJ
                         (629, 132), (684, 127), (758, 129), (761, 201),
                         # Physical Plant, Root, CampPo, Field House
                         (761, 252), (762, 304), (763, 360), (763, 409),
                         # Science Center, Community Chest, Library, Faculty
                         (763, 460), (763, 516), (763, 567), (765, 621)]
                         # Chance, Alumni Gym, Tuition, Little Pub
    
        # Adds pawns to the board
        self._pawns = []
        for color, which, money in PLAYERIDENTITY:
            singlePawn = Pawn(self, color, which, money, 0)
            singlePawn.addTo(win)
            self._pawns.append(singlePawn)
        self.updatePawnLocations()
        # Establishes the identity of the current player
        self._current = 0
        
        # Lists name, initial price, location, rent and availability
        self._prop = [('Wertimer', 60, (683, 696), 2, 'Unowned'), 
                      ('Wallace Johnson', 60, (569, 695), 4, 'Unowned'), 
                      ('Laundry', 200, (511, 693), 25, 'Unowned'), 
                      ('Bus', 200, (455, 693), 25, 'Unowned'), 
                      ('Major', 100, (393, 693), 6, 'Unowned'),
                      ('Keehn', 100, (278, 693), 6, 'Unowned'), 
                      ('Opus 1', 120, (221, 696), 8, 'Unowned'), 
                      ('Kirner-Johnson', 140, (151, 620), 10, 'Unowned'), 
                      ('Bon Appetit', 150, (152, 567), 25, 'Unowned'), 
                      ('McEwen', 140, (150, 514), 10, 'Unowned'), 
                      ('Diner', 160, (148, 461), 12, 'Unowned'), 
                      ('Jitney', 200, (148, 409), 25, 'Unowned'), 
                      ('Sadove Center', 180, (148, 353), 14, 'Unowned'), 
                      ('Wellin Museum', 180, (145, 249), 14, 'Unowned'), 
                      ('Commons', 200, (147, 194), 16, 'Unowned'), 
                      ('Dunham', 220, (223, 124), 18, 'Unowned'), 
                      ('South', 220, (339, 124), 18, 'Unowned'), 
                      ('North', 220, (397, 124), 20, 'Unowned'), 
                      ('Zip Car', 200, (456, 124), 25, 'Unowned'), 
                      ('Benedict Hall', 260, (513, 125), 22, 'Unowned'), 
                      ('Christian Johnson', 260, (571, 124), 22, 'Unowned'), 
                      ('Physical Plant', 150, (629, 132), 25, 'Unowned'), 
                      ('Root Hall', 280, (684, 127), 22, 'Unowned'), 
                      ('Field House', 300, (761, 201), 26, 'Unowned'), 
                      ('Science Center', 300, (761, 252), 26, 'Unowned'), 
                      ('Burke Library', 320, (763, 360), 28, 'Unowned'), 
                      ('Faculty Parking', 200, (763, 409), 25, 'Unowned'), 
                      ('Alumni Gym', 350, (763, 516), 35, 'Unowned'), 
                      ('Little Pub', 400, (765, 621), 50, 'Unowned')]

    def reportPawnClick(self, ident):
        """Gives reaction after pawn is clicked"""
        if ident == self._current:
            movingPawn = self._pawns[ident]
            pos = movingPawn.getPosition()
            pos = pos + self._die.getValue()
            pos = pos % len(self._centers)
            movingPawn.setPosition(pos)
            self.updatePawnLocations()
            self.properties()
            self.changeTurn()

    def changeTurn(self):
        """Switches turn to the next player"""
        self._die.activate()
        self._current = (self._current + 1) % len(self._pawns)
        
    def currentPlayer(self):
        """Returns the identity of the current player"""
        return self._current
        
    def updatePawnLocations(self):
        """Places pawns in same location on each tile in formation of 3x3"""
        
        # Establishes the centers of the spaces that each player is on
        self._playerLocations = []
        for i in range(NUMPLAYERS):
            # Puts the first three pawns in a column
            if i < 3:
                pos = self._pawns[i].getPosition()
                self._theCenter = self._centers[pos]
                self._pawns[i].moveTo(self._theCenter)
                self._playerLocations.append(self._theCenter)
                self._pawns[i].move(-13, i * 15 - 20)
            # Puts next three pawns in a column next to first column
            if 3 <= i < 6:
                pos = self._pawns[i].getPosition()
                self._theCenter = self._centers[pos]                
                self._pawns[i].moveTo(self._theCenter)
                self._playerLocations.append(self._theCenter)
                self._pawns[i].move(0, i * 15 - 65)
            # Puts next three pawns in a column next to second column
            if i >= 6:
                pos = self._pawns[i].getPosition()
                self._theCenter = self._centers[pos]                
                self._pawns[i].moveTo(self._theCenter)
                self._playerLocations.append(self._theCenter)
                self._pawns[i].move(13, i * 15 - 110)
                
    def playLocations(self):
        """Returns a list of where all the pawns are"""
        return self._playerLocations

    def properties(self):    
        """Asks players if they want to buy a property when on a space"""
        
        playLoc = self._playerLocations[self._current]
        for i in range(len(self._prop)):
            if playLoc == self._prop[i][2] and self._prop[i][4] == 'Unowned' \
            and PLAYERIDENTITY[self._current][2] > self._prop[i][1]:
                answer = str(input("Would you like to buy " \
                + str(self._prop[i][0]) + " for $" + str(self._prop[i][1]) \
                + "?"))
                if answer == 'yes':
                    # Changes identifier to say what player now owns property
                    self._prop[i][4] = int(PLAYERIDENTITY[self._current][1])
                    # Takes away money from said player
                    PLAYERIDENTITY[self._current][2] -= self._prop[i][1]
                    print(PLAYERIDENTITY)
                    return
                else:
                    print(PLAYERIDENTITY)
                    return
            elif playLoc == self._prop[i][2] and self._prop[i][4] \
                         != 'Unowned':
                print(str("Player " + str(self._prop[i][4]) \
                          + " owns this property, pay them $" \
                          + str(self._prop[i][3]) + " for rent."))
                # Takes away money from victim who landed on space
                ownerMoney = PLAYERIDENTITY[self._prop[i][4]][2]
                ownerMoney += self._prop[i][3]
                PLAYERIDENTITY[self._prop[i][4]][2] = ownerMoney
                victimMoney = PLAYERIDENTITY[self._current][2]
                victimMoney -= self._prop[i][3]
                PLAYERIDENTITY[self._current][2] = victimMoney
                print(PLAYERIDENTITY)
                return

    def reportCommunityChest(self, location):
        """Ensures that report is happening on the board"""
        # Uses -1 to make sure that the person who clicks is one affected
        self._pawns[self._current - 1].moveTo(location)
        
    def reportChance(self, number):
        """Ensures that report is happening on the board"""
        # Uses -1 to make sure that the person who clicks is one affected
        PLAYERIDENTITY[self._current-1][2] += number
                    
class CommunityChest(EventHandler):
    """Establishes characteristics of the clickable community card"""
    
    def __init__(self, board):
        """Establishes characteristics of a single card"""
        
        self._comm = [('Community Chest 1', (627, 696)),
                      ('Community Chest 2', (147, 302)),
                      ('Community Chest 3', (762, 304))]
        
        EventHandler.__init__(self)
        self._board = board
        self._square = Rectangle(15, 15, (100, 20))
        self._square.setFillColor('yellow')
        self._square.addHandler(self)
        
        # A list of possible actions that a card might show with locations
        self._locationMovements = [("You have a problem with your roommate - move to Wertimer!", (683, 696)), ("You got a failing grade on your Calc exam - go to CJ for Office Hours.", (571, 124)), ("This final CS project is really kicking your ass - go to Science Center for TA hours!", (761, 252))]
        
    def addTo(self, win):
        """Adds card to board"""
        win.add(self._square)
    
    def handleMouseRelease(self, event):
        """Notifies board that the card has been clicked"""
        
        # Randomly chooses a card action from possible actions
        randomCard = random.randrange(0, len(self._locationMovements))
        self._board.reportCommunityChest(self._locationMovements[randomCard][1])
        print(self._locationMovements[randomCard][0])

class ChanceCard(EventHandler):
    """Establishes characteristics of the clickable chance card"""
    
    def __init__(self, board):
        
        self._chance = [('Chance 1', (336, 689)),
                        ('Chance 2', (2811, 1211))]
                        
        EventHandler.__init__(self)
        self._board = board
        self._square2 = Rectangle(15, 15, (120, 20))
        self._square2.setFillColor('orange')
        self._square2.addHandler(self)
        
        self._possChances = [("You won $5 in a Hamilton raffle!", 5), ("Someone dropped $100 on the floor and you take it for yourself", 100), ("You did a Psych study - earn $20!", 20), ("You ran out of bonus swipes - pay $10", -10), ("You bought something at Euphoria - pay $10", -10)]
        
    def addTo(self, win):
        """Adds card to window"""
        win.add(self._square2)
        
    def handleMouseRelease(self, event):
        """Notifies board that the card has been clicked"""
        randomCard = random.randrange(0, len(self._possChances))
        self._board.reportChance(self._possChances[randomCard][1])
        print(self._possChances[randomCard][0])
        print(PLAYERIDENTITY)

def main(win):
    """Begins game"""
    Board(win)
    
StartGraphicsSystem(main, WINDOW_WIDTH, WINDOW_HEIGHT)
