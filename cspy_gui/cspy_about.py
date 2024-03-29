#------------------------------------------------------------------------------#
# cspy_about.py                                                                #
# This program creates a new Tkinter window and displays information about     #
# CSPy, the editor, and the graphics library.                                  #
#                                                                              #
# Written by Paul Magnus '18, Ines Ayara '20, Matthew R. Jenkins '20           #
# Summer 2017                                                                  #
#------------------------------------------------------------------------------#

# PYTHON MODULES
from Tkinter import *
from PIL import Image, ImageTk
# from Image import Image, ImageTk

#------------------------------------------------------------------------------#
# class About                                                                  #
#   This class is a Tkinter window that contains information about the         #
#   development of CSPy, the editor, and the graphics library.                 #
#------------------------------------------------------------------------------#

class About:
    def __init__(self):
        # Make the window
        self.root = Toplevel()
        self.root.title("About CSPy")

        # CSPy Image Logo
        self.img = ImageTk.PhotoImage(Image.open(
                "/home/acampbel/CSPy-shared/ulysses/cspy_gui/CSPy Logo.png"))
        self.about = Label(self.root, image=self.img)
        self.about.image = self.img
        self.about.pack()

        # 5 text labels
        self.text = Label(self.root,
                          text="Developed by Eric Collins '17 and Alex Dennis" +
                          " '18 (Summer 2015), Lyndsay LaBarge '17 and Maya" +
                          " Montgomery '18 (Summer 2016), Paul Magnus '18," +
                          " Ines Ayara '20' and Matthew R. Jenkins '20 " +
                          "(Summer 2017), under the guidance of Alistair " + 
                          "Campbell.",
                          font=("Monospace", 10), wraplength=350)
        self.text.pack()

        self.text = Label(self.root,
                           text="Questions, comments, or concerns should be" +
                           " directed to: pmagnus@hamilton.edu," +
                           " iayara@hamilton.edu, mjenkins@hamilton.edu," +
                           " and/or acampbel@hamilton.edu.",
                           font=("Monospace", 10), wraplength=350)
        self.text.pack()

        self.text = Label(self.root,
                          text="Released in 2017, under the GNU General " +
                          "Public License.",
                           font=("Monospace", 10),
                           wraplength=350)
        self.text.pack()

        # Close button
        self.okay = Button(self.root, text="Close", command=self.root.destroy)
        self.okay.pack()
