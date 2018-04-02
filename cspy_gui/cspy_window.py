#------------------------------------------------------------------------------#
# cspy_window                                                                  #
#                                                                              #
# This file contains a single class App which represents the window.           #
#                                                                              #
# Written by Ines Ayara '20, Paul Magnus '18, Matthew R. Jenkins '20           #
# Summer 2017                                                                  #
#------------------------------------------------------------------------------#

# TKINTER MODULES
from Tkinter import *
from ttk import *
from tkFileDialog import askopenfile

# LOCAL MODULES
from cspy_texteditor import *
from cspy_statusbar import *
from cspy_notebook import *
from cspy_menu import *
import cspy_frame


class App:

    def __init__(self):
        self.root = Tk()
        self.root.geometry("710x450")          # Width corresponds to 79 chars
        self.root.title("CSPy Text Editor")
        self.root.minsize(width=1, height=450)
        self.root.maxsize(width=710, height=2000)
        
        self.notebook = CustomNotebook(self.root)
        self.frame = cspy_frame.CustomFrame(self.root, self.notebook)
        self.frame.linenumbers.redraw()
        self.notebook.add(child=self.frame,
                          text="Untitled")
        self.notebook.pack()
        self.menubar = Menubar(self.root, self.notebook)
        self.root.config(menu=self.menubar)
        self.set_global_bindings()
        self.root.mainloop()
        
    def get_root(self):
        return self.root

#------------------------------------------------------------------------------#
#                                   Key bindings                               #
#------------------------------------------------------------------------------#

    def set_global_bindings(self):

        bindings = {
            "<Control-f>" : self.key_control_f,
            "<Control-n>" : self.key_control_n,
            "<Control-o>" : self.key_control_o,
            "<Control-q>" : lambda _ : self.root.destroy(),
            "<Control-r>" : self.key_control_r,
            "<Control-s>" : self.key_control_s,
            "<Control-S>" : self.key_control_shift_s,
            "<Control-w>" : self.key_control_w,
            }

        for binding in bindings:
            self.root.bind_all(binding, bindings[binding])

    #----------------------------------------------------------------------#
    #                               New                                    #
    #----------------------------------------------------------------------#

    def key_control_n(self, key):
        # create a new empty tab
        self.notebook.new_tab()

    #----------------------------------------------------------------------#
    #                               Open                                   #
    #----------------------------------------------------------------------#

    def key_control_o(self, key):
        f = askopenfile(parent=self.root,
                        mode='rb',
                        title="Select a file",
                        filetypes=[("CSPy files", "*.cspy"),])

        if f is not None:
            self.notebook.new_tab(f)

    #----------------------------------------------------------------------#
    #                               Find                                   #
    #----------------------------------------------------------------------#

    def key_control_f(self, key):
        """ Search function """
        textbox = self.notebook.get_current_textbox()
        
        # search only works with a tab open
        if textbox is not None:
            SearchBox(textbox)

    #----------------------------------------------------------------------#
    #                               Save                                   #
    #----------------------------------------------------------------------#

    def key_control_s(self, key):
        """ Save key binding """
        textbox = self.notebook.get_current_textbox()

        # save only works with a tab open
        if textbox is not None:
            textbox.save()

    #----------------------------------------------------------------------#
    #                              Save As                                 #
    #----------------------------------------------------------------------#

    def key_control_shift_s(self, key):
        """ 'Save as' key binding """
        textbox = self.notebook.get_current_textbox()
        
        # save as only works with a tab open
        if textbox is not None:
            textbox.save_as()

    #----------------------------------------------------------------------#
    #                            Close Tab                                 #
    #----------------------------------------------------------------------#
    
    def key_control_w(self, key):
        """ Close tab """
        self.notebook.close_tab()

    #----------------------------------------------------------------------#
    #                               Run                                    #
    #----------------------------------------------------------------------#

    def key_control_r(self, key):
        textbox = self.notebook.get_current_textbox()

        # run only works with a tab open
        if textbox is not None:
            textbox.save()
            filename = textbox.filename

            if filename == None or filename == "Untitled":
                return
            
            def runCSPyProgram(cspy_file_name):
                script_dir = os.path.dirname(os.path.realpath(__file__))
                os.system(script_dir + "/../bin/.cspy_terminal.sh " +
                          cspy_file_name)

            thread = threading.Thread(target=runCSPyProgram, args=(filename,))
            thread.setDaemon(True)
            thread.start()
