from cs110graphics import *


class Card:
    def __init__(self, suit, name, faceFileName, backFileName):
        faceurl = "http://cs.hamilton.edu/~mbailey/cards/" + faceFileName
        self._face = Image(faceurl, width=71, height=96)
        #backurl...
        #self._back....
        
    def addTo(self, win):
        win.add(self._face)
    
    def move(self, dx, dy):
        self._face.move(dx, dy)
        
def main2(win):
    dy = 50
    dx = 40
    for suit in ['clubs', 'diamonds', 'hearts', 'spades']:
        for name in ['ace', '2', '3' ,'4' ,'5' ,'6', '7', '8', '9',
                      '10', 'jack', 'queen', 'king']:
            c = Card(suit, name, suit[0]+name[0]+'.gif', 'back.gif')
            c.addTo(win)
            c.move(dx, dy)
            dx += 6

        
def main(win):
    cf = Image("http://cs.hamilton.edu/~mbailey/cards/sa.gif", 
            width=71, height=96)
    win.add(cf)
    cf.moveTo((200, 200))

    cb = Image("http://cs.hamilton.edu/~mbailey/cards/back.gif", 
            width=71, height=96)
    win.add(cb)
    cb.moveTo((200, 200))
    
StartGraphicsSystem(main2)
