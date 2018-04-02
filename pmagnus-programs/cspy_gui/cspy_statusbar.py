from Tkinter import *
from ttk import*


class StatusBar(Frame):

    def __init__(self, master, notebook):
        Frame.__init__(self, master)
        self.variable = StringVar()
        self.variable.set('    Line:1' + ', Column:1' +
                          '                                    ' +
                          '         ' + 'CSPy')

        s = Style()
        s.configure("BW.TLabel",
                    foreground="white",
                    background="#575757",
                    padding=2,
                    relief="raised",
                    bd=0,
                    highlightthickness=0)

        self.label = Label(self,
                           textvariable=self.variable,
                           font=("Monospace", 12),
                           style="BW.TLabel")

        self.label.pack(fill=X)
        self.pack(side=BOTTOM, fill=X)
        self.notebook = notebook

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

    def lineCol(self, line, col):
        self.variable.set('    Line:' + str(line) + ', Column:' + str(col) +
                          '                                    ' +
                          '         ' + 'CSPy')

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
                          '         ' + "Saved...")

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
                          '         ' + "CSPy")
