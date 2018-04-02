from cs110graphics import *
import random
import math


def rnd(x):
    return random.randrange(x)


def randomColor():
    digits = "0123456789ABCDEF"
    answer = "#"
    for _ in range(6):
        answer += digits[rnd(16)]
    return answer


def setColor(smiley, color):
    face = smiley[0]
    face.set_fill_color(color)


def makeSmiley(win, radius, center, color='yellow'):
    face = Circle(win, radius, center)
    face.set_fill_color(color)
    cx, cy = center
    leftEye = Circle(win, radius / 20, (cx - radius / 2, cy - radius / 2))
    leftEye.set_fill_color('black')
    rightEye = Circle(win, radius / 20, (cx + radius / 2, cy - radius / 2))
    rightEye.set_fill_color('black')

    points = []
    theta = math.pi
    while theta <= 2 * math.pi:
        x = cx + radius / 2 * math.cos(theta)
        y = cy - radius / 2 * math.sin(theta)
        points.append((x, y))
        theta += 0.1

    # repeat points backwards:
    points.extend(points[-2::-1])
    mouth = Polygon(win, points)
    ans = [face, leftEye, rightEye, mouth]
    return ans


def makeMover(graphics, x, y, dx, dy, window_width, window_height):
    """ make list with 7 elements:
        0: a list of graphics
        1 : x coordinate
        2 : y coordinate
        3 : dx motion
        4 : dy motion
        5 : window width
        6 : window height """
    return [graphics, x, y, dx, dy, window_width, window_height]


def moveMover(mover):
    """ move all graphics in the mover by the mover's dx, dy """
    graphics, x, y, dx, dy = mover[:5]
    x += dx
    y += dy
    moveAll(graphics, dx, dy)
    mover[1] = x
    mover[2] = y


def moveWithBounce(mover):
    moveMover(mover)
    x, y, dx, dy, width, height = mover[1:]
    if x < 0 or x >= width:
        dx = -dx
    if y < 0 or y >= height:
        dy = -dy
    mover[3] = dx
    mover[4] = dy


def addAll(win, objects):
    """ given a list of objects, add all of them to the window """
    for obj in objects:
        win.add(obj)


def moveAll(objects, dx, dy):
    """ move all objects by dx pixels horizontally, and dy pixels vertically"""
    for obj in objects:
        obj.move(dx, dy)


WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def change_colors_if_close(smileys):
    for i in range(len(smileys)):
        for j in range(len(smileys)):
            if i != j:
                xi, yi = smileys[i][1], smileys[i][2]
                xj, yj = smileys[j][1], smileys[j][2]
                if distance(xi, yi, xj, yj) <= 100:
                    setColor(smileys[i][0], randomColor())
                    setColor(smileys[j][0], randomColor())


def first(win):
    """ first function always takes a parameter of type Window """

    dim = min(WINDOW_WIDTH, WINDOW_HEIGHT)
    smileys = []
    for _ in range(6):
        x, y = rnd(WINDOW_WIDTH), rnd(WINDOW_HEIGHT)
        smile = makeSmiley(win, random.randrange(0.3 * dim / 10, 1.7 * dim / 10),
                           (x, y), randomColor())
        addAll(win, smile)
        dx, dy = random.randrange(-3, 4), random.randrange(-3, 4)
        movingSmile = makeMover(smile, x, y, dx, dy, WINDOW_WIDTH,
                                WINDOW_HEIGHT)
        smileys.append(movingSmile)
    while True:
        for mover in smileys:
            moveWithBounce(mover)
        change_colors_if_close(smileys)
        yield 20


def program(win):
    RunWithYieldDelay(win, first(win))


StartGraphicsSystem(program, WINDOW_WIDTH, WINDOW_HEIGHT)

