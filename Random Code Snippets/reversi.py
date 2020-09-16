import numpy as np

def printBoard(board):
	print("  |1|2|3|4|5|6|")	
	for i in range(6):
		print("  -------------")
		print(chr(ord('A') + i) + " |", end='')
		for j in range(6):
			print(board[i][j] + "|", end='')
		print("\n", end='')

def validMove(board,row,col,players,turn):
	valid = False
	if (row < 6) & (row >= 0) & (col >= 0 ) & (col < 6):
		if board[row][col] == ' ':
			neighPos = checkNeigh(board,row,col,players,turn)
			if neighPos:
				valid = True		
	return valid

def checkNeigh(board,row,col,players,turn):
	direction = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,0],[0,1],[1,-1],[1,0],[1,1]]	
	tempCords = []
	for i in range(0,9):
		checkRow = row + direction[i][0]
		checkCol = col + direction[i][1]
		j = 1
		while (checkRow < 6) & (checkRow >= 0) & (checkCol >= 0 ) & (checkCol < 6):
			if board[checkRow][checkCol] == players[(turn+1)%2]:
				checkRow += direction[i][0]
				checkCol += direction[i][1]
				j += 1
			elif (board[checkRow][checkCol] == players[turn%2]) & (j > 1):
				tempCords.append([checkRow,checkCol])
				break
			else:
				break
	return tempCords

def flipBoard(board,row,col,player,neighPos):
	tempBoard = board
	tempCords = []
	direction = [0,0]
	print(neighPos)
	print([row, col])
	for coord in neighPos:
		print(coord)		
		direction[0] = (np.sign(coord[0] - row))
		direction[1] = (np.sign(coord[1] - col))
		print(direction)
		for i in range(max(np.abs(coord[0]-row),np.abs(coord[1]-col))):
			tempBoard[row + direction[0]][col + direction[1]] = player
	board = tempBoard
	return

def checkMoves(board,players,turn):
	num = 0
	for i in range(6):
		for j in range(6):
			if board[i][j] == ' ':
				num += validMove(board,i,j,players,turn)
	return num

## Main Function
players = ['O','X']
turn = 0
board = np.empty([6,6], dtype='str')
board[:] = ' '
board[2][2] = 'O'
board[3][3] = 'O'
board[2][3] = 'X'
board[3][2] = 'X'
possibleMoves = checkMoves(board,players,turn)

while possibleMoves > 0:
	printBoard(board)
	scoreO = np.sum(board[:]=='O')
	scoreX = np.sum(board[:]=='X')
	print("Score: O = " + str(scoreO) + " | X = " + str(scoreX)
	print("Player " + players[turn%2])
	print("Number of possible moves: " + str(possibleMoves))
	while True:		
		user = input("Input Move: ")
		user = user.lower()
		if len(user) >= 2:
			row = ord(user[0]) - ord('a')
			col = ord(user[1]) - ord('1')
			if validMove(board,row,col,players,turn):
				neighPos = checkNeigh(board,row,col,players,turn)
				flipBoard(board,row,col,players[turn%2],neighPos)
				break;		
		print("Invalid Move")
	board[row][col] = players[turn%2]
	print(turn%2)
	print(row)
	print(col)
	turn += 1
	possibleMoves = checkMoves(board,players,turn)
if score0 != scoreX:
	print("Congratulations Player " + players[scoreX > scoreO)] + "! You have won!")
else:
	print("The game has ended in a tie!")