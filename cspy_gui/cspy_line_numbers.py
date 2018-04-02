#------------------------------------------------------------------------------#
# cspy_line_numbers                                                            #
# This file contains one class, TextLineNumbers. This is used to show the line #
# numbers of the text widget at the beginning of each line.                    #
#                                                                              #
# Written by Paul Magnus '18, Ines Ayara '20, Matthew R. Jenkins '20           #
# Summer 2017                                                                  #
#------------------------------------------------------------------------------#

# PYTHON MODULES
from Tkinter import *
from ttk import *

# LOCAL FILES
import solarized

#------------------------------------------------------------------------------#
#  class TextLineNumbers                                                       #
#     Attributes:                                                              #
#         - theme       : Color code (Dark/Light)                              #
#         - font        : Font size (int)                                      #
#         - textwidget  : Tkinter text widget                                  #
#                                                                              #
#     Methods:                                                                 #
#         - set_theme   : Set/configure color theme for the line num canvas    #
#         - get_theme   : Return theme color code                              #
#         - attach      : Set textwidget attribute to the current text widget  #
#         - redraw      : Updates the line numbers on the canvas               #
#------------------------------------------------------------------------------#

# Themes
DARK = solarized.BASE03
LIGHT = solarized.BASE3

class TextLineNumbers(Canvas):

    #---------------------------------------------------------------------#
    # __init__(frame : CustomFrame, font : string)                        #
    #---------------------------------------------------------------------#
    def __init__(self, frame, font):
        Canvas.__init__(self, frame)
        self.theme = DARK
        self.config(background=self.theme,
                    bd=0,
                    highlightthickness=0,
                    relief='ridge',
                    width=55)
        self.font = font
        self.textwidget = None
    
    #---------------------------------------------------------------------#
    # set_theme(theme : string)                                           #
    #   Set/configure color theme for the line num canvas.                #
    #   Standard themes:                                                  #
    #   solarized.BASE03 = "002b36"                                       #
    #   solarized.BASE3  = "fdf6e3"                                       #
    #---------------------------------------------------------------------#
    def set_theme(self, theme):
        self.theme = theme
        self.config(background=self.theme)

    #---------------------------------------------------------------------#
    # get_theme() -> string                                               #
    #   Return the color code of the theme                                #
    #---------------------------------------------------------------------#
    def get_theme(self):
        return self.theme

    #---------------------------------------------------------------------#
    # attach(text_widget : Text_editor)                                   #
    #   Set textwidget attribute to the current text widget               #
    #---------------------------------------------------------------------#
    def attach(self, text_widget):
        self.textwidget = text_widget

    #---------------------------------------------------------------------#
    # redraw()                                                            #
    #   Updates the line numbers on the canvas                            #
    #---------------------------------------------------------------------#
    def redraw(self):
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(40, y,
                             anchor="ne",
                             text=linenum,
                             font=("Monospace", self.font),
                             fill="#808080")
            i = self.textwidget.index("%s+1line" % i)
