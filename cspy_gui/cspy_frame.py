#------------------------------------------------------------------------------#
# cspy_frame.py                                                                #
# This contains a single class, CustomFrame, which is a frame to be used       #
# inside of the tabs in the notebook widget for the CSPy editor.               #
#                                                                              #
# Written by Paul Magnus '18, Ines Ayara '20, Matthew R. Jenkins '20           #
# Summer 2017                                                                  #
#------------------------------------------------------------------------------#

# PYTHON MODULES
from Tkinter import *
from ttk import *

# LOCAL FILES
import cspy_line_numbers
import cspy_statusbar
import cspy_texteditor

#------------------------------------------------------------------------------#
# class CustomFrame                                                            #
#    Attributes:                                                               #
#        - root        : Tk()                                                  #
#        - notebook    : Notebook ttk widget                                   #
#        - statusbar   : Customized Tkinter label to display current line/ col #
#        - scrollbar   : Tkinter scrollbar                                     #
#        - text        : Customized Tkinter text widget                        #
#        - linenumbers : Canvas on the left to show the current line           #
#                                                                              #
#    Methods:                                                                  #
#        - get_text_widget : Returns the text widget                           #
#------------------------------------------------------------------------------#


class CustomFrame(Frame):

    def __init__(self, root, notebook):
        Frame.__init__(self, notebook)

        # main window
        self.root = root

        # parent
        self.notebook = notebook

        # status bar at the bottom of the frame
        self.statusbar = cspy_statusbar.StatusBar(self, self.notebook)

        # scrollbar on the right side of the frame
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)

        # text editor where code is written
        self.text = cspy_texteditor.Text_editor(self.root, self,
                                                self.notebook,
                                                self.statusbar)

        # line numbers on the left side of the text editor
        self.linenumbers = \
            cspy_line_numbers.TextLineNumbers(self, self.text.get_fontsize())
        self.linenumbers.attach(self.text)
        self.linenumbers.pack(side=LEFT, fill=Y)
        
        self.text.pack(side=RIGHT, fill=BOTH, expand=True)

        # link the scrollbar and the text editor
        self.scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)

    #---------------------------------------------------------------------#
    # get_text_widget() -> Text_editor                                    #
    #   Returns the current text widget                                   #
    #---------------------------------------------------------------------#
    def get_text_widget(self):
        return self.text

    #---------------------------------------------------------------------#
    # get_linenumbers() -> TextLineNumers                                 #
    #   Returns the current linenumbers widget                            #
    #---------------------------------------------------------------------#
    def get_linenumbers(self):
        return self.linenumbers