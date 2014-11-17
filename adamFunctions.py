# Constants for referencing players
PLAYER1 = 0
PLAYER2 = 1

# Global "Hash Table"
transTable = {}

#########################################
#										#
# AND-OR Search Algorithm Functionality #
#										#
#########################################

def andOrGraphSearch(gameBoard):
	if( not isValidBoard(gameBoard) ):
		return False


def orSearch(state, problem, path):
	return False

def andSearch(states, problem, path):
	return True

def goalTest(gameBoard):
	bPlayer1Empty = True
	bPlayer2Empty = True
	bGoalState = False

	if( not isValidBoard(gameBoard) ):
		return False

	for i in range( len( gameBoard[PLAYER1] ) ):
		if( gameBoard[PLAYER1][i] != 0 ):
			bPlayer1Empty = False

		if( gameBoard[PLAYER2][i] != 0 ):
			bPlayer2Empty = False

	if( bPlayer1Empty or bPlayer2Empty ):
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

	for i in range( len( gameBoard[PLAYER1] ) ):
		hashIndex1 += str(gameBoard[PLAYER1][i])
		hashIndex2 += str(gameBoard[PLAYER2][i])

	return hashIndex1 + hashIndex2

def getMinimaxFromHashTable(hashIndex):
	if( hashIndex in transTable ):
		returnValue = transTable[hashIndex]
	else:
		returnValue = False

	return returnValue

def storeMinimaxInHashTable(hashIndex, minimaxValue):
	global transTable

	if( getMinimaxFromTransTable(hashIndex) == False ):
		transTable[hashIndex] = minimaxValue
		return True
	else:
		return False

def isValidBoard(gameBoard):
	if( len(gameBoard) != 2 ):
		return False
	else:
		return True