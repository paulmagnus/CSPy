class stack:
    def __init__(self):
        self.contents = []
        self.size = 0

    def top(self):
        if self.size == 0:
            print("Nope")
            
        else:
            return self.contents[self.size - 1] 
    
    def pop(self):
        if self.size == 0:
            print("Nope")
        else:
            del self.contents[-1]
            self.size -= 1

    def push(self, item):
        self.contents.append(item)
        self.size += 1
    
    def empty(self):
        return self.size == 0

    def display(self):
        if self.empty():
            print("I'm empty")
            
        else:
            for i in range(0, self.size):
                print(self.contents[i])

def paren_match(text):
    s1 = stack()
    s2 = stack()
    for i in range(len(text)):
        if (text[i] == "(" or text[i] == "{" or text[i] == "]"):
            s1.push(text.index(text[i]))
            s2.push(text[i])
        
        elif (text[i] == ")" or text[i] == "}" or text[i] == "]"):
            if text[i] == s2.top():
                #highlight
                s1.pop()
                s2.pop()
