from Tkinter import*
import lib

def main():
    root = Tk()
    f = lib.Frame()
    f.setHeight(10)
    f.setWidth(20)
    f.setBackground("red")
    f.pack()

    l = lib.Label()
    l.setWidth(50)
    l.setHeight(80)
    l.setText("Ines")
    l.setBorderWidth(3)
    l.pack()

    mainloop()


main()
