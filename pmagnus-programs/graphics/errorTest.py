from Tkinter import *
import subprocess
from threading import Thread
from Queue import Queue, Empty

from errorFrame import ErrorFrame
from interactiveFrame import InteractiveFrame

def readlines(process, queue):
    while process.poll() is None:
        queue.put(process.stdout.readline())

class Application(Frame):
    process = 0
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = Button(self, text="Quit", command=self.quit)
        self.quitButton.grid()
        self.console = Text(self)
        self.console.config(state=DISABLED)
        self.console.grid()

    def startProcess(self):
        self.process = subprocess.Popen(["./test.py"],
                                         stdout=subprocess.PIPE,
                                         stdin=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
        
        self.queue = Queue()
        self.thread = Thread(target=readlines, args=(self.process, self.queue))
        self.thread.start()

        self.after(100, self.updateLines)

    def updateLines(self):
        try:
            line = self.queue.get(False) # False for non-blocking, raises Empty if empty
            self.console.config(state=NORMAL)
            self.console.insert(END, line)
            self.console.config(state="disabled")
        except Empty:
            pass
        
        if self.process.poll() is None:
            self.after(100, self.updateLines)

app = Application()
app.startProcess()
app.mainloop()

# root = Tk()

# e = InteractiveFrame(root)
# e.grid(row=0, column=0, sticky="nsew")

# error = ErrorFrame(root)
# error.grid(row=1, column=0, sticky="nsew")

# b = Button(root, text="QUIT", command=root.quit)
# b.grid(row=2, column=0, sticky="nsew")

# def entryreturn(event):
#     proc.stdin.write(e.get("1.0", END)+"\n") # the '\n' is important to flush stdin

# # when you press Return in Entry, use this as stdin and remove it
# e.bind("<Return>", entryreturn)

# proc = subprocess.Popen('./test.py', stdin=subprocess.PIPE)

# root.mainloop()                 