""" 
-------------------------------------------------------------------------------
*******************************************************************************
* Game.py                                                                     *
* Author:Conor Courtney                                                       *
* Date:5/1/17                                                                 *
* Partner: N/A                                                                * 
* Description: A program to create and run a version of the game Risk         *
*******************************************************************************
"""
import random
from cs110graphics import *

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 725
GSOLDIER = "https://cs.hamilton.edu/~ccourtne/images/gsoldier.png"
BSOLDIER = "https://cs.hamilton.edu/~ccourtne/images/bsoldier.png"
YSOLDIER = "https://cs.hamilton.edu/~ccourtne/images/ysoldier.png"
RSOLDIER = "https://cs.hamilton.edu/~ccourtne/images/rsoldier.png"
SOLDIERCARD = "https://cs.hamilton.edu/~ccourtne/images/soldiercard.png"
HORSECARD = "https://cs.hamilton.edu/~ccourtne/images/horsecard.png"
CANNONCARD = "https://cs.hamilton.edu/~ccourtne/images/cannoncard.png"

def inputNumber(formatstr, low, high):
    """Gets number from input box for various things"""
    #CITE: Professor Campbell-HarnessBots.py
    #DETAILS: Modified to make sure input is in range
    loop = True
    while loop is True:
        try:
            val = int(input(formatstr.format(low, high)))
            if val >= low and val <= high:
                return val
        except ValueError:
            pass
            
class Piece():
    """Class establishes troops which are controlled in armies by capitals"""
    def __init__(self, win, board, pos, color, army):
        self._board = board
        self._pos = pos
        self._color = color
        self._army = army
        self._win = win
        self.whichColorArmy(color)
        self._num = str(army)
        self._label = Text(self._num, ((self._pos[0] + 17), (self._pos[1] + 5)),
                           18)
        self._labelback = Square(20, ((self._pos[0] + 17), (self._pos[1])))
        self._labelback.setDepth(95)
        self._labelback.setFillColor("white")
        self._soldier.setDepth(95)
        self._soldier.resize(70, 70)
        self._label.setDepth(94)
        self.moveTo()
        
    def takeOver(self, invader):   
        """function to visually take over"""
        self.remove(self._win)
        self.whichColorArmy(invader)
        self._num = str(1)
        self._label.setText(self._num)
        self.addTo(self._win)
    
    def whichColorArmy(self, color):
        """sets the army to a certain color"""
        if color == "green":
            self._soldier = Image(GSOLDIER)
        elif color == "blue":
            self._soldier = Image(BSOLDIER)
        elif color == "yellow":
            self._soldier = Image(YSOLDIER)
        elif color == "red":
            self._soldier = Image(RSOLDIER)
            
        self._color = color 
        self._soldier.setDepth(95)
        self._soldier.resize(70, 70)
        self.moveTo()

    def update(self, armies):
        """function to update armies"""
        self.remove(self._win)
        self._num = str(armies)
        self._label.setText(self._num)
        self.addTo(self._win)
        
    def updateSide(self, team):
        """Visually updates army side"""
        self.remove(self._win)
        self.whichColorArmy(team)
        self.addTo(self._win)
        
    def addTo(self, win):
        """Function to add armies to window"""
        win.add(self._soldier)
        win.add(self._label)
        win.add(self._labelback)
        
    def remove(self, win):
        """function to remove armies"""
        win.remove(self._soldier)
        win.remove(self._label)
        win.remove(self._labelback)   
    
    def moveTo(self):
        """Function to move armies into position"""
        self._soldier.moveTo(self._pos)
    
class Capital(EventHandler):
    """Class which acts as countries, controls armies, team, fight, fortify"""
    def __init__(self, place, board, win):
        EventHandler.__init__(self)
        self._name = place[0]
        self._pos = place[1]
        self._bordering = []
        self._board = board
        self._win = win
        self._team = None
        self._troops = 1
        
        self._cap = Image("https://cs.hamilton.edu/~ccourtne/images/bflag.png")
        self._cap.addHandler(self)
        self._cap.setDepth(90)
        self._cap.scale(2)
        
        self._here = Image("https://cs.hamilton.edu/~ccourtne/images/wfla.png")
        self._here.addHandler(self)
        self._here.setDepth(91)
        self._here.scale(1.8)
        
        self._clicked = 0
        self._army = None
        self._turn = 0
        self.moveTo()
        
    def getBordering(self):
        """Returns list of bordering countries"""
        return self._bordering
    
    def getTurn(self):
        """Tells turn so only colors whose turn it is can move"""
        return self._turn
        
    def getName(self):
        """Returns name of capital"""
        return self._name
    
    def addBorders(self, borders):
        """Adds the neighboring capitals to the capital as an attribute"""
        self._bordering.extend(borders)
        
    def changeTeam(self, color):
        """sets team of capital"""
        self._team = color
        teams = [(0, "green"), (1, "blue"), (2, "yellow"), (3, "red")]
        
        for team in teams:
            if team[1] == color:
                self._turn = team[0]
                
        self._army.updateSide(self._team)
    
    def getTeam(self):
        """returns number of troops"""
        return self._team
        
    def defineTroops(self, troops):
        """sets number of troops"""
        self._troops = troops
        self._army.update(self._troops)
    
    def addTroops(self, update):
        """add troops from capital"""
        self._troops += update
        self._army.update(self._troops)
        
    def getTroops(self):
        """returns number of troops in capital"""
        return self._troops
        
    def addTo(self, win):
        """Function to add the capital to the window visually"""
        win.add(self._cap)
        win.add(self._here)
    
    def getPos(self):
        """Function to get the position of the capital"""
        return self._pos 
        
    def moveTo(self):
        """Function to move the capital to its position, offset b/c flagpole"""
        posx, posy = self._pos
        posx += 15
        wposx = posx + 1
        posy -= 15
        wposy = posy - 1
        offpos = (posx, posy)
        offposw = (wposx, wposy)
        
        self._cap.moveTo(offpos)
        self._here.moveTo(offposw)
    
    def checkIfClicked(self):
        """returns True if capital is clicked"""
        return self._clicked == 1
        
    def selectVis(self):
        """Visually select capital"""
        self._here.setDepth(89)
    
    def deselectVis(self):
        """Visually deselect capital"""
        self._here.setDepth(91)
    
    def handleMouseRelease(self, event):
        if self._clicked == 0:
            self._clicked = 1
            color = self._board.getTeam()
            self._army = Piece(self._win, self._board, self._pos, color,
                               self._troops)
            self._army.addTo(self._win)
            self.changeTeam(color)
            self._board.nextTurnBeg()
        else:
            if self._board.checkAllClicked() is False:
                return
            else:
                self._board.updateSelected(self)
                
        
class Fightbutton(EventHandler):
    """Creates the button which can be pressed to have two capitals fight"""
    def __init__(self, pos, board, win):
        EventHandler.__init__(self)
        self._fbut = Image("https://cs.hamilton.edu/~ccourtne/images/fight.png",
                           width=100, height=100)
        self._fbut.setDepth(90)
        self._fbut.addHandler(self)
        self._clicked = 0
        self._board = board
        self._fbut.moveTo(pos)
        win.add(self._fbut)

    def handleMouseRelease(self, event):
        self._board.report(0)

class Movebutton(EventHandler):
    """Creates the button which can be pressed to have troops move"""
    def __init__(self, pos, board, win):
        EventHandler.__init__(self)
        self._mbut = Image("https://cs.hamilton.edu/~ccourtne/images/move.png",
                           width=100, height=100)
        self._mbut.setDepth(90)
        self._mbut.addHandler(self)
        self._clicked = 0
        self._board = board
        self._mbut.moveTo(pos)
        win.add(self._mbut)
        
    def click(self):
        """clicks button"""
        self._clicked = 1
        
    def unclick(self):
        """unclicks button"""
        self._clicked = 0
        
    def getClick(self):
        """tells if button is clicked"""
        return self._clicked

    def handleMouseRelease(self, event):
        self._board.report(1)
        
class Nextbutton(EventHandler):
    """Creates the button which can be pressed to end turn"""
    def __init__(self, pos, board, win):
        EventHandler.__init__(self)
        self._nbut = Image("https://cs.hamilton.edu/~ccourtne/images/next.png",
                           width=100, height=100)
        self._nbut.setDepth(90)
        self._nbut.addHandler(self)
        self._clicked = 0
        self._board = board
        self._nbut.moveTo(pos)
        win.add(self._nbut)

    def handleMouseRelease(self, event):
        self._board.report(2)
        
class Cardback(EventHandler):
    """Creates the button which can be pressed to view cards"""
    def __init__(self, pos, board, win):
        EventHandler.__init__(self)
        self._cbut = Image("https://cs.hamilton.edu/~ccourtne/images/carp.png",
                           width=100, height=150)
        self._cbut.setDepth(90)
        self._cbut.addHandler(self)
        self._clicked = 0
        self._board = board
        self._cbut.moveTo(pos)
        win.add(self._cbut)

    def handleMouseRelease(self, event):
        self._board.report(3)
        
class Board():
    """Creates the interactive board, made of capitals and buttons"""
    def __init__(self, win):
        self._capitals = []
        self._places = [("Alaska0", (82, 173)), ("NW Territory1", (209, 180)),
                        ("Alberta2", (214, 240)), ("Ontario3", (300, 250)),
                        ("Quebec4", (388, 248)), ("Greenland5", (500, 104)),
                        ("Western US6", (237, 301)), 
                        ("Eastern US7", (322, 322)), 
                        ("Central America8", (268, 386)),
                        ("Venezuela9", (389, 445)), ("Brazil10", (468, 500)),
                        ("Peru11", (380, 523)), ("Argentina12", (407, 590)),
                        ("South Africa13", (730, 547)), 
                        ("East Africa14", (778, 444)), ("Congo15", (726, 468)),
                        ("North Africa16", (640, 393)), ("Egypt17", (734, 364)),
                        ("Iceland18", (577, 177)), 
                        ("Scandanavia19", (704, 175)), 
                        ("Great Britain20", (643, 243)), 
                        ("Western Europe21", (630, 304)), 
                        ("Northern Europe22", (698, 256)), 
                        ("Southern Europe23", (723, 287)),
                        ("Ukraine24", (785, 230)), 
                        ("Western Australia25", (1112, 560)),
                        ("Eastern Australia26", (1187, 560)),
                        ("Oceania27", (1062, 465)), 
                        ("Middle East28", (807, 338)),
                        ("Afghanistan29", (885, 282)), ("Ural30", (893, 201)),
                        ("Siberia31", (995, 190)), ("Yakutsk32", (1110, 180)),
                        ("Kamchatka33", (1200, 180)), 
                        ("Irkutsk34", (1060, 234)),
                        ("Mongolia35", (1070, 277)), ("China36", (1000, 325)),
                        ("Siam37", (1016, 400)), ("India38", (930, 370))]
                         
        for i in range(len(self._places)):
            capital = Capital(self._places[i], self, win)
            self._capitals.append(capital)
            capital.addTo(win)
            
        self._borders = [("NW Territory1", "Alberta2", "Kamchatka33"),
                         ("Alaska0", "Alberta2", "Ontario3", "Greenland5"),
                         ("Alaska0", "NW Territory1", "Ontario3", 
                          "Western US6"), 
                         ("Quebec4", "Eastern US7", 
                          "Western US6", "Alberta2", "NW Territory1"), 
                         ("Ontario3", "Eastern US7", "Greenland5"), 
                         ("NW Territory1", "Quebec4", "Iceland18"), 
                         ("Alberta2", "Ontario3", "Eastern US7",
                          "Central America8"), 
                         ("Ontario3", "Quebec4", "Western US6",
                          "Central America8"), 
                         ("Western US6", "Eastern US7", "Venezuela9"), 
                         ("Central America8", "Brazil10", "Peru11"), 
                         ("Venezuela9", "Peru11", "Argentina12", 
                          "North Africa16"), 
                         ("Venezuela9", "Brazil10", "Argentina12"), 
                         ("Brazil10", "Peru11"), 
                         ("East Africa14", "Congo15"), 
                         ("Middle East28", "Congo15", "North Africa16", 
                          "Egypt17", "South Africa13"), 
                         ("South Africa13", "East Africa14", "North Africa16"), 
                         ("Brazil10", "Congo15", "East Africa14", "Egypt17", 
                          "Western Europe21", "Southern Europe23"), 
                         ("Southern Europe23", "North Africa16", 
                          "East Africa14", "Middle East28"), 
                         ("Greenland5", "Scandanavia19", "Great Britain20"), 
                         ("Iceland18", "Ukraine24", "Northern Europe22", 
                          "Great Britain20"), 
                         ("Iceland18", "Scandanavia19", "Northern Europe22", 
                          "Western Europe21"), 
                         ("North Africa16", "Northern Europe22", 
                          "Southern Europe23", "Great Britain20"), 
                         ("Scandanavia19", "Great Britain20", 
                          "Southern Europe23", "Western Europe21", "Ukraine24"),
                         ("Middle East28", "North Africa16", "Egypt17", 
                          "Western Europe21", "Ukraine24", "Northern Europe22"),
                         ("Scandanavia19", "Northern Europe22", 
                          "Southern Europe23", "Middle East28", "Afghanistan29",
                          "Ural30"), ("Eastern Australia26", "Oceania27"), 
                         ("Western Australia25", "Oceania27"), 
                         ("Western Australia25", "Eastern Australia26", 
                          "Siam37"), 
                         ("India38", "Afghanistan29", "Ukraine24", 
                          "Southern Europe23", "Egypt17", "East Africa14"), 
                         ("Ukraine24", "Middle East28", "India38", "China36", 
                          "Ural30"), 
                         ("Siberia31", "China36", "Afghanistan29", "Ukraine24"),
                         ("Ural30", "China36", "Mongolia35",
                          "Irkutsk34", "Yakutsk32"), 
                         ("Siberia31", "Irkutsk34", "Kamchatka33"), 
                         ("Yakutsk32", "Irkutsk34", "Mongolia35", "Alaska0"), 
                         ("Yakutsk32", "Kamchatka33", "Siberia31", 
                          "Mongolia35"), 
                         ("Kamchatka33", "Irkutsk34", "China36", "Siberia31"),
                         ("Mongolia35", "Siberia31", "Ural30", "Afghanistan29",
                          "India38", "Siam37"), 
                         ("India38", "China36", "Oceania27"), 
                         ("Siam37", "China36", "Afghanistan29", 
                          "Middle East28")]
                         
        for i in range(len(self._capitals)):
            self._capitals[i].addBorders(self._borders[i])
        
        self._turnCounter = Square(15, (82, 645)) 
        self._turnCounter.setDepth(50)
        win.add(self._turnCounter)
        
        self._pCheck = 0
        self._turn = 0
        self._win = win
        self._capa = None
        self._capaTroops = 0
        self._capb = None
        self._capbTroops = 0
        
        self._fbut = Fightbutton((1325, 284), self, win)
        self._mbut = Movebutton((1325, 390), self, win)
        self._nbut = Nextbutton((1325, 497), self, win)
        self._cbut = Cardback((1325, 630), self, win)
        
        self._pocket = Pocket(self._win, self)
        self._deck = Card(self._win)
        self._dbutPressed = False
        
    def getTeam(self):
        """Tells whose turn it was who clicked country"""
        if self._turn == 0:
            return "green"
        elif self._turn == 1: 
            return "blue"
        elif self._turn == 2: 
            return "yellow"
        elif self._turn == 3: 
            return "red"
            
    def report(self, button):
        """recieves input from various buttons"""
        if button == 2:
            self.nextTurn()
            
        if button == 3:
            if self._dbutPressed is False:
                self._deck.showCards(self._turn)
                self._dbutPressed = True
            elif self._dbutPressed is True:
                self._deck.removeCards()
                self._dbutPressed = False
                
        if  not self.bordering(): 
            return 
        
        if button == 0:
            if not self.sameteam():    
                if self._capaTroops < 2:
                    return
                if self._mbut.getClick() == 1:
                    return
                self.fight()
            return
        
        if button == 1:
            if self.sameteam():
                self.move()

    def updateSelected(self, capital):
        """updates which capitals are selected"""
        if self._capa is None:
            if capital.getTurn() != self._turn:
                return
       
        if self._pocket.getCurrent() != 0:
            update = inputNumber("How many armies do you want to place? {}--{}",
                                 0, self._pocket.getCurrent())
            self._pocket.updatePocket(update)
            capital.addTroops(update)
            
            if (self._pocket.getCurrent() == 0 and
                    self._pocket.emptyPockets() is False):
                self.nextTurnBeg()
            return
        
        if self._capa is None:
            self._capa = capital
            self._capaTroops = self._capa.getTroops()
            self.visualUpdateSelected()
            return 
        elif self._capb is None:
            self._capb = capital
            if self._capb == self._capa:
                self._capb = None
                return
            self._capbTroops = self._capb.getTroops()
            self.visualUpdateSelected()
        else:
            self._capa = None
            self._capaTroops = 0
            self._capb = None
            self._capbTroops = 0
            self.visualUpdateSelected()

    def visualUpdateSelected(self):
        """visually updates selected capital"""
        if self._capa and self._capb is not None:       
            self._capb.selectVis()
        elif self._capa is not None:
            self._capa.selectVis()
        else:
            self.deselectAll()
    
    def getTurn(self):
        """returns the current turn"""
        return self._turn
        
    def deselectAll(self):
        """deselect all capitals"""
        for item in self._capitals:
            item.deselectVis()

    def fight(self):
        """function simulates dice rolling in risk battles"""
        attacker = []
        defender = []
        
        if self._capaTroops > 3:
            for _ in range(3):
                attacker.append(random.randrange(6))
        elif self._capaTroops == 3:
            for _ in range(2):
                attacker.append(random.randrange(6))
        elif self._capaTroops == 2:
            attacker.append(random.randrange(6))
            
        if self._capbTroops >= 2:
            for _ in range(2):
                defender.append(random.randrange(6))
        elif self._capbTroops == 1:
            defender.append(random.randrange(6))
        
        attacking = len(attacker)
        defending = len(defender)

        for _ in range(min(attacking, defending)):
            attack = max(attacker)
            attacker.remove(attack)
            defend = max(defender)
            defender.remove(defend)
            if attack > defend:
                self._capb.defineTroops(self._capbTroops - 1)
                self._capbTroops = self._capb.getTroops()
            else:
                self._capa.defineTroops(self._capaTroops - 1)
                self._capaTroops = self._capa.getTroops()
            if self._capbTroops == 0:
                self.takeover()   
                
    def checkAllClicked(self):
        """returns true is all capitals are selected"""
        for capital in self._capitals:
            if capital.checkIfClicked() is False:
                return False
        return True
            
    def move(self):
        """Function to move troops in order to fortify"""
        if self._mbut.getClick() == 1:
            return
        
        troops = self._capaTroops - 1
        formatstr = "How many troops do you wish to move? {}--{}"
        answer = inputNumber(formatstr, 0, troops)
        
        self._capa.defineTroops(self._capaTroops - answer)
        self._capaTroops = self._capa.getTroops()
        self._capb.defineTroops(self._capbTroops + answer)
        self._capbTroops = self._capb.getTroops()

        self._mbut.click()
        
    def bordering(self):
        """Checks if the capitals are bordering"""
        if self._capa is None or self._capb is None:
            return
        
        capital = self._capa.getName()
        bordering = self._capb.getBordering()
        
        for i in range(len(bordering)):
            if bordering[i] == capital:
                return True
        return False
        
    def sameteam(self):
        """Checks if the capitals are occupied by the same team"""
        capaTeam = self._capa.getTeam() 
        capbTeam = self._capb.getTeam()
        return capaTeam == capbTeam
            
    def takeover(self):
        """function called to have country switch possession"""
        formatstr = "How many troops do you wish to move? {}--{}"
        troops = self._capaTroops - 1
        answer = inputNumber(formatstr, 1, troops)
        
        self._capa.defineTroops(self._capa.getTroops() - answer)
        self._capb.defineTroops(answer)
        self._capb.changeTeam(self._capa.getTeam())
        self.checkWin()

    def checkWin(self):
        """function called to check if player had won"""
        base = self._capitals[0].getTeam()
        
        for i in range(len(self._capitals)):
            if self._capitals[i].getTeam() != base:
                return 
            
        self.initiateWin(base)        
        
    def initiateWin(self, team):
        """Function ends game and declares winner"""
        self.deselectAll()
        rect = Rectangle(SCREEN_WIDTH, SCREEN_HEIGHT)
        rect.setFillColor(team)
        #CITE: http://stackoverflow.com/questions/9237419/python-capitalize-on-
        #      a-string-starting-with-space
        #Details: How to capitalize the first letter of a string
        team = team.capitalize()
        rect.setDepth(0)
        rect.moveTo(((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)))
        self._win.add(rect)
        text = Text((team + " Wins!"), ((SCREEN_WIDTH / 2), 
                                        (SCREEN_HEIGHT / 2)), 100)
        self._win.add(text)
        text.setDepth(0)
    
    def nextTurnBeg(self):
        """Moves turn forward one in beginning of game"""
        if self._pCheck == 0:
            self._pCheck = inputNumber("How many players do you want? {}--{}",
                                       2, 4)
            self._turn = (self._turn + 1) % self._pCheck                       
        else:
            self._turn = (self._turn + 1) % self._pCheck
            
        self._pocket.setTurn(self._turn)
        self.moveTurnCounter()
        
    def nextTurn(self):
        """Ends current turn"""
        self._mbut.unclick()
        self.deselectAll()
        turn = (self._turn + 1) % 4
        check = True
        
        while check is True:
            if self.checkDeath(turn) is True:
                turn = (turn + 1) % 4
            else:
                check = False
                
        self.setTurn(turn)
        self.moveTurnCounter()
        self._pocket.fillPocket()
        self._deck.newCard(turn)
        
    def getTurnPos(self):
        """returns the position of a counter"""
        if self._turn == 0:
            pos = (82, 645)
        elif self._turn == 1:
            pos = (148, 645)
        elif self._turn == 2:
            pos = (216, 645)
        elif self._turn == 3:
            pos = (283, 645)
        return pos
        
    def moveTurnCounter(self):
        """Shows visually whose turn it is"""
        if self._pocket.getText() is not None:
            self._pocket.removeVis()
            
        pos = self.getTurnPos()
        self._turnCounter.moveTo(pos)
        self._pocket.visPocket(pos)
        
    def setTurn(self, turn):
        """sets current turn identifier"""
        self._turn = turn
        self._pocket.setTurn(turn)
        
    def checkDeath(self, turn):
        """true if a player has been eliminated from the game"""
        return self.countCountries(turn) == 0
            
    def countContinents(self, turn):
        """determines extra armies based on continents"""
        armies = 0
        asia = ["Middle East28", "Afghanistan29", "Ural30", "Siberia31",
                "Yakutsk32", "Kamchatka33", "Irkutsk34", "Mongolia35",
                "China36", "Siam37", "India38"]
        africa = ["South Africa13", "East Africa14", "Congo15", 
                  "North Africa16", "Egypt17"]
        north_america = ["Alaska0", "NW Territory1", "Alberta2", "Ontario3",
                         "Quebec4", "Greenland5", "Western US6",
                         "Eastern US7", "Central America8"]
        south_america = ["Venezuela9", "Brazil10", "Peru11", "Argentina12"]
        europe = ["Iceland18", "Scandanavia19", "Great Britain20",
                  "Western Europe21", "Northern Europe22", 
                  "Southern Europe23", "Ukraine24"]
        australia = ["Western Australia25", "Eastern Australia26", "Oceania27"]
        continents = [asia, africa, north_america, south_america, europe,
                      australia]
        conqueredContinents = []
        
        for continent in continents:
            count = 0
            for country in continent:
                for capital in self._capitals:
                    if (capital.getName() == country and 
                            capital.getTurn() == turn):
                        count += 1
            if count == len(continent):
                conqueredContinents.append(continent)
                
        for continent in conqueredContinents:
            if continent == asia:
                armies += 7
            elif continent == africa:
                armies += 3
            elif continent == north_america:
                armies += 5
            elif continent == south_america:
                armies += 2
            elif continent == europe:
                armies += 5
            elif continent == australia:
                armies += 2
           
        return armies
        
    def countCountries(self, turn):
        """counts the countries that are conquered"""
        count = 0
        for country in self._capitals:
            if country.getTurn() == turn:
                count += 1
        return count
  
    def countCards(self, turn):
        """adds value of cards"""
        return self._deck.countCards(turn)
        
class Pocket:
    """Class to count and add armies based on controlled territories"""
    def __init__(self, win, board):
        self._board = board
        self._turn = 0
        self._gPocket = 35
        self._bPocket = 35
        self._yPocket = 35
        self._rPocket = 35
        self._win = win
        self._text = None
        self._placed = False
       
    def getText(self):
        """returns text"""
        return self._text
    
    def emptyPockets(self):
        """checks if all the pockets are empty"""
        return self._placed
        
    def setTurn(self, turn):
        """sets turn to board's turn"""
        self._turn = turn
        
    def visPocket(self, pos):
        """Visually sets the pocket"""
        current = self.getCurrent()
        self._text = Text(str(current), (pos[0], (pos[1] + 4)), 10)
        self._win.add(self._text)
        self._text.setDepth(0)
    
    def getCurrent(self):
        """returns the current pocket"""
        if self._turn == 0:
            current = self._gPocket
        elif self._turn == 1:
            current = self._bPocket
        elif self._turn == 2:
            current = self._yPocket    
        elif self._turn == 3:
            current = self._rPocket 
        return current
        
    def removeVis(self):
        """removes the visual element of the pocket"""
        self._win.remove(self._text)
        self._text = None
    
    def fillPocket(self):
        """determines the total value to add to the pocket"""
        self._placed = True
        countries = self._board.countCountries(self._turn)
        countries = countries // 3
        continents = self._board.countContinents(self._turn)
        cards = self._board.countCards(self._turn)
        value = countries + continents + cards
        self.addArmies(value)
        
    def addArmies(self, value):
        """adds armies to the pocket"""
        self.removeVis()
        pos = self._board.getTurnPos()

        if self._turn == 0:
            self._gPocket += value
        elif self._turn == 1:
            self._bPocket += value
        elif self._turn == 2:
            self._yPocket += value
        elif self._turn == 3:
            self._rPocket += value

        self.visPocket(pos)


    def updatePocket(self, update):
        """updates the number of armies in the pocket"""
        self.removeVis()
        pos = self._board.getTurnPos()
        
        if self._turn == 0:
            self._gPocket -= update
        elif self._turn == 1:
            self._bPocket -= update
        elif self._turn == 2:
            self._yPocket -= update    
        elif self._turn == 3:
            self._rPocket -= update
 
        self.visPocket(pos)
        


class Card:
    """The risk cards which can be redeemed for more troops"""
    def __init__(self, win):
        self._gcards = []
        self._bcards = []
        self._ycards = []
        self._rcards = []
        self._win = win
        self._placed = []
        self._totalCards = 0
        
    def newCard(self, turn):
        """adds a new card to deck"""
        #CITE: https://docs.python.org/2/library/random.html
        #DETAILS: Learned how to choose a random list item instead of number
        card = random.choice(("soldier", "horse", "cannon"))
        if turn == 0:
            self._gcards.append(card)
        elif turn == 1:
            self._bcards.append(card)
        elif turn == 2:
            self._ycards.append(card)   
        elif turn == 3:
            self._rcards.append(card)
            
        for deck in [self._gcards, self._bcards, self._ycards, self._rcards]:
            if (len(deck)) > 5:
                deck.pop(0)
                
    def showCards(self, turn):
        """"shows the user the cards they hold"""
        if turn == 0:
            self.placeCards(self._gcards)
        elif turn == 1:
            self.placeCards(self._bcards)
        elif turn == 2:
            self.placeCards(self._ycards)
        elif turn == 3:
            self.placeCards(self._rcards)
            
    def placeCards(self, cards):
        """places the cards on the window"""
        pos = (185, 365)
        width = 130
        height = 170
        
        for card in cards:
            if card == "soldier":
                card = Image(SOLDIERCARD, pos, width, height)
            elif card == "horse":
                card = Image(HORSECARD, pos, width, height)
            elif card == "cannon":
                card = Image(CANNONCARD, pos, width, height)
            posx = pos[0] + 250
            pos = (posx, pos[1])
            card.setDepth(35)
            self._placed.append(card)
            
        rect = Rectangle(SCREEN_WIDTH, (SCREEN_HEIGHT / 2), 
                         ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)))
        rect.setFillColor("white")
        rect.setDepth(37)
        self._placed.append(rect)
        
        for item in self._placed:
            self._win.add(item)
        
    def removeCards(self):
        """removes cards from the table"""
        for item in self._placed:
            self._win.remove(item)
            
        self._placed = []
        
    def countCards(self, turn):
        """counts cards of a group"""
        if turn == 0:
            count = self.howManyArmies(self._gcards)[0]
            item = self.howManyArmies(self._gcards)[1]
            if item is not None:
                for _ in range(3):
                    self._gcards.remove(item)
        elif turn == 1:
            count = self.howManyArmies(self._bcards)[0]
            item = self.howManyArmies(self._bcards)[1]
            if item is not None:
                for _ in range(3):
                    self._bcards.remove(item)
        elif turn == 2:
            count = self.howManyArmies(self._ycards)[0]
            item = self.howManyArmies(self._ycards)[1]
            if item is not None:
                for _ in range(3):
                    self._ycards.remove(item)
        elif turn == 3:
            count = self.howManyArmies(self._rcards)[0]
            item = self.howManyArmies(self._rcards)[1]
            if item is not None:
                for _ in range(3):
                    self._rcards.remove(item)
            
        return count
        
    def howManyArmies(self, deck):
        """checks to see if any armies are added, removes those cards"""
        scount = 0
        hcount = 0
        ccount = 0
        armies = 0
        
        for card in deck:
            if card == "soldier":
                scount += 1
            elif card == "horse":
                hcount += 1
            elif card == "cannon":
                ccount += 1
                
        counts = [scount, hcount, ccount]
        for count in counts:
            if count == 3:
                armies = self._totalCards * 2 + 4
                self._totalCards += 1
                
        if scount == 3:
            removable = "soldier"
        elif hcount == 3:
            removable = "horse"
        elif ccount == 3:
            removable = "cannon"
        else:
            removable = None
                
        return (armies, removable)
                
def risk(win):
    """Everything runs through risk, the main function"""
    #CITE:http://thefutureofeuropes.wikia.com/wiki/File:Risk_Map.png
    #DETAILS: Used picture as a base outline of risk countries in GIMP
    world = Image("https://cs.hamilton.edu/~ccourtne/images/newBoard.png")
    world.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
    world.setDepth(100)
    world.moveTo(((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2)))
    win.add(world)
    Board(win)
    
StartGraphicsSystem(risk, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
