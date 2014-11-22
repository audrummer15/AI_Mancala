import adamFunctions as AO

if __name__ == '__main__':
	board = [[0 for x in range(5)] for x in range(2)] 
	board[0][2] = 1
	board[1][4] = 6

	print board
	print "Result of Get: ", AO.getMinimaxFromHashTable(board)
	print "Result of Store: ", AO.storeMinimaxInHashTable(board, 1000)
	print "Result of Store: ", AO.storeMinimaxInHashTable(board, 1001)
	print "Result of Get: ", AO.getMinimaxFromHashTable(board)

	print AO.utilityH2(board)