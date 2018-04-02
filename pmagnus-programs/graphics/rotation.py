import cmath
from Tkinter import *

def rotate(point, angle, pivot=(0,0)):
    assert isinstance(point, tuple) and len(point) == 2, \
        "Point must be an (x,y) pair"
    assert isinstance(pivot, tuple) and len(pivot) == 2, \
        "Pivot must be an (x,y) pair"

    cplx_pt = point[0] + point[1] * 1j - pivot[0] - pivot[1] * 1j
    cplx_rotation = cmath.exp(angle * 1j)

    new_pt = cplx_pt * cplx_rotation
    return (new_pt.real + pivot[0], new_pt.imag + pivot[1])

class Rectangle:
    def __init__(self, *bbox):
        assert len(bbox) == 4
        self.bbox = bbox
        
class Window:
    def __init__(self):
        self.root = Tk()
        self.title("Spin simulation")
        self.canvas = Canvas(root, width=200, height=100)
        self.canvas.pack()

    def add(self, obj):
        
        
r = Rectangle(50, 25, 150, 75)