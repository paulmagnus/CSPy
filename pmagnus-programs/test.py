class C:
    def __init__(self):
        self = None

    def f(self):
        self = None

c = C()
c.f()