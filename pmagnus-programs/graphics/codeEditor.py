from Tkinter import *
from ttk import *
from tkFont import Font
import re
import string

class CodeEditor(Text):

    def initialize(self):
        self.config(tabs="28")    # 28 pixels = 4 character indentation for font
        
        # tag configuration
        self.tag_configure("RED_TEXT", foreground="red")
        
        
        for key in key_bindings:
            self.bind(key, key_bindings[key])
        # for key in post_entry_key_bindings:
        #     self.bind_class("post-class-bindings", key, post_entry_key_bindings[key])
            
        self.mark_set("ITEM_START", self.index(INSERT))
        self.mark_set("ITEM_END", self.index(INSERT))
        self.mark_gravity("ITEM_START", LEFT)
        print(self.index("ITEM_START"))   # for debug

#------------------------------------------------------------------------------#
#                                  HELPERS                                     #
#------------------------------------------------------------------------------#

def is_input_between_marks(markstart, markend):
    return codeEditor.compare(codeEditor.index(markstart), "<=", INSERT) and \
        codeEditor.compare(INSERT, "<=", codeEditor.index(markend))

def addToIndex(i, dr, dc):
    indexLoc = codeEditor.index(i)
    row, col = [int(s) for s in string.split(indexLoc, ".")]
    row += dr
    col += dc
    while col <= 0:
        row -= 1
        
    if row <= 0:
        row = 0
    return str(row) + "." + str(col)

#------------------------------------------------------------------------------#
#                                SPECIAL KEYS                                  #
#------------------------------------------------------------------------------#

def key_enter(event):
    update_markers("<Return>")

def key_tab(event):
    codeEditor.insert(INSERT, "\t")
    update_markers("<Tab>")
    return "break"

def key_backspace(event):
    return

def key_delete(event):
    return

def key_cancel(event):
    return

def key_insert(event):
    return

def key_left(event):
    codeEditor.mark_set(INSERT, addToIndex(INSERT, 0, -1))
    return "break"

def key_right(event):
    codeEditor.mark_set(INSERT, addToIndex(INSERT, 0, 1))
    return "break"

def key_up(event):
    return

def key_down(event):
    return

def key_control_w(event):
    root.destroy()

def key(event):
    update_markers(event.char)
    update_tags()

    # startindex = codeEditor.search("print",
    #                                INSERT,
    #                                stopindex=1.0,
    #                                backwards=True)

    # if startindex == "":
    #     codeEditor.tag_remove("RED_TEXT", 1.0, "end")
    #     return
    # codeEditor.tag_add("RED_TEXT", startindex, float(startindex) + 0.5)

def update_markers(lastKey):
    '''
    Updates the markers ITEM_START and ITEM_END to the beginning and end of the current item
    '''
    start = codeEditor.search(r"[A-Za-z0-9_]*",
                              codeEditor.index(INSERT),
                              stopindex=1.0,
                              backwards=True,
                              regexp=True)
    
    end = codeEditor.search(r"[^A-Za-z0-9_]+",
                            codeEditor.index(INSERT),
                            stopindex=END,
                            regexp=True)

    print(start)
    print(end)
    
    codeEditor.mark_set("ITEM_START",
                        start if start != "" else 1.0)
    codeEditor.mark_gravity("ITEM_START", LEFT)
    codeEditor.mark_set("ITEM_END",
                        end if end != "" else codeEditor.index(END))

    print codeEditor.get("ITEM_START", "ITEM_END").strip()

    if re.match(r"[^a-zA-Z0-9_]+",
                codeEditor.get("ITEM_START", "ITEM_END").strip()):
        # on a separator
        codeEditor.mark_set("ITEM_NEW_START",
                            codeEditor.search(r"[A-Za-z0-9_]*",
                                              "ITEM_END",
                                              stopindex="ITEM_START",
                                              backwards=True,
                                              regexp=True))

        codeEditor.mark_set("ITEM_NEW_END",
                            codeEditor.search(r"[^A-Za-z0-9_]+",
                                              "ITEM_START",
                                              stopindex="ITEM_END",
                                              regexp=True))

        print "ITEM_NEW_START:", codeEditor.index("ITEM_NEW_START")
        print "ITEM_NEW_END:", codeEditor.index("ITEM_NEW_END")

        if codeEditor.compare(INSERT, "<=", "ITEM_NEW_END"):
            codeEditor.mark_set("ITEM_END",
                                "ITEM_NEW_END")

        if codeEditor.compare("ITEM_NEW_START", "<=", INSERT):
            codeEditor.mark_set("ITEM_START", "ITEM_END")
    
# key bindings to functions within the CodeEditor
key_bindings = {
    "<Control-w>"    : key_control_w,
    "<KeyRelease>"   : key
    }

# separating characters
separators = [
    " ",
    "<Tab>",
    "<Return>",
    ",",
    ".",
    ":",
    "(",
    ")",
    "'",
    '"',
    ]

# the following are the keywords in CSPy
keywords = [
    "None",
    "and",
    "as",
    "assert",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "extends",
    "finally",
    "fn",
    "for",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "not",
    "of",
    "or",
    "pass",
    "proc",
    "raise",
    "return",
    "try",
    "while",
    "list",
    "tuple",
    "dict",
    "set",
    "frozenset",
    "print"
    ]

root = Tk()

codeEditor = CodeEditor(root, wrap=NONE)
codeEditor.grid(row=0, column=0)
codeEditor.initialize()
codeEditor.focus()

scrollbar = Scrollbar(root, command=codeEditor.yview)
scrollbar.grid(row=0, column=1, sticky="nsew")

codeEditor['yscrollcommand'] = scrollbar.set

root.mainloop()