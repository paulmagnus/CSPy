#!/bin/bash

#------------------------------------------------------------------------------#
# run_python.sh                                                                #
#                                                                              #
# Usage: run_python.sh FILE DIRECTORY                                          #
# This script runs the python program FILE using python2.7 with the current    #
# directory being DIRECTORY.                                                   #
#                                                                              #
# Written by Paul Magnus '18, Ines Ayara '20, Matthew R. Jenkins '20           #
# Summer 2017                                                                  #
#------------------------------------------------------------------------------#

print_help ()
{
    printf "Usage: run_python.sh FILE DIRECTORY\n"
    printf "This script runs the python program FILE using python2.7 with the"
    printf " current\n"
    printf "directory being DIRECTORY.\n"
    printf "\n"
    printf "Written by Paul Magnus '18, Ines Ayara '20, Matthew R. Jenkins"
    printf " '20\n"
    printf "Summer 2017\n"
}

# parse arguments
while :; do
    case $1 in
        -h|--help)
            print_help
            exit;;
        *)
            break
    esac
done

if [ $# != 2 ]; then
    printf "run_python takes two arguments, the python file to run and the" >&2
    printf "directory to run it in\n" >&2
    exit 1
fi

DIR=$PWD
FILE=$1
directory=$2

# silently push the current directory on to the stack
pushd $directory > /dev/null

if [[ "$FILE" = /* ]]; then
    # Absolute path
    python2.7 $FILE
else
    # Relative path
    python2.7 "$DIR/$FILE"
fi

# silently return to the previous directory
popd > /dev/null