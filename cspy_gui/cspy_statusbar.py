#------------------------------------------------------------------------------#
# cspy_statusbar.py                                                            #
#                                                                              #
# This file contains a single class StatusBar which is an extension on the     #
# standard tkinter frame.                                                      #
#                                                                              #
# Written by Ines Ayara '20, Paul Magnus '18, and Matthew R. Jenkins '20       #
# Summer 2017                                                                  #
#------------------------------------------------------------------------------#

# TKINTER MODULES
from Tkinter import *
from ttk import*

#------------------------------------------------------------------------------#
# class statusBar                                                              #
#    Attributes:                                                               #
#        - variable   : StringVar                                              #
#        - label      : Tkinter standard label                                 #
#        - notebook   : CustomNotebook                                         #
#                                                                              #
#    Methods:                                                                  #
#        - set        : Updates the status bar                                 #
#        - clear      : Clears the status bar                                  #
#        - lineCol    : Updates the line/col numbers                           #
#        - set_text   : Changes the word "CSPy" to "Saved"                     #
#        - reset_text : Changes the word "Saved" back to "CSPy"                #
#------------------------------------------------------------------------------#


class StatusBar(Frame):

    def __init__(self, master, notebook):
        Frame.__init__(self, master)
        self.variable = StringVar()
        self.variable.set('    Line:1' + ', Column:1' +
                          '                                    ' +
                          '     ' + 'CSPy')

        s = Style()
        # Configure style features
        s.configure("BW.TLabel",
                    foreground="white",
                    background="#575757",
                    padding=2,
                    relief="flat",
                    bd=0,
                    highlightthickness=0)

        self.label = Label(self,
                           textvariable=self.variable,
                           font=("Monospace", 12),
                           style="BW.TLabel")

        self.label.pack(fill=X)
        self.pack(side=BOTTOM, fill=X)

        # The status bar knows about the notebook
        self.notebook = notebook

    # This method is responsible for updating the status bar
    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

    # Updates the lin/col numbers from the cursor's position
    def lineCol(self, line, col):
        self.variable.set('    Line:' + str(line) + ', Column:' + str(col) +
                          '                                    ' +
                          '     ' + 'CSPy')
    #--------------------------------------------------------------------------#
    # Changes the word "CSPy" to "Saved" when the user clicks on Save, Save as,#
    # or Run. It is also changed when the user uses any of the shortcuts:      #
    # Ctrl+S/ Shift+Ctrl+S/Ctrl+R                                              #
    #--------------------------------------------------------------------------#
    def set_text(self):
        current_frame = self.notebook.children[
            self.notebook.select().split('.')[2]]
        for key, val in current_frame.children.iteritems():
            if isinstance(val, Text):
                text = val

        index = text.index("insert")
        self.variable.set('    Line:' + str(index.split('.')[0]) +
                          ', Column:' + str(index.split('.')[1]) +
                          '                                    ' +
                          '     ' + "Saved")

    #--------------------------------------------------------------------------#
    #                Changes the word "Saved" back to "CSPy"                   #
    #--------------------------------------------------------------------------#
    def reset_text(self):
        current_frame = self.notebook.children[
            self.notebook.select().split('.')[2]]
        for key, val in current_frame.children.iteritems():
            if isinstance(val, Text):
                text = val

        index = text.index("insert")
        self.variable.set('    Line:' + str(index.split('.')[0]) +
                          ', Column:' + str(index.split('.')[1]) +
                          '                                    ' +
                          '     ' + "CSPy")
