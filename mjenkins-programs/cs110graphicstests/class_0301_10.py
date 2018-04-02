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


def makeSmiley(win, radius, center):
    face = Circle(win, radius, center)
    face.set_fill_color(randomColor())
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


def drawSmiley(win, radius, center):
    """ draw a smiley face centered at center, with radius """
    face = Circle(win, radius, center)
    face.set_fill_color('yellow')
    cx, cy = center
    leftEye = Circle(win, radius / 20, (cx - radius / 2, cy - radius / 2))
    leftEye.set_fill_color('black')
    rightEye = Circle(win, radius / 20, (cx + radius / 2, cy - radius / 2))
    rightEye.set_fill_color('black')
    mouth = Rectangle(radius, radius / 8, (cx, cy + radius / 4))
    win.add(face)
    win.add(leftEye)
    win.add(rightEye)
    win.add(mouth)


def addAll(win, objects):
    """ given a list of objects, add all of them to the window """
    for obj in objects:
        win.add(obj)


def moveAll(objects, dx, dy):
    """ move all objects by dx pixels horizontally, and dy pixels vertically"""
    for obj in objects:
        obj.move(dx, dy)


def first(win):
    """ first function always takes a parameter of type Window """

    circles = []
    for _ in range(10):
        radius = rnd(50)
        cx = rnd(400)
        cy = rnd(400)
        circle = Circle(win, radius, (cx, cy))
        circles.append(circle)

    smileys = []
    for _ in range(10):
        smileys.append(makeSmiley(win, rnd(50), (rnd(400), rnd(400))))
    for smile in smileys:
        addAll(win, smile)
    for _ in range(100):
        for smile in smileys:
            dx, dy = rnd(10) - 5, rnd(10) - 5
            moveAll(smile, dx, dy)
        yield 20


def program(win):
    RunWithYieldDelay(win, first(win))


StartGraphicsSystem(program)


























