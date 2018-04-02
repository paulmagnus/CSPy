from cs110graphics import *
import random


def rnd(x):
    return random.randrange(x)


def makeSmiley(win, radius, center):
    face = Circle(win, radius, center)
    face.set_fill_color('yellow')
    cx, cy = center
    leftEye = Circle(win, radius / 20, (cx - radius / 2, cy - radius / 2))
    leftEye.set_fill_color('black')
    rightEye = Circle(win, radius / 20, (cx + radius / 2, cy - radius / 2))
    rightEye.set_fill_color('black')
    mouth = Rectangle(win, radius, radius / 8, (cx, cy + radius / 4))
    return [face, leftEye, rightEye, mouth]


def drawSmiley(win, radius, center):
    """ draw a smiley face centered at center, with radius """
    face = Circle(win, radius, center)
    face.set_fill_color('yellow')
    cx, cy = center
    leftEye = Circle(win, radius / 20, (cx - radius / 2, cy - radius / 2))
    leftEye.set_fill_color('black')
    rightEye = Circle(win, radius / 20, (cx + radius / 2, cy - radius / 2))
    rightEye.set_fill_color('black')
    mouth = Rectangle(win, radius, radius / 8, (cx, cy + radius / 4))
    win.add(face)
    win.add(leftEye)
    win.add(rightEye)
    win.add(mouth)


def add_all(win, objects):
    """ given a list of objects, add all of them to the window """
    for obj in objects:
        win.add(obj)


def move_all(objects, dx, dy):
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
        add_all(win, smile)
    for _ in range(100):
        for smile in smileys:
            dx, dy = rnd(10) - 5, rnd(10) - 5
            move_all(smile, dx, dy)
        yield 20


def program(win):
    RunWithYieldDelay(win, first(win))


StartGraphicsSystem(program)
