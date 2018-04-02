from cs110graphics import *
import random

def colorGen():
    def r():
        return random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())


def main(Window):
    list = []

    # making one object of each type
    circ = Circle(Window)
    list.append(circ)
    rect = Rectangle(Window)
    list.append(rect)
    square = Square(Window)
    list.append(square)
    oval = Oval(Window)
    list.append(oval)
    polygon = Polygon(Window, [(200, 250), (250, 150), (150, 150)])
    list.append(polygon)
    text = Text(Window, "Hello, world!")
    list.append(text)
    image = Image(Window, "Lenna.png")
    list.append(image)

    print("\n\tAdding...")
    # removing
    for item in list:
        print item, item._tag
        Window.add(item)

    print("\n\tChanging size of image...")
    print item, item._tag
    list[6].resize(200, 200)

    print("\n\tChanging parameters of text...")
    print item, item._tag
    list[5].set_text("The quick brown fox jumps over the lazy dog.")
    list[5].set_size(24)

    print("\n\tChanging parameters of circle and square...")
    print item, item._tag
    list[0].set_radius(100)
    list[2].set_side_length(100)

    print("\n\tChanging parameters of oval and rectangle...")
    print item, item._tag
    list[1].set_side_lengths(100, 150)
    list[3].set_radii(100, 150)

    print("\n\tSetting Fill Color (if applicable)...")
    # setting fill color
    for item in list:
        print item, item._tag
        if isinstance(item, Fillable):
            item.set_fill_color(colorGen())
            print(item.get_fill_color())

    print("\n\tSetting Border Color (if applicable)...")
    # setting border color
    for item in list:
        print item, item._tag
        if isinstance(item, Fillable):
            item.set_border_color(colorGen())
            print(item.get_border_color())

    print("\n\tMoving 100 pixels to left, 100 pixels up...")
    # move
    for item in list:
        print item, item._tag
        item.move(-100, -100)

    print("\n\tMoving to 200, 200...")
    # moveTo
    for item in list:
        print item, item._tag
        item.move_to((200, 200))

    print("\n\tRotating...")
    # rotating
    for item in list:
        print item, item._tag
        if isinstance(item, Fillable) or isinstance(item, Image):
            item.rotate(90)

    print("\n\tScaling...")
    # scaling
    for item in list:
        print item, item._tag
        if isinstance(item, Fillable) or isinstance(item, Image):
            item.scale(1.5)

    print("\n\tSetting depth of each object depending on add order...")
    i = 0
    for item in list:
        print item, item._tag
        item.set_depth(i)
        i += 1

    print("\n\tSetting depth of each object in reversed add order...")
    i = len(list) - 1
    for item in list:
        print item, item._tag
        item.set_depth(i)
        i -= 1

    print("\n\tRemoving...")
    # removing
    for item in list:
        print item, item._tag
        Window.remove(item)


StartGraphicsSystem(main)
