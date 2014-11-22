# Constants for referencing players
PLAYER = 0
OPPONENT = 1

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

	# Problem is the board given
	# State is the current state of the board
	return orSearch(problem.Initial-State, problem, [])


def orSearch(state, problem, path):
	if problem.goalTest(state) then return the empty plan
	if state is on path then return failure

	for each action in problem.Actions(state) do 
		plan <- and-search(Results(state, action), problem, [state | path])
		if plan != failure then return [action | plan]

	return False

def andSearch(states, problem, path):
	for each Si in states do
		plani <- or-search(Si, problem, path)
		if plani = failure then return failure

	return [if s1 then plan1 else if s2 then plan2 else ... if s(n-1) then plan(n-1) else plann]

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

def utilityH2(gameBoard):
	if( not isValidBoard(gameBoard) ):
		return False

	playerPebbles = 0
	opponentPebbles = 0

	for i in range( len( gameBoard[PLAYER] ) ):
		playerPebbles += gameBoard[PLAYER][i]
		opponentPebbles += gameBoard[OPPONENT][i]

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