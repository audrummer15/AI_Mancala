from copy import deepcopy

# Constants for referencing players
PLAYER = 0
OPPONENT = 1

PLAYER1 = 0
PLAYER2 = 1

ACTION = 0
VALUE = 1

# Global "Hash Table"
transTable = {}

#########################################
#										#
# AND-OR Search Algorithm Functionality #
#										#
#########################################

def andOrGraphSearch(gameBoard, ply, heurValue, player):
	if( not isValidBoard(gameBoard) ):
		return False

	# Problem is the board given
	# State is the current state of the board
	return orSearch(gameBoard, [], ply, heurValue, player)[ACTION]


def orSearch(board, path, moves, heurValue, player):
	plan = False

	print "***OR***"
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
	
	print "---AND---"
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

def goalTest(gameBoard):
	bPlayerEmpty = True
	bOpponentEmpty = True
	bGoalState = False

	if( not isValidBoard(gameBoard) ):
		return False

	for i in range( len( gameBoard[PLAYER] ) ):
		if( gameBoard[PLAYER][i] != 0 ):
			bPlayerEmpty = False

		if( gameBoard[OPPONENT][i] != 0 ):
			bOpponentEmpty = False

	if( bPlayerEmpty or bOpponentEmpty ):
		bGoalState = True

	return bGoalState


#########################################
#										#
# 	Transposition Table Functionality   #
#										#
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

def getMinimaxFromHashTable(gameBoard):
	if( not isValidBoard(gameBoard) ):
		return False

	hashIndex = boardToHashIndex(gameBoard)

	if( hashIndex in transTable ):
		returnValue = transTable[hashIndex]
	else:
		returnValue = False

	return returnValue

def storeMinimaxInHashTable(gameBoard, minimaxValue):
	global transTable

	if( not isValidBoard(gameBoard) ):
		return False

	if( getMinimaxFromHashTable(gameBoard) == False ):
		hashIndex = boardToHashIndex(gameBoard)
		transTable[hashIndex] = minimaxValue
		return True
	else:
		return False

#########################################
#										#
# 		Heuristic 2 Functionality       #
#										#
#########################################

def utilityH2(currentPlayer, gameBoard):
    playerPebbles = 0
    opponentPebbles = 0

    for i in range( len( gameBoard[currentPlayer] ) ):
        playerPebbles += gameBoard[currentPlayer][i]
        opponentPebbles += gameBoard[not(currentPlayer)][i]

    return playerPebbles - opponentPebbles

#########################################
#										#
# 		  Helper Functionality   		#
#										#
#########################################

def isValidBoard(gameBoard):
	if( len(gameBoard) != 2 ):
		return False
	else:
		return True


#########################################
#										#
#				Allison					#
#										#
#########################################
def result(state, action, player):
    numberOfColumns = len(state[0])
    tempState = [[state[x][y] for y in range(numberOfColumns)] for x in range(2)]
    makeMove(tempState, player, action)
    return tempState

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
    else:
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

def printGameBoard(gameBoardIn):
    rowString = "Player 1 (Computer):  "
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

def heuristicFunction1(currentPlayer, gameBoardIn):
    totalPlayerPebs = 0

    printGameBoard(gameBoardIn)

    for i in range(len(gameBoardIn[currentPlayer])):
        totalPlayerPebs += gameBoardIn[currentPlayer][i]
    return totalPlayerPebs