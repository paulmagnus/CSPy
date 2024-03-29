#------------------------------------------------------------------------------#
# split.py                                                                     #
# This file contains two functions for working with strings and lists of       #
# strings.                                                                     #
#                                                                              #
# Written by Paul Mangus '18, Ines Ayara '20, Matthew R. Jenkins '20           #
# Summer 2017                                                                  #
#------------------------------------------------------------------------------#

# PYTHON MODULES
import string

#------------------------------------------------------------------------------#
# split_string(s:string, charList:list of string) -> list of string            #
#   Returns a list of substrings of s. These strings are either elements of    #
#   charList or the strings in between the elements of charList.               #
#                                                                              #
# eg: split_string("hi:x", [":"])                                              #
#     ["hi", ":", "x"]                                                         #
#------------------------------------------------------------------------------#
def split_string(s, charList):
    for char in charList:
        loc = string.find(s, char)
        if loc != -1:
            # found the character
            str_list = [split_string(s[:loc], charList),
                        s[loc:loc+len(char)],
                        split_string(s[loc+len(char):], charList)]
            return flatten_list(str_list)
    return [s]

#------------------------------------------------------------------------------#
# flatten_list(lst:list of strings and lists of strings) -> list of string     #
#   Returns a list containing all of the strings in the list and sublists.     #
#   This only works one layer deep.                                            #
#                                                                              #
# eg: flatten_list(["hi", ["x", ":", "=", "48"], "3"])                         #
#     ["hi", "x", ":", "=", "48", "3"]                                         #
#------------------------------------------------------------------------------#
def flatten_list(lst):
    ret_list = []
    for sublist in lst:
        if type(sublist) == list:
            for item in sublist:
                if len(item) != 0:
                    ret_list.append(item)
        else:
            if len(sublist) != 0:
                ret_list.append(sublist)
    return ret_list