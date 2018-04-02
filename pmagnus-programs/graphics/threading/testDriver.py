import Tkinter as tk
import interactive_frame

def runProgram():
    terminal.runCSPyProgram("/home/acampbel/CSPy-shared/ulysses/magnus_programs/test.cspy")

root = tk.Tk()

terminal = interactive_frame.InteractiveFrame(root)
terminal.grid(row=0, column=0, sticky="nsew")

button = tk.Button(root, text="Start program", command=runProgram)
button.grid(row=1, column=0, sticky="nsew")

root.mainloop()