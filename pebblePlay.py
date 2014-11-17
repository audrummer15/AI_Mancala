'''
Created on Nov 16, 2014

@author: allisonholt
'''
#!/usr/bin/python

import sys

if (len(sys.argv) == 1):
    print 'Please use parameters'
#parameter order:
# 1) number of columns (MAX IS 10)
# 2) pebbles per square
# 3) look ahead ply
else:
    numCols = int(sys.argv[1])
    #print numCols #how does this make since...
    if (numCols < 2):
        print 'There must be at least two columns'
        print 'Updated the number of columns to 2'
        numCols = 2
    elif (numCols > 10):
        print 'The max number of columns is 10'
        print 'Updated the number of columns to 10'
        numCols = 10
    
    pebsPerSq = int(sys.argv[2])
    ply = int(sys.argv[3])
    
    print ""
    
    #print 'Computer (A):  '
    counter = 0
    rowString = "Player A (Computer):  "
    while (counter < numCols):
        rowString += "["
        rowString += str(pebsPerSq)
        rowString += "]"
        counter += 1
    print rowString
    
    #print 'Player B:      '
    counter = 0
    rowString = "Player B:             "
    while (counter < numCols):
        rowString += "["
        rowString += str(pebsPerSq)
        rowString += "]"
        counter += 1
    print rowString