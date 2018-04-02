class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.size = 0
        self.head = None
    def insert(self, value):
        temp = Node(value)
        temp.next = self.head
        self.head = temp
        self.size += 1
    def search(self, value):
        index = 0;
        current = self.head
        while current is not None:
            if value == current.value:
                return index
            else:
                current = current.next
                index += 1
        return -1
    def remove(self, index):
        if index > self.size or index < 0:
            raise ValueError("Your index is either greater than the size of the list or less than zero.")
        if self.head is None:
            return
        temp = self.head
        if index == 0:
            self.head = temp.next
            temp = none
            return
        for i in range(index - 1):
            temp = temp.next
            if temp is None:
                break
        if temp is None:
            return
        if temp.next is None:
            return
        next = temp.next.next
        temp.next = None
        temp.next = next
        self.size -= 1
    def printList(self):
        temp = self.head
        while temp is not None:
            print temp.value
            temp = temp.next
        print('\n')

def main():
    listy = LinkedList();
    listy.insert(1)
    listy.insert(2)
    listy.insert(4)
    listy.insert(8)
    listy.insert(16)
    listy.printList()
    listy.remove(listy.search(8))
    listy.printList()

main()
