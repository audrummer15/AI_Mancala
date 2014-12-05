'''
Created on Nov 16, 2014

@author: allisonholt
'''
#!/usr/bin/python
from __builtin__ import True
from macerrors import nilHandleErr
from findertools import move
from copy import deepcopy

# Constants for referencing players
PLAYER1 = 0  #player A
PLAYER2 = 1  #player B

PLAYER = 0   #For redundancy used in the AND-OR
OPPONENT = 1 #For redundancy used in the AND-OR

# For referencing pieces of and-or return tuples
ACTION = 0
VALUE = 1

#global variables
'''
This global variable is used to store the number plys
The way we have our algorithm set up, the depth starts
at zero and the searching continues until the depth
gets to the specified ply.
'''
depthForCutOffTest = 0

'''
Function:  heuristicFunction1
Purpose:  Calculates the current player's heuristic value.  In this case,
          the heuristic value is based off the current player's total
          number of pebbles.
Parameters:
    currentPlayer:  Used to determine which player's heuristic value to calculate
    gameBoardIn:  This is the current gameBoard and is used to determine the current
                  player's number of pebbles.
Returns:  The current player's number of pebbles
'''
def heuristicFunction1(currentPlayer, gameBoardIn):
    totalPlayerPebs = 0
    for i in range(len(gameBoardIn[currentPlayer])):
        totalPlayerPebs += gameBoardIn[currentPlayer][i]
    return totalPlayerPebs

#Adam's function
def utilityH2(currentPlayer, gameBoard):
    playerPebbles = 0
    opponentPebbles = 0

    for i in range( len( gameBoard[currentPlayer] ) ):
        playerPebbles += gameBoard[currentPlayer][i]
        opponentPebbles += gameBoard[not(currentPlayer)][i]

    return playerPebbles - opponentPebbles

#########################################
#                                        #
#     Transposition Table Functionality   #
#                                        #
#########################################

def boardToHashIndex(gameBoard):
    if( not isValidBoard(gameBoard) ):
        return False

    hashIndex1 = ""
    hashIndex2 = ""

    for i in range( len( gameBoard[PLAYER] ) ):
        hashIndex1 += str(gameBoard[PLAYER][i])
        hashIndex2 += str(gameBoard[OPPONENT][i])

    return hashIndex1 + hashIndex2

def getMinimaxFromHashTable(gameBoard, transTable):
    hashIndex = boardToHashIndex(gameBoard)

    if( hashIndex in transTable ):
        returnValue = transTable[hashIndex]
    else:
        returnValue = False

    return returnValue

def storeMinimaxInHashTable(gameBoard, minimaxValue, transTable):
    if( getMinimaxFromHashTable(gameBoard) == False ):
        hashIndex = boardToHashIndex(gameBoard)
        transTable[hashIndex] = minimaxValue
        return True
    else:
        return False
    
'''
Function:  result
Purpose:  Copies the current game board and starts testing moves the current player
          can make.
Parameters:
    state:  This is the current gameBoard and is used to determine the current
                  player's number of pebbles.
    action:  This is the column number the current player is moving his or her
            pebbles from
    currentPlayer:  Used to determine which player's heuristic value to calculate
Returns:  The hypothetical game board for testing a move the player is thinking
          about making
'''
def result(state, action, currentPlayer):
    numberOfColumns = len(state[0])
    tempState = [[state[x][y] for y in range(numberOfColumns)] for x in range(2)]
    makeMove(tempState, currentPlayer, action)
    return tempState

'''
Function:  cutoffTest
Purpose:  Tests to see if the search has reached the end of the ply or if the
          state currently being searched is a goal state.
Parameters:
    state:  This is the current gameBoard and is used to if the state has reached
             a goal state.
    depth:  The current depth of the search tree
Returns:  If the current state is at the specified ply or a goal state
'''
def cutOffTest(state, depth):
    if (depth == depthForCutOffTest):
        return True
    elif (goalTest(state)):
        return True
    else:
        return False

'''
Function:  maxValue
Purpose:  Used to determine which move the current player can make to maximize
          his or her heuristic value
Parameters:
    state:  This is the current gameBoard and is used to determine the current
                  player's number of pebbles.
    alpha:  The minimum utility value in the search
    beta:   The maximum utility value in the search
    depth:  The current depth of the search tree
    pathStates:  The list of states the search has already come across.  Used to
                 prevent looping.
    currentPlayer:  Used to determine which player's heuristic value to calculate
                    while searching
    heurValue:  Used to determine which heuristic function to use
    playerToMakeMove:  Used to determine which player is making the moves and 
                       affecting the game board during this part of the search
    transTable:  The transpositionTable used to store the hash values of a game
                 state and its heuristic value
Returns:  The maximum heuristic value for that level and branch of the search tree
'''
def maxValue(state, alpha, beta, depth, pathStates, currentPlayer, heurValue, playerToMakeMove, transTable):
    if (state in pathStates):
        return float('-inf')
    if (cutOffTest(state, depth) == True):
        #check which utility is used
        if(heurValue == 1):
            return heuristicFunction1(currentPlayer, state)
        else:
            return utilityH2(currentPlayer, state)
    pathStates.append(state)
    v = float('-inf')
    for move in range(len(state[0])):
        if(state[playerToMakeMove][move] > 0):
            statePrime = result(state, move, playerToMakeMove)
            if (getMinimaxFromHashTable(state, transTable) != False): #statePrime in transTable
                vPrime = getMinimaxFromHashTable(state, transTable)
                #return
            else:
                vPrime = minValue(statePrime, alpha, beta, (depth + 1), pathStates, currentPlayer, heurValue, not(playerToMakeMove), transTable)
                storeMinimaxInHashTable(state, vPrime, transTable)
            if (vPrime > v):
                v = vPrime
            if (v >= beta):
                return v
            elif (v > alpha):
                alpha = v
    return v
            
'''
Function:  minValue
Purpose:  Used to determine which move the current player's opponent can make 
          to minimize the current player's heuristic value
Parameters:
    state:  This is the current gameBoard and is used to determine the current
                  player's number of pebbles.
    alpha:  The minimum utility value in the search
    beta:   The maximum utility value in the search
    depth:  The current depth of the search tree
    pathStates:  The list of states the search has already come across.  Used to
                 prevent looping.
    currentPlayer:  Used to determine which player's heuristic value to calculate
                    while searching
    heurValue:  Used to determine which heuristic function to use
    playerToMakeMove:  Used to determine which player is making the moves and 
                       affecting the game board during this part of the search
    transTable:  The transpositionTable used to store the hash values of a game
                 state and its heuristic value
Returns:  The minimum heuristic value for that level and branch of the search tree
''' 
def minValue(state, alpha, beta, depth, pathStates, currentPlayer, heurValue, playerToMakeMove, transTable):
    if (state in pathStates):
        return float('inf')
    if (cutOffTest(state, depth) == True):
        #check which utility is used
        if(heurValue == 1):
            return heuristicFunction1(currentPlayer, state)
        else:
            return utilityH2(currentPlayer, state)
    pathStates.append(state)
    v = float('inf')
    for move in range(len(state[0])):
        if(state[playerToMakeMove][move] > 0):
            statePrime = result(state, move, playerToMakeMove)
            if (getMinimaxFromHashTable(state, transTable) != False): #statePrime in transTable
                vPrime = getMinimaxFromHashTable(state, transTable)
                #return 
            else:
                vPrime = maxValue(statePrime, alpha, beta, (depth + 1), pathStates, currentPlayer, heurValue, not(playerToMakeMove), transTable)
                storeMinimaxInHashTable(state, vPrime, transTable)
            if (vPrime < v):
                v = vPrime
            if (v <= alpha):
                return v
            elif (v > beta):
                beta = v
    return v

'''
Function:  alphaBetaSearch
Purpose:  Used to determine which move the current player can make to maximize
          his or her heuristic value.  Uses the functions minValue and maxValue
          in the process
Parameters:
    state:  This is the current gameBoard and is used to determine the current
                  player's number of pebbles.
    depth:  The current depth of the search tree
    currentPlayer:  Used to determine which player's heuristic value to calculate
                    while searching
    heurValue:  Used to determine which heuristic function to use
    transTable:  The transpositionTable used to store the hash values of a game
                 state and its heuristic value
Returns:  The column number from which the current player should move to maximize
          his or her utility
'''  
def alphaBetaSearch(state, depth, currentPlayer, heurValue, transTable): #state is game board and depth is the ply
    playerToMakeMove = currentPlayer
    v = float('-inf')
    a = None
    alpha = float('-inf')
    beta = float('inf')
    pathStates = []
    for move in range(len(state[0])): #each column is a move
        #if state is goal state
        if(state[currentPlayer][move] > 0):
            statePrime = result(state, move, currentPlayer)  #need to make fake gameboard?
            vPrime = maxValue(statePrime, alpha, beta, depth, pathStates, currentPlayer, heurValue, playerToMakeMove, transTable) #had as min in algorithm, but shouldn't it be max?
            if (vPrime > v):
                v = vPrime
                a = move
            if (v >= beta):
                return a
            elif (v > alpha):
                alpha = v
    return a

'''
Function:  makeMove
Purpose:  Allows players to move their pebbles on the game board.  The variable
          colToMoveFromIn is the slot where the pebbles are removed and then
          distributed in a clockwise manner.
Parameters:
    gameBoardIn:  This is the current state of the game board
    currentPlayersMove:  Used to determine which row to move the pebble from
    colToMoveFromIn:  Used to determine which column to remove the pebbles from
Returns:  Nothing
'''
def makeMove(gameBoardIn, currentPlayersMove, colToMoveFromIn):
    if (currentPlayersMove == PLAYER1):
        pebsToMove = gameBoardIn[currentPlayersMove][colToMoveFromIn]
        gameBoardIn[currentPlayersMove][colToMoveFromIn] = 0
        maxColIndex = len(gameBoardIn[currentPlayersMove]) - 1
        if(colToMoveFromIn == maxColIndex):
            currentRow = PLAYER2
            currentColumn = maxColIndex
        else:
            currentRow = currentPlayersMove
            currentColumn = (colToMoveFromIn + 1)
        while (pebsToMove > 0):
            gameBoardIn[currentRow][currentColumn] += 1
            pebsToMove -= 1
            if((currentColumn == 0) and (currentRow == PLAYER2)):
                currentRow = PLAYER1
            elif((currentColumn == maxColIndex) and (currentRow == PLAYER1)):
                currentRow = PLAYER2
            elif (currentRow == PLAYER2):
                currentColumn -= 1
            elif (currentRow == PLAYER1):
                currentColumn += 1
    else: #player 2
        pebsToMove = gameBoardIn[currentPlayersMove][colToMoveFromIn]
        gameBoardIn[currentPlayersMove][colToMoveFromIn] = 0
        maxColIndex = len(gameBoardIn[currentPlayersMove]) - 1
        if(colToMoveFromIn == 0):
            currentRow = PLAYER1
            currentColumn = 0
        else:
            currentRow = currentPlayersMove
            currentColumn = (colToMoveFromIn - 1)
        while (pebsToMove > 0):
            gameBoardIn[currentRow][currentColumn] += 1
            pebsToMove -= 1
            if((currentColumn == 0) and (currentRow == PLAYER2)):
                currentRow = PLAYER1
            elif((currentColumn == maxColIndex) and (currentRow == PLAYER1)):
                currentRow = PLAYER2
            elif (currentRow == PLAYER2):
                currentColumn -= 1
            elif (currentRow == PLAYER1):
                currentColumn += 1
    return
        

def goalTest(gameBoard):
    bPlayer1Empty = True
    bPlayer2Empty = True
    bGoalState = False

    for i in range( len( gameBoard[PLAYER1] ) ):
        if( gameBoard[PLAYER1][i] != 0 ):
            bPlayer1Empty = False

        if( gameBoard[PLAYER2][i] != 0 ):
            bPlayer2Empty = False

    if( bPlayer1Empty or bPlayer2Empty ):
        bGoalState = True

    return bGoalState

'''
Function:  printGameBoard
Purpose:  Prints the current state of the game board
Parameters:
    gameBoardIn:  The game board at its current state
Returns:  Nothing
'''
def printGameBoard(gameBoardIn):
    rowString = "Player 1:             "
    for i in range(len(gameBoardIn[0])):
        rowString += "["
        rowString += str(gameBoardIn[0][i])
        rowString += "]"
    print rowString
    
    rowString = "Player 2:             "
    for i in range(len(gameBoardIn[1])):
        rowString += "["
        rowString += str(gameBoardIn[1][i])
        rowString += "]"
    print rowString
    return

'''
Function:  main
Purpose:  Used interact with user and set up the Pebble Play game.  We
          are assuming that Player 1 is always the computer and always 
          gets to make the first move.
Parameters:  None
Returns:  None
'''
def main():
    
    '''
    Collect User Input at Beginning of Program Execution
    '''
    #Get the number of columns per player
    numCols = int(input("Please enter the number of columns per player:  "))
    if (numCols < 2):
        print "There must be at least two columns"
        print "Updated the number of columns to 2"
        numCols = 2
    elif (numCols > 10):
        print "The max number of columns is 10"
        print "Updated the number of columns to 10"
        numCols = 10
    
    #Get the number of pebbles per column
    pebsPerSq = int(input("Please enter the number of pebbles per square:  "))
    ply = int(input("Please enter the number of plys:  "))
    depthForCutOffTest = ply
    print ""
    
    #Determine if the user if running or stepping through the game
    notProperInput = True
    while(notProperInput):
        runOrStep = int(input("How are you viewing the game?  0-run through or 1-step through:  "))
        if ((runOrStep == 0) or (runOrStep == 1)):
            notProperInput = False
    print "" 
      
    #If the user is stepping through, are they playing the game or watching the computer play itself
    if(runOrStep == 1):
        notProperInput = True
        while(notProperInput):
            userPlaying = int(input("Is the computer playing itself (enter 0) or are you playing against the computer (enter 1)?:  "))
            if ((userPlaying == 0) or (userPlaying == 1)):
                notProperInput = False
                
    if(runOrStep == 0):  #means computer must be playing itself
        userPlaying = 0
    print ""
    
    #If the user is playing against the computer
    if(userPlaying):
        #Get the heuristic for the computer to use
        notProperInput = True
        print "Heuristics"
        print "1) Number of Pebbles of Player"
        print "2) Difference Between Your Pebbles and Opponent's Pebbles"
        while(notProperInput):
            hValue = int(input("Which heuristic do you want computer to use?  1 or 2:  "))
            if((hValue == 1) or (hValue == 2)):
                notProperInput = False
        print""
        
        #Get the algorithm for the computer to use
        notProperInput = True
        print "Planning Algorithms"
        print "1) And-Or Search"
        print "2) Alpha-Beta Minimax"
        while(notProperInput):
            algValue = int(input("Which algorithm do you want computer to use?  1 or 2:  "))
            if((algValue == 1) or (algValue == 2)):
                notProperInput = False
        print ""
    #Else the user is watching the computer play itself   
    else:
        #Get Player 1's heuristic
        notProperInput = True
        print "Heuristics"
        print "1) Number of Pebbles of Player"
        print "2) Difference Between Your Pebbles and Opponent's Pebbles"
        while(notProperInput):
            hValuePlayer1 = int(input("Which heuristic do you want to use for player 1?  1 or 2:  "))
            if((hValuePlayer1 == 1) or (hValuePlayer1 == 2)):
                notProperInput = False
        print ""        
        
        #Get Player 2's heuristic
        notProperInput = True
        print "Heuristics"
        print "1) Number of Pebbles of Player"
        print "2) Difference Between Your Pebbles and Opponent's Pebbles"
        while(notProperInput):
            hValuePlayer2 = int(input("Which heuristic do you want to use for player 2?  1 or 2:  "))
            if((hValuePlayer2 == 1) or (hValuePlayer2 == 2)):
                notProperInput = False
        print ""
        
        #Get Player 1's algorithm        
        notProperInput = True
        print "Planning Algorithms"
        print "1) And-Or Search"
        print "2) Alpha-Beta Minimax"
        while(notProperInput):
            algValuePlayer1 = int(input("Which algorithm do you want to use for player 1?  1 or 2:  "))
            if((algValuePlayer1 == 1) or (algValuePlayer1 == 2)):
                notProperInput = False
        print ""
        
        #Get Player 2's algorithm
        notProperInput = True
        print "Planning Algorithms"
        print "1) And-Or Search"
        print "2) Alpha-Beta Minimax"
        while(notProperInput):
            algValuePlayer2 = int(input("Which algorithm do you want to use for player 2?  1 or 2:  "))
            if((algValuePlayer2 == 1) or (algValuePlayer2 == 2)):
                notProperInput = False
        print ""

    '''
    Set Up Game Board
    '''
    gameBoard = [[pebsPerSq for y in range(numCols)] for x in range(2)]
    
    #As stated before, we are allowing Player 1 to always make the first move
    currentMove = PLAYER1
    #If the user is playing, it alternates between the computer making moves
    #and the user specifying which column they want to move
    if(userPlaying):
        print "Note:  You are Player 2"
        print ""
        while(not(goalTest(gameBoard))):
            '''
            Use Function to Print Game Board
            '''
            printGameBoard(gameBoard)
            print ""
            
            if(currentMove == PLAYER1):
                raw_input("Press enter to continue and see Player 1's next move.  ")
                
                print ""
                print "Player 1's move"
                print ""
                    
                if(algValue == 1):
                    colToMoveFrom = andOrGraphSearch(gameBoard, depthForCutOffTest, hValue, PLAYER1)
                    makeMove(gameBoard, PLAYER1, colToMoveFrom)
                    print "Algorithm returned: ", colToMoveFrom, "\n"
                else:
                    # Not Global "Hash Table"
                    transTable = {}
                    colToMoveFrom = alphaBetaSearch(gameBoard, 0, PLAYER1, hValue, transTable)
                    makeMove(gameBoard, PLAYER1, colToMoveFrom)
                    print ""
            
                currentMove = PLAYER2
                
            else:  
                print ""
                print "Your move"
                print ""
                
                notValidInput = True
                while (notValidInput):
                    colToMoveFrom = int(input("Which of your squares do you empty?  The numbering starts from the left with value 0:  "))
                    if((colToMoveFrom < 0) or (colToMoveFrom >= numCols)):
                        print "The column number is invalid.  Remember the numbering starts at 0."
                    elif(gameBoard[PLAYER2][colToMoveFrom] == 0):
                        print "This is an invalid move since you have no pebbles there."
                    else:
                        notValidInput = False
                
                makeMove(gameBoard, PLAYER2, colToMoveFrom)
                print ""
                
                currentMove = PLAYER1
        print ""
        print "--END OF GAME RESULTS--"
        print "Final Game Board:"
            
        printGameBoard(gameBoard)
            
        print ""
        if(heuristicFunction1(PLAYER2, gameBoard) != 0):
            print "Congratulations you won!"
        else:
            print "Sorry you lost. Better luck next time."
    
    #If the user is watching the computer play itself, the user only interacts with
    #the program if they are stepping through.  When stepping through, the user has
    #the ability to change to the run through mode.    
    else:
        printGameBoard(gameBoard)
        while(not(goalTest(gameBoard))):
            
            if(currentMove == PLAYER1):
                print ""
                print "Player 1's move"
                print ""
                    
                if(algValuePlayer1 == 1):
                    colToMoveFrom = andOrGraphSearch(gameBoard, depthForCutOffTest, hValuePlayer1, PLAYER1)
                    makeMove(gameBoard, PLAYER1, colToMoveFrom)
                    print "Algorithm returned: ", colToMoveFrom, "\n"
                else:
                    # Not Global "Hash Table"
                    transTable = {}
                    colToMoveFrom = alphaBetaSearch(gameBoard, 0, PLAYER1, hValuePlayer1, transTable)
                    makeMove(gameBoard, PLAYER1, colToMoveFrom)
                    debugString = "Algorithm returned:  "
                    debugString += str(colToMoveFrom)
                    print debugString
                    print ""
            
                currentMove = PLAYER2
                
                printGameBoard(gameBoard)
                
                if(runOrStep == 1 and not(goalTest(gameBoard))):
                    notProperInput = True
                    while(notProperInput):
                        runOrStep = int(input("Would you like to run though the rest of the game or continue stepping through?  0-run through or 1-step through:  "))
                        if ((runOrStep == 0) or (runOrStep == 1)):
                            notProperInput = False
                        
            else:
                print ""
                print "Player 2's move"
                print ""
                    
                if(algValuePlayer2 == 1):
                    colToMoveFrom = andOrGraphSearch(gameBoard, depthForCutOffTest, hValuePlayer2, PLAYER2)
                    makeMove(gameBoard, PLAYER2, colToMoveFrom)
                    print "Algorithm returned: ", colToMoveFrom, "\n"
                else:      
                    # Not Global "Hash Table"
                    transTable = {}
                    colToMoveFrom = alphaBetaSearch(gameBoard, 0, PLAYER2, hValuePlayer2, transTable)
                    makeMove(gameBoard, PLAYER2, colToMoveFrom)
                    debugString = "Algorithm returned:  "
                    debugString += str(colToMoveFrom)
                    print debugString
                    print ""
            
                currentMove = PLAYER1
                
                printGameBoard(gameBoard)
                
                if(runOrStep == 1 and not(goalTest(gameBoard))):
                    notProperInput = True
                    while(notProperInput):
                        runOrStep = int(input("Would you like to run though the rest of the game or continue stepping through?  0-run through or 1-step through:  "))
                        if ((runOrStep == 0) or (runOrStep == 1)):
                            notProperInput = False
        print ""
        print "Final Game Board:"
            
        printGameBoard(gameBoard)
            
        print ""
        if(heuristicFunction1(PLAYER2, gameBoard) != 0):
            print "Player 2 won!"
        else:
            print "Player 1 won!"
    
    return

#########################################
#                                       #
# AND-OR Search Algorithm Functionality #
#                                       #
#########################################

def andOrGraphSearch(gameBoard, ply, heurValue, player):
    if( not isValidBoard(gameBoard) ):
        return False

    # Problem is the board given
    # State is the current state of the board
    return orSearch(gameBoard, [], ply, heurValue, player)[ACTION]


def orSearch(board, path, moves, heurValue, player):
    plan = False

    if goalTest(board): 
        return [-1, float('inf')]

    if moves <= 0:
        if(heurValue == 1):
            return [float('-inf'), heuristicFunction1(player, board)]
        else:
            return [float('-inf'), utilityH2(player, board)]

    value = float('-inf')
    
    if boardToHashIndex(board) in path:
        return False

    for action in range( len( board[player] ) ):
        if board[player][action] != 0: #if the move is valid
            if moves > 1:
                newPath = deepcopy(path)
                newPath.insert(0, boardToHashIndex(board))
                newValue = andSearch( results(board, action, player), newPath, moves - 1, heurValue, player)
            else:
                if(heurValue == 1):
                    newValue = heuristicFunction1(player, result(board, action, player))
                else:
                    newValue = utilityH2(player, result(board, action, player))

            if newValue != False:
                if newValue > value:
                    value = newValue
                    plan = [action, newValue]

            if plan == False:
                plan = [action, value]

    return plan

def andSearch(states, path, moves, heurValue, player):
    if not states:
        return float('-inf')

    returnValue = 0

    for state in states:
        if moves <= 0:
            if(heurValue == 1):
                returnValue = returnValue + heuristicFunction1(player, state)
            else:
                returnValue = returnValue + utilityH2(player, state)
        else:
            newPlan = orSearch( state, path, moves - 1, heurValue, PLAYER )
            
            if newPlan == False:
                return False

            returnValue = returnValue + newPlan[VALUE]

    #return average of board heuristics
    if( len(states) != 0):
        return (returnValue / len(states))
    else:
        return returnValue


#results returns a list of states that are potentially presented after player makes a move
# and the opponent responds
def results(state, action, player):
    resultStates = []
    numberOfColumns = len(state[0])
    newState = [[state[x][y] for y in range(numberOfColumns)] for x in range(2)]

    newState = result(newState, action, player)

    if goalTest(newState):
        print "AO-RESULTS RETURN EMPTY"
        return resultStates

    opponent = 1 - player

    for action in range( numberOfColumns ):
        tempState = deepcopy(newState)
        if tempState[opponent][action] != 0:
            makeMove(tempState, opponent, action)
            resultStates.append(tempState)

    return resultStates

#########################################
#                                       #
#         Helper Functionality          #
#                                       #
#########################################

def isValidBoard(gameBoard):
    if( len(gameBoard) != 2 ):
        return False
    else:
        return True

if __name__ == '__main__':
    main()
    