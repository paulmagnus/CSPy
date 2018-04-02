import Tkinter as tk
import threading
import logging
import time
import sys

import thread1

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

class OutRedirector(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        sys.stdout = self
        self.input_buffer = ""
        self.input_lines = []
        self.bind("<Key>", self.key)
        sys.stdin = InRedirector(self)

    def key(self, key):
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
        self.update()

class ErrorHandler(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.config(state="disabled")
        
    def write(self, s):
        self.config(state="normal")
        self.insert("end", s)
        self.config(state="disabled")
        self.update()

    def flush(self):
        pass

def main():
    root = tk.Tk()

    text = OutRedirector(root)
    text.grid()

    err = ErrorHandler(root)
    err.grid()

    logger = logging.getLogger("error_logger")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(err)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    info = {'stop' : False}
    thread = threading.Thread(target=thread1.fun, args=(info,))
    thread.daemon = True
    thread.start()

    root.mainloop()

if __name__ == '__main__':
    main()