from Tkinter import *
from ttk import*
from tkFileDialog import *
from tkMessageBox import *
import keyword
import re
import threading
import os

from cspy_searchbox import *
from cspy_texteditor import *

filename = "Untitled"


class Menubar(Menu):

    def __init__(self, root, notebook):

        Menu.__init__(self, root)
        self.root = root
        self.notebook = notebook
        self.config(font=("Corbert", 12))

        #File menu
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
        self.filemenu.add_command(label="New folder")
        self.filemenu.add_command(label="Open folder")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit                     Ctrl+Q",
                                  command=lambda: self.exit)
        self.add_cascade(label="File ", menu=self.filemenu)
        self.filemenu.config(font=("Corbert", 11), bg="#FFFFFF")

        # Edit menu
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

        # Selection menu
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

        # Find menu
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

        # Project menu
        self.projmenu = Menu(self, tearoff=0)
        self.projmenu.add_command(label="Run Code",
                                  command=self.run)
        self.projmenu.add_command(label="Submit Code")
        self.add_cascade(label="Project ", menu=self.projmenu)
        self.projmenu.config(font=("Corbert", 11), bg="#FFFFFF")

        # Preferences menu
        self.prefmenu = Menu(self, tearoff=0)
        self.prefmenu.add_command(label="Change theme",
                                  command=self.get_textbox().change_theme)
        self.prefmenu.add_command(label="Larger font",
                                  command=lambda: self.larger_font
                                  (self.get_textbox()))
        self.prefmenu.add_command(label="Smaller font",
                                  command=lambda: self.smaller_font
                                  (self.get_textbox()))
        self.add_cascade(label="Preferences ", menu=self.prefmenu)
        self.prefmenu.config(font=("Corbert", 11), bg="#FFFFFF")

        # Help menu
        self.helpmenu = Menu(self, tearoff=0)
        self.helpmenu.add_command(label="Documentation")
        self.helpmenu.add_command(label="Ask a TA")
        self.helpmenu.add_command(label="About CSPy")
        self.add_cascade(label="Help? ", menu=self.helpmenu)
        self.helpmenu.config(font=("Corbert", 11), bg="#FFFFFF")

        self.tab_paths = {}

    def get_textbox(self):
        """ Returns the current text widget """
        current_frame = self.notebook.children[
            self.notebook.select().split('.')[2]]
        for key, val in current_frame.children.iteritems():
            if isinstance(val, Text):
                textbox = val

        if textbox is None:
            print("Something is wrong!")
        return textbox

    #COPY-CUT-PASTE
    def copy(self, texteditor):
        texteditor.clipboard_clear()
        text = texteditor.get("sel.first", "sel.last")
        texteditor.clipboard_append(text)

    def cut(self, texteditor):
        self.copy(texteditor)
        texteditor.delete("sel.first", "sel.last")

    def paste(self, texteditor):
        text = texteditor.selection_get(selection='CLIPBOARD')
        texteditor.insert('insert', text)
        cline = 1
        while cline != int(texteditor.index(END).split('.')[0]):
            syn_highlight(texteditor, cline)
            cline += 1

    #UNDO-REDO
    def undo(self, text):
        text.edit_undo()

    def redo(self, text):
        text.edit_redo()

    #FONT
    def smaller_font(self, text):
        text.config(font=("Monospace", 12))

    def larger_font(self, text):
        text.config(font=("Monospace", 14))

    #EXIT/ CLOSE FILE
    def exit(self):
        self.root.destroy()

    def close_file(self):
        self.notebook.hide(self.notebook.select())

    #SELECT: ALL/ LINE/ WORD, UNDO SELECTION
    def select_all(self, text):
        text.tag_remove(SEL, "1.0", END)
        text.tag_add(SEL, "1.0", END)
        text.mark_set(INSERT, END)
        text.see(INSERT)
        return 'break'

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

    def select_word(self, text):
        cline = text.index(INSERT).split('.')[0]
        lastcol = 0
        char = text.get('%s.%d' % (cline, lastcol))
        while char != " ":
            lastcol += 1
            char = text.get('%s.%d' % (cline, lastcol))
        text.tag_remove(SEL, INSERT, '%s.%d' % (cline, lastcol))
        text.tag_add(SEL, INSERT, '%s.%d' % (cline, lastcol))
        text.mark_set(INSERT, '%s.%d' % (cline, lastcol))
        text.see(INSERT)
        return 'break'

    def undo_selection(self, text):
        text.tag_remove(SEL, "1.0", END)

    #NEW FILE/NEW FOLDER/ SAVE/ SAVE AS/ OPEN
    def new_file(self):
        """ Creates a new file """
        global filename
        filename = "Untitled"

        new_page = CustomFrame(self.root, self.notebook)
        new_page.linenumbers.redraw()

        self.notebook.add(child=new_page, text=filename)
        self.notebook.select(new_page)
        self.root.update()

    def save_file(self):
        """ Saves an existing file """
        global filename
        if filename == "Untitled":
            self.saveas
        else:
            current_frame = self.notebook.children[
                self.notebook.select().split('.')[2]]
            for key, val in current_frame.children.iteritems():
                if isinstance(val, Text):
                    text = val

            if text is None:
                print("Something is wrong!")

            for key, val in current_frame.children.iteritems():
                if isinstance(val, StatusBar):
                    statusbar = val

            if statusbar is None:
                print("Something is wrong!")

            statusbar.set_text()
            self.root.after(3000, statusbar.reset_text)

            t = text.get("0.0", END)
            f = open(filename, 'w')
            f.write(t)
            f.close()

    def saveas(self):
        """ Saves a new file """
        f = asksaveasfile(mode='w', defaultextension='.cspy')
        if f is None:
            return
        global filename
        filename = f.name

        #str = filename

        # match = re.match('(?P<path>.*)/(?P<name>[^/]+)$', filename)
        # str = match.group('name')
        # path = match.group('path')

        # self.tab_paths[str] = path

        self.notebook.tab(self.notebook.select(), text=filename)
        current_frame = self.notebook.children[
            self.notebook.select().split('.')[2]]
        for key, val in current_frame.children.iteritems():
            if isinstance(val, Text):
                text = val

        if text is None:
            print("Something is wrong!")

        t = text.get("0.0", END)

        for key, val in current_frame.children.iteritems():
            if isinstance(val, StatusBar):
                statusbar = val

        if statusbar is None:
            print("Something is wrong!")

        statusbar.set_text()
        self.root.after(3000, statusbar.reset_text)

        try:
            f.write(t.rstrip())
            filename = f.name
        except:
            showerror(title="Oops!", message="Unable to save file...")

    def open_file(self):
        """ Open an existing file """
        f = askopenfile(parent=self.root,
                        mode='rb',
                        title="Select a file")
        if f is not None:
            global filename
            filename = f.name

            #str = filename
            # match = re.match('(?P<path>.*)/(?P<name>[^/]+)$', filename)
            # str = match.group('name')
            # path = match.group('path')

            # self.tab_paths[str] = path

            new_page = CustomFrame(self.root, self.notebook)
            new_page.linenumbers.redraw()

            self.notebook.add(child=new_page, text=filename)
            self.notebook.select(new_page)
            self.root.update()

            t = f.read()
            new_page.get_text_widget().insert("1.0", t)
            cline = 1
            while cline != int(new_page.get_text_widget().index(END).
                               split('.')[0]):
                self.syn_highlight(cline, new_page.get_text_widget())
                cline += 1
            f.close()

    def run(self):
        """ Compiles/Runs the program """
        self.save_file()
        filename = self.notebook.tab(self.notebook.select(), "text")

        def runCSPyProgram(cspy_file_name):
            os.system('/home/acampbel/CSPy-shared/ulysses/bin/cspy_terminal.sh ' + 
                      cspy_file_name)

        thread = threading.Thread(target=runCSPyProgram, args=(filename,))
        thread.setDaemon(True)
        thread.start()

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
        for token in tokenized:
            end = start + len(token)
            if token == "import":
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
            start += len(token) + 1

        # Comment highlighting
        comment_start = buffer.find('#')
        if comment_start != -1:
            text.tag_add('line_comment',
                         '%s.%d' % (cline, comment_start),
                         '%s.%d' % (str(int(cline) + 1), 0))
        text.tag_remove('block_comment', 1.0, END)
        text.tag_remove('declaration_block', 1.0, END)
        text.tag_remove('string', 1.0, END)

        # Docstring highlighting
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
            text.tag_add('block_comment', start, end + "+3c")
            start = end + "+3c"

        # Declaration highlighting
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

        # Function highlighting
        start = "1.0"
        while True:
            start = text.search(r"def",
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

        # Class highlighting
        start = "1.0"
        while True:
            start = text.search(r"class",
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

        # String highlighting
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
