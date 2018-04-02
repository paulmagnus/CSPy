#------------------------------------------------------------------------------#
# cspy_notebook.py                                                             #
#                                                                              #
# This file contains a single class CustomNotebook which is an extension on    #
# the standard ttk notebook.                                                   #
#                                                                              #
# Written by Paul Magnus '18, Ines Ayara '20, Matthew R. Jenkins '20           #
# Summer 2017                                                                  #
#------------------------------------------------------------------------------#

# PYTHON MODULES
from Tkinter import *
from ttk import*
import os

# LOCAL FILES
import cspy_frame
import solarized

#------------------------------------------------------------------------------#
# class Custom Notebook                                                        #
#     Attributes:                                                              #
#         - root             : The main window                                 #
#         - theme            : string theme color                              #
#         - _active          : boolean for whether the notebook is active      #
#                                                                              #
#     Methods:                                                                 #
#      - set_theme           : changes the color theme                         #
#      - get_theme           : returns the color theme                         #
#      - on_close_press      : called when the tab close button is pressed     #
#      - on_close_release    : called when the tab close button is released    #
#      - __initialize_custom_style : creates styles for widget                 #
#      - get_current_textbox : returns the current text widget                 #
#      - get_current_statusbar : returns the current statusbar widget          #
#      - get_current_linenumbers : returns the current linenumbers widget      #
#      - get_current_frame   : returns the current CustomFrame widget          #
#      - new_tab             : creates a new tab                               #
#      - close_tab           : closes the current tab                          #
#------------------------------------------------------------------------------#
class CustomNotebook(Notebook):
    """A ttk Notebook with close buttons on each tab"""
    __initialized = False

    def __init__(self, root, *args, **kwargs):

        self.root = root
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "Dark.CustomNotebook"
        Notebook.__init__(self, root, *args, **kwargs)
        self._active = None
        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)
        self.theme = solarized.BASE03

#------------------------------------------------------------------------------#
#                                    THEME                                     #
#------------------------------------------------------------------------------#

    #---------------------------------------------------------------------#
    # set_theme(theme : string)                                           #
    #   Changes the color theme to 'theme'                                #
    #   Themes are:                                                       #
    #   solarized.BASE03                                                  #
    #   solarized.BASE3                                                   #
    #---------------------------------------------------------------------#
    def set_theme(self, theme):
        self.theme = theme
        
        # Dark theme
        if theme == solarized.BASE03:
            c1 = solarized.BASE03
            c2 = solarized.BASE3
            self.configure(style = "Dark.CustomNotebook")

        # Light theme
        else:
            c1 = solarized.BASE3
            c2 = solarized.BASE03
            self.configure(style = "Light.CustomNotebook")

        # Pass theme to all tabs
        for tab, frame in self.children.iteritems():
            if isinstance(frame, cspy_frame.CustomFrame):
                frame.text.set_theme(c1, c2, c2)
                frame.linenumbers.set_theme(c1)
    
    #---------------------------------------------------------------------#
    # get_theme() -> string                                               #
    #   Returns the color theme                                           #
    #---------------------------------------------------------------------#
    def get_theme(self):
        return self.theme

#------------------------------------------------------------------------------#
#                                 STYLES                                       #
#------------------------------------------------------------------------------#

    #---------------------------------------------------------------------#
    # on_close_press(event : Event)                                       #
    #   This is called when the tab close button is pressed. This changes #
    #   the button to a blue x rather than a grey x.                      #
    #---------------------------------------------------------------------#
    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""
        element = self.identify(event.x, event.y)
        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index

    #---------------------------------------------------------------------#
    # on_close_release(event : Event)                                     #
    #   This is called when the tab close button is released. This        #
    #   closes the tab if the close button was clicked, otherwise changes #
    #   the close button to a grey x.                                     #
    #---------------------------------------------------------------------#
    def on_close_release(self, event):
        """Called when the button is released over the close button"""
        if not self.instate(['pressed']):
            return

        element = self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))

        if "close" in element and self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

            if not self.get_current_frame():
                self.new_tab()
        self.state(["!pressed"])
        self._active = None

    #---------------------------------------------------------------------#
    # __initialize_custom_style()                                         #
    #   This creates the styles for the notebook                          #
    #---------------------------------------------------------------------#
    def __initialize_custom_style(self):
        self.style = Style()
        self.style.theme_create("notebook_theme", parent="alt", settings={
                "CustomNotebook" : { "configure" :
                                         {"tabmargins" : [2, 5, 2, 0] } },

                # General tab settings
                "CustomNotebook.Tab" : {
                    "configure" : { "padding" : [5, 1], "relief" : "flat" },
                    "map" : { "expand" : [("selected", [1, 3, 1, 0])] }
                    },

                # Dark theme
                "Dark.CustomNotebook.Tab" : {
                    "configure" : { "background" : solarized.BASE02,
                                    "foreground" : solarized.BASE3 },
                    "map" : { "background" : [("selected", solarized.BASE03)] }
                    },

                # Light theme
                "Light.CustomNotebook.Tab" : {
                    "configure" : { "background" : solarized.BASE2,
                                    "foreground" : solarized.BASE03 },
                    "map" : { "background" : [("selected", solarized.BASE3)] }
                    }
                })

        self.style.theme_use("notebook_theme")

        # load close button images
        path = os.path.dirname(os.path.realpath(__file__))
        self.images = (
            PhotoImage("img_close", file=path + "/greyX.gif"),
            PhotoImage("img_closeactive", file=path + "/greyX.gif"),
            PhotoImage("img_closepressed", file=path + "/blueX.gif")
        )

        self.style.element_create("close", "image", "img_close",
                                  ("active", "pressed", "!disabled",
                                   "img_closepressed"),
                                  ("active", "!disabled",
                                   "img_closeactive"),
                                  border=10, sticky='e')

        # set style layout
        self.style.layout("CustomNotebook", [("CustomNotebook.client",
                                              {"sticky": "nswe"})])
        self.style.layout("CustomNotebook.Tab", [
                ("CustomNotebook.tab", {
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.padding", {
                                    "side": "top",
                                    "sticky": "nswe",
                                    "children": [
                                        ("CustomNotebook.focus", {
                                                "side": "top",
                                                "sticky": "nswe",
                                                "children": [
                                                    ("CustomNotebook.label",
                                                     {"side": "left",
                                                      "sticky": ''}),
                                                    ("CustomNotebook.close",
                                                     {"side": "left",
                                                      "sticky": ''}),
                                                    ]})]})]})])

#------------------------------------------------------------------------------#
#                                 WIDGETS                                      #
#------------------------------------------------------------------------------#

    #---------------------------------------------------------------------#
    # get_current_textbox() -> Text_editor                                #
    #   Returns the current text widget                                   #
    #---------------------------------------------------------------------#
    def get_current_textbox(self):
        current_frame = self.get_current_frame()
        if current_frame == None:
            return None
        return current_frame.text

    #---------------------------------------------------------------------#
    # get_current_statusbar() -> StatusBar                                #
    #   Returns the current status bar                                    #
    #---------------------------------------------------------------------#
    def get_current_statusbar(self):
        current_frame = self.get_current_frame()
        if current_frame is None:
            return None
        return current_frame.statusbar

    #---------------------------------------------------------------------#
    # get_current_linenumbers() -> TextLineNumers                         #
    #   Returns the current linenumbers widget                            #
    #---------------------------------------------------------------------#
    def get_current_linenumbers(self):
        current_frame = self.get_current_frame()
        if current_frame is None:
            return None
        return current_frame.linenumbers

    #---------------------------------------------------------------------#
    # get_current_frame() -> CustomFrame                                  #
    #   Returns the current frame widget                                  #
    #---------------------------------------------------------------------#
    def get_current_frame(self):

        try:
            ID = self.select().split('.')[2]
            current_frame = self.children[ID]
        except IndexError:
            return None
        return current_frame
    
#------------------------------------------------------------------------------#
#                               TAB INTERACTIONS                               #
#------------------------------------------------------------------------------#

    #----------------------------------------------------------------------#
    # new_tab(f = None : ?file)                                            #
    #   This creates a new tab in the notebook                             #
    #----------------------------------------------------------------------#
    def new_tab(self, f=None):
        """ Creates a new tab in the notebook
        
        'f' is the file to be loaded into the new texteditor widget
        """
        new_page = cspy_frame.CustomFrame(self.root, self)
        new_page.linenumbers.redraw()
        
        if f is None:
            filename = "Untitled"
        else:
            filename = f.name

        self.add(child=new_page, text=filename)

        self.select(new_page)
        self.root.update()
        
        new_page.get_text_widget().filename = filename
        
        # Theme update
        curr_text = new_page.get_text_widget()
        curr_linenumbers = new_page.linenumbers
        
        if self.get_theme() == solarized.BASE03:
            curr_text.set_theme(solarized.BASE03,
                                solarized.BASE3,
                                solarized.BASE3)
            curr_linenumbers.set_theme(solarized.BASE03)
        else:
            curr_text.set_theme(solarized.BASE3,
                                solarized.BASE03,
                                solarized.BASE03)
            curr_linenumbers.set_theme(solarized.BASE3)
            
        if f is not None:
            # read in file
            t = f.read()
            new_page.get_text_widget().insert("1.0", t)
            cline = 1
            while cline != int(new_page.get_text_widget().
                               index(END).split('.')[0]):
                curr_text.syn_highlight(cline)
                cline += 1
            f.close()

    def close_tab(self):
        """ Closes the current tab if there is a tab left """
        if self.select():
            self.forget(self.select())
            self.event_generate("<<NotebookTabClosed>>")            

        # add an empty tab if the last tab is deleted
        if not self.get_current_frame():
            self.new_tab()
