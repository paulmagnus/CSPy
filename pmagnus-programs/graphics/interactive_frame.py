from Tkinter import Frame, Text, Label, Tk, END
from threading import Thread
from Queue import Queue, Empty
import subprocess
import re
import sys
import select

def read_out(process, queue):
    poll_obj = select.poll()
    poll_obj.register(process.stdout, select.POLLIN)
    poll_obj.register(process.stdout, select.POLLPRI)
    while process.poll() is None:
        print "Process running"
        sys.stdout.flush()
        if poll_obj.poll():
            print "Polling stdout"
            out = process.stdout.readline()
            while out != "":
                match = re.match("^(?P<before>.*)\x1B\[\?1034h(?P<after>.*)$", out)
                if match:
                    out = match.group('before') + match.group('after')
                queue.put(out)
                sys.stdout.flush()
                if poll_obj.poll():
                    print "Polling stdout"
                    out = process.stdout.readline()
                else:
                    out = ""

def read_err(process, queue):
    poll_obj = select.poll()
    poll_obj.register(process.stderr, select.POLLIN)
    poll_obj.register(process.stderr, select.POLLPRI)
    while process.poll() is None:
        print "Process running"
        sys.stderr.flush()
        if poll_obj.poll():
            print "Polling stderr"
            err = process.stderr.readline()
            while err != "":
                queue.put(err)
                sys.stderr.flush()
                if poll_obj.poll():
                    print "Polling stderr"
                    err = process.stdout.readline()
                else:
                    err = ""




class InteractiveFrame(Frame):
    process = 0
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.createWidgets()

    def createWidgets(self):
        self.consoleLabel = Label(self, text="Console")
        self.consoleLabel.grid(row=0, column=0, sticky="nsew")

        self.console = Text(self)
        self.console.grid(row=1, column=0, sticky="nsew")

        self.errorLabel = Label(self, text="Errors:")
        self.errorLabel.grid(row=2, column=0, sticky="nsew")

        self.errorText = Text(self, state="disabled")
        self.errorText.grid(row=3, column=0, sticky="nsew")

    def startProcess(self):
        # self.process = subprocess.Popen(["/home/acampbel/CSPy-shared/ulysses/bin/cspy",
        #                                  "/home/acampbel/CSPy-shared/ulysses/magnus_programs/sudoku/sudoku.cspy"],
        #                                 stdout=subprocess.PIPE,
        #                                 stdin=subprocess.PIPE,
        #                                 stderr=subprocess.PIPE)

        self.process = subprocess.Popen(["python2.7", "./test.py"],
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE,
                                        stderr=subprocess.PIPE)

        self.out_queue = Queue()
        self.err_queue = Queue()

        self.thread = Thread(target=read_out, args=(self.process,
                                                     self.out_queue))
        self.err_thread = Thread(target=read_err, args=(self.process,
                                                        self.err_queue))
        
        self.thread.setDaemon(True)
        self.err_thread.setDaemon(True)
        self.thread.start()
        self.err_thread.start()

        self.after(100, self.updateLines)

    def updateLines(self):

        while not self.out_queue.empty():
            line = self.out_queue.get(False)
            self.console.insert(END, line)
        
        while not self.err_queue.empty():
            err_line = self.err_queue.get(False)
            self.errorText.config(state="normal")
            self.errorText.insert(END, err_line)
            self.errorText.config(state="disabled")

        if self.process.poll() is None:
            self.after(100, self.updateLines)

root = Tk()
frame = InteractiveFrame(root)
frame.grid(row=0, column=0, sticky="nsew")
frame.startProcess()
root.mainloop()