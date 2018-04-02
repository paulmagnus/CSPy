#------------------------------------------------------------------------------#
# cspy_menu.py                                                                 #
#                                                                              #
# This file contains a single class Menubar which is an extension on the       #
# standard tkinter menu.                                                       #
#                                                                              #
# Written by Ines Ayara '20, Paul Magnus '18, Matthew R. Jenkins '20           #
# Summer 2017                                                                  #
#------------------------------------------------------------------------------#

# TKINTER MODULES
from Tkinter import *
from ttk import*
from tkFileDialog import *
from tkMessageBox import *

# PYTHON MODULES
import keyword
import re
import threading
import os
import webbrowser

# LOCAL FILES
from cspy_searchbox import *
from cspy_texteditor import *
import cspy_window
import cspy_about
import solarized

# THEMES
DARK = solarized.BASE03
LIGHT = solarized.BASE3

#------------------------------------------------------------------------------#
# class Menubar                                                                #
#     Attributes:                                                              #
#         - root             : Tk()                                            #
#         - notebook         : ttk widget for tab management                   #
#         - file_menu        : Contains: New/Open/Save/Save as/Close/Exit      #
#         - edit_menu        : Contains: Copy/Cut/Paste/Undo/Redo              #
#         - select_menu      : Contains: Select all/Line/Word/Undo selection   #
#         - find_menu        : Contains: Find/Find next/Find previous          #
#         - project_menu     : Contains: Run/ Submit                           #
#         - preference_menu  : Contains: Change theme/Larger/Smaller font      #
#         - help_menu        : Contains: Documentation/Ask a TA/About          #
#                                                                              #
#     Methods:                                                                 #
#         - get_text_box     : Returns the current text widget                 #
#         - get_line_numbers : Returns the current line number canvas          #
#         - Syn_highlight    : A function that takes care of syn highlighting  #
#         - All menu functions mentioned above                                 #
#------------------------------------------------------------------------------#

class Menubar(Menu):

    def __init__(self, root, notebook):

        Menu.__init__(self, root)
        self.root = root
        self.notebook = notebook
        self.config(font=("Corbert", 12))

                           #-------------------------#
                           #           File          #
                           #-------------------------# 
        self.filemenu = Menu(self, tearoff=0)
        self.filemenu.add_command(label="New File...            Ctrl+N",
                                  command=self.new_file)
        self.filemenu.add_command(label="Open File...          Ctrl+O",
                                  command=self.open_file)
        self.filemenu.add_command(label="Close file            Ctrl+W",
                                  command=self.close_file)
        self.filemenu.add_command(label="Save                   Ctrl+S",
                                  command=self.save_file)
        self.filemenu.add_command(label="Save as...    Shift+Ctrl+S",
                                  command=self.saveas)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit                     Ctrl+Q",
                                  command=self.exit)
        self.add_cascade(label="File ", menu=self.filemenu)
        self.filemenu.config(font=("Corbert", 11), bg="#FFFFFF")

                           #--------------------------#
                           #       Edit Menu          #
                           #--------------------------#
        self.editmenu = Menu(self, tearoff=0)
        self.editmenu.add_command(label="Copy            Ctrl+C",
                                  command=lambda: self.copy
                                  (self.get_textbox()))
        self.editmenu.add_command(label="Cut               Ctrl+X",
                                  command=lambda: self.cut
                                  (self.get_textbox()))
        self.editmenu.add_command(label="Paste            Ctrl+V",
                                  command=lambda: self.paste
                                  (self.get_textbox()))
        self.filemenu.add_separator()
        self.editmenu.add_command(label="Undo            Ctrl+Z",
                                  command=lambda: self.undo
                                  (self.get_textbox()))
        self.editmenu.add_command(label="Redo            Ctrl+Y",
                                  command=lambda: self.redo
                                  (self.get_textbox()))
        self.add_cascade(label="Edit ", menu=self.editmenu)
        self.editmenu.config(font=("Corbert", 11), bg="#FFFFFF")

                           #--------------------------#
                           #       Selection Menu     #
                           #--------------------------#
        self.selectmenu = Menu(self, tearoff=0)
        self.selectmenu.add_command(label="Select All          " +
                                    "                         Ctrl+A",
                                    command=lambda: self.select_all
                                    (self.get_textbox()))
        self.selectmenu.add_command(label="Expand selection to line" +
                                    "             Ctrl+L",
                                    command=lambda: self.select_line
                                    (self.get_textbox()))
        self.selectmenu.add_command(label="Expand selection to word" +
                                    "           Ctrl+D",
                                    command=lambda: self.select_word
                                    (self.get_textbox()))
        self.selectmenu.add_command(label="Undo selection",
                                    command=lambda: self.undo_selection
                                    (self.get_textbox()))
        self.add_cascade(label="Selection ", menu=self.selectmenu)
        self.selectmenu.config(font=("Corbert", 11), bg="#FFFFFF")

                           #--------------------------#
                           #        Find Menu         #
                           #--------------------------#
        self.findmenu = Menu(self, tearoff=0)
        self.findmenu.add_command(label="Find            Ctrl+F",
                                  command=lambda: SearchBox
                                  (self.get_textbox()))
        self.findmenu.add_command(label="Find next",
                                  command=lambda: SearchBox
                                  (self.get_textbox(), 0, 1))
        self.findmenu.add_command(label="Find previous",
                                  command=lambda: SearchBox
                                  (self.get_textbox(), 1, 0))
        self.add_cascade(label="Find ", menu=self.findmenu)
        self.findmenu.config(font=("Corbert", 11), bg="#FFFFFF")

                           #--------------------------#
                           #       Project Menu       #
                           #--------------------------#
        self.projmenu = Menu(self, tearoff=0)
        self.projmenu.add_command(label="Run Code         Ctrl+R",
                                  command=self.run)
        self.projmenu.add_command(label="Submit Code",
                                  command=self.submit)
        self.add_cascade(label="Project ", menu=self.projmenu)
        self.projmenu.config(font=("Corbert", 11), bg="#FFFFFF")

                           #--------------------------#
                           #    Preferences Menu      #
                           #--------------------------#
        self.prefmenu = Menu(self, tearoff=0)
        self.prefmenu.add_command(label="Change theme",
                                  command=lambda: self.change_theme())
        self.prefmenu.add_command(label="Larger font",
                                  command=lambda: self.larger_font
                                  (self.get_textbox(), self.get_line_numbers()))
        self.prefmenu.add_command(label="Smaller font",
                                  command=lambda: self.smaller_font
                                  (self.get_textbox(), self.get_line_numbers()))
        self.add_cascade(label="Preferences ", menu=self.prefmenu)
        self.prefmenu.config(font=("Corbert", 11), bg="#FFFFFF")

                           #--------------------------#
                           #        Help Menu         #
                           #--------------------------# 
        self.helpmenu = Menu(self, tearoff=0)
        self.helpmenu.add_command(label="Documentation",
                                  command=self.link_documentation)
        self.helpmenu.add_command(label="Ask a TA",
                                  command=self.link_piazza)
        self.helpmenu.add_command(label="About CSPy",
                                  command=self.about_cspy)
        self.add_cascade(label="Help? ", menu=self.helpmenu)
        self.helpmenu.config(font=("Corbert", 11), bg="#FFFFFF")

        self.tab_paths = {}

#------------------------------------------------------------------------------#
#                          Access current tab objects                          #
#------------------------------------------------------------------------------#
    #---------------------------------------------------------------------#
    # get_current_textbox() -> Text_editor                                #
    #   Returns the current text widget                                   #
    #---------------------------------------------------------------------#
    def get_textbox(self):
        """ Returns the current text widget """
        return self.notebook.get_current_textbox()

    #---------------------------------------------------------------------#
    # get_line_numbers() -> TextLineNumers                                #
    #   Returns the current linenumbers widget                            #
    #---------------------------------------------------------------------#
    def get_line_numbers(self):
        """ Returns the current linenumbers widget """
        current_frame = self.notebook.children[
            self.notebook.select().split('.')[2]]

        return current_frame.get_linenumbers()

#------------------------------------------------------------------------------#
#                                 Edit Menu                                    #
#------------------------------------------------------------------------------#
    #--------------------------------------------------------------------#
    #                               Copy                                 #
    #--------------------------------------------------------------------#
    def copy(self, texteditor):
        texteditor.clipboard_clear()
        text = texteditor.get("sel.first", "sel.last")
        texteditor.clipboard_append(text)

    #--------------------------------------------------------------------#
    #                               Cut                                  #
    #--------------------------------------------------------------------#
    def cut(self, texteditor):
        self.copy(texteditor)
        texteditor.delete("sel.first", "sel.last")

    #--------------------------------------------------------------------#
    #                              Paste                                 #
    #--------------------------------------------------------------------#
    def paste(self, texteditor):
        text = texteditor.selection_get(selection='CLIPBOARD')
        texteditor.insert('insert', text)
        cline = 1
        while cline != int(texteditor.index(END).split('.')[0]):
            syn_highlight(texteditor, cline)
            cline += 1

    #--------------------------------------------------------------------#
    #                              Undo                                  #
    #--------------------------------------------------------------------#
    def undo(self, text):
        text.edit_undo()
    
    #--------------------------------------------------------------------#
    #                              Redo                                  #
    #--------------------------------------------------------------------#
    def redo(self, text):
        text.edit_redo()

#------------------------------------------------------------------------------#
#                             Preferences Menu                                 #
#------------------------------------------------------------------------------#
    #--------------------------------------------------------------------#
    #                     Change theme (Dark/Light)                      #
    #--------------------------------------------------------------------#
    def change_theme(self):
        if self.get_textbox().get_theme() == DARK:
            self.notebook.set_theme(LIGHT)
        else:
            self.notebook.set_theme(DARK)

    #--------------------------------------------------------------------#
    #                       Smaller font (Min: 12)                       #
    #--------------------------------------------------------------------#  
    def smaller_font(self, text, line_numbers):
        if (text.get_fontsize() > 12):
            text.config(font =("Monospace", text.get_fontsize() - 1))
            text.fontsize -= 1
            line_numbers.font -= 1
    
    #--------------------------------------------------------------------#
    #                    Larger font (Max: 15/Normal: 13)                #
    #--------------------------------------------------------------------#
    def larger_font(self, text, line_numbers):
        if (text.get_fontsize() < 15):
            text.config(font=("Monospace", text.get_fontsize() + 1))
            text.fontsize += 1 
            line_numbers.font += 1
            self.adjust_window()

    #--------------------------------------------------------------------#
    #                     Adjust window to font size                     #
    #--------------------------------------------------------------------#
    def adjust_window(self):
        self.root.geometry("790x470")
        self.root.minsize(width=1, height=470)
        self.root.maxsize(width=790, height=2000)
        self.root.update()
        
#------------------------------------------------------------------------------#
#                               Selection Menu                                 #
#------------------------------------------------------------------------------#
    #--------------------------------------------------------------------#
    #                             Select all                             #
    #--------------------------------------------------------------------#   
    def select_all(self, text):
        text.tag_remove(SEL, "1.0", END)
        text.tag_add(SEL, "1.0", END)
        text.mark_set(INSERT, END)
        text.see(INSERT)
        return 'break'

    #--------------------------------------------------------------------#
    #                            Select line                             #
    #--------------------------------------------------------------------#
    def select_line(self, text):
        cline = text.index(INSERT).split('.')[0]
        lastcol = 0
        char = text.get('%s.%d' % (cline, lastcol))
        while char != '\n':
            lastcol += 1
            char = text.get('%s.%d' % (cline, lastcol))
        text.tag_remove(SEL, INSERT, '%s.%d' % (cline, lastcol))
        text.tag_add(SEL, INSERT, '%s.%d' % (cline, lastcol))
        text.mark_set(INSERT, '%s.%d' % (cline, lastcol))
        text.see(INSERT)
        return 'break'
    
    #--------------------------------------------------------------------#
    #                           Select word                              #
    #--------------------------------------------------------------------#
    def select_word(self, text):
        cline = text.index(INSERT).split('.')[0]
        lastcol = 0
        char = text.get('%s.%d' % (cline, lastcol))
        while char != " " and  char != "\n" and\
                str(END) != str('%s.%d' % (cline, lastcol)):
            lastcol += 1
            char = text.get('%s.%d' % (cline, lastcol))
        text.tag_remove(SEL, INSERT, '%s.%d' % (cline, lastcol))
        text.tag_add(SEL, INSERT, '%s.%d' % (cline, lastcol))
        text.mark_set(INSERT, '%s.%d' % (cline, lastcol))
        text.see(INSERT)
        return 'break'
    
    #--------------------------------------------------------------------#
    #                           Undo selection                           #
    #--------------------------------------------------------------------#
    def undo_selection(self, text):
        text.tag_remove(SEL, "1.0", END)

#------------------------------------------------------------------------------#
#                                  File Menu                                   #
#------------------------------------------------------------------------------#
    #--------------------------------------------------------------------#
    #                              New file                              #
    #--------------------------------------------------------------------#
    def new_file(self):
        """ Creates a new file """

        self.notebook.new_tab()
    
    #--------------------------------------------------------------------#
    #                                Save                                #
    #--------------------------------------------------------------------#
    def save_file(self):
        textbox = self.notebook.get_current_textbox()

        # save only works with a tab open
        if textbox is not None:
            textbox.save()
    
    #--------------------------------------------------------------------#
    #                               Save as                              #
    #--------------------------------------------------------------------#
    def saveas(self):
        textbox = self.notebook.get_current_textbox()

        # save as only works with a tab open
        if textbox is not None:
            textbox.save_as()
    
    #--------------------------------------------------------------------#
    #                                Open                                #
    #--------------------------------------------------------------------#
    def open_file(self):
        f = askopenfile(parent=self.root,
                        mode='rb',
                        title="Select a file",
                        filetypes=[("CSPy files", "*.cspy"),])

        if f is not None:
            self.notebook.new_tab(f)

    #--------------------------------------------------------------------#
    #                         Close current tab                          #
    #--------------------------------------------------------------------# 
    def close_file(self):
        self.notebook.close_tab()


    #--------------------------------------------------------------------#
    #                           Exit the window                          #
    #--------------------------------------------------------------------#
    def exit(self):
        self.root.destroy()

#------------------------------------------------------------------------------#
#                                Project Menu                                  #
#------------------------------------------------------------------------------#
    #--------------------------------------------------------------------#
    #                                Run                                 #
    #--------------------------------------------------------------------#
    def run(self):
        textbox = self.notebook.get_current_textbox()

        # run only works with a tab open
        if textbox is not None:
            textbox.save()
            filename = textbox.filename

            if filename == None or filename == "Untitled":
                # save failed
                return
            
            # create process to be run
            def runCSPyProgram(cspy_file_name):
                script_dir = os.path.dirname(os.path.realpath(__file__))
                os.system(script_dir + "/../bin/.cspy_terminal.sh " +
                          cspy_file_name)

            # run program in separate thread
            thread = threading.Thread(target=runCSPyProgram, args=(filename,))
            thread.setDaemon(True)
            thread.start()

    #--------------------------------------------------------------------#
    #                                 Submit                             #
    #--------------------------------------------------------------------#
    def submit(self):
        # save the file before submission
        self.save_file()

        # get the folder path
        filename = self.notebook.tab(self.notebook.select(), "text")
        path = re.match(r'(?P<path>.*)/[^/]+', filename).group('path')

        # create submission process
        # -i : interactvie mode
        # --folder : give the folder of the submission
        def submitCSPyProgram(cspy_folder_name):
            os.system('submit_terminal -i --folder ' + cspy_folder_name)

        # run process in separate thread
        thread = threading.Thread(target=submitCSPyProgram, args=(path,))
        thread.setDaemon(True)
        thread.start()

#------------------------------------------------------------------------------#
#                                 Help Menu                                    #
#------------------------------------------------------------------------------#
    #--------------------------------------------------------------------#
    #                Opens the CSPy documentation on emacs               #
    #--------------------------------------------------------------------#
    def link_documentation(self):
        os.system('emacs /home/acampbel/CSPy-shared/ulysses/documentation/'+
                  'CSPy-general.pdf &')
    
    #--------------------------------------------------------------------#
    #         Opens Piazza's login page on a browser (Mozilla)           #
    #--------------------------------------------------------------------#
    def link_piazza(self):
        webbrowser.open('https://piazza.com/account/login')

    #--------------------------------------------------------------------#
    #                              About CSPy                            #
    #--------------------------------------------------------------------#
    def about_cspy(self):
        cspy_about.About()
    
    #--------------------------------------------------------------------------#
    #     This is a syntax highlighting method called when a                   #
    #     pre-existing file is opened in the text editor.                      #
    #                                                                          #
    #     Parameters:                                                          #
    #       - A text widget (Text_editor)                                      #
    #       - A current line index (int)                                       #
    #--------------------------------------------------------------------------#
    def syn_highlight(self, cline, text):
        """ Takes care of syntax highlighting for an opened file"""
        lastcol = 0
        char = text.get('%s.%d' % (cline, lastcol))
        while char != '\n':
            lastcol += 1
            char = text.get('%s.%d' % (cline, lastcol))
    
        buffer = text.get('%s.%d' % (cline, 0),
                          '%s.%d' % (cline, lastcol))
        tokenized = re.split("[^A-Za-z0-9_=><:*+-/]", buffer)

        text.remove_tags('%s.%d' % (cline, 0),
                         '%s.%d' % (cline, lastcol))
        
        start, end = 0, 0
        for s in tokenized:
            lst = split_string(s, [":", ",", "."])
            for token in lst:
                end = start + len(token)
                if token == "import" or token == "pyimport":
                    text.tag_add('import_kw', '%s.%d' % (cline, start), 
                                 '%s.%d' % (cline, end))
                
                elif token in keyword.kwlist:
                    text.tag_add('kw', '%s.%d' % (cline, start), 
                                 '%s.%d' % (cline, end))
            
                elif token in type_kw:
                    text.tag_add('type_kw', '%s.%d' % (cline, start),
                                 '%s.%d' % (cline, end))

                elif token in other_kw:
                    text.tag_add('other_kw', '%s.%d' % (cline, start),
                                 '%s.%d' % (cline, end))

                elif token in type_conv:
                    text.tag_add('type_conv', '%s.%d' % (cline, start),
                                 '%s.%d' % (cline, end))
            
                elif token in spec_chars:
                    text.tag_add('spec_chars', '%s.%d' % (cline, start),
                                 '%s.%d' % (cline, end))
    
                start += len(token)
            start += 1     

        #LINE COMMENT
        comment_start = buffer.find('#')
        if comment_start != -1:
            text.tag_add('line_comment', '%s.%d' % (cline, comment_start),
                         '%s.%d' % (str(int(cline) + 1), 0))
        text.tag_remove('docstring', 1.0, END)
        text.tag_remove('block_comment', 1.0, END)
        text.tag_remove('declaration_block', 1.0, END)
        text.tag_remove('string', 1.0, END)

        #BLOCK COMMENT
        start = "1.0"
        while True:
            start = text.search(r"\/\*",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break
            
            if text.get(start, start + "+2c") == "/*":
                end = text.search(r"\*\/",
                                  start + "+2c",
                                  stopindex=END,
                                  regexp=True)

            else:
                end = text.search(r'\*\/',
                                  start + "+2c",
                                  stopindex=END,
                                  regexp=True)

            if not end:
                end = END
            text.tag_add('block_comment', start, end + "+2c")

            start = end + "+2c"

        #DOCSTRING
        start = "1.0"
        while True:
            start = text.search(r"(''')|(\"\"\")",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break
            
            if text.get(start, start + "+3c") == "'''":
                end = text.search(r"'''",
                                  start + "+3c",
                                  stopindex=END,
                                  regexp=True)

            else:
                end = text.search(r'"""',
                                  start + "+3c",
                                  stopindex=END,
                                  regexp=True)

            if not end:
                end = END
            text.tag_add('docstring', start, end + "+3c")

            start = end + "+3c"

        #VAR DECLARATION
        start = "1.0"
        while True:
            start = text.search(r"::",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break

            end = text.search(r"::",
                              start + "+2c",
                              stopindex=END,
                              regexp=True)

            if not end:
                end = END
            
            text.tag_add('declaration_block',
                         start,
                         end + "+2c")

            start = end + "+2c"

        #FUNCTION
        start = "1.0"
        while True:
            start = text.search(r"def ",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break
            end = text.search(r'\(',
                              start + "+4c",
                              stopindex=END,
                              regexp=True)
            if not end:
                end = END
                
            text.tag_add('function',
                         start + "+4c",
                         end)

            start = end + "+1c"

        #CLASS
        start = "1.0"
        while True:
            start = text.search(r"class ",
                                start,
                                stopindex=END,
                                regexp=True)
            
            if not start:
                break
            
            end = text.search(r"(:)|(\()",
                              start + "+6c",
                              stopindex=END,
                              regexp=True)
            if not end:
                end = END
            
            text.tag_add('class',
                         start + "+6c",
                         end)

            start = end + "+1c"

        #STRING
        start = "1.0"
        while True:
            start = text.search(r"(')|(\")",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break
            
            if text.get(start, start + "+1c") == "'":
                end = text.search(r"'",
                                  start + "+1c",
                                  stopindex=END,
                                  regexp=True)

            else:
                end = text.search(r'"',
                                  start + "+1c",
                                  stopindex=END,
                                  regexp=True)

            if not end:
                end = END
            text.tag_add('string', start, end + "+1c")

            start = end + "+1c"
