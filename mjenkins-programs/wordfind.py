"""
FILE: wordfind.py

AUTHOR: Matthew R. Jenkins

PARTNER: N/A

ASSIGNMENT: Project 0

DATE: September 28th, 2016

DESCRIPTION: The aim of this project is to generate the number of times words
appear in a grid of characters, and to capitalize them once they have been
found.

"""

# CITE: Eric Collins
# DESCRIPTION: Helped debug the code in general.


def printGrid(grid):
    """ Display the grid in a nice way """
    rows = len(grid)
    for row in range(rows):
        print(grid[row])


def inBounds(grid, direction, start, word):
    "Testing whether the word is in the bounds of the grid"

    # Trying to test bounds.

    # CITE: Mitchel Herman
    # DESCRIPTION: Helped me with the bounds issues.
    endPointX = start[0] + (len(word)) * direction[0]
    endPointY = start[1] + (len(word)) * direction[1]
    if endPointX > len(grid):
        return False
    if endPointX < 0:
        return False
    if endPointY > len(grid[0]):
        return False
    if endPointY < 0:
        return False
    return True


def getString(grid, direction, start, word):
    """when given a grid, a direction represented as a tuple, a starting
    point represented as a tuple, and a word from words, return a string
    generated from a certain point in a certain direction."""

    # CITE: Ryan Woo
    # DESCRIPTION: Gave me the idea for this function.

    string = ''

    if inBounds(grid, direction, start, word):
        for i in range(len(word)):
            string = string + str(grid[start[0] + (direction[0] * i)]
                                  [start[1] + (direction[1] * i)])
    return string

    # Concactenating a string from a certain starting point and direction


def wordfind(grid, words):
    """ For each word in words, if possible,
    find it once in the grid, case insensitive.
    Convert those found letters in the grid to upper-case."""
    foundWord = ''
    count = 0
    # The first two increment the starting point
    for word in words:
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                # The next two increment the direction from -1 to 1
                for rowDir in range(3):
                    for colDir in range(3):
                        # Running getString
                        foundWord = getString(grid, (rowDir - 1, colDir - 1),
                                              (x, y), word)
                        # If getString yields a word which matches
                        # words[x], count gets incremented
                        if foundWord.lower() == word.lower():
                            # I am aware of +=, it doesn't work in Sublime Text
                            count = count + 1
                            capitalize(grid, (rowDir - 1, colDir - 1),
                                       (x, y), word)
    return count


def capitalize(grid, direction, start, word):
    """when given a grid, a direction represented as a tuple, a starting
    point represented as a tuple, and a word from words, modifies the grid
    so that the string in the grid is capitalized."""

    for i in range(len(word)):
        (grid[start[0] + (direction[0] * i)]
         [start[1] + (direction[1] * i)]) = \
        (grid[start[0] + (direction[0] * i)]
         [start[1] + (direction[1] * i)]).upper()
    return grid

def sandbox():
    """Sandbox for testing.  Modify this in any
    way you wish. It will not be graded."""
    myGrid = [['j', 'm', 'w', 'e'],
              ['e', 'e', 'p', 'p'],
              ['q', 'o', 'x', 'u'],
              ['w', 'w', 'e', 'd'],
              ['w', 'g', 'j', 'o']]
    words = ['meow', 'wed', 'do', 'justice']
    count = wordfind(myGrid, words)
    printGrid(myGrid)
    print(count)


sandbox()
