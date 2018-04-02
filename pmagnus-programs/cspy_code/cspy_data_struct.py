#------------------------------------------------------------------------------#
# cspy_data_struct.py                                                          #
#                                                                              #
# Originally written by Alex Dennis '18 and Eric Collins '17                   #
# June 2015                                                                    #
#                                                                              #
# Revised and edited by Lyndsay LaBarge '17 and Maya Montgomery '18            #
# June 2016                                                                    #
#                                                                              #
# Revised and edited by Paul Magnus '18, Ines Ayara and Matthew R. Jenkins '20 #
# Summer 2017                                                                  #
#                                                                              #
# This library contains classes for the following CSPy data structures:        #
#      - AST (Abstract Syntax Tree)                                            #
#      - DeclarationException                                                  #
#      - NotYetDeclaredException                                               #
#      - SignatureException                                                    #
#                                                                              #
#------------------------------------------------------------------------------#
import ply.yacc as yacc
from cspy_builtins import builtins, is_callable, callmatch

# This dictionary associates binary operators to the names of their
# corresponding functions
binary_overload = {
    "+"   : "__add__",
    "-"   : "__sub__",
    "*"   : "__mul__",
    "/"   : "__div__",
    "//"  : "__floordiv__",
    "%"   : "__mod__",
    "**"  : "__pow__",
    "<<"  : "__lshift__",
    ">>"  : "__rshift__",
    "&"   : "__and__",
    "^"   : "__xor__",
    "|"   : "__or__",
    "<"   : "__lt__",
    "<="  : "__le__",
    "=="  : "__eq__",
    "!="  : "__ne__",
    ">"   : "__gt__",
    ">="  : "__ge__",
    "&&"  : "__booland__",
    "||"  : "__boolor__",
    "and" : "__booland__",
    "or"  : "__boolor__"
    
}

# This dictionary associates unary operators to the names of their
# corresponding functions
unary_overload = {
    "-"   : "__neg__",
    "+"   : "__pos__",
    "~"   : "__invert__",
    "!"   : "__boolnot__",
    "not" : "__boolnot__"
}

# This list contains the types of abstract syntax tree nodes which can contain
# an environment
holds_env = ["FILE","CLASS_DEFINITION","BLOCK_WITH_ENVIRONMENT","SUITE_INLINE",
             "BLOCK_PASS", "LITERAL_FUNCTION", "LITERAL_PROCEDURE", 
             "EXCEPT_ALIAS"]

#------------------------------------------------------------------------------#
# ast                                                                          #
# A CSPy abstract syntax tree node.                                            #
#                                                                              #
# Attributes:                                                                  #
# label - This is the name of the node.  It is used in several processes to    #
#   differentiate betweeen different types of nodes.                           #
#                                                                              #
# type - This is the type of the node. Call det_type(found in type_checking.py)#
#   to set the type attributes for all of the nodes in a tree.                 #
#                                                                              #
# children - This is a list of the children of this node. Children are usually #
#   abstract syntax tree nodes but may be strings.  The number and types of    #
#   children are consistent across all nodes of the same kind.  Children can   #
#   also be accessed through the overloaded indexing operator (n.children[0] is#
#   equivalent to n[0])                                                        #
#                                                                              #
# parent - This is the abstract syntax tree node which contains this node as a #
#   child.  All nodes have a parent defined except for the root node which has #
#   a parent of None.                                                          #
#                                                                              #
# env - This is a dictionary representing the environment contained by this    #
#   node.  Only nodes of a type defined in "holds_env" will have an "env"      #
#   attribute defined.                                                         #
#                                                                              #
# python_env - This is a dictionary representing the environment variables     #
#   that originated from a python import. Only "FILE" nodes will have a        #
#   "python_env" attribute defined.                                            #
#                                                                              #
# lineNum - This is an integer representing the line number upon which the code#
#   that this node represents resides in the CSPy code.                        #
#                                                                              #
# endLineNum - This is an integer representing the line number upon which the  #
#   end of the code that this node represents resides in the CSPy code.        #
#                                                                              #
# position - This is an integer representing the index of the first character  #
#   of the code that this node represents with respect to the whole file.      #
#                                                                              #
# endPosition - This is an integer representing the index of the last character#
#   of the code that this node represents with respect to the whole file.      #
#                                                                              #
# column - This is an integer representing the index of the first character    #
#   of the code that this node represents with respect to the line that the    #
#   code is on. The function "set_column_num(sourceCode)" must be called on    #
#   the root of the tree in order to initialize this attribute.                #
#                                                                              #
# endColumn - This is an integer representing the index of the last character  #
#   of the code that this node represents with respect to the line that the    #
#   code is on.  If the code spans multiple lines, then "endColumn" is the     #
#   number of characters after the first character of the first line of the    #
#   code.  The function "set_column_num(sourceCode)" must be called on the     #
#   root of the tree in order to initialize this attribute.                    #
#                                                                              #
# line - This is a string representing the line or line upon which the code    #
#   that this node represents resides in the CSPy code.  The function          #
#   "set_column_num(sourceCode)" must be called on the root of the tree        #
#   in order to initialize this attribute.                                     #
#------------------------------------------------------------------------------#
class ast(object):
    #-----------------------------------------------------------------------#
    # __init__(p:YaccProduction, label:string, * children:int)              #
    # This method initializes the Abstract Syntax Tree node.  The method is #
    # a YaccProduction "p" which is the parsing symbol that the ast node    #
    # represents, a string "label" which is the name and type of the node,  #
    # and a tuple of integers "children" which are the indexes of "p" that  #
    # should be added to "self.children".                                   #
    #-----------------------------------------------------------------------# 
    def __init__(self, p, label, * children):
        self.label = label
        self.type = None
        self.children = []
        self.add_children(list(children), p)
        self.parent = None
        if(self.label in holds_env):
            self.env = {}
        if self.label == "FILE":
            self.python_env = {}
        self.column = 0
        self.endColumn = 0
        self.line = ""
        
        # Set line number and position for non empty nodes
        if (isinstance(p, yacc.YaccProduction)): # and len(p) > 1):
            self.lineNum, self.endLineNum = p.linespan(0)
            self.position, self.endPosition = p.lexspan(0)
            if len(p) > 1:
                if (type(self.children[len(self.children) - 1]) == str):
                    self.endPosition += len(self.children[len(self.children) -1])-1
        else:
            self.lineNum = 0
            self.endLineNum = 0
            self.position = 0
            self.endPosition = 0

    #-----------------------------------------------------------------------#
    # set_column_num(s:string)                                              #
    # This method sets the values of the "column", "endColumn", and "line"  #
    # attributes for this node and for all nodes that this node dominates.  #
    # The method is given a string "s" which is the CSPy source code.       #
    #-----------------------------------------------------------------------#
    def set_column_num(self, s):
        last_nl = s.rfind('\n',0,self.position)
        if last_nl < 0:
            last_nl = -1
        next_nl = s.find('\n',self.endPosition,len(s))
        if next_nl < 0:
            next_nl = len(s)
        self.column = self.position - last_nl
        self.endColumn = self.endPosition - last_nl
        self.line = s[last_nl+1:next_nl]
        for child in self.children:
            if (isinstance(child, ast)):   
                child.set_column_num(s)

    #-----------------------------------------------------------------------#
    # add_children(children:list of int, p:YaccProduction)                  #
    # This method adds certain children from "p" to the children of the     #
    # current node given their indices.  The method is given a list of      #
    # integers "children" which are the indices of the children of "p"      #
    # which should be added to the children of the current node, and        #
    # a YaccProduction "p" which is the grammar symbol whose children are   #
    # being added to the children of the current node.                      #
    #-----------------------------------------------------------------------#
    def add_children(self, children, p):
        for i in children:
            if (isinstance(p[i], ast)):
                p[i].parent = self
            self.children.append(p[i])

    #-----------------------------------------------------------------------#
    # lookup_var(var:string) -> type_obj                                    #
    # This method looks up the instance of the variable with the given name #
    # and within the scope of the current node.  The method is given a      #
    # string "var" which is the name of the variable being looked up.  The  #
    # method returns an instance object which is the variable of the given  #
    # name and within the scope of the current node.  If the variable does  #
    # not exist within the current scope, a "NotYetDeclaredException"       #
    # is raised.                                                            #
    #-----------------------------------------------------------------------# 
    def lookup_var(self, var):
        # Built-in
        if (var in builtins):
            return builtins[var]

        if var == 'self':
            # Check if node is class
            if self.label == 'CLASS_DEFINITION':
                # lookup the class type
                return ast.lookup_var(self.parent, self[0])

            # Reached the root of the tree
            if not self.parent:
                raise NotYetDeclaredException
            
            # Look in parent environment
            return ast.lookup_var(self.parent, var)

        # Check if node can hold an environment
        if self.label in holds_env:
            if var in self.env:
                return self.env[var]
            # Check if node is a class
            if self.label == 'CLASS_DEFINITION':
                # Check for superclass
                super_class = self[1]
                if super_class.label == 'TYPE':
                    # there is a superclass
                    super_class = \
                        ast.lookup_var(self.parent, super_class[0])
                    if var in super_class.methods:
                        # inherited method from the superclass
                        return super_class.methods[var]
                

        # Reached the root of the tree
        if (not self.parent):
            raise NotYetDeclaredException

        # Look in parent environment
        return ast.lookup_var(self.parent, var)
        
    #-----------------------------------------------------------------------#
    # initiate_var(var:string, typ:type_obj)                                #
    # This method initiates a variable with the given name and the given    #
    # instance. The method is given a string "var" which is the name of the #
    # variable being initiated and an type_obj "typ" which is the type of   #
    # variable being initiated.  If the variable already exists and either  #
    # of the pre-existing type_obj or new type_obj is not a subroutine,     #
    # then a "DeclarationException" is raised.  If the variable already     #
    # exists and both the pre-existing and the new instances are            #
    # subroutines, then the pre-existing type_obj and the new type_obj are  #
    # appended into list and stored under the given name.                   #
    #-----------------------------------------------------------------------#
    def initiate_var(self, var, typ):
        # Reached the root of the tree
        if (not self):
            raise DeclarationException

        # Current tree node has an environment
        elif (self.label in holds_env):
            # Function/Procedure Overloading
            if (var in self.env):
                
                if self.label == "FILE" and var in self.python_env:
                    # Mix of python declarations and cspy declarations
                    raise DeclarationException

                # Check if the value you want to assign is a function/procedure
                if (is_callable(typ)):
                    # Make sure all of the variables current values
                    # are functions/procedures
                    if (isinstance(self.env[var],list)):
                        for elem in self.env[var]:
                            if (not is_callable(elem)):
                                raise DeclarationException

                            if callmatch(elem, typ):
                                raise SignatureException

                        # Add the new function/proc signature to the environment
                        self.env[var].append(typ)
                        return
                    # First overload - make sure its original value is a 
                    # function/procedure
                    elif (is_callable(self.env[var])):  
                        if callmatch(self.env[var], typ):
                            raise SignatureException
                        else:
                            self.env[var] = [self.env[var], typ]
                            return
                raise DeclarationException
            # Undeclared variable - add it to the environment
            else:
                self.env[var] = typ

        # Keep searching for the closest environment
        else:
            ast.initiate_var(self.parent, var, typ)

    #-----------------------------------------------------------------------#
    # initiate_py_var(var:string, typ:type_obj)                             #
    # This method initiates a variable with the given name and the given    #
    # instance. This method is given a string "var" which is the name of    #
    # the variable being initiated and a type_obj "typ" which is the type   #
    # of variable being initiated. If the variable already exists then a    #
    # "DeclarationException" is raised. This variable is stored in both     #
    # "env" and "python_env" at the file level.                             #
    #-----------------------------------------------------------------------#
    def initiate_py_var(self, var, typ):
        # Reached the root of the tree
        if not self:
            raise DeclarationException

        # Current tree node is FILE
        if self.label == "FILE":
            # Check if the value has already been defined
            if var in self.env:
                raise DeclarationException
            
            self.env[var] = typ
            self.python_env[var] = typ

        # Keep searching for the file
        else:
            ast.initiate_py_var(self.parent, var, typ)


    #-----------------------------------------------------------------------#
    # is_class_var(var:string) -> bool                                      #
    # This method returns whether the variable is a local class variable.   #
    # This means that in the python conversion this variable needs "self."  #
    # before the variable is written. If the variable is undefined, raises  #
    # a NotYetDeclaredException.                                            #
    #-----------------------------------------------------------------------#
    def is_class_var(self, var):

        if self.label == "CLASS_DEFINITION":
            if var in self.env:
                return True
            
            # check for superclass
            super_class = self[1]
            if super_class.label == 'TYPE':
                # there is a superclass
                super_class = \
                    ast.lookup_var(self.parent, super_class[0])
                if var in super_class.methods:
                    # inherited method from the superclass
                    return True

        if not self.parent:
            return False

        return self.parent.is_class_var(var)


    #-----------------------------------------------------------------------#
    # is_python(var:string) -> bool                                         #
    # This method returns whether the variable is from a python import.     #
    #-----------------------------------------------------------------------#
    def is_python(self, var):
        # Current tree node is FILE
        if self.label == "FILE":
            return var in self.python_env

        # Current tree node has environment
        if self.label in holds_env:
            if var in self.env:
                return False

        # Continue searching for environment
        return ast.is_python(self.parent, var)

    #-----------------------------------------------------------------------#
    # flatten(label:string) -> list of ast                                  #
    # This method flattens the current tree an return a list of tree nodes. # 
    # The method is given a string "label" which is the label of the nodes  #
    # which should be the elements of the list.                             #
    #-----------------------------------------------------------------------#
    def flatten(self, label):
        if (self.label == label):
            return [self]
        result = []
        for child in self.children:
            if (isinstance(child, ast)):
                result += ast.flatten(child,label)
        return result


    #-----------------------------------------------------------------------#
    # __getitem__(index:int) -> ast                                         #
    # This method overloades the indexing operator for abstract syntax      #
    # trees.  The method is given an integer "index" which is the index of  #
    # the element returned. The method return an element of "self.children" #
    # with the given index. Thus, the following expressions are equivalent: #
    # myTree[index]                                                         #
    # myTree.__getitem__(index)                                             #
    # myTree.children[index]                                                #
    #-----------------------------------------------------------------------#
    def __getitem__(self, index):
        return self.children[index]

    #-----------------------------------------------------------------------#
    # __setitem__(index:int, value:ast)                                     #
    # This method overloads the indexing assignment operator for abstract   #
    # syntax tree.  The method is given an integer "index" which is the     #
    # index of the element to be set and an abstract syntax tree "value"    #
    # which is the value to be set at the given index.  The method sets the #
    # values of "self.children" at the given index.  Thus, the following    #
    # statements are equivalent:                                            #
    # myTree[index] = childTree                                             #
    # myTree.__setitem__(index, childTree)                                  #
    # myTree.children[index] = childTree                                    #
    #-----------------------------------------------------------------------#
    def __setitem__(self, index, value):
        self.children[index] = value

    #-----------------------------------------------------------------------#
    # __repr__() -> string                                                  #
    # This method returns a string representation of the abstract syntax    #
    # tree.  The string representation is formatted as follows:             #
    # (lineNum,lexPosition:treeDepth:label:environment:type,                #
    #  child1,                                                              # 
    #  child2,                                                              #
    #  ...                                                                  #
    #  childn                                                               #
    # )                                                                     #
    #-----------------------------------------------------------------------#
    def __repr__(self):
        return self.str_traverse()

    #-----------------------------------------------------------------------#
    # str_traverse(depth:int) -> string                                     #
    # This method is a recursive helper function for the "__repr__" method. #
    # The method is given an integer "depth" which represents the recursive #
    # depth of the current node.  The output is formatted as follows:       #
    # (lineNum,lexPosition:treeDepth:label:environment:type,                #
    #  child1,                                                              #
    #  child2,                                                              #
    #  ...                                                                  #
    #  childn                                                               #
    # )                                                                     #
    #-----------------------------------------------------------------------#
    def str_traverse(self, depth = 0):
        result = "(" + repr(self.lineNum) + "," + repr(self.position) + ":" +\
            repr(depth) + ":" + repr(self.label)
        if(self.label in holds_env):
            result += ":" + repr(self.env)
        if self.label == "FILE":
            result += ":" + repr(self.python_env)
        if(self.type != None):
            result += ":" + repr(self.type)
        for child in self.children:
            result += ",\n" + " " * (depth+1)              
            if isinstance(child, ast):
                result += child.str_traverse(depth+1)
            else:
                result += repr(child)
        result += "\n" + " " * depth + ")"
        return result

#------------------------------END CLASS AST-----------------------------------#

#------------------------------------------------------------------------------#
# DeclarationException                                                         #
#  Raised if a variable declaration failed.                                    #
#------------------------------------------------------------------------------#
class DeclarationException(Exception):
    pass

#------------------------------------------------------------------------------#
# NotYetDeclaredException                                                      #
#  Raised if a variable has not been declared.                                 #
#------------------------------------------------------------------------------#
class NotYetDeclaredException(Exception):
    pass

#------------------------------------------------------------------------------#
# SignatureException                                                           #
#  Raised if a function has already been declared with a given signature.      #
#------------------------------------------------------------------------------#
class SignatureException(Exception):
    pass



