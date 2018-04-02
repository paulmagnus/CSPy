import Tkinter as tk 
from PIL import Image, ImageTk
import subprocess

class Application(tk.Frame):              
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg='#FFFFFF')
        self.grid()                       
        self.createWidgets()

    def checkCredentials(self):
        if self.username.get() == "mjenkins" and self.password.get() == "hunter2":
            subprocess.call('python2.7 ~acampbel/CSPy-shared/ulysses/jenkins-workspace/jenkins-tkinter/Ulysses.py', shell=True)
            quit()

    def createWidgets(self):
        leftCanvas = tk.Canvas(self)
        leftCanvas.config(width=100, height=100, bg='#FFFFFF', highlightthickness=0)
        leftCanvas.grid(row=0, column=0, sticky = tk.W)

        image = Image.open("CSPy Logo.png")
        cspylogo = ImageTk.PhotoImage(image)
        
        label = tk.Label(image=cspylogo)
        label.image = cspylogo
        label.grid(row=0, column=0, sticky = tk.N)

        self.username = tk.Entry(self)
        self.password = tk.Entry(self)
        self.username.insert(0, "Username")
        self.password.insert(0, "Password")

        self.username.grid(row=2, column=1, sticky=tk.S)
        self.password.grid(row=3, column=1, sticky=tk.S)

        self.login = tk.Button(self, text="Submit", command=self.checkCredentials, bg='#FFFFFF')
        self.login.grid(row=4, column=1, sticky=tk.S)

        rightCanvas = tk.Canvas(self)
        rightCanvas.config(width=100, height=100, bg='#FFFFFF', highlightthickness=0)
        rightCanvas.grid(row=0, column=3, sticky=tk.E)
        

app = Application()                       
app.master.title('CSPy Development Engine')    
app.mainloop()    