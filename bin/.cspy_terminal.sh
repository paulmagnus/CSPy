#!/bin/bash

#------------------------------------------------------------------------------#
# cspy_terminal.sh                                                             #
#                                                                              #
# This shell script runs CSPy code as a new thread in a new terminal window.   #
#                                                                              #
# Written by Paul Magnus '18, Ines Ayara '20, Matthew R. Jenkins '20           #
# Summer 2017                                                                  #
#------------------------------------------------------------------------------#

# Get directory of script, resolving links
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
    DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

# run the CSPy code in a new terminal window
xterm -e "$DIR/.cspy" "$@" &