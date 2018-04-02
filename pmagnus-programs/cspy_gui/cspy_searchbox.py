from Tkinter import *
from ttk import*


class SearchBox:

    def __init__(self, texteditor, prev=0, next=0):
        self.texteditor = texteditor
        self.prev = prev
        self.next = next
        self.root = Tk()
        self.root.title("Find ")
        self.entry = Entry(self.root)
        self.root.geometry("180x25")
        self.entry.focus()
        self.entry.pack()
        self.config_tags()
        self.entry.config(background="white",
                          foreground="black",
                          font=("Monospace", 13))
        self.characters = ascii_letters + digits + punctuation
        self.entry.bind('<KeyRelease>', self.key_release)
        self.entry.bind('<Control-w>', self.key_control_w)
        self.texteditor.bind('<Button-1>', self.button_1)

    def _callback(self, result, *args):
        self.texteditor.callback(result, *args)

    def config_tags(self):
        self.texteditor.tag_configure("search", background="#A9A9A9")

    def remove_tags(self, start, end):
        self.texteditor.tag_remove("search", 1.0, END)

    def get_text(self):
        entry_text = self.entry.get()
        return entry_text

    def button_1(self, key):
        self.remove_tags("1.0", END)

    def key_release(self, key):
        """ Highlight any matching string """
        self.remove_tags("1.0", END)
        search_text = self.get_text()

        if self.prev == 1:
            index = self.texteditor.index(INSERT)
            start = 1.0
            count = 0
            while True:
                countVar = StringVar()
                pos = self.texteditor.search(search_text,
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
                self.texteditor.tag_add("search",
                                        last_pos,
                                        "%s+%sc" % (last_pos,
                                                    last_countVar.get()))

        elif self.next == 1:
            index = self.texteditor.index(INSERT)
            start = index

            countVar = StringVar()
            pos = self.texteditor.search(search_text,
                                         start,
                                         stopindex=END,
                                         count=countVar,
                                         regexp=True)

            if not pos:
                pass

            else:
                self.texteditor.tag_add("search",
                                        pos,
                                        "%s+%sc" % (pos, countVar.get()))

        else:

            start = 1.0
            while True:
                countVar = StringVar()
                pos = self.texteditor.search(search_text,
                                             start,
                                             stopindex=END,
                                             count=countVar,
                                             regexp=True)
                if not pos:
                    break
                else:
                    self.texteditor.tag_add("search",
                                            pos,
                                            "%s+%sc" % (pos, countVar.get()))
                start = pos + "+1c"

    def key_control_w(self, key):
        """ Close the search box """
        self.remove_tags("1.0", END)
        self.root.destroy()
