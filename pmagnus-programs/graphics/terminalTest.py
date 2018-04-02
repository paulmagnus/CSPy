from Tkinter import *
import subprocess as sub


root = Tk()

text = Text(root)
text.pack()


p = sub.Popen('./test.sh', stdout=sub.PIPE, stderr=sub.PIPE)
output, errors = p.communicate()

text.insert(END, output)

root.mainloop()