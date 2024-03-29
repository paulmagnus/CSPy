#------------------------------------------------------------------------------#
# cspy_searchbox.py                                                            #
#                                                                              #
# This file contains a single class SearchBox which is a window that pops up   #
# when the user presses the button "Find" or "Ctrl+F" to search for string.    #
#                                                                              #
# Written by Ines Ayara '20, Paul Magnus, Matthew R. Jenkins '20               #
# Summer 2017                                                                  #
#------------------------------------------------------------------------------#

# TKINTER MODULES
from Tkinter import *
from ttk import*

#------------------------------------------------------------------------------#
# class SearchBox                                                              #
#    Attributes:                                                               #
#        - text  : Tkinter Customized text widget                              #
#        - prev  : Optional parameter for find previous                        #
#        - next  : Optional parameter for find next                            #
#        - root  : Tk()                                                        #
#        - entry : Tkinter entry widget                                        #
#                                                                              #
#    Methods:                                                                  #
#        - config/remove tags : Dealing with tags                              #
#        - get_text           : Returns search text                            #
#        - button_1           : Binding on left mouse click                    #
#        - key_release        : On key release, highlights matching strings    #
#        - key_control_w      : Closes the search box                          #
#------------------------------------------------------------------------------#

class SearchBox:

    def __init__(self, text, prev=0, next=0):
        self.text = text  
        self.prev = prev  #For Find previous
        self.next = next  #For Find next
        self.root = Tk()  #Window
        self.root.title("Find ")
        self.entry = Entry(self.root) #Tkinter entry widget
        self.root.geometry("180x25")
        self.entry.focus()
        self.entry.pack()
        self.config_tags()
        self.entry.config(background="white",
                          foreground="black",
                          font=("Monospace", 13))
        self.entry.bind('<KeyRelease>', self.key_release)
        self.entry.bind('<Control-w>', self.key_control_w) #Close the searchbox
        self.text.bind('<Button-1>', self.button_1)

    def config_tags(self):
        self.text.tag_configure("search", background="#A9A9A9")

    def remove_tags(self, start, end):
        self.text.tag_remove("search", 1.0, END)

    #--------------------------------------------------------------------------#
    # get_text() -> entry_text : string                                        #
    #   returns the text entered by the user                                   #
    #--------------------------------------------------------------------------#
    def get_text(self):
        entry_text = self.entry.get()
        return entry_text

    def button_1(self, key):
        self.remove_tags("1.0", END)

    #--------------------------------------------------------------------------#
    # On every key release, it highlights any string in the current text widget#
    # that matches the string entered by the user.                             #
    #--------------------------------------------------------------------------#
    def key_release(self, key):
        self.remove_tags("1.0", END)
        search_text = self.get_text()

        # The user clicked on Find previous
        if self.prev == 1:
            index = self.text.index(INSERT)
            start = 1.0
            count = 0
            while True:
                countVar = StringVar()
                pos = self.text.search(search_text,
                                             start,
                                             stopindex=index,
                                             count=countVar,
                                             regexp=True)
                if not pos:
                    break
                else:
                    last_pos = pos
                    last_countVar = countVar
                    count += 1

                start = pos + "+1c"
            if count > 0:
                self.text.tag_add("search",
                                        last_pos,
                                        "%s+%sc" % (last_pos,
                                                    last_countVar.get()))
        # The user clicked on Find next
        elif self.next == 1:
            index = self.text.index(INSERT)
            start = index

            countVar = StringVar()
            pos = self.text.search(search_text,
                                         start,
                                         stopindex=END,
                                         count=countVar,
                                         regexp=True)

            if not pos:
                pass

            else:
                self.text.tag_add("search",
                                        pos,
                                        "%s+%sc" % (pos, countVar.get()))
        # The user clicked on Find/ Ctrl+F
        else:

            start = 1.0
            while True:
                countVar = StringVar()
                pos = self.text.search(search_text,
                                             start,
                                             stopindex=END,
                                             count=countVar,
                                             regexp=True)
                if not pos:
                    break
                else:
                    self.text.tag_add("search",
                                            pos,
                                            "%s+%sc" % (pos, countVar.get()))
                start = pos + "+1c"

    #--------------------------------------------------------------------------#
    #                           Close the search box                           #
    #--------------------------------------------------------------------------#
    def key_control_w(self, key):
        self.remove_tags("1.0", END)
        self.root.destroy()
