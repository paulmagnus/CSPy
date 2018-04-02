from Tkinter import *
import sys
import time
from threading import Thread
import re
import subprocess
import StringIO
import logging

class InRedirector():
    def __init__(self, outRedirector):
        sys.stdin = self
        self.outRedirector = outRedirector
        
    def readline(self):
        line = self.outRedirector.getInputLine()
        while not line:
            line = self.outRedirector.getInputLine()
            time.sleep(0.1)
        return line

class OutRedirector(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        sys.stdout = self
        self.input_buffer = ""
        self.input_lines = []
        self.bind("<Key>", self.key)
        sys.stdin = InRedirector(self)

    def key(self, key):
        f.write(key.char)
        if key.char:
            self.input_buffer += key.char
            if key.char == "\r" or key.char == "\n":
                self.input_lines.append(self.input_buffer[:-1] + "\n")
                self.input_buffer = ""

    def getInputLine(self):
        if self.input_lines == []:
            return None
        else:
            line = self.input_lines[0]
            self.input_lines = self.input_lines[1:]
            return line

    def write(self, s):
        self.insert("end", s)
        root.update()

class ErrRedirector(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self.config(state="disabled")
        sys.stderr = self

    def write(self, s):
        self.config(state="enabled")
        self.insert("end", s)
        self.config(state="disabled")
        root.update()

def program():

    # p = subprocess.Popen(['python2.7', './test.py'],
    #                      stdout=out_buffer,
    #                      stderr=err_buffer,
    #                      stdin=in_buffer)

    # sys.path.append("/home/acampbel/CSPy-shared/ulysses")
    # import cspy_master

    # sys.argv.append("/home/acampbel/CSPy-shared/ulysses/magnus_programs/test.cspy")

    # cspy_master.main()

    # sys.path.append("/home/acampbel/CSPy-shared/ulysses/magnus_programs/cspy_code")
    # import cspy_master
    # sys.argv.append("/home/acampbel/CSPy-shared/ulysses/magnus_programs/test.cspy")
    # cspy_master.main()

    print 'hi'
    time.sleep(2)
    print 'hello'
    name = raw_input('What is your name? ')
    print "Hello " + name
    print >> sys.stderr, "Error"

def run():
    thread = Thread(target=program)
    thread.daemon = True
    thread.start()

f = open("out.txt", "w+")

root = Tk()
text = OutRedirector(root)
text.grid()
err = ErrRedirector(root)
err.grid()
root.after(100, run)
root.mainloop()

f.close()