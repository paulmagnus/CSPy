from Tkinter import *

root = Tk()
root.title("Menu")
root.geometry("400x800")
root.configure(background = "black")

#frame = Frame(root)
#frame.config(height = 800)
#frame.config(width = 400)
#frame.config(bg = "black")
#frame.pack()

button1 = Button(root)
button1.config(bg = "green")
button1.config(text = "Submit")
button1.pack(padx = 5, pady = 5, side = BOTTOM)
button1.config(width = 10)

button2 = Button(root)
button2.config(bg = "blue")
button2.config(text = "Run")
button2.pack(padx = 5, pady = 5, side = BOTTOM)
button2.config(width = 10)

button3 = Button(root)
button3.config(bg = "red")
button3.config(text = "Save")
button3.pack(padx = 5, pady = 5, side = BOTTOM)
button3.config(width = 10)

listbox = Listbox(root)
listbox.pack(padx = 10, pady = 30)

listbox.insert(END, "       My Projects:")
for item in ["Project0", "Project1", "Project2", "Project3", "Project4"]:
    listbox.insert(END, " ")
    listbox.insert(END, item)
    
listbox.config(bg = "blue")
listbox.config(height = 15)
listbox.config(width = 25)

root.mainloop()

