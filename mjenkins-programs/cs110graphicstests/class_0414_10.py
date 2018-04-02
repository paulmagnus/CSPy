from cs110graphics import *


class Piece(EventHandler):
    def __init__(self, win, kind, player):
        EventHandler.__init__(self)
        self._kind = kind
        self._player = player
        self._front = Text(win, kind)
        self._back = Rectangle(win, 25, 25)
        if kind == 'X':
            self._back.set_fill_color('red')
        else:
            self._back.set_fill_color("blue")
        self._back.add_handler(self)
        self._front.add_handler(self)
        self._moving = False
        self._location = (0, 0) # where the piece is 
        self._startLoc = None  # where the mouse was when we started moving
        self._active = False
        
    def activate(self):
        self._active = True
        self._back.set_border_color('green')
        
    def deactivate(self):
        self._active = False
        self._back.set_border_color('black')
    
    def highlight(self):
        self._back.set_border_color('blue')
        
    def addTo(self, win):
        win.add(self._back)
        win.add(self._front)

    def move_to(self, pos):
        self._front.move_to(pos)
        self._back.move_to(pos)
        self._location = pos
    
    def move(self, dx, dy):
        oldx, oldy = self._location
        newx = oldx + dx
        newy = oldy + dy
        self.move_to((newx, newy))
    
    def getLocation(self):
        return self._location
        
    def getKind(self):
        return self._kind
    
    def handle_mouse_release(self, event):
        if not self._active:
            return
        if self._moving:
            self._moving = False
            self._player.report(self, event)
        else:
            self._moving = True
            self._startLoc = event.get_mouse_location()

    def handle_mouse_move(self, event):
        if not self._active:
            return
        if self._moving:
            oldx, oldy = self._startLoc
            newx, newy = event.get_mouse_location()
            self.move(newx - oldx, newy - oldy)
            self._startLoc = self._location


class Cell:
    def __init__(self, win, pos):
        self._location = pos
        self._rect = Rectangle(win, 30, 30, pos)
        win.add(self._rect)
        self._piece = None
        
    def getLocation(self):
        return self._location
        
    def getPiece(self):
        return self._piece
        
    def addPiece(self, piece):
        self._piece = piece


class Player:
    def __init__(self, win, kind, board):
        self._board = board
        self._pieces = []
        count = 5
        if kind == 'O':
            count = 4
        for i in range(count):
            piece = Piece(win, kind, self)
            piece.addTo(win)
            piece.move_to((50 + i * 25, 50 + (count - 4) * 200))
            self._pieces.append(piece) 

    def report(self, piece, event):
        self._board.report(piece, event)

    def activateAll(self):
        for piece in self._pieces:
            piece.activate()
    
    def removePiece(self, piece):
        pos = None
        for i in range(len(self._pieces)):
            if self._pieces[i] == piece:
                pos = i
        if pos != None:
            self._pieces.pop(pos)

           
    def deactivateAll(self):
        for piece in self._pieces:
            piece.deactivate()

class Board:
    def __init__(self, win):
        self._players = []
        for kind in ['X', 'O']:
            self._players.append(Player(win, kind, self))
        x, y = 55, 100
        self._cells = []
        for row in range(3):
            self._cells.append([])
            for col in range(3):
                newCell = Cell(win, (x + 30 * row, y + 30 * col))
                self._cells[-1].append(newCell)
        self._current = 1
        self.changeTurn()
    
    def changeTurn(self):
        self._players[self._current].deactivateAll()
        self._current += 1
        self._current %= 2
        self._players[self._current].activateAll()
    
    def getWinnerConfig(self):
        """ return a list of logical positions where pieces match,  or
            None, if there is not yet a winner """
        configs = [[(0, 0), (0, 1), (0, 2)],
                   [(1, 0), (1, 1), (1, 2)],
                   [(2, 0), (2, 1), (2, 2)],
                   [(0, 0), (1, 0), (2, 0)],
                   [(0, 1), (1, 1), (2, 1)],
                   [(0, 2), (1, 2), (2, 2)],
                   [(0, 0), (1, 1), (2, 2)],
                   [(2, 0), (1, 1), (0, 2)]]
        for config in configs:
            kind = None
            count = 0
            for row, col in config:
                piece = self._cells[row][col].getPiece() #missing getPiece
                if piece == None:   # was !=
                    break
                if kind == None:
                    kind = piece.getKind()
                elif piece.getKind() != kind:
                    break
                count += 1
                print(count)
            if count == 3:
                return config
        return None
                    
    
    def computeLanding(self, piece):
        """ Return the empty cell where the user has left the piece """
        x0, y0 = self._cells[0][0].getLocation()
        x0 -= 15 # left edge
        y0 -= 15 # top
        x1, y1 = piece.getLocation()
        row = (x1 - x0) // 30
        col = (y1 - y0) // 30
        if row < 0 or col < 0 or row > 2 or col > 2:
            return None
        if self._cells[row][col].getPiece() != None:
            return None
        return self._cells[row][col]
    
    def report(self, piece, event):
        landing = self.computeLanding(piece)   # type(landing) is Cell
        if landing != None:
            piece.deactivate()
            self._players[self._current].removePiece(piece)
            landing.addPiece(piece)
            piece.move_to(landing.getLocation())
            config = self.getWinnerConfig()
            if config == None:
                self.changeTurn()
            else:
                self._players[self._current].deactivateAll()
                for row, col in config:
                    self._cells[row][col].getPiece().highlight()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

def play(win):
    Board(win)

StartGraphicsSystem(play)
