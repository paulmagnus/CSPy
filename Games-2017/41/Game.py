"""
-------------------------------------------------------------------------------
FILE:         Deck.py
AUTHOR:       Rina Ding
ASSIGNMENT:   Final Project
DATE:         05/01/17
PARTNER:      None
DESCRIPTION:  Play the game "Risk" online.

Basic setting: 
The game board shows the map of the world. There are 42 countries in total.
Black lines signifies borders of the countries. If two countries have part of
their borders overlapping, then they are neighbour countries. Orange lines
signify additional neighbour countries-any two countries that are linked by the
orange line are identified as neighbour countries.

3 players, red, blue and yellow, take turns to play the game. There are
unlimited armies owned by each player.

Stage:
There are two stages in the game: "ready" and "play". In the "ready" stage,
players take turns to occupy unoccupied countries on the map each with 1 of
their own armies. In the "play" stage, players are allowed to add armies to his
own countries or/and attack other players' countries. 

Playing guidelines:
Players play this game by following the hint at the bottom of the window, and
click at places which are activated. Activated areas or buttons are shown in
green, while the unactivated are shown in black.

There are two buttons in this game: "next" and "attack".
In the "ready" stage, only "next" will be activated. Click on "next" to start
the game. Then a player chooses an unoccupied country to occupy, and then clicks
on "next" to switch to next player. Each occupied country shows the color of the
player by which it is chosen, and the number "1", which means that there is
currently 1 army in this country. 

When all countries on the map are occupied, the game switch to stage "play".

In the "play" stage, at the beginning of each player's turn, he can choose one
of his own countries to add 3 armies to.  Then he can choose either to click on
"next" to end his turn, or to click on "attack" to attack other countries. If he
chooses "attack", he will choose one of his own countries to start his attack
from. He then clicks on "next" to show that he finishes his choice. Then he can
choose from the neighboring countries of the chosen own country to attack. 

If he wins the fight, he leaves 1 army in his original country and moves the
rest to the country conquered. If he loses the fight, he loses the number of
armies equal to the number of armies of the country that he attacked. 

A player can attack multiple times in his turn. He can also end the turn anytime
he finishes an attack by clicking on "next". Note that the "attack" button will
not be activated if there are no qualified countries to start an attack from.

Armies can only be moved during a fight when the attacker wins. The players are
not allowed to move their armies among their own countries.

A player wins when he has conquered all the countries on the map.

-------------------------------------------------------------------------------
"""

import random
from cs110graphics import *
from borders import name, extraBorder, neighbour

class Board:
    """control the whole game"""
    
    def __init__(self, win):
        """attributes for the game board"""
        
        # among 'red', 'yellow' and 'blue', indicate the current player
        self._players = ["red", "yellow", "blue"]
        self._current = "blue"
        
        #form the map
        self._countries = []
        borders = name()
        for border in borders:
            self._countries.append(Country(border, self))
        self._otherBorders = extraBorder()
        self.formGraph(win)
        
        # start the game with "ready" stage
        self._stage = "ready"
        
        # add and activate the "Next" button
        goNext = GoNext(self)
        goNext.addTo(win)
        goNext.activate()
        self._next = goNext
        
        # add the "attack" button
        attack = Attack(self)
        attack.addTo(win)
        self._attack = attack
        
        # add the hint to the window
        self._hint = Text("", (300, 350))
        win.add(self._hint)
        
        # Steps during the stage "play"
        self._step = "addArmy"   
        
        # set an attacker and defender when a player starts an attack
        self._attacker = None
        self._defender = None
    
    def formGraph(self, win):
        """Add graphs of countries' borders and additional border lines to 
           the window"""
        
        for country in self._countries:
            country.addTo(win)
        for item in self._otherBorders:
            border = Polygon(item)
            border.setBorderColor("orange")
            win.add(border)

    def getCountries(self):
        """return the list of countries"""
        
        return self._countries
        
    def deactivateAll(self):
        """deactivate all countries"""
        
        for country in self._countries:
            country.deactivate()
        
    def getNeighb(self, country):
        """return the list of neighbouring countries of the given country"""
        
        # find index of the given country
        indexGiven = None
        for i in range(len(self._countries)):
            if self._countries[i] == country:
                indexGiven = i
        
        # find the list of neighbouring countries' borders    
        neighbours = neighbour()
        neighBorderList = neighbours[indexGiven]
        
        # list of neighbouring countries
        neighList = []
        countries = name()
        for neighBorder in neighBorderList:
            for j in range(len(countries)):
                if countries[j] == neighBorder:
                    neighList.append(self._countries[j])

        return neighList
        
    def getStage(self):
        """return the stage of the game"""
        
        return self._stage
        
    def changeStage(self, stage):
        """change the stage of the game to the given stage"""
        
        self._stage = stage
    
    def getStep(self):
        """return the step during stage 'play'"""
        
        return self._step
        
    def changeStep(self, step):
        """change the step during stage 'play' to the given step"""
        
        self._step = step
    
    def getPlayer(self):
        """return the current player that is playing"""
        
        return self._current
    
    def getHint(self):
        """return the current hint"""
        
        return self._hint
        
    def getNext(self):
        """return the 'Next' button"""
        
        return self._next
        
    def getAttack(self):
        """return the 'Attack' button"""
        
        return self._attack
        
    def qualifyAttack(self):
        """return True if there is any country in the world that can be 
           attacked; that is to say, there is at least one country owned by
           the current player which have available neighbouring countries to
           attack"""
        
        for country in self._countries:
            if country.getPlayer() == self._current:
                if len(country.borderToAttack()) != 0:
                    return True
        return False
            
    def setAttacker(self, attacker):
        """set the attacker as the given attacker country"""
        
        self._attacker = attacker
        
    def getAttacker(self):
        """return the attacker country"""
        
        return self._attacker
    
    def setDefender(self, defender):
        """set the defender as the given defender country"""
        
        self._defender = defender
        
    def findWinner(self):
        """use random function to replace the role of dice to determine 
           winner of an attack"""
        
        winner = None
        
        # attacker needs 1 army to maintain its original country, thus minus 1
        attNum = self._attacker.getNumArmy() - 1
        defNum = self._defender.getNumArmy()
        
        result = random.randrange(attNum + defNum)
        if result < defNum:
            winner = self._defender
        else:
            winner = self._attacker
        
        return winner
    
    def gameEndTest(self):
        """test if the game ends after an attacker wins his attack; the game
        ends when only one player exists in the player list"""
        
        return len(self._players) == 1
    
    def findLoser(self):
        """determine if there is a loser of the whole game after he loses a 
           fight. If so, remove him from the player list. A player loses the
           whole game when he does not own any countries after the 'play' stage
           starts"""
          
        for player in self._players:
            ownership = 0
            for country in self._countries:
                if country.getPlayer() == player:
                    ownership += 1
            if ownership == 0:
                self._players.remove(player)
           
    def fight(self):
        """determine the winner and loser of a fight. If the attacker wins, 
           retain 1 army in its original country, move the rest armies to the 
           country conquered and change its color to the attacker's color;
           if the attacker lose, the attacker lose the number of armies
           that is equal to the defender country's armies. Deactivate all 
           countries. At the end of a fight, always test if there is any player
           who loses the game. When there is only one player left, he becomes
           the winner and the game ends. If there is still more than one player,
           activate 'Next' button, and also activate 'Attack' button if 
           applicable"""
        
        winner = self.findWinner()
        
        if self._attacker == winner:
            loser = self._defender
            
            self._hint.setText("Player " + str(self._current) + ": you win" +
                               " this fight!")
            loser.changeArmy(winner.getPlayer(), winner.getNumArmy() - 1)
            winner.changeArmy(winner.getPlayer(), 1)
            
            # delete the player from the player list if he loses the whole game
            self.findLoser()
            
        else:
            loser = self._attacker
            self._hint.setText("Player " + str(self._current) + ": you lose" + 
                               " this fight!")
            loser.changeArmy(loser.getPlayer(), loser.getNumArmy() - \
                             winner.getNumArmy())
        
        self.deactivateAll()
        
        # test if the game ends
        if self.gameEndTest():
            self._hint.setText("Player " + str(self._current) + ": you win " +
                               "the game!")
        # continue the game by activating two buttons if game does not end
        else:
            self._next.activate()
            if self.qualifyAttack():
                self._attack.activate()
    
    def changeTurn(self):
        """player 'red', 'yellow' and 'blue' take turns to play the game. Change
           the current player when the its turn ends. When a player owns no 
           country on the map, he loses the game and will no longer have his
           turn to play"""

        for i in range(len(self._players)):
            if self._players[i] == self._current:
                self._current = self._players[(i + 1) % len(self._players)]
                break
    
    def occupyCountries(self):
        """activate all countries that are unoccupied, switch to the next
        player and deactivate the 'Next' button"""
        
        for country in self._countries:
            if country.getPlayer() is None:
                country.activate()
                
        self.changeTurn()
        self._hint.setText("Player " + str(self._current) + ": choose a " +    
                           "country to occupy")
        self._next.deactivate()
        
    def allOccupied(self):
        """return whether or not all countries are occupied"""
        
        count = 0
        for country in self._countries:
            if country.getPlayer() != None:
                count += 1
        return count == 42
    
    def ifSwitchStage(self):
        """switch the stage from "ready" to "play" when all countries are 
           occupied"""
           
        if self.allOccupied():
            self.changeStage("play")
            # no need to change turn here, but in stage "play" it need to change
            # turn, so change turn twice here to restore the player
            self.changeTurn()
            self.changeTurn()
    
    def addArmy(self):
        """in stage 'play', when it is a new player's turn, add 3 armies to its
           selected own country"""
           
        if self._step == "attack":
            self.changeStep("addArmy")
            self._attack.deactivate()
        if self._step == "addArmy":
            self.changeTurn()
            for country in self._countries:
                if country.getPlayer() == self.getPlayer():
                    country.activate()
            self._hint.setText("Player " + str(self._current) + ": choose one" +
                               " of your countries to add 3 armies to")
            self._next.deactivate()
            
    def startFrom(self):
        """activate all own countries where attack to border countries can be
           initiated, and deactivate 'Next' and 'Attack' button"""
           
        if self._step == "startFrom":
            for country in self._countries:
                if len(country.borderToAttack()) != 0:
                    if country.getPlayer() == self._current:
                        country.activate()
            self._hint.setText("Player " + str(self._current) + ": choose " + 
                               "one of your countries to prepare your attack " +
                               "to border countries")
            self._next.deactivate()
            self._attack.deactivate()
            
    def readyToAttack(self):
        """when an own country has been chosen to start attack from, activate
           its border countries which can be attacked"""
           
        if self._step == "attackReady":
            for country in self._attacker.borderToAttack():
                country.activate()
            self._hint.setText("Player " + str(self._current) + ": choose one" +
                               " of the border countries to attack")
            self.changeStep("attack")
            self._next.deactivate()
        
        
class GoNext(EventHandler):
    """construct the 'Next button. In the 'ready' stage, 'Next' button is
       used to end a player's turn and switch to next player. In the 
       'play' stage, when during an attack, 'Next' button is used to 
       confirm that the player has chosen an own country to attack its
       border countries; when not during an attack, 'Next' button is used
       to end the current player's turn and switch to next player"""
       
    def __init__(self, board, text="Next"):
        """construct the 'Next' button"""
        
        EventHandler.__init__(self)
        
        self._board = board
        self._back = Rectangle(30, 20, (580, 327))
        self._back.setFillColor("yellow")
        self._back.addHandler(self)
        self._front = Text(text, (580, 327))
        self._active = False
        
    def addTo(self, win):
        """add the 'Next' button to the window"""
        
        win.add(self._back)
        win.add(self._front)

    def activate(self):
        """activate the 'Next' button and set its border color as green"""
        
        self._active = True
        self._back.setBorderColor("green")
    
    def deactivate(self):
        """deactivate the 'Next' button and set its border color back to 
           black"""
           
        self._active = False
        self._back.setBorderColor("black")
    
    def handleMouseRelease(self, event):
        """actions when the 'Next' button is clicked"""
        
        if not self._active:
            return 
        else:
            if self._board.getStage() == "ready":
                # switch to stage "play" when all countries are occupied
                self._board.ifSwitchStage()
                    
                #when not all countries are occupy, continue occupying countries
                self._board.occupyCountries()
                    
            if self._board.getStage() == "play":
                # if the player give up attacking, it's next player's turn to 
                # add armies
                self._board.addArmy()
                # activate border countries to attack when the StartFrom country
                # has been chosen
                self._board.readyToAttack()
            
            
class Attack(EventHandler):
    """click on Attack button to attack other players' countries"""
    
    def __init__(self, board, text="Attack"):
        """construct the 'Attack' button"""
        
        EventHandler.__init__(self)
        
        self._board = board
        self._back = Rectangle(35, 20, (580, 300))
        self._back.setFillColor("yellow")
        self._back.addHandler(self)
        self._front = Text(text, (580, 300))
        self._active = False
        
    def addTo(self, win):
        """add the 'Attack' button to the window"""
        
        win.add(self._back)
        win.add(self._front)

    def activate(self):
        """activate the 'Attack' button and set its border color as green"""
        
        self._active = True
        self._back.setBorderColor("green")
    
    def deactivate(self):
        """deactivate the 'Attacj' button and set its border color back to 
           black"""
        
        self._active = False
        self._back.setBorderColor("black")
    
    def handleMouseRelease(self, event):
        """actions when the 'Attack' button is clicked"""
        
        if not self._active:
            return 
        else:
            self._board.changeStep("startFrom")
            self._board.startFrom()
            
            
class Country(EventHandler):
    """each country on the map"""
    def __init__(self, border, board):
        """border is a list of points that denotes the border of the country,  
           except that the last point denotes the center of the country; player
           indicates ownership of the country, and numArmy indiactes number 
           of army that is placed in the country"""
        
        EventHandler.__init__(self)
        self._board = board
        
        # exclude the final tuple, which is the center of the country
        self._border = border[:len(border)-1]
        self._shape = Polygon(self._border)
        self._shape.addHandler(self)
        self._shape.setFillColor("white")
        
        self._player = None
        self._numArmy = 0
        self._active = False
        
        self._center = border[-1]
        self._text = Text(self._numArmy, self._center, 12)
        
    def addTo(self, win):
        """add the country to the window, with number of armies in the 
           country"""
           
        win.add(self._shape)
        win.add(self._text)
    
    def getPlayer(self):
        """return the player that occupies the country"""
        
        return self._player
    
    def getNumArmy(self):
        """return the number of armies in the country"""
        
        return self._numArmy
    
    def getActive(self):
        """return whether or not the country is activated"""
        
        return self._active
    
    def addArmy(self, player, numArmy):
        """in the 'ready' stage, assign ownership of the country as player, 
           and add 1 army to the country; in the 'play' stage, at the 
           beginning of each player's turn, add 3 armies to its own country"""
           
        self._player = player
        self._numArmy += numArmy
        
        self._shape.setFillColor(player)
        self._text.setText(self._numArmy)
        
    def changeArmy(self, player, numArmy):
        """when a player wins or loses, change the number of armies in the 
           country and possibly also the ownership of the country"""
        
        self._player = player
        self._numArmy = numArmy
        
        self._shape.setFillColor(player)
        self._text.setText(self._numArmy)
        
    def activate(self):
        """activate the country and set its border color as green"""
        
        self._active = True
        self._shape.setBorderColor("green")
        
    def deactivate(self):
        """deactivate the country and set its border color back to black"""
        
        self._active = False
        self._shape.setBorderColor("black")
        
    def borderToAttack(self):
        """return the list of border countries that can be attacked; boder 
           countries that can be attacked should be owned by other players, and
           number of armies on the opposing countries should be less than the 
           own country"""
        
        counToAttack = []
        for country in self._board.getNeighb(self):
            if country.getPlayer() != self._player:
                if country.getNumArmy() < self.getNumArmy():
                    counToAttack.append(country)
        return counToAttack
        
    def handleMouseRelease(self, event):
        """actions when a given country is clicked"""
        
        if not self._active:
            return 
        else:
            if self._board.getStage() == "ready":
                self.addArmy(self._board.getPlayer(), 1)
                self._board.getNext().activate()
                self._board.deactivateAll()
            if self._board.getStage() == "play":
                if self._board.getStep() == "addArmy":
                    self.addArmy(self.getPlayer(), 3)
                    self._board.getNext().activate()
                    if self._board.qualifyAttack():
                        self._board.getAttack().activate()
                    self._board.deactivateAll()
                if self._board.getStep() == "startFrom":
                    self._board.setAttacker(self)
                    self._board.changeStep("attackReady")
                    self._board.getNext().activate()
                    self._board.deactivateAll()
                if self._board.getStep() == "attack":
                    self._board.setDefender(self)
                    self._board.fight()
                    
                    
def play(win):
    """start the game"""
    Board(win)

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 360    

StartGraphicsSystem(play, WINDOW_WIDTH, WINDOW_HEIGHT)
