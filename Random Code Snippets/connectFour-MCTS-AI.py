from math import sqrt, log
import random
import colorama
from colorama import Fore

class GameState:
	def __init__(self):
		self.playerJustMoved = 1

	def Clone(self):
		st = GameStat()
		st.playerJustMoved = self.playerJustMoved
		return st

	def DoMove(self,move):
		self.playerJustMoved = 3 - self.playerJustMoved

	def GetMoves(self):
		pass

	def IsGameOver(self):
		return self.GetMoves() == []

	def GetResult(self,player):
		pass

class Connect4State(GameState):
	def __init__(self, width=7, height=6, connect=4):
		self.playerJustMoved = 1
		self.winner = 0
		self.width = width
		self.height = height
		self.connect = connect
		self.InitializeBoard()

	def InitializeBoard(self):
		self.board = []
		for y in range(self.width):
			self.board.append([0] * self.height)

	def Clone(self):
		st = Connect4State(width=self.width,height=self.height)
		st.playerJustMoved = self.playerJustMoved
		st.winner = self.winner
		st.board = [self.board[col][:] for col in range(self.width)]
		return st

	def DoMove(self,movecol):
		assert movecol >= 0 and movecol <= self.width and self.board[movecol][self.height - 1] == 0
		row = self.height - 1
		while row >= 0 and self.board[movecol][row] == 0:
			row -= 1
		row += 1
		self.playerJustMoved = 3 - self.playerJustMoved
		self.board[movecol][row] = self.playerJustMoved
		if self.DoesMoveWin(movecol,row):
			self.winner = self.playerJustMoved

	def GetMoves(self):
		if self.winner != 0:
			return []		
		return [col for col in range(self.width) if self.board[col][self.height - 1] == 0]

	def DoesMoveWin(self, x, y):		
		me = self.board[x][y]
		for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
			p = 1
			while self.IsOnBoard(x+p*dx, y+p*dy) and self.board[x+p*dx][y+p*dy] == me:
				p += 1
			n = 1
			while self.IsOnBoard(x-n*dx, y-n*dy) and self.board[x-n*dx][y-n*dy] == me:
				n += 1

			if p + n >= (self.connect + 1): # want (p-1) + (n-1) + 1 >= 4, or more simply p + n >- 5
				return True

		return False

	def IsOnBoard(self, x, y):
		return x >= 0 and x < self.width and y >= 0 and y < self.height

	def GetResult(self, player):		
		return player == self.winner

	def __repr__(self):
		s = ""
		for i in range(self.width): s += str(i+1)
		s += "\n"
		for x in range(self.height - 1, -1, -1):
			for y in range(self.width):
				#s += [Fore.WHITE + '.', Fore.RED + 'X', Fore.YELLOW + 'O'][self.board[y][x]]
				s += ['.', 'X', 'O'][self.board[y][x]]
				#s += Fore.RESET
			s += "\n"
		return s

class Node:
	def __init__(self, move=None, parent=None, state=None):
		self.move = move  # Move that was taken to reach this game state 
		self.parentNode = parent  # "None" for the root node
		self.childNodes = []
		
		self.wins = 0
		self.visits = 0
		self.untriedMoves = state.GetMoves()  # Future childNodes
		self.playerJustMoved = state.playerJustMoved  # To check who won or who lost.
		
	def IsFullyExpanded(self):
		return self.untriedMoves == []

	def AddChild(self, move, state):
		node = Node(move=move, parent=self, state=state)
		self.untriedMoves.remove(move)
		self.childNodes.append(node)
		return node

	def Update(self, result):
		self.visits += 1
		self.wins += result

def UCB1(node, child, exploration_constant=sqrt(2)):
	return child.wins / child.visits + exploration_constant * sqrt(log(node.visits) / child.visits)

def selection_phase(node, state, selection_policy=UCB1, selection_policy_args=[]):
	if not node.IsFullyExpanded() or node.childNodes == []:
		return node
	selected_node = sorted(node.childNodes, key=lambda child: selection_policy(node, child, *selection_policy_args))[-1]
	state.DoMove(selected_node.move)
	return selection_phase(selected_node, state)

def expansion_phase(node, state):
	if node.untriedMoves !=[]:
		move = random.choice(node.untriedMoves)
		state.DoMove(move)
		node = node.AddChild(move,state)
	return node

def rollout_phase(state):
	while state.GetMoves() != []:
		state.DoMove(random.choice(state.GetMoves()))

def backpropagation_phase(node, state):
	if node is not None:
		node.Update(state.GetResult(node.playerJustMoved))
		backpropagation_phase(node.parentNode, state)

def action_selection_phase(node):
	return sorted(node.childNodes, key=lambda c: c.visits)[-1].move

def MCTS_UCT(rootstate, itermax, exploration_factor_ucb1=sqrt(2)):
	rootnode = Node(state=rootstate)
	
	for i in range(itermax):
		node  = rootnode
		state = rootstate.Clone()

		node  = selection_phase(node, state, selection_policy=UCB1, selection_policy_args=[exploration_factor_ucb1])

		node  = expansion_phase(node, state)
			
		rollout_phase(state)
			
		backpropagation_phase(node, state)
	
	return action_selection_phase(rootnode)

def PlayGame(initialState):
	state = initialState
	move = None
	while not state.IsGameOver():  # If we're not in a terminal state
		print(str(state))

		while True:
			move = input("Player " + ['O','X'][state.playerJustMoved-1] + ", Input Move: ")
			move = ord(move) - ord('1')
			if move < state.width and move >= 0:
				break
			else:
				print("Invalid Move! Try again!")

		state.DoMove(move)
	PrintGameResults(state)

def PlayGameAI(initialState,difficulty):
	state = initialState
	itermax = 10**difficulty
	move = None
	while not state.IsGameOver():  # If we're not in a terminal state
		print(str(state))
		if state.playerJustMoved == 1:
			# Player 1 turn
			if move: 
				print("Player 2/AI (X) has played : " + str(move+ 1))
			while True:
				move = input("Player 1 (O), Input Move: ")
				move = ord(move) - ord('1')
				if move < state.width and move >= 0:
					break
				else:
					print("Invalid Move! Try again!")
		else:
			# Player 2 turn
			move = MCTS_UCT(state, itermax)
		state.DoMove(move)
	PrintGameResults(state)

def PlayGameRand(initialState):
 	state = initialState
 	while not state.IsGameOver():
 		# Render
 		print(str(state))
 		# Capture user input
 		if state.playerJustMoved == 1:
 			# Player 1 turn
 			move = random.choice(state.GetMoves())
 		else:
 			# Player 2 turn
 			move = random.choice(state.GetMoves())
 		# Update game state
 		state.DoMove(move)

 	PrintGameResults(state)

def PrintGameResults(state):
	if state.GetResult(state.playerJustMoved) == 0.0:
		print(str(state))
		print("Player " + str(state.playerJustMoved) + " (O) wins!")
	elif state.GetResult(state.playerJustMoved) == 1.0:
		print(str(state))
		print("Player " + str(3 - state.playerJustMoved) + " (X) wins!")
	else:
		print("Nobody wins!")

InitialState = Connect4State()
print("Select a Game Mode:")
print("(1) Player vs Player")
print("(2) Player vs AI")
print("(3) Random vs Random")
while True:
	gameMode = input()
	gameMode = ord(gameMode) - ord('0')
	if gameMode <= 3 and gameMode >= 1:
		break
	else:
		print("Invalid Game Mode!")
if gameMode == 1:
	PlayGame(InitialState)
elif gameMode == 2:
	while True:
		diff = input("Select Difficulty (1-4): ")
		diff = ord(diff) - ord('0')
		if diff <= 4 and diff >= 1:
			break
		else:
			print("Invalid Difficulty!")
	PlayGameAI(InitialState,diff)
elif gameMode == 3:
	PlayGameRand(InitialState)
