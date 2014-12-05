import adamFunctions as AO
PLAYER1 = 0
PLAYER2 = 1

if __name__ == '__main__':
	board = [[0 for x in range(3)] for x in range(2)] 
	board[0][0] = 0
	board[0][1] = 0
	board[0][2] = 3
	board[1][0] = 2
	board[1][1] = 1
	board[1][2] = 0

	#print AO.boardToHashIndex(board)
	#print "Result of Get: ", AO.getMinimaxFromHashTable(board)
	#print "Result of Store: ", AO.storeMinimaxInHashTable(board, 1000)
	#print "Result of Store: ", AO.storeMinimaxInHashTable(board, 1001)
	#print "Result of Get: ", AO.getMinimaxFromHashTable(board)

	AO.printGameBoard(board)
	print "\n"
	#AO.printGameBoard(AO.results(board, 1, PLAYER1)[0])
	#print "\n"
	#AO.printGameBoard(AO.results(board, 1, PLAYER1)[1])
	#print "Result"
	result = AO.andOrGraphSearch(board, 4, 1, PLAYER1)
	print "AOResult: ", result
	#print "Original"
	#AO.printGameBoard(board)
