import andOr as AO

if __name__ == '__main__':
	board = [[0 for x in range(5)] for x in range(2)] 
	board[0][2] = 1
	board[1][4] = 6

	print board
	print AO.getMinimaxFromTransTable(AO.boardToHashIndex(board))
	print AO.storeMinimaxValue(AO.boardToHashIndex(board), 1000)
	print AO.storeMinimaxValue(AO.boardToHashIndex(board), 1001)
	print AO.getMinimaxFromTransTable(AO.boardToHashIndex(board))