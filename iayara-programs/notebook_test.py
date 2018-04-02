from Tkinter import *
from ttk import *
class Notebook(Frame):
    """Notebook Widget"""
    def __init__(self, parent, activerelief = RAISED, inactiverelief = RIDGE,
                 xpad = 4, ypad = 6, activefg = 'black', inactivefg = 'black', **kw):
       
                                                                                           
        self.activefg = activefg                                                           
        self.inactivefg = inactivefg
        self.deletedTabs = []        
        self.xpad = xpad
        self.ypad = ypad
        self.activerelief = activerelief
        self.inactiverelief = inactiverelief                                               
        self.kwargs = kw                                                                   
        self.tabVars = {}                                                                  
        self.tabs = 0                                                                                                                                                   
        self.noteBookFrame = Frame(parent)                                                 
        self.BFrame = Frame(self.noteBookFrame)                                            
        self.noteBook = Frame(self.noteBookFrame, relief = RAISED, padding = 2, **kw)           
        self.noteBook.grid_propagate(0)                                                    
        Frame.__init__(self)
        self.noteBookFrame.grid()
        self.BFrame.grid(row =0, sticky = W)
        self.noteBook.grid(row = 1, column = 0, columnspan = 27)

    def change_tab(self, IDNum):
        """Internal Function"""
        
        for i in (a for a in range(0, len(self.tabVars.keys()))):
            if not i in self.deletedTabs:                                                  
                if i <> IDNum:                                                             
                    self.tabVars[i][1].grid_remove()                                       
                    self.tabVars[i][0]['relief'] = self.inactiverelief                     
                    self.tabVars[i][0]['foreground'] = self.inactivefg                             
                else:                                                                      
                    self.tabVars[i][1].grid()                                                                    
                    self.tabVars[IDNum][0]['relief'] = self.activerelief                   
                    self.tabVars[i][0]['foreground'] = self.activefg                               

    def add_tab(self, width = 2, **kw):
        """Creates a new tab, and returns it's corresponding frame

        """
        
        temp = self.tabs                                                                   
        self.tabVars[self.tabs] = [Label(self.BFrame, relief = RIDGE, **kw)]               
        self.tabVars[self.tabs][0].bind("<Button-1>", lambda Event:self.change_tab(temp))  
        self.tabVars[self.tabs][0].pack(side = LEFT, ipady = self.ypad, ipadx = self.xpad) 
        self.tabVars[self.tabs].append(Frame(self.noteBook, **self.kwargs))                
        self.tabVars[self.tabs][1].grid(row = 0, column = 0)                               
        self.change_tab(0)                                                                 
        self.tabs += 1                                                                     
        return self.tabVars[temp][1]                                                       

    def destroy_tab(self, tab):
        """Delete a tab from the notebook, as well as it's corresponding frame

        """
        
        self.iteratedTabs = 0                                                              
        for b in self.tabVars.values():                                                    
            if b[1] == tab:                                                                
                b[0].destroy()                                                             
                self.tabs -= 1                                                             
                self.deletedTabs.append(self.iteratedTabs)                                 
                break                                                                      
            self.iteratedTabs += 1                                                         
    
    def focus_on(self, tab):
        """Locate the IDNum of the given tab and use
        change_tab to give it focus

        """
        
        self.iteratedTabs = 0                                                              
        for b in self.tabVars.values():                                                    
            if b[1] == tab:                                                                
                self.change_tab(self.iteratedTabs)                                         
                break                                                                      
            self.iteratedTabs += 1                                                        

def demo():
    def adjustCanvas(someVariable = None):
        fontLabel["font"] = ("arial", var.get())
    
    root = Tk()
    root.title("tkNotebook Example")
    note = Notebook(root, width= 400, height =400, activefg = 'red', inactivefg = 'blue')  
    note.grid()
    tab1 = note.add_tab(text = "Tab One")                                                  
    tab2 = note.add_tab(text = "Tab Two")                                                  
                                                                                      
    text = Text(tab1)
    text.pack() 
    scrollbar = Scrollbar(tab1)
    scrollbar.pack()
    text.config(yscrollcommand= scrollbar.set)
    scrollbar.config(command=text.yview)

    fontLabel = Label(tab1, text = "TEXT", font = ("Arial", 10))
    fontLabel.pack()
   
    note.focus_on(tab1)
    root.mainloop()

if __name__ == "__main__":
    demo()
