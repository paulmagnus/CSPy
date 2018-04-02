class Stack:
    def __init__(self):
        self.Contents = []
        self.Size = 0
    def push(self, item):
        self.Contents.append(item)
        self.Size += 1
        print(self.Contents)
    def peek(self):
        if self.Size == 0:
            print("No items found in stack.")
            return;
        else:
            return self.Contents[self.Size - 1]
    def pop(self):
        if self.Size == 0:
            print("No items found in stack.")
        else:
            del self.Contents[-1]
            self.Size -= 1
    def printstack(self):
        if self.Size == 0:
            return;
        for i in range(0, self.Size):
            print(self.Contents[i])

def main():
    stacky = Stack()
    stacky.push(1)
    stacky.push(2)
    stacky.push(3)
    print(stacky.peek())

main()
