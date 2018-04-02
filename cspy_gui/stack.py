#------------------------------------------------------------------------------#
# stack.py                                                                     #
#                                                                              #
# This contains an implementatin of a list-based stack class.                  #
#                                                                              #
# Written by Ines Ayara '20, Paul Magnus '18, Matthew R. Jenkins '20           #
# Summer 2017                                                                  #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# stack                                                                        #
#   This is an implementation of a list-based stack                            #
#   Attributes:                                                                #
#     contents : list - the elements in the stack, the last element is the top #
#     size : int - the size of the stack                                       #
#   Methods:                                                                   #
#     top() -> element - returns the top element of the stack                  #
#     pop() - removes the top element from the stack                           #
#     push(element) - adds element to the top of the stack                     #
#     empty() -> bool - returns true if the stack is empty                     #
#     __str__() -> string - returns a representation of the stack's list       #
#------------------------------------------------------------------------------#

class stack:
    def __init__(self):
        self.contents = []
        self.size = 0

    #--------------------------------------------------------------------#
    # top() -> element                                                   #
    #   Returns but does not remove the top element of the stack. If the #
    #   stack is empty, a StackEmptyException is raised.                 #
    #--------------------------------------------------------------------#
    def top(self):
        if self.size == 0:
            raise StackEmptyException
        else:
            return self.contents[self.size - 1] 
    
    #--------------------------------------------------------------------#
    # pop()                                                              #
    #   Removes the top element of the stack. If the stack is empty, a   #
    #   StackEmptyException is raised.                                   #
    #--------------------------------------------------------------------#
    def pop(self):
        if self.size == 0:
            raise StackEmptyException
        else:
            del self.contents[-1]
            self.size -= 1

    #--------------------------------------------------------------------#
    # push(element)                                                      #
    #   Adds 'element' to the top of the stack                           #
    #--------------------------------------------------------------------#
    def push(self, item):
        self.contents.append(item)
        self.size += 1
    
    #--------------------------------------------------------------------#
    # empty() -> bool                                                    #
    #   Returns true if the stack is empty, returns false otherwise.     #
    #--------------------------------------------------------------------#
    def empty(self):
        return self.size == 0

    #--------------------------------------------------------------------#
    # __str__() -> string                                                #
    #   Returns a string representation of the stack's undelying list.   #
    #--------------------------------------------------------------------#
    def __str__(self):
        return str(self.contents)

#------------------------------------------------------------------------------#
# StackEmptyException                                                          #
# This is the exception raised by the stack class if top or pop is called when #
# the stack is empty.                                                          #
#------------------------------------------------------------------------------#
class StackEmptyException(Exception):
    pass