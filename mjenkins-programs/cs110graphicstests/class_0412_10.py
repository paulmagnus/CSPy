from cs110graphics import *


class Piece(EventHandler):
    def __init__(self, win, kind, player):
        EventHandler.__init__(self)
        self._kind = kind
        self._player = player
        self._back = Rectangle(win, 25, 25)
        self._front = Text(win, kind)
        self._back.set_fill_color('red')
        self._back.add_handler(self)
        self._moving = False
        self._location = (0, 0)  # window location of the piece
        self._startPos = None    # mouse position where movement started
        self._active = False

    def activate(self):
        self._active = True
        self._back.set_border_color('green')

    def deactivate(self):
        self._active = False
        self._back.set_border_color('black')

    def add_to(self, win):
        win.add(self._back)
        win.add(self._front)

    def move_to(self, pos):
        self._back.move_to(pos)
        self._front.move_to(pos)
        self._location = pos

    def move(self, dx, dy):
        oldx, oldy = self._location
        newx = oldx + dx
        newy = oldy + dy
        self.move_to((newx, newy))

    def handle_mouse_release(self, event):
        if not self._active:
            return
        if self._moving:
            self._moving = False
            self._player.report(self, event)
        else:
            self._moving = True
            self._startPos = event.get_mouse_location()

    def handle_mouse_move(self, event):
        if not self._active:
            return
        if self._moving:
            oldx, oldy = self._startPos
            newx, newy = event.get_mouse_location()
            self.move(newx - oldx, newy - oldy)
            self._startPos = newx, newy


class Player:
    def __init__(self, win, kind, board):
        self._pieces = []
        self._board = board
        count = 5
        if kind == 'O':
            count = 4
        for i in range(count):
            piece = Piece(win, kind, self)
            piece.add_to(win)
            piece.move_to((50 + i * 25, 50 + (count - 4) * 200))
            self._pieces.append(piece)

    def report(self, piece, event):
        self._board.report(piece, event)

    def activateAll(self):
        for piece in self._pieces:
            piece.activate()

    def deactivateAll(self):
        for piece in self._pieces:
            piece.deactivate()


class Board:
    def __init__(self, win):
        self._players = []
        for kind in ['X', 'O']:
            self._players.append(Player(win, kind, self))
        self._current = 1
        self.changeTurn()

    def changeTurn(self):
        self._players[self._current].deactivateAll()
        self._current += 1
        self._current %= 2
        self._players[self._current].activateAll()

    def report(self, piece, event):
        print("Something happened with {}".format(piece))
        self.changeTurn()


def play(win):
    Board(win)


StartGraphicsSystem(play)
