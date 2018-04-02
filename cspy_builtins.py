#------------------------------------------------------------------------------#
# cspy_builtins.py                                                             #
# Lyndsay LaBarge '17                                                          #
# Summer 2016                                                                  #
#                                                                              #
# Revised and edited by Paul Magnus '18, Ines Ayara and Matthew R. Jenkins '20 #
# Summer 2017                                                                  #
#                                                                              #
# Contains the following class definitions and the CSPy builtin library        #
# and type system:                                                             #
#     type_obj   : class to represent data types                               #
#     signature  : class to represent a function signature                     #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# class type_obj                                                               #
#   A data type object.                                                        #
#   Attributes:                                                                #
#       - type_str:str   : string version of the type name                     #
#       - type: type_obj  : type this object is an instance of                 #
#       - super: type_obj  : super type of the object                          #
#       - elem_type:list : list of type obj for container types list, tuple,   #
#                          and dict                                            #
#       - sig:signature  : signature of the type_obj                           #
#                          only applies to 'fn' and 'proc' types               #
#       - methods:dict   : key:str - method name                               #
#                          value:type_obj or list of type_obj                  #
#                                which contains 'fn' or 'proc' type objects    #
#       - extendable:bool : true if the class can be a superclass of a user    #
#                           defined class                                      #
#------------------------------------------------------------------------------#
class type_obj(object):   
    #-----------------------------------------------------------------------#
    # __init__(self:type_obj, type_str:string, typ:type_obj,                #
    #          sup:type_obj = None, elem_type:[type_obj] = None,            #
    #          sig:signature = None,                                        #
    #          methods:dict of [string | type_obj or [type_obj]])           #
    #                                                                       #
    #  Initalizes attribute to their default values or given                #
    #  values if they were passed in an argument list.                      #
    #-----------------------------------------------------------------------#
    def __init__(self, type_str, typ, sup = None,
                 elem_type = [], sig = None, methods = {}, extendable=True):
        self.type_str = type_str
        self.type = typ
        self.super = sup
        self.sig = sig
        self.extendable = extendable

        # method dictionary
        #   keys   : string - method name
        #   values : type_obj or list of type_obj - 'fn' or 'proc'
        self.methods = methods

        # elem_type indices for built-in types
        #   0  - list:element type, dictionary:key type, tuple:element type
        #   1  - dictionary:value type, tuple:element type
        #   2+ - tuple:element type
        self.elem_type = elem_type


    #-----------------------------------------------------------------------#
    # lookup_method(self:type_obj, name:string) -> list of type_obj         #
    #    Returns a list of class methods whose identifier is name that      #
    #    the current type has access to either via its own method           #
    #    dictionary or the inherited method dictionary of its parent type.  #
    #-----------------------------------------------------------------------#
    def lookup_method(self, name):
        if not self.type:
            return []

        method = []
        if name in self.methods:
            method = self.methods[name]
            method = method if isinstance(method, list) else [method]

        sup_method = []
        if self.super:
            sup_method = self.super.lookup_method(name)

        for m_sig in sup_method:
            if not m_sig in method:
                method.append(m_sig)

        typ_method = type_obj.lookup_method(self.type, name)
        for typ_sig in typ_method:
            if not typ_sig in method:
                method.append(typ_sig)

        return method


    #-----------------------------------------------------------------------#
    # __eq__(self:type_obj, other:type_obj) -> bool                         #
    #    Overrides the '==' comparison operator for type_objs. Returns true #
    #    if the current type_obj has the same type signature as the other   # 
    #    type_obj.                                                          #
    #-----------------------------------------------------------------------#   
    def __eq__(self, other):
        if (not isinstance(other, type_obj)):
            return False

        # base type is different eg. IntType is FloatType - return false
        elif not basetype(self) is basetype(other):
            return False

        # container types - tuple, list, set, dictionary
        elif self.type in containertypes:
            nonempty = self.elem_type and other.elem_type 
            if nonempty:
                if (len(self.elem_type) != len(other.elem_type)):
                    return False
                else:
                    typematch = zip(self.elem_type, other.elem_type)
                    if filter(lambda t : t[0] != t[1], typematch):
                        return False
                    else:
                        return True
            else:
                # empty container - eg. l:list of int = [] is valid
                return True

        # function or procedure
        elif is_callable(self):
            return self.sig == other.sig

        # simple type - int, bool, string, float, or user type
        else:
            return True

            
                    
    #-----------------------------------------------------------------------#
    # __ne__(self:type_obj, other:type_obj) -> bool                         #
    #    Overrides the '!=' comparison operator for type_objs. Returns true #
    #    if the current type_obj does NOT have the same type signature as   #
    #    the other type_obj.                                                #
    #-----------------------------------------------------------------------#
    def __ne__(self, other):
        return not self.__eq__(other)



    #-----------------------------------------------------------------------#
    # __repr__(self:type_obj) -> string                                     #
    #    Returns a string representation of a type_obj for printing         #
    #    purposes.                                                          #
    #-----------------------------------------------------------------------#
    def __repr__(self):
        rep = self.type_str 
        if self.elem_type:
            if self.type in (builtins["list"], builtins["set"], 
                             builtins["frozenset"]):
                rep += " of " + repr(self.elem_type[0])
            if self.type is builtins["dict"]:
                rep += " of [" + repr(self.elem_type[0]) + "|" +  \
                       repr(self.elem_type[1]) + "]"
            if self.type is builtins["tuple"]:
                rep += " ("
                for e in range(len(self.elem_type)):
                    rep += repr(self.elem_type[e])
                    if e != len(self.elem_type) - 1:
                        rep += " * "
                    if (e != len(self.elem_type) - 1):
                        rep += " "
                rep += ")"
            
        if self.sig:
            rep += " " + repr(self.sig)
        return rep

#------------------------------------------------------------------------------#
# class signature                                                              #
#   Function or procedure signature object.                                    #
#   Attributes:                                                                #
#      param_types: list of type_obj      : list of the parameter types        #
#      default_types: list of type_obj    : list of default parameter types    #
#      return_type: type_obj              : method return type ('fn' only)     #
#------------------------------------------------------------------------------#
class signature(object):
    def __init__(self, params = [], defaults = [], ret = None):
        self.param_types = params
        self.default_types = defaults
        self.return_type = ret

    
    #-----------------------------------------------------------------------#
    # __eq__(self:type_obj, other:type_obj) -> bool                         #
    #    Overrides the '==' comparison operator for signatures. Returns     #
    #    true if the current signature object has the same types as         #
    #    as the other signature object.                                     #
    #-----------------------------------------------------------------------#
    def __eq__(self, other):
        assert isinstance(other, signature), "Comparing non signature object"

        if len(self.param_types) != len(other.param_types):
            return False

        elif len(self.default_types) != len(other.default_types):
            return False

        else:
            parameter_match = self.parameterCmp(other)
            return_match = self.return_type == other.return_type
            return parameter_match and return_match


    #----------------------------------------------------------------------#
    # parameterCmp(self:signature, other:signature) -> bool                #
    #   Returns true if the types of the parameters of two signature       #
    #   match each other, returns false otherwise.                         #
    #   If the current signature object contains default parameters and    #
    #   the other does not, it will attempt to match the others normal     #
    #   parameters to its defaults.This is used to match the signature     #
    #   of a function or procedure call since it is impossible to identify #
    #   which parameter is a default in a call.                            #
    #----------------------------------------------------------------------#
    def parameterCmp(self, other):
        assert isinstance(other, signature), \
            "Comparing non signature object"

        if not self.default_types and not other.default_types:
            if len(self.param_types) != len(other.param_types):
                return False

        if not self.default_types:
            if len(self.param_types) > \
                    len(other.param_types) + len(other.default_types):
                return False

        if not other.default_types:
            if len(other.param_types) > \
                    len(self.param_types) + len(self.default_types):
                return False

        current_params = self.param_types + self.default_types
        other_params = other.param_types + other.default_types
        
        match_params = zip(current_params, other_params)
        no_match = filter(lambda p : 
                          (p[0] != p[1] and p[0] != None and p[1] != None) or
                          (p[0] is None and p[1] in builtins) or
                          (p[1] is None and p[0] in builtins),
                          match_params)
      
        return False if no_match else True 


    #-----------------------------------------------------------------------#
    # __repr__(self:signature) -> string                                    #
    #    Returns a string representation of a signature for printing        #
    #    purposes.                                                          #
    #-----------------------------------------------------------------------#
    def __repr__(self):
        rep = "("
        if self.param_types != []:
            for i in range(len(self.param_types)):
                rep += repr(self.param_types[i])
                if i != (len(self.param_types) - 1):
                    rep += ", "

        if self.default_types:
            rep += ", "
            for j in range(len(self.default_types)):
                rep += "?" + repr(self.default_types[j]) 
                if j != (len(self.default_types)) - 1:
                    rep += ", "
        rep += ")"
        if self.return_type:
            rep += " -> " + repr(self.return_type)
        return rep 


#------------------------------HELPER FUNCTIONS--------------------------------#

#------------------------------------------------------------------------------#
# is_callable(typ:type_obj) -> bool                                            #
#   Returns true iff the current type is a function or procedure.              #
#------------------------------------------------------------------------------#
def is_callable(typ):
    return ((typ.type is builtins["fn"]) or (typ.type is builtins["proc"]))


#------------------------------------------------------------------------------#
# callmatch(fn1:type_obj, fn2:type_obj) -> bool                                #
#   Determines whether or not two function or procedure type objects have the  #
#   same signature (excludes return type).                                     #
#------------------------------------------------------------------------------#
def callmatch(fn1, fn2):
    sig1 = fn1.sig
    sig2 = fn2.sig
    return sig1.parameterCmp(sig2)

#------------------------------------------------------------------------------#
# is_type(typ:type_obj) -> bool                                                #
#   Returns true iff the current type obj represents a built in type           #
#   or a user defined type.                                                    #
#------------------------------------------------------------------------------#
def is_type(typ):
    types =  (builtins["type"], builtins["IntType"], 
              builtins["FloatType"], builtins["StringType"],
              builtins["BoolType"], builtins["TupleType"], 
              builtins["ListType"], builtins["FnType"], 
              builtins["ProcType"], builtins["SetType"], 
              builtins["FileType"], builtins["ExceptionType"])

    # special case for overloaded class methods
    if type(typ) == list:
        return False
    istype = map(lambda t: typ.type is t, types)
    return any(istype)

#------------------------------------------------------------------------------#
# def usertype(t:type_obj) -> bool                                             #
#   Returns true iff the type is a user defined type, not a built in type.     #
#------------------------------------------------------------------------------#
def usertype(t):
    return (basetype(t).type_str not in builtins)


#------------------------------------------------------------------------------#
# basetype(t:type_obj) -> type_obj                                             #
#  Returns the base type of a type.                                            #
#    eg) int -> IntType                                                        #
#        list of int -> ListType                                               #
#------------------------------------------------------------------------------#
def basetype(t):
        if not t or t.type is builtins["type"]:
            return t
        else:
            return basetype(t.type)


#------------------------------------------------------------------------------#
# listTostr(lst:list of type_obj)                                              #
#   Returns a string that represents a list of types.                          #
#------------------------------------------------------------------------------#
def listTostr(lst): 
    s = ""
    for i in range(len(lst)):
            s += " \'" + repr(lst[i]) + "\'"
            if len(lst) > 2:
                if (i != len(lst) - 1):
                    s += ', '
            if (i == len(lst) - 2):
                    s += ' and '
    return s


#------------------------------BUILT IN LIBRARY--------------------------------#

builtins = {}

#-------------------------------Built-In Types---------------------------------#

# Simple Types
builtins["TypeType"] = type_obj("TypeType", None, extendable=False)
builtins["type"] = type_obj("type", builtins["TypeType"], extendable=False)
builtins["object"] = type_obj("object", builtins["type"])
builtins["IntType"] = type_obj("IntType", builtins["type"], extendable=False)
builtins["int"] = type_obj("int", builtins["IntType"],
                           sup = builtins["object"], extendable=False)
builtins["BoolType"] = type_obj("BoolType", builtins["type"], extendable=False)
builtins["bool"] = type_obj("bool", builtins["BoolType"],
                            sup = builtins["object"], extendable=False)
builtins["FloatType"] = type_obj("FloatType", builtins["type"],
                                 extendable=False)
builtins["float"] = type_obj("float", builtins["FloatType"],
                             sup = builtins["object"], extendable=False)
builtins["StringType"] = type_obj("StringType", builtins["type"],
                                  extendable=False)
builtins["string"] = type_obj("string", builtins["StringType"],
                              sup = builtins["object"], extendable=False)
builtins["FileType"] = type_obj("FileType", builtins["type"], extendable=False)
builtins["file"] = type_obj("file", builtins["FileType"],
                            sup = builtins["object"], extendable=False)

# Container Types
builtins["ListType"] = type_obj("ListType", builtins["type"], extendable=False)
builtins["list"] = type_obj("list", builtins["ListType"],
                            sup=builtins["object"],
                            extendable=False)
builtins["TupleType"] = type_obj("TupleType", builtins["type"],
                                 extendable=False)
builtins["tuple"] = type_obj("tuple", builtins["TupleType"],
                             sup=builtins["object"],
                             extendable=False)
builtins["DictType"] = type_obj("DictType", builtins["type"],
                                extendable=False)
builtins["dict"] = type_obj("dict", builtins["DictType"],
                            sup=builtins["object"], extendable=False)
builtins["SetType"] = type_obj("SetType", builtins["type"], extendable=False)
builtins["set"] = type_obj("set", builtins["SetType"], sup=builtins["object"],
                           extendable=False)
builtins["FrozenSetType"] = type_obj("FrozenSetType", builtins["type"],
                                     extendable=False)
builtins["frozenset"] = type_obj("fronzenset", builtins["FrozenSetType"],
                                 sup=builtins["object"], extendable=False)
builtins["GeneratorType"] = type_obj("GeneratorType", builtins["type"],
                                     extendable=False)
builtins["generator"] = type_obj("generator", builtins["GeneratorType"],
                                 sup=builtins["object"], extendable=False)

# Types you can testing for membership in
sequencetypes = (builtins["ListType"], builtins["TupleType"],
                 builtins["DictType"], builtins["SetType"],
                 builtins["FrozenSetType"], builtins["StringType"])

# Container types that hold elements
containertypes = (builtins["ListType"], builtins["TupleType"],
                 builtins["DictType"], builtins["SetType"], 
                 builtins["FrozenSetType"])

# Types you can iterate over
iterabletypes = (builtins["ListType"], builtins["DictType"], 
                 builtins["SetType"], 
                 builtins["FrozenSetType"], builtins["StringType"],
                 builtins["FileType"], builtins["GeneratorType"])

# Function Types
builtins["FnType"] = type_obj("FnType", builtins["type"], extendable=False)
builtins["fn"] = type_obj("fn", builtins["FnType"], extendable=False)
builtins["ProcType"] = type_obj("ProcType", builtins["type"], extendable=False)
builtins["proc"] = type_obj("proc", builtins["ProcType"], extendable=False)


# Import Module
builtins["ImportModuleType"] = type_obj("ImportModuleType", builtins["type"],
                                        extendable=False)
builtins["ImportModule"] = type_obj("ImportModule",
                                    builtins["ImportModuleType"],
                                    extendable=False)

# Exceptions
#
# Exception Hierarchy (from https://docs.python.org/2/library/exceptions.html)
# BaseException
#  +-- SystemExit
#  +-- KeyboardInterrupt
#  +-- GeneratorExit
#  +-- Exception
#       +-- StopIteration
#       +-- StandardError
#       |    +-- BufferError
#       |    +-- ArithmeticError
#       |    |    +-- FloatingPointError
#       |    |    +-- OverflowError
#       |    |    +-- ZeroDivisionError
#       |    +-- AssertionError
#       |    +-- AttributeError
#       |    +-- EnvironmentError
#       |    |    +-- IOError
#       |    |    +-- OSError
#       |    |         +-- WindowsError (Windows) -> not implemented
#       |    |         +-- VMSError (VMS) -> not implemented
#       |    +-- EOFError
#       |    +-- ImportError
#       |    +-- LookupError
#       |    |    +-- IndexError
#       |    |    +-- KeyError
#       |    +-- MemoryError
#       |    +-- NameError
#       |    |    +-- UnboundLocalError
#       |    +-- ReferenceError
#       |    +-- RuntimeError
#       |    |    +-- NotImplementedError
#       |    +-- SyntaxError
#       |    |    +-- IndentationError
#       |    |         +-- TabError
#       |    +-- SystemError
#       |    +-- TypeError
#       |    +-- ValueError
#       |         +-- UnicodeError
#       |              +-- UnicodeDecodeError
#       |              +-- UnicodeEncodeError
#       |              +-- UnicodeTranslateError
#       +-- Warning
#            +-- DeprecationWarning
#            +-- PendingDeprecationWarning
#            +-- RuntimeWarning
#            +-- SyntaxWarning
#            +-- UserWarning
#            +-- FutureWarning
# 	     +-- ImportWarning
# 	     +-- UnicodeWarning
# 	     +-- BytesWarning
builtins["ExceptionType"] = type_obj("ExceptionType", builtins["type"],
                                     extendable=False)

builtins["BaseException"] = type_obj("BaseException",
                                     builtins["ExceptionType"],
                                     sup = builtins["object"],
                                     methods = {
        "__str__" : type_obj("fn", builtins["fn"],
                                sig = signature(ret = builtins["string"])),
        "__repr__" : type_obj("fn", builtins["fn"],
                              sig = signature(ret = builtins["string"])),
        "BaseException" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                     extendable=False)

builtins["SystemExit"] = type_obj("SystemExit",
                                  builtins["ExceptionType"],
                                  sup=builtins["BaseException"],
                                  methods = {
        "SystemExit" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                  extendable=False)

builtins["KeyboardInterrupt"] = type_obj("KeyboardInterrupt",
                                         builtins["ExceptionType"],
                                         sup=builtins["BaseException"],
                                         methods = {
        "KeyboardInterrupt" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                         extendable=False)

builtins["GeneratorExit"] = type_obj("GeneratorExit",
                                     builtins["ExceptionType"],
                                     sup=builtins["BaseException"],
                                     methods = {
        "GeneratorExit" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                     extendable=False)

builtins["Exception"] = type_obj("Exception", 
                                 builtins["ExceptionType"],
                                 sup = builtins["BaseException"],
                                 methods = {
        "Exception" : type_obj("proc", builtins["proc"],
                               sig = signature(params = [builtins["string"]])),
        })

builtins["StopIteration"] = type_obj("StopIteration",
                                     builtins["ExceptionType"],
                                     sup=builtins["Exception"],
                                     methods = {
        "StopIteration" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                     extendable=False)

builtins["StandardError"] = type_obj("StandardError",
                                     builtins["ExceptionType"],
                                     sup=builtins["Exception"],
                                     methods = {
        "StandardError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                     extendable=False)

builtins["Warning"] = type_obj("Warning",
                               builtins["ExceptionType"],
                               sup=builtins["Exception"],
                               methods = {
        "Warning" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        })

builtins["BufferError"] = type_obj("BufferError", 
                                   builtins["ExceptionType"],
                                   sup=builtins["StandardError"],
                                   methods = {
        "BufferError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                   extendable=False)

builtins["ArithmeticError"] = type_obj("ArithmeticError",
                                       builtins["ExceptionType"],
                                       sup=builtins["StandardError"],
                                       methods = {
        "ArithmeticError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                       extendable=False)

builtins["FloatingPointError"] = type_obj("FloatingPointError",
                                          builtins["ExceptionType"],
                                          sup=builtins["ArithmeticError"],
                                          methods = {
        "FloatingPointError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                          extendable=False)

builtins["OverflowError"] = type_obj("OverflowError",
                                     builtins["ExceptionType"],
                                     sup=builtins["ArithmeticError"],
                                     methods = {
        "OverflowError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                     extendable=False)

builtins["ZeroDivisionError"] = type_obj("ZeroDivisionError",
                                         builtins["ExceptionType"],
                                         sup=builtins["ArithmeticError"],
                                         methods = {
        "ZeroDivisionError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                         extendable=False)

builtins["AssertionError"] = type_obj("AssertionError",
                                      builtins["ExceptionType"],
                                      sup=builtins["StandardError"],
                                      methods = {
        "AssertionError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                      extendable=False)

builtins["AttributeError"] = type_obj("AttributeError",
                                      builtins["ExceptionType"],
                                      sup=builtins["StandardError"],
                                      methods = {
        "AttributeError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                      extendable=False)

builtins["EnvironmentError"] = type_obj("EnvironmentError",
                                        builtins["ExceptionType"],
                                        sup=builtins["StandardError"],
                                        methods = {
        "EnvironmentError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                        extendable=False)

builtins["IOError"] = type_obj("IOError",
                               builtins["ExceptionType"],
                               sup=builtins["EnvironmentError"],
                               methods = {
        "IOError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                               extendable=False)

builtins["OSError"] = type_obj("OSError",
                               builtins["ExceptionType"],
                               sup=builtins["EnvironmentError"],
                               methods = {
        "OSError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                               extendable=False)

builtins["EOFError"] = type_obj("EOFError",
                                builtins["ExceptionType"],
                                sup=builtins["StandardError"],
                                methods = {
        "EOFError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                extendable=False)

builtins["ImportError"] = type_obj("ImportError",
                                   builtins["ExceptionType"],
                                   sup=builtins["StandardError"],
                                   methods = {
        "ImportError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                   extendable=False)

builtins["LookupError"] = type_obj("LookupError",
                                   builtins["ExceptionType"],
                                   sup=builtins["StandardError"],
                                   methods = {
        "LookupError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                   extendable=False)

builtins["IndexError"] = type_obj("IndexError",
                                  builtins["ExceptionType"],
                                  sup=builtins["LookupError"],
                                  methods = {
        "IndexError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                  extendable=False)

builtins["KeyError"] = type_obj("KeyError",
                                builtins["ExceptionType"],
                                sup=builtins["LookupError"],
                                methods = {
        "KeyError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                extendable=False)

builtins["MemoryError"] = type_obj("MemoryError",
                                   builtins["ExceptionType"],
                                   sup=builtins["StandardError"],
                                   methods = {
        "MemoryError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                   extendable=False)

builtins["NameError"] = type_obj("NameError",
                                 builtins["ExceptionType"],
                                 sup=builtins["StandardError"],
                                 methods = {
        "NameError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                 extendable=False)

builtins["UnboundLocalError"] = type_obj("UnboundLocalError",
                                         builtins["ExceptionType"],
                                         sup=builtins["NameError"],
                                         methods = {
        "UnboundLocalError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                         extendable=False)

builtins["ReferenceError"] = type_obj("ReferenceError",
                                      builtins["ExceptionType"],
                                      sup=builtins["StandardError"],
                                      methods = {
        "ReferenceError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                      extendable=False)

builtins["RuntimeError"] = type_obj("RuntimeError",
                                    builtins["ExceptionType"],
                                    sup=builtins["StandardError"],
                                    methods = {
        "RuntimeError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                    extendable=False)

builtins["NotImplementedError"] = type_obj("NotImplementedError",
                                           builtins["ExceptionType"],
                                           sup=builtins["RuntimeError"],
                                           methods = {
        "NotImplementedError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                           extendable=False)

builtins["SyntaxError"] = type_obj("SyntaxError",
                                   builtins["ExceptionType"],
                                   sup=builtins["StandardError"],
                                   methods = {
        "SyntaxError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                   extendable=False)

builtins["TypeError"] = type_obj("TypeError",
                                 builtins["ExceptionType"],
                                 sup=builtins["StandardError"],
                                 methods = {
        "TypeError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                 extendable=False)

builtins["ValueError"] = type_obj("ValueError",
                                  builtins["ExceptionType"],
                                  sup=builtins["StandardError"],
                                  methods = {
        "ValueError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                  extendable=False)

builtins["UnicodeError"] = type_obj("UnicodeError",
                                    builtins["ExceptionType"],
                                    sup=builtins["ValueError"],
                                    methods = {
        "UnicodeError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                    extendable=False)

builtins["UnicodeDecodeError"] = type_obj("UnicodeDecodeError",
                                          builtins["ExceptionType"],
                                          sup=builtins["UnicodeError"],
                                          methods = {
        "UnicodeDecodeError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                          extendable=False)

builtins["UnicodeEncodeError"] = type_obj("UnicodeEncodeError",
                                          builtins["ExceptionType"],
                                          sup=builtins["UnicodeError"],
                                          methods = {
        "UnicodeEncodeError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                          extendable=False)

builtins["UnicodeTranslateError"] = type_obj("UnicodeTranslateError",
                                             builtins["ExceptionType"],
                                             sup=builtins["UnicodeError"],
                                             methods = {
        "UnicodeTranslateError" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        },
                                             extendable=False)

builtins["DeprecationWarning"] = type_obj("DeprecationWarning",
                                          builtins["ExceptionType"],
                                          sup=builtins["Warning"],
                                          methods = {
        "DeprecationWarning" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        })

builtins["PendingDeprecationWarning"] = type_obj("PendingDeprecationWarning",
                                                 builtins["ExceptionType"],
                                                 sup=builtins["Warning"],
                                                 methods = {
        "PendingDeprecationWarning" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        })

builtins["RuntimeWarning"] = type_obj("RuntimeWarning",
                                      builtins["ExceptionType"],
                                      sup=builtins["Warning"],
                                      methods = {
        "RuntimeWarning" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        })

builtins["SyntaxWarning"] = type_obj("SyntaxWarning",
                                     builtins["ExceptionType"],
                                     sup=builtins["Warning"],
                                     methods = {
        "SyntaxWarning" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        })

builtins["UserWarning"] = type_obj("UserWarning",
                                   builtins["ExceptionType"],
                                   sup=builtins["Warning"],
                                   methods = {
        "UserWarning" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        })

builtins["FutureWarning"] = type_obj("FutureWarning",
                                     builtins["ExceptionType"],
                                     sup=builtins["Warning"],
                                     methods = {
        "FutureWarning" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        })

builtins["ImportWarning"] = type_obj("ImportWarning",
                                     builtins["ExceptionType"],
                                     sup=builtins["Warning"],
                                     methods = {
        "ImportWarning" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        })

builtins["UnicodeWarning"] = type_obj("UnicodeWarning",
                                      builtins["ExceptionType"],
                                      sup=builtins["Warning"],
                                      methods = {
        "UnicodeWarning" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        })

builtins["BytesWarning"] = type_obj("BytesWarning",
                                    builtins["ExceptionType"],
                                    sup=builtins["Warning"],
                                    methods = {
        "BytesWarning" : type_obj("proc", builtins["proc"],
                                   sig = signature(params =
                                                   [builtins["string"]])),
        })

#------------------------------------------------------------------------------#
# is_exception(typ:type_obj) -> bool                                           #
#   Returns true if typ is a builtin exception or has a superclass of a        #
#   builtin exception.                                                         #
#------------------------------------------------------------------------------#
def is_exception(typ):
    if not isinstance(typ, type_obj):
        return False
    
    if basetype(typ) == builtins["ExceptionType"]:
        return True

    return is_exception(typ.super)

#---------------------------------Type Methods---------------------------------#

#------------------------------------------------------------------------------#
# Methods of the form __methodname__ are not callable in CSPy, instead 

#------------------------------------------------------------------------------#
# init_tuple(types:list of type_obj) -> type_obj                               #
#   Returns a tuple object with a method dictionary.                           #
#------------------------------------------------------------------------------#
def init_tuple(types):
    newtuple = type_obj("tuple", builtins["tuple"], elem_type = types,
                        extendable=False)
    methods = {      
          
                 "__repr__" : type_obj("fn", builtins["fn"], 
                                    sig = signature(ret = builtins["string"])),

                "__str__" : type_obj("fn", builtins["fn"], 
                                    sig = signature(ret = builtins["string"])),

                "__bool__" : type_obj("fn", builtins["fn"], 
                                    sig = signature(ret = builtins["bool"])),
    
                # Exact return types of indexing,splicing, *, and +
                # are determined in type checker
                "__getitem__" : type_obj("fn", builtins["fn"],
                                sig = signature(params = [builtins["int"]],
                                                ret = builtins["object"])),

                "__getslice__" : type_obj("fn", builtins["fn"], 
                              sig = signature(defaults = [builtins["int"],
                                                          builtins["int"], 
                                                          builtins["int"]], 
                                               ret = type_obj("tuple", 
                                                          builtins["tuple"]))),

                "__add__" : type_obj("fn", builtins["fn"], 
                            sig = signature(params = [builtins["tuple"]], 
                                            ret = builtins["tuple"])), 
                
                "__mul__" : type_obj("fn", builtins["fn"], 
                            sig = signature(params = [builtins["int"]], 
                                            ret = builtins["tuple"])), 

                "__ne__" : type_obj("fn", builtins["fn"], 
                                    sig = signature(params = [newtuple], 
                                                    ret = builtins["bool"])), 
                "__eq__" : type_obj("fn", builtins["fn"], 
                                    sig = signature(params = [newtuple], 
                                                    ret = builtins["bool"])) }
    newtuple.methods = methods
    return newtuple


#------------------------------------------------------------------------------#
# init_list([elem_type: type_obj]) -> type_obj                                 #
#   Returns a list type_obj whose method signatures match the element type of  #
#   the list.                                                                  #
#------------------------------------------------------------------------------#
def init_list(elem_type):
     listtype = type_obj("list", builtins["list"], elem_type = elem_type,
                         extendable=False)
     try:
         elem_type = elem_type[0]
     except IndexError:
         elem_type = None
                        
     methods = {    "append" : type_obj("proc", builtins["proc"], 
                                        sig = signature(params = [elem_type])),
                    
                    
                    "__bool__" : type_obj("fn", builtins["fn"],
                                          sig = signature(ret =
                                                          builtins["int"])), 
                    
                    "extend" : type_obj("proc", builtins["proc"],
                                        sig = signature(params = [listtype])), 
                    
                    "insert" : type_obj("proc", builtins["proc"], 
                                        sig = signature(params =
                                                        [builtins["int"], 
                                                         elem_type])),
                    
                    "remove" : type_obj("proc", builtins["proc"],
                                        sig = signature(params = [elem_type])),
                    
                    "pop" : type_obj("fn", builtins["fn"], 
                                     sig = signature(defaults =
                                                     [builtins["int"]], 
                                                     ret = elem_type)), 
                    
                    "clear" : type_obj("proc", builtins["proc"],
                                       sig = signature()), 
                    
                    "index" : type_obj("fn", builtins["fn"], 
                                       sig = signature(params = [elem_type], 
                                                       ret = builtins["int"])), 
                    
                    "count" : type_obj("fn", builtins["fn"], 
                                       sig = signature(params = [elem_type], 
                                                       ret = builtins["int"])),
                    
                    "reverse" : type_obj("proc", builtins["proc"], 
                                         sig = signature()),
                    
                    "sort" : type_obj("proc", builtins["proc"],
                                      sig = signature()),
                    
                    "copy" : type_obj("fn", builtins["fn"], 
                                      sig = signature(ret =
                                                      type_obj("list", 
                                                               builtins["list"],
                                                               elem_type =
                                                               [elem_type]))), 
                    
                    "__getslice__" : type_obj("fn", builtins["fn"], 
                                              sig = signature(defaults =
                                                              [builtins["int"],
                                                               builtins["int"], 
                                                               builtins["int"]],
                                                              ret = listtype)),
                    
                    "__getitem__" : type_obj("fn", builtins["fn"], 
                                             sig = signature(params =
                                                             [builtins["int"]], 
                                                             ret = elem_type)),
                    
                    "__add__" : type_obj("fn", builtins["fn"], 
                                         sig = signature(params = [listtype], 
                                                         ret = listtype)),
                    
                    "__eq__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [listtype], 
                                                        ret =
                                                        builtins["bool"])),
                    
                    "__ne__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [listtype], 
                                                        ret =
                                                        builtins["bool"])),
                    
                    "__mul__" : type_obj("fn", builtins["fn"], 
                                         sig = signature(params =
                                                         [builtins["int"]], 
                                                         ret = listtype)),
                    
                    "__repr__" : type_obj("fn", builtins["fn"], 
                                          sig = signature(ret =
                                                          builtins["string"])),
                    
                    "__str__" : type_obj("fn", builtins["fn"], 
                                         sig = signature(ret =
                                                         builtins["string"])),
                    
                    }

     listtype.methods = methods
     return listtype


#------------------------------------------------------------------------------#
# init_dict([key_type:type_obj, value_type:type_obj]) -> type_obj              #
#   Returns a dictionary type_obj whose method signatures match the key type   #
#   and value type of the dictionary.                                          #
#------------------------------------------------------------------------------#
def init_dict(types):
    newdict = type_obj("dict", builtins["dict"], elem_type = types,
                       extendable=False)
    try:
        key_type, value_type = types
    except ValueError:
        key_type, value_type = (None, None)
    methods =   {  "clear" : type_obj("proc", builtins["proc"], 
                                      sig = signature()),
                   
                   "copy" : type_obj("fn", builtins["fn"],
                                     sig = signature(ret = newdict)),
                   
                   
                   
                   "get" : type_obj("fn", builtins["fn"],
                                    sig = signature(params =
                                                    [key_type, value_type],
                                                    ret = value_type)),
                   
                   "has_key" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [key_type], 
                                                        ret =
                                                        builtins["bool"])),
                   
                   "items" : type_obj("fn", builtins["fn"],
                                      sig =
                                      signature(ret =
                                               init_list([init_tuple(types)]))),
                   
                   "keys" : type_obj("fn", builtins["fn"], 
                                     sig = signature(ret =
                                                     init_list([key_type]))),
                   
                   "pop" : type_obj("fn", builtins["fn"], 
                                    sig = signature(params = [key_type], 
                                                    defaults = [value_type], 
                                                    ret = value_type)), 
                   
                   "popitem" : type_obj("fn", builtins["fn"], 
                                        sig = signature(ret =
                                                        init_tuple(types))), 
                   
                   
                   "setdefault" : type_obj("proc", builtins["proc"], 
                                           sig = signature(params =
                                                           [key_type, 
                                                            value_type])),
                   
                   "update" : type_obj("proc", builtins["proc"], 
                                       sig = signature(params = [newdict])),
                   
                   "values" : type_obj("fn", builtins["fn"], 
                                       sig =
                                       signature(ret =
                                                 init_list([value_type]))),
                   
                   "__eq__" : type_obj("fn", builtins["fn"], 
                                       sig = signature(params = [newdict], 
                                                       ret = builtins["bool"])),
                   
                   "__getitem__" : type_obj("fn", builtins["fn"],
                                            sig = signature(params = [key_type],
                                                            ret = value_type)),
                   
                   "__ne__" : type_obj("fn", builtins["fn"], 
                                       sig = signature(params = [newdict], 
                                                       ret = builtins["bool"])),
                   
                   "__repr__" : type_obj("fn", builtins["fn"], 
                                         sig = signature(ret =
                                                         builtins["string"])),
                   
                   "__str__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(ret =
                                                        builtins["string"])),
                   
                   
                   "__bool__" : type_obj("fn", builtins["fn"],
                                         sig = signature(ret =
                                                         builtins["int"])), 
                   
                   }

    newdict.methods = methods
    return newdict


#------------------------------------------------------------------------------#
# init_set(settype: list of type_obj)                                          #
#   Returns a new set instance whose method dictionary corresponds to its      #
#   element type.                                                              #
#------------------------------------------------------------------------------#
def init_set(settype):
    newset = type_obj("set", builtins["set"], elem_type = settype,
                      extendable=False)

    # Corresponding types for other iterables, used in 
    # method signatures
    newlist = type_obj("list", builtins["list"], elem_type = settype,
                       extendable=False)
    newfrzset = type_obj("frozenset", builtins["frozenset"], 
                         elem_type = settype,
                         extendable=False)

    try:
        settype = settype[0]
    except IndexError:
        settype = None
    

    methods = {
                 "isdisjoint" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),
                 "issubset" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),
                 "__le__"   : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),
                 "__lt__"   : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),
                 "issuperset" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),
                 "__ge__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),
                 "__gt__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),
                 "union" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = newset)),
                 "intersection" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = newset)),
                 "difference" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = newset)),

                 "symmetric_difference" : type_obj("fn", builtins["fn"], 
                                            sig = signature(params = [newset], 
                                                            ret = newset)),
                 "copy" : type_obj("fn", builtins["fn"], 
                                        sig = signature(ret = newset)),

                 "__and__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = newset)),

                 "__or__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = newset)),

                 "__sub__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = newset)),

                 "__xor__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = newset)), 
                 "__repr__" : type_obj("fn", builtins["fn"], 
                                    sig = signature(ret = builtins["string"])),

                 "__str__" : type_obj("fn", builtins["fn"], 
                                    sig = signature(ret = builtins["string"])),
                 
                 "__bool__" : type_obj("fn", builtins["fn"],
                            sig = signature(ret = builtins["int"])), 

                 "__eq__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),

                 "__ne__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),

                 # Set only - frozen set does not have 

                 "update" : type_obj("proc", builtins["proc"], 
                                        sig = signature(params = [newset])), 

                 "intersection_update" :[ type_obj("proc", builtins["proc"], 
                                        sig = signature(params = [newset])),

                                        type_obj("proc", builtins["proc"], 
                                        sig = signature(params = [newlist])), 
                                         
                                        type_obj("proc", builtins["proc"], 
                                        sig = signature(params = [newfrzset]))],
                                                                                

                 "difference_update" : [ type_obj("proc", builtins["proc"], 
                                        sig = signature(params = [newset])),

                                        type_obj("proc", builtins["proc"], 
                                        sig = signature(params = [newlist])), 
                            
                                        type_obj("proc", builtins["proc"], 
                                        sig = signature(params = [newfrzset]))],

                 "symmetric_difference_update": [
                                        type_obj("proc", builtins["proc"], 
                                        sig = signature(params = [newset])),

                                        type_obj("proc", builtins["proc"], 
                                        sig = signature(params = [newlist])), 
                                          
                                        type_obj("proc", builtins["proc"], 
                                        sig = signature(params = [newfrzset]))],


                 "add": type_obj("proc", builtins["proc"], 
                                 sig = signature(params = [settype])), 

                 "remove": type_obj("proc", builtins["proc"], 
                                 sig = signature(params = [settype])),

                 "discard" : type_obj("proc", builtins["proc"], 
                                 sig = signature(params = [settype])),

                 "pop" : type_obj("fn", builtins["fn"], 
                                 sig = signature(ret = settype)),

                 "clear" : type_obj("proc", builtins["proc"], 
                                 sig = signature())}

    newset.methods = methods
    return newset



#------------------------------------------------------------------------------#
# init_frzset(settype:list of type_obj) -> type_obj                            #
#   Returns a set type objects whose method dictionary corresponds to its      #
#   element type.                                                              #
#------------------------------------------------------------------------------#
def init_frzset(settype): 
    newset = type_obj("frozenset", builtins["frozenset"], elem_type = settype,
                      extendable=False)

    try:
        settype = settype[0]
    except IndexError:
        settype = None

    methods = {
                 "isdisjoint" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),
                 "issubset" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),
                 "__le__"   : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),
                 "__lt__"   : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),
                 "issuperset" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),
                 "__ge__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),
                 "__gt__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),
                 "union" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = newset)),

                 "intersection" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = newset)),

                 "difference" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = newset)),
                 "symmetric_difference" : type_obj("fn", builtins["fn"], 
                                            sig = signature(params = [newset], 
                                                            ret = newset)),
                 "copy" : type_obj("fn", builtins["fn"], 
                                        sig = signature(ret = newset)),

                 "__and__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = newset)),

                 "__or__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = newset)),

                 "__sub__ " : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = newset)),

                 "__xor__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = newset)), 
                 "__repr__" : type_obj("fn", builtins["fn"], 
                                    sig = signature(ret = builtins["string"])),

                 "__bool__" : type_obj("fn", builtins["fn"],
                            sig = signature(ret = builtins["int"])), 

                 "__str__" : type_obj("fn", builtins["fn"], 
                                    sig = signature(ret = builtins["string"])),

                 "__eq__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),

                 "__ne__" : type_obj("fn", builtins["fn"], 
                                        sig = signature(params = [newset], 
                                                       ret = builtins["bool"])),

                 }
    newset.methods = methods
    return newset


#------------------------------------------------------------------------------#
# init_generator([elem_type: type_obj]) -> type_obj                            #
#   Returns a generator type_obj whose method signatures match the element     #
#   type of the generator.                                                     #
#------------------------------------------------------------------------------#
def init_generator(elem_type):
    generatortype = type_obj("generator", builtins["generator"],
                             elem_type = elem_type,
                             extendable=False)
    try:
        elem_type = elem_type[0]
    except IndexError:
        elem_type = None

    methods = {
        "close" : type_obj("proc", builtins["proc"],
                           sig = signature()),
        "next" : type_obj("fn", builtins["fn"],
                          sig = signature(ret = elem_type))
                    }

    generatortype.methods = methods
    return generatortype

# Float Methods
builtins["float"].methods = {

    "__add__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["float"]], 
                                         ret = builtins["float"])),
    
    "__bool__" : type_obj("fn", builtins["fn"],
                          sig = signature(ret = builtins["int"])), 
    
    "__div__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["float"]],
                                         ret = builtins["float"])),
    
    "__eq__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["float"]], 
                                        ret = builtins["bool"])),
    
    "__float__" : type_obj("fn", builtins["fn"],
                           sig = signature(ret = builtins["float"])),
    
    "__floordiv__" : type_obj("fn", builtins["fn"], 
                              sig = signature(params = [builtins["float"]],
                                              ret = builtins["float"])), 
    
    "__ge__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["float"]], 
                                        ret = builtins["bool"])),
    
    "__gt__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["float"]], 
                                        ret = builtins["bool"])),
    
    "__int__" : type_obj("fn", builtins["fn"],
                         sig = signature(ret = builtins["int"])), 
    
    "__le__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["float"]], 
                                        ret = builtins["bool"])), 
    
    "__lt__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["float"]], 
                                        ret = builtins["bool"])),
    
    "__mod__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["float"]],
                                         ret = builtins["float"])),
    
    "__mul__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["float"]],
                                         ret = builtins["float"])),
    
    "__ne__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["float"]], 
                                        ret = builtins["bool"])),
    
    "__neg__" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["float"])),
    
    "__pos__" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["float"])),
    
    "__pow__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["float"]],
                                         ret = builtins["float"])),
    
    "__repr__" : type_obj("fn", builtins["fn"], 
                          sig = signature(ret = builtins["string"])),
    
    "__str__" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["string"])),
    
    "__sub__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["float"]],
                                         ret = builtins["float"])),
    
    "__trunc__" : type_obj("fn", builtins["fn"], 
                           sig = signature(ret = builtins["int"])) }

# Int Methods
builtins["int"].methods =  {  
    
    "__add__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["int"]],
                                         ret = builtins["int"])),
    
    "__and__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["int"]], 
                                         ret = builtins["int"])),
    
    "__bool__" : type_obj("fn", builtins["fn"],
                          sig = signature(ret = builtins["int"])), 
    
    "__cmp__" : type_obj("fn", builtins["fn"],
                         sig = signature(params = [builtins["int"]],
                                         ret = builtins["int"])),
    
    "__div__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["int"]],
                                         ret = builtins["int"])),
    
    "__eq__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["int"]], 
                                        ret = builtins["bool"])),
    
    "__float__" : type_obj("fn", builtins["fn"],
                           sig = signature(ret = builtins["float"])),
    
    "__floordiv__" : type_obj("fn", builtins["fn"], 
                              sig = signature(params = [builtins["int"]],
                                              ret = builtins["int"])), 
    
    "__ge__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["int"]], 
                                        ret = builtins["bool"])),
    
    "__gt__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["int"]], 
                                        ret = builtins["bool"])),
    
    "__int__" : type_obj("fn", builtins["fn"],
                         sig = signature(ret = builtins["int"])),
    
    "__invert__" : type_obj("fn", builtins["fn"], 
                            sig = signature(ret = builtins["int"])), 
    
    "__le__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["int"]], 
                                        ret = builtins["bool"])), 
    
    "__lshift__" : type_obj("fn", builtins["fn"], 
                            sig = signature(ret = builtins["int"])),
    
    "__lt__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["int"]], 
                                        ret = builtins["bool"])),
    
    "__mod__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["int"]],
                                         ret = builtins["int"])),
    
    "__mul__" : [type_obj("fn", builtins["fn"], 
                          sig = signature(params = [builtins["int"]],
                                          ret = builtins["int"])),
                 
                 type_obj("fn", builtins["fn"], 
                          sig = signature(params = [builtins["list"]],
                                          ret = builtins["list"])),
                 
                 type_obj("fn", builtins["fn"], 
                          sig = signature(params = [builtins["tuple"]],
                                          ret = builtins["tuple"])),
                 
                 type_obj("fn", builtins["fn"], 
                          sig = signature(params = [builtins["string"]],
                                          ret = builtins["string"]))],
    

    "__ne__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["int"]], 
                                        ret = builtins["bool"])),
    
    "__neg__" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["int"])),
    
    "__oct__" : type_obj("fn", builtins["fn"], 
                            sig = signature(ret = builtins["string"])),
    
    "__or__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["int"]], 
                            ret = builtins["int"])),
    
    "__pos__" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["int"])),
    
    "__pow__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["int"]],
                                                     ret = builtins["int"])),
    
    "__repr__" : type_obj("fn", builtins["fn"], 
                          sig = signature(ret = builtins["string"])),
    
    "__str__" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["string"])),
    
    "__sub__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["int"]],
                                         ret = builtins["int"])),
    
    "__xor__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["int"]], 
                                         ret = builtins["int"])) }


# Bool Methods
builtins["bool"].methods = {
    
    "__bool__" : type_obj("fn", builtins["fn"], 
                          sig = signature(ret = builtins["bool"])),
    
    "__booland__" :  type_obj("fn", builtins["fn"], 
                              sig = signature(params = [builtins["bool"]],
                                              ret = builtins["bool"])),
    
    "__boolor__" : type_obj("fn", builtins["fn"], 
                            sig = signature(params = [builtins["bool"]],
                                            ret = builtins["bool"])),
    
    "__boolnot__" : type_obj("fn", builtins["fn"], 
                             sig = signature(ret = builtins["bool"])),
    
    "__eq__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["bool"]],
                                        ret = builtins["bool"])),
    
    "__ne__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["bool"]],
                                        ret = builtins["bool"])),
    
    "__str__" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["string"])),
    "__repr__" : type_obj("fn", builtins["fn"], 
                          sig = signature(ret = builtins["string"]))}

# String Methods
builtins["string"].methods = {

    "__add__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["string"]],
                                         ret = builtins["string"])),
    
    
    "__bool__" : type_obj("fn", builtins["fn"],
                          sig = signature(ret = builtins["bool"])), 
    
    "__eq__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["string"]], 
                                        ret = builtins["bool"])),
    
    "__ne__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["string"]], 
                                        ret = builtins["bool"])),
    
    "__ge__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["string"]], 
                                        ret = builtins["bool"])),
    # Indexing
    
    "__getitem__" : type_obj("fn", builtins["fn"], 
                             sig = signature(params = [builtins["int"]], 
                                             ret = builtins["string"])),
    
    
    # Slicing                
    "__getslice__" : type_obj("fn", builtins["fn"], 
                              sig = signature(defaults = [builtins["int"],
                                                          builtins["int"], 
                                                          builtins["int"]], 
                                              ret = builtins["string"])),
    
    
    "__gt__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["string"]], 
                                        ret = builtins["bool"])),
    
    "__le__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["string"]], 
                                        ret = builtins["bool"])),
    
    
    "__lt__" : type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["string"]], 
                                        ret = builtins["bool"])),
    
    "__mul__" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["int"]],
                                         ret = builtins["string"])),
    
    "__str__" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["string"])),
    
    "__int__" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["int"])), 
    
    "__float__" : type_obj("fn", builtins["fn"], 
                           sig = signature(ret = builtins["float"])), 
    
    "__repr__" : type_obj("fn", builtins["fn"], 
                          sig = signature(ret = builtins["string"])),
    
    
    "capitalize" : type_obj("fn", builtins["fn"], 
                            sig = signature(ret = builtins["string"])),
    
    "center" : type_obj("fn", builtins["fn"],
                        sig = signature(params = [builtins["int"]],
                                        defaults = [builtins["string"]],
                                        ret = builtins["string"])),
    
    "count" : type_obj("fn", builtins["fn"],
                       sig = signature(params = [builtins["string"]],
                                       defaults = [builtins["int"], 
                                                   builtins["int"]], 
                                       ret = builtins["int"])),
    
    "decode" : type_obj("fn", builtins["fn"], 
                        sig = signature(defaults = [builtins["string"],
                                                    builtins["string"]],
                                        ret = builtins["string"])),
    
    "encode" : type_obj("fn", builtins["fn"], 
                        sig = signature(defaults = [builtins["string"],
                                                    builtins["string"]],
                                        ret = builtins["string"])),
    
    "endswith" : type_obj("fn", builtins["fn"], 
                          sig = signature(params = [builtins["string"]], 
                                          defaults = [builtins["int"],
                                                      builtins["int"]],
                                          ret = builtins["bool"])),
    
    "expandtabs" : type_obj("fn", builtins["fn"],
                            sig = signature(defaults = [builtins["int"]],
                                            ret = builtins["string"])),
    
    "find" : type_obj("fn", builtins["fn"], 
                      sig = signature(params = [builtins["string"]], 
                                      defaults = [builtins["int"], 
                                                  builtins["int"]],
                                      ret = builtins["int"])),
    
    "index" : type_obj("fn", builtins["fn"], 
                       sig = signature(params = [builtins["string"]], 
                                       defaults = [builtins["int"],
                                                   builtins["int"]])),
    
    "isalnum" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["bool"])),
    
    "isalpha" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["bool"])),
    
    
    "isdigit" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["bool"])),
    
    
    "islower" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["bool"])),
    
    
    "istitle" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["bool"])),
    
    
    "isnumeric" : type_obj("fn", builtins["fn"], 
                           sig = signature(ret = builtins["bool"])),
    
    "isspace" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["bool"])),
    
    "isupper" : type_obj("fn", builtins["fn"], 
                         sig = signature(ret = builtins["bool"])),
    
    "join" : type_obj("fn", builtins["fn"], 
                      sig = signature(params = [type_obj("list",
                                                         builtins["list"], 
                                                         elem_type =
                                                         [builtins["string"]])],
                                      ret = builtins["string"])),
    
    "ljust" : type_obj("fn", builtins["fn"], 
                       sig = signature(params = [builtins["int"]],
                                       defaults = [builtins["string"]], 
                                       ret = builtins["string"])),
    
    "lower" : type_obj("fn", builtins["fn"],
                       sig = signature(ret = builtins["string"])),
    
    
    "lstrip" : type_obj("fn", builtins["fn"], 
                        sig = signature(ret = builtins["string"])), 
    
    
    "replace" : type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["string"],
                                                   builtins["string"]], 
                                         defaults = [builtins["int"]], 
                                         ret = builtins["string"])),
    
    
    "rfind" :  type_obj("fn", builtins["fn"], 
                        sig = signature(params = [builtins["string"]], 
                                        defaults = [builtins["int"], 
                                                    builtins["int"]],
                                        ret = builtins["int"])),
    
    "rindex" :  type_obj("fn", builtins["fn"], 
                         sig = signature(params = [builtins["string"]], 
                                         defaults = [builtins["int"],
                                                     builtins["int"]])),
    
    "rjust" : type_obj("fn", builtins["fn"], 
                       sig = signature(params = [builtins["int"]],
                                       defaults = [builtins["string"]], 
                                       ret = builtins["string"])),
    
    "rstrip" : type_obj("fn", builtins["fn"], 
                        sig = signature(ret = builtins["string"])), 
    
    
    "split" : type_obj("fn", builtins["fn"], 
                       sig = signature(defaults = [builtins["string"], 
                                                   builtins["int"]],
                                       ret = init_list([builtins["string"]]))),
    
    
    "splitlines" : type_obj("fn", builtins["fn"],
                            sig = signature(defaults = builtins["int"], 
                                            ret =
                                            init_list([builtins["string"]]))),
    
    
    "startswith" : type_obj("fn", builtins["fn"], 
                            sig = signature(params = [builtins["string"]],
                                            defaults = [builtins["int"], 
                                                        builtins["int"]],
                                            ret = builtins["bool"])),
    
    "strip" : type_obj("fn", builtins["fn"], 
                       sig = signature(defaults = [builtins["string"]], 
                                       ret = builtins["string"])),
    
    "swapcase" : type_obj("fn", builtins["fn"], 
                          sig = signature(ret = builtins["string"])),
    
    "title" : type_obj("fn", builtins["fn"], 
                       sig = signature(ret = builtins["string"])), 
    
    "upper" : type_obj("fn", builtins["fn"], 
                       sig = signature(ret = builtins["string"])) }

# File methods
builtins["file"].methods = {
    
    "close" : type_obj("proc", builtins["proc"], 
                       sig = signature()), 
    
    "closed" : builtins["bool"],
    
    "flush" : type_obj("proc", builtins["proc"], 
                       sig = signature()), 
    
    
    "fileno" : type_obj("fn", builtins["fn"], 
                        sig = signature(ret = builtins["int"])),
    
    "mode" : builtins["string"], 
    
    "name" : builtins["string"],
    
    "next" : type_obj("fn", builtins["fn"], 
                      sig = signature(ret = builtins["string"])),
    
    "read" : type_obj("fn", builtins["fn"], 
                      sig = signature(defaults = [builtins["int"]], 
                                      ret = builtins["string"])),
    
    "readline" : type_obj("fn", builtins["fn"], 
                          sig = signature(defaults = [builtins["int"]], 
                                          ret = builtins["string"])),
    
    "readlines" : type_obj("fn", builtins["fn"], 
                           sig = signature(defaults = 
                                           [builtins["int"]],
                                           ret =
                                           type_obj("list", 
                                                    builtins["list"],
                                                    elem_type = 
                                                    [builtins["string"]]))), 
    
    
    "seek" : type_obj("proc", builtins["proc"], 
                      sig = signature(params = [builtins["int"]], 
                                      defaults = [builtins["int"]])), 
    "tell" : type_obj("fn", builtins["fn"], 
                      sig = signature(ret = builtins["int"])), 
    
    
    "truncate": type_obj("proc", builtins["proc"], 
                         sig = signature(defaults = [builtins["int"]])),
    
    
    "write" : type_obj("proc", builtins["proc"], 
                       sig = signature(params = [builtins["string"]])),
    
    "writelines" : type_obj("proc", builtins["proc"], 
                            sig = signature(params =
                                            [type_obj("list", 
                                                      builtins["list"],
                                                      elem_type = 
                                                      [builtins["string"]])])),
    }



#-----------------------TYPE CONVERSIONS, CONSTRUCTORS-------------------------#


# equivalent to python bool()
def builtins_tobool(parameters):
    if len(parameters) != 1:
        return (None, "'tobool' expected exactly 1 argument, but received " + 
                str(len(parameters)) + " instead.")
    else:
        p = parameters[0]
        m = p.lookup_method("__bool__")
        
        if m:
            # type can be converted to bool
            return (type_obj("fn", builtins["fn"], 
                            sig = signature(params = parameters, 
                                            ret = m[0].sig.return_type)), None)
        else:
            # type cannot be converted to bool
            return (None,  "'" + repr(p) + "' type cannot be converted " +
                    "to 'bool' type.")

builtins["tobool"] = builtins_tobool



# equivalent to python int()
def builtins_toint(parameters):
    if len(parameters) != 1:
        return (None, "'toint' expected exactly 1 argument, but received " + 
                str(len(parameters)) + " instead.")
    else:
        p = parameters[0]
        m = p.lookup_method("__int__")
        if m:
            # type can be converted to integer
            return (type_obj("fn", builtins["fn"], 
                            sig = signature(params = parameters, 
                                            ret = m[0].sig.return_type)), None)
        else:
            # type cannot be converted to integer
            return (None,  "'" + repr(p) + "' type cannot be converted " +
                    "to 'int' type.")

builtins["toint"] = builtins_toint



# equivalent to python float()
def builtins_tofloat(parameters):
    if len(parameters) != 1:
        return (None, "'tofloat' expected exactly 1 argument, but received " + 
                str(len(parameters)) + " instead.")
    else:
        p = parameters[0]
        m = p.lookup_method("__float__")
        if m:
            # type can be converted to float
            return (type_obj("fn", builtins["fn"], 
                            sig = signature(params = parameters, 
                                            ret = m[0].sig.return_type)), None)
        else:
            # type cannot be converted to float
            return (None,  "'" + repr(p) + "' type cannot be converted " +
                    "to 'float' type.")

builtins["tofloat"] = builtins_tofloat



# equivalent to python str()
def builtins_tostring(parameters):
    if len(parameters) != 1:
        return (None, "'tostring' expected exactly 1 argument, but received " + 
                str(len(parameters)) + " instead.")
    else:
        p = parameters[0]
        m = p.lookup_method("__str__")
        if m:
            # type can be converted to string
            return (type_obj("fn", builtins["fn"],
                            sig = signature(params = parameters,
                                            ret = m[0].sig.return_type)), None)
        else:
            # type cannot be converted to string
            return (None,  "'" + repr(p) + "' type cannot be converted " +
                    "to 'string' type.")

builtins["tostring"] = builtins_tostring



# equivalent to python list()
def builtins_tolist(parameters):
    if len(parameters) != 1:
        return (None, "'tolist' expected exactly 1 argument, but received " + 
                str(len(parameters)) + " instead.")
    else:
        p = parameters[0]
        base = basetype(p)
        # cannot convert to list eg. tolist(4)
        if base not in sequencetypes:
            return (None,  "'" + repr(p) + "' type cannot be converted " +
                    "to 'list' type.'")
        else:

            # tuples with multiple types cannot be converted to lists
            if base is builtins["TupleType"] and len(p.elem_type) > 1:
                heterogeneous = [t != p.elem_type[0] for t in p.elem_type]
                if any(heterogeneous):
                    return (None, "'" + repr(p) + "' cannot be converted to " +
                        "'list' type because it contains more than 1 " + 
                        "element type.")

            # set
            # if  base is builtins["SetType"]:
            # frozenset

            # type can be converted to a list
            newlist = init_list([builtins["string"]] \
                                    if basetype(p) is builtins["StringType"] \
                                    else [p.elem_type[0]])
            return (type_obj("fn", builtins["fn"], 
                                sig = signature(params = parameters, 
                                                ret = newlist)), None)

builtins["tolist"] = builtins_tolist


def builtins_todict(parameters):
    if len(parameters) != 1:
        return (None, "'todict' expected exactly 1 argument, but received " + 
                str(len(parameters)) + " instead.")
    
    # only a list, tuple, or set can be converted to a dictionary
    elif basetype(parameters[0]) not in containertypes:
        return (None,  "'" + repr(parameters[0]) + 
                "' type cannot be converted " +
                "to 'dictionary' type.'")
    else:
        container = parameters[0]
        containertype = basetype(container)

        if not container.elem_type:
            return (type_obj("fn", builtins["fn"], 
                             sig = signature(params = parameters, 
                                             ret = init_dict([]))), None)
            
        if containertype is builtins["TupleType"] and \
                len(container.elem_type) > 1:
            heterogeneous = \
                [t != container.elem_type[0] for t in container.elem_type]
            if any(heterogeneous):
                return (None, "'" + repr(p) + "' cannot be converted to " +
                        "'list' type because it contains more than 1 " + 
                        "element type.")

        element = container.elem_type[0]
        # the elements in the container must be a tuple 
        # consisting of two items (key value, value value)
        if basetype(element) is not builtins["TupleType"]:
            return (None,  "'" + repr(container) + "' type cannot be "\
                        "converted to 'dictionary' type.'")

        elif len(element.elem_type) != 2:
            return (None,  "'" + repr(container) + "' type cannot be " \
                        "converted to 'dictionary' type.'")

        else:
            key = element.elem_type[0]
            value = element.elem_type[1]
            newdict = init_dict([key, value])
            return (type_obj("fn", builtins["fn"], 
                             sig = signature(params = parameters, 
                                             ret = newdict)), None)



builtins["todict"] = builtins_todict

                
# equivalent to python frozenset()
def builtins_frzset(parameters):
    if len(parameters) > 1:
        return (None, "'frzset' expected at most 1 argument, but received " + 
                str(len(parameters)) + " instead.")

    else:

        # Check if empty set
        try:
            p = parameters[0]
        except IndexError:
             return (type_obj("fn", builtins["fn"], 
                                sig = signature(params = parameters, 
                                                ret = init_frzset([]))), None)

        base = basetype(p)    
        if base not in sequencetypes:
            # cannot covert type to frozenset eg. frzset(4)
            return (None,  "'" + repr(p) + "' type cannot be converted " +
                    "to 'frozenset' type.'")
        else:
            # tuples with multiple types cannot be converted to sets
            if base is builtins["TupleType"] and len(p.elem_type) > 1:
                heterogeneous = [t != p.elem_type[0] for t in p.elem_type]
                if any(heterogeneous):
                    return (None, "'" + repr(p) + "' cannot be converted to " +
                        "'frozenset' type because it contains more than 1 " + 
                        "element type.")

            # convert to frozenset
            newset = \
                init_frzset([builtins["string"]] \
                                if basetype(p) is builtins["StringType"] \
                                else [p.elem_type[0]])
            return (type_obj("fn", builtins["fn"], 
                                sig = signature(params = parameters, 
                                                ret = newset)), None)

builtins["frzset"] = builtins_frzset

# equivalent to python set()
def builtins_makeset(parameters):
    if len(parameters) > 1:
        return (None, "'makeset' expected at most 1 argument, but received " + 
                str(len(parameters)) + " instead.")
    else:        

        # Check if empty set
        try:
            p = parameters[0]
        except IndexError:
            return (type_obj("fn", builtins["fn"], 
                                sig = signature(params = parameters, 
                                                ret = init_set([]))), None) 

        base = basetype(p)
        if basetype(p) not in sequencetypes:
            # cannot convert type to set
            return (None,  "'" + repr(p) + "' type cannot be converted " +
                    "to 'set' type.'")

        else:
            # only homogeneous tuples can becomes sets
            # tuples with multiple types cannot be converted to sets
            if base is builtins["TupleType"] and len(p.elem_type) > 1:
                heterogeneous = [t != p.elem_type[0] for t in p.elem_type]
                if any(heterogeneous):
                    return (None, "'" + repr(p) + "' cannot be converted to " +
                        "'set' type because it contains more than 1 " + 
                        "element type.")

            # convert to set
            newset  = \
                init_set([builtins["string"]] \
                             if basetype(p) is builtins["StringType"] \
                             else [p.elem_type[0]])
            return (type_obj("fn", builtins["fn"], 
                                sig = signature(params = parameters, 
                                                ret = newset)), None)

builtins["makeset"] = builtins_makeset


#---------------------BUIlT IN FUCTIONS WITH DEPENDENT RETURNS-----------------#

# cmp(a:int, b:int) -> int
# cmp(a:float, b:float) -> int
# cmp(a:string, b:string) -> int
# cmp(a:bool, b:bool) -> int
# cmp(a:list, b:list) -> int
# cmp(a:tuple, b:tuple) -> int
# cmp(a:dict, b:dict) -> int
# cmp(a:set, b:set) -> int
# cmp(a:frozenset, b:frozenset) -> int
def builtins_cmp(parameters):
    if len(parameters) != 2:
        return (None, "'cmp' expected exactly 2 arguments, but received " + 
                str(len(parameters)) + " instead.")

    elif parameters[0] != parameters[1]:
        # comparing mismatching types like cmp(1, 2.0)
        return (None, "Cannot compare '" + repr(parameters[0]) + 
                    "' type with '" + repr(parameters[1]) + "' type.")

    else:
        return (type_obj("fn", builtins["fn"], 
                         sig = signature(params = parameters, 
                                         ret = builtins["int"])), None)

builtins["cmp"] = builtins_cmp


# filter(fn, iterable) -> iterable
def builtins_filter(parameters):
    if len(parameters) != 2:
        return (None, "'filter' expected exactly 2 arguments, but received " + 
                 str(len(parameters)) + " instead.")
 

    # first paramater must be a function
    if basetype(parameters[0]) is not builtins["FnType"]:
        return (None, "The first argument to 'filter' must have type 'fn'" + 
                 ", not type '" + parameters[0] + "'.")
 
    # second paramater must be a sequence
    if basetype(parameters[1]) not in sequencetypes:
        return (None, "The second argument to 'filter' must be a sequence" + 
                 ", not type '" + parameters[0] + "'.")
 
    
    iterable = parameters[1]
    fn = parameters[0]
    base = basetype(iterable)
 
    if base in containertypes:
        if len(fn.sig.param_types) != 1:
            return (None, "A filterable function must take exactly 1 " + 
                        "argument, not " + str(len(fn.sig.param_types)) + ".")
        
    if base is builtins["TupleType"] and len(iterable.elem_type) > 1:
        heterogeneous = [t != iterable.elem_type[0] for t in iterable.elem_type]
        if any(heterogeneous):
            return (None, "'" + repr(iterable) + "' contains more than one " + 
                    "element type.")
             
    if fn.sig.param_types[0] != iterable.elem_type[0]:
            return (None, "The type signature of the function '" + 
                    repr(fn.sig) + "' does not match the element type of the" +
                    " container '" + repr(iterable) + "'.")
 
    return (type_obj("fn", builtins["fn"], 
                         sig = signature(params = parameters, 
                                         ret = iterable)), None)

builtins["filter"] = builtins_filter


# map(fn, iterable) -> iterable
def builtins_map(parameters):
    if len(parameters) != 2:
         return (None, "'map' expected exactly 2 arguments, but received " + 
                str(len(parameters)) + " instead.")

    if basetype(parameters[1]) not in sequencetypes:
        return (None, "The second argument to 'filter' must be a sequence" + 
                ", not type '" + parameters[0] + "'.")
    
    iterable = parameters[1]

    if type(parameters[0]) == list:
        fn = None
        # find correct parameter type
        for function in parameters[0]:
            params = function.sig.param_types
            if len(params) == 1:
                if params[0] == iterable.elem_type[0]:
                    # found the overloaded function
                    fn = function
                    break
        if not fn:
            return (None, "The first argument of 'map' must have type 'fn'" + 
                    ", take one argument, and the argument type must match" +
                    " type " + iterable + ".")
    else:
        if parameters[0].type is not builtins["fn"]:
            return (None, "The first argument to 'map' must have type 'fn'" + 
                    ", not type '" + parameters[0] + "'.")
        fn = parameters[0]

    base = basetype(iterable)

    if base in containertypes:
        if len(fn.sig.param_types) != 1:
            return (None, "A mapable function must take exactly 1 " + 
                        "argument, not " + str(len(fn.sig.param_types)) + ".")

    if base is builtins["TupleType"] and len(iterable.elem_type) > 1:
        heterogeneous = [t != iterable.elem_type[0] for t in iterable.elem_type]
        if any(heterogeneous):
            return (None, "'" + repr(iterable) + "' contains more than one " + 
                    "element type.")

    if fn.sig.param_types[0] != iterable.elem_type[0]:
        return (None, "The type signature of the function '" + 
                    repr(fn.sig) + "' does not match the element type " +  
                    "of the container '" + repr(iterable) + "'.")

    newtype = fn.sig.return_type
    result = type_obj("list", builtins["list"],
                               elem_type = [newtype])
    return (type_obj("fn", builtins["fn"], 
                        sig = signature(params = parameters, 
                                        ret = result)), None)
builtins["map"] = builtins_map

# max(a:int, b:int) -> int
# max(a:float, b:float) -> float
# max(seq:list of elem_type) -> elem_type
# max(seq:tuple of (elem_type)) -> elem_type
# max(seq:set of elem_type) -> elem_type
# max(seq:frozenset of elem_type) -> elem_type
# max(seq:dict of [key_type|value_type]) -> key_type
# max(seq:string) -> string
def builtins_max(parameters):
    if len(parameters) not in (1,2):
        return (None, "'max' expected at most 2 arguments, but received " + 
                str(len(parameters)) + " instead.")

    elif len(parameters) == 1:
        seq = parameters[0]
        if basetype(seq) not in sequencetypes:
            return(None, "'max' is not defined for '" + repr(seq) + "' type.")

        if basetype(seq) is builtins["TupleType"]:
            heterogeneous = [t != seq.elem_type[0] for t in seq.elem_type]
            if any(heterogeneous):
                return (None,  "'" + repr(seq) + "' contains more than one " +
                    "type.")

        returntype = seq.elem_type[0]
        return (type_obj("fn", builtins["fn"], 
                            sig = signature(params = parameters, 
                                            ret = returntype)), None)

    else:
        numerictype = parameters[0] is builtins["int"] or \
                      parameters[0] is builtins["float"]

        if not numerictype:
             return(None, "'max' is not defined for '" + repr(parameters[0]) + 
                    "' and '" + repr(parameters[0]) + "' type.")

        elif parameters[0] == parameters[1]:
            return (type_obj("fn", builtins["fn"], 
                             sig = signature(params = parameters, 
                                             ret = parameters[0])), None)
        else:
            (None, "'max' is not defined for '" + repr(parameters[0]) + 
                    "' and '" + repr(parameters[0]) + "' type.")

builtins["max"] = builtins_max
                    

# min(a:int, b:int) -> int
# min(a:float, b:float) -> float
# min(seq:list of elem_type) -> elem_type
# min(seq:tuple of (elem_type)) -> elem_type
# min(seq:set of elem_type) -> elem_type
# min(seq:frozenset of elem_type) -> elem_type
# min(seq:dict of [key_type|value_type]) -> key_type
# min(seq:string) -> string
def builtins_min(parameters):
    if len(parameters) not in (1,2):
        return (None, "'min' expected at most 2 arguments, but received " + 
                str(len(parameters)) + " instead.")

    elif len(parameters) == 1:
        seq = parameters[0]
        if basetype(seq) not in sequencetypes:
            return(None, "'min' is not defined for '" + repr(seq) + "' type.")
        
        if basetype(seq) is builtins["TupleType"]:
            heterogeneous = [t != seq.elem_type[0] for t in seq.elem_type]
            if any(heterogeneous):
                return (None,  "'" + repr(seq) + "' contains more than one " +
                        "type.")
           
        returntype = seq.elem_type[0]
        return (type_obj("fn", builtins["fn"], 
                         sig = signature(params = parameters, 
                                         ret = returntype)), None)

    else:
        numerictype = parameters[0] is builtins["int"] or \
            parameters[0] is builtins["float"]
        if not numerictype:
            return(None, "'min' is not defined for '" + repr(parameters[0]) + 
                   "' and '" + repr(parameters[0]) + "' type.")

        elif parameters[0] == parameters[1]:
            return (type_obj("fn", builtins["fn"], 
                             sig = signature(params = parameters, 
                                             ret = parameters[0])), None)
        else:
            return (None, "'min' is not defined for '" + repr(parameters[0]) + 
                    "' and '" + repr(parameters[0]) + "' type.")

builtins["min"] = builtins_min
             

# repr(object) -> string
def builtins_repr(parameters):
    if len(parameters) != 1:
        return (None, "'repr' expected exactly 1 argument, but received " + 
                str(len(parameters)) + " instead.")
    else:
        rep = parameters[0].lookup_method("__repr__")
        if rep:
            rep = rep[0].sig
            return (type_obj("fn", builtins["fn"], 
                             sig = signature(params = parameters, 
                                             ret = rep.return_type)), None)
        else:
            return (None, "'" + repr(parameters[0]) + "' type does not " + 
                    "have a 'repr' method.")

builtins["repr"] = builtins_repr


# print(object1)
def builtins_print(parameters):
    if len(parameters) != 1:
        return (None, "'print' expected 1 argument, but received " +
                str(len(parameters)) + " instead.")

    rep = parameters[0].lookup_method("__str__")
    if rep:
        return (type_obj("proc", builtins["proc"],
                         sig = signature(params = parameters)), None)
    else:
        return (None, "'" + repr(parameters[0]) + "' type cannot be " +
                "converted to a string.")

builtins["print"] = builtins_print
                                                               
                                                           
#----------------------------BUILT IN FUNCTIONS--------------------------------#
   
# abs(x:int) -> int
# abs(x:float) -> float  
builtins["abs"] = [type_obj("fn", builtins["fn"], 
                            sig = signature(params = [builtins["int"]], 
                                            ret = builtins["int"])), 

                   type_obj("fn", builtins["fn"], 
                            sig = signature(params = [builtins["float"]], 
                                            ret = builtins["float"]))]


# all(l:list) -> bool
builtins["all"] = type_obj("fn", builtins["fn"], 
                           sig = signature(params = [builtins["list"]],
                                           ret = builtins["bool"]))
    

# any(l:list) -> bool
builtins["any"] = type_obj("fn", builtins["fn"], 
                           sig = signature(params = [builtins["list"]],
                                           ret = builtins["bool"]))   
 

# bin(x:int) -> string
builtins["bin"] = type_obj("fn", builtins["fn"], 
                           sig = signature(params = [builtins["int"]], 
                                           ret = builtins["string"]))


# chr(iu:int) -> string
builtins["chr"] = type_obj("fn", builtins["fn"], 
                           sig = signature(params = [builtins["int"]], 
                                           ret = builtins["string"]))


# divmod(a:int, b:int) -> tuple of (int * int)
# divmod(a:float, b:float) -> tuple of (float * float)
builtins["divmod"] = [type_obj("fn", builtins["fn"], 
                               sig = signature(params = [builtins["int"], 
                                                         builtins["int"]], 
                                              ret = init_tuple([builtins["int"],
                                                           builtins["int"]]))),
                      type_obj("fn", builtins["fn"], 
                               sig = signature(params = [builtins["float"], 
                                                         builtins["float"]], 
                                            ret = init_tuple([builtins["float"],
                                                        builtins["float"]])))]

# exit(code:int)
builtins["exit"] = type_obj("proc", builtins["proc"], 
                            sig = signature(defaults = [builtins["int"]]))

# hex(x:int) -> string
builtins["hex"] = type_obj("fn", builtins["fn"], 
                          sig = signature(params = [builtins["int"]], 
                                          ret = builtins["string"]))



# input(s:string) -> string 
builtins["input"] = type_obj("fn", builtins["fn"], 
                            sig = signature(params = [builtins["string"]], 
                                            ret = builtins["string"]))

# len(s:string) -> int
# len(l:list) -> int
# len(t:tuple) -> int
# len(d:dict) -> int
# len(mset:set) -> int
# len(fr:frozenset) -> int
builtins["len"] = [type_obj("fn", builtins["fn"], 
                           sig = signature(params = [builtins["string"]], 
                                           ret = builtins["int"])), 
                  type_obj("fn", builtins["fn"], 
                           sig = signature(params = [builtins["list"]], 
                                           ret = builtins["int"])), 
                  type_obj("fn", builtins["fn"], 
                           sig = signature(params = [builtins["tuple"]], 
                                           ret = builtins["int"])), 
                  type_obj("fn", builtins["fn"], 
                           sig = signature(params = [builtins["dict"]], 
                                           ret = builtins["int"])),
                  type_obj("fn", builtins["fn"], 
                           sig = signature(params = [builtins["set"]], 
                                           ret = builtins["int"])),
                  type_obj("fn", builtins["fn"], 
                           sig = signature(params = [builtins["frozenset"]], 
                                           ret = builtins["int"]))]
                 
# oct(x:int) -> string
builtins["oct"] = type_obj("fn", builtins["fn"], 
                          sig = signature(params = [builtins["int"]], 
                                          ret = builtins["string"]))

# ord(s:string) -> int
builtins["ord"] = type_obj("fn", builtins["fn"], 
                          sig = signature(params = [builtins["string"]], 
                                          ret = builtins["int"]))

# open(name:string, ?mode:string = "r") -> file
builtins["open"] = type_obj("fn", builtins["fn"], 
                            sig = signature(params = [builtins["string"]], 
                                            defaults = [builtins["string"]], 
                                            ret = builtins["file"]))

# pow(x:int, y:int) ->
# pow(x:int, y:int, z:int) -> int 
builtins["pow"] = type_obj("fn", builtins["fn"], 
                            sig = signature(params = [builtins["int"], 
                                                      builtins["int"]], 
                                            defaults = [builtins["int"]], 
                                            ret = builtins["int"]))


# range(x:int) -> list of int
# range(x:int, y:int, z:int = 1) - > list of int
builtins["range"] = type_obj("fn", builtins["fn"], 
                            sig = signature(params = [builtins["int"]], 
                                            defaults = [builtins["int"], 
                                                        builtins["int"]], 
                                            ret = init_list([builtins["int"]])))


# round(x:float, y:int) -> int
builtins["round"] = type_obj("fn", builtins["fn"], 
                             sig = signature(params = [builtins["float"]], 
                                             defaults = [builtins["int"]], 
                                             ret = builtins["int"]))

# sum(l:list of int, start:int = 0) -> int
# sum(l:list of float, start:float = 0.0) -> float
# sum(t:tuple of int, start:int = 0) -> int
# sum(t:tuple of float, start:float = 0.0) -> float
# sum(t:set of int, start:int = 0) -> int
# sum(t:set of float, start:float = 0.0) -> float
# sum(t:frozenset of int, start:int = 0) -> int
# sum(t:frozenset of float, start:float = 0.0) -> float
builtins["sum"] = [type_obj("fn", builtins["fn"], 
                          sig = signature(params = [type_obj("list", 
                                                    builtins["list"], 
                                                    elem_type =
                                                    [builtins["int"]])], 
                                          defaults = [builtins["int"]], 
                                          ret = builtins["int"])),

                    type_obj("fn", builtins["fn"], 
                          sig = signature(params = [type_obj("list", 
                                                    builtins["list"], 
                                                    elem_type =
                                                    [builtins["float"]])], 
                                          defaults = [builtins["float"]],
                                          ret = builtins["float"])),

                    type_obj("fn", builtins["fn"], 
                          sig = signature(params = [type_obj("tuple", 
                                                    builtins["tuple"], 
                                                    elem_type =
                                                    [builtins["int"]])], 
                                          defaults = [builtins["int"]],
                                          ret = builtins["int"])),

                    type_obj("fn", builtins["fn"], 
                          sig = signature(params = [type_obj("tuple", 
                                                    builtins["tuple"], 
                                                    elem_type =
                                                    [builtins["float"]])], 
                                          defaults = [builtins["float"]],
                                          ret = builtins["float"])),

                    type_obj("fn", builtins["fn"], 
                          sig = signature(params = [type_obj("set", 
                                                    builtins["set"], 
                                                    elem_type =
                                                    [builtins["int"]])], 
                                          defaults = [builtins["int"]],
                                          ret = builtins["int"])),

                    type_obj("fn", builtins["fn"], 
                          sig = signature(params = [type_obj("set", 
                                                    builtins["set"], 
                                                    elem_type =
                                                    [builtins["float"]])], 
                                          defaults = [builtins["float"]],
                                          ret = builtins["float"])),

                    type_obj("fn", builtins["fn"], 
                          sig = signature(params = [type_obj("frozenset", 
                                                    builtins["frozenset"], 
                                                    elem_type =
                                                    [builtins["int"]])], 
                                          defaults = [builtins["int"]],
                                          ret = builtins["int"])),

                    type_obj("fn", builtins["fn"], 
                          sig = signature(params = [type_obj("frozenset", 
                                                    builtins["frozenset"], 
                                                    elem_type =
                                                    [builtins["float"]])], 
                                          defaults = [builtins["float"]],
                                          ret = builtins["float"]))]

