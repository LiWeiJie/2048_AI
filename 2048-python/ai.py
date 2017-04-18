#! /usr/bin/python3
# -*- coding:utf-8 -*-  


class AI(object):
	"""using Minimax search algorithm and Alpha-beta pruning to search a best move for 2048"""
	def __init__(self, grid):
		super(AI, self).__init__()
		self.grid = grid

	smoothWeight = 0.1
	maxWeight = 1.0
	emptyWeight = 2.0

	deep = 3

	MAXSCORE = 100000

	def eval(self):
		grid = self.grid
		return 	grid.smoothness()*self.smoothWeight +\
				grid.maxValue()*self.maxWeight+\
				len(grid.availableCells())*self.emptyWeight

	def search(self, depth, alpha, beta, moveCount, cutoffs):
		bestScore = 0
		bestMove = -1
		grid = self.grid
		result = {}

		if grid.playerTurn:
			bestScore = alpha
			for direction in range(4):
				newGrid = grid.clone()
				if newGrid.move(direction):
					moveCount = moveCount+1
					if newGrid.won:
						return {
							"move":direction,
							"score":self.MAXSCORE
							}

					newAI = AI(newGrid)

					if depth==0:
						result = {
							"move":direction,
							"score":newAI.eval()
						}
					else:
						result = newAI.search(depth-1, bestScore, beta, moveCount, cutoffs)
						if (result["score"]==self.MAXSCORE):


	def nextMove(self, grid):
		self.grid = grid.clone()
		return self.iterativeDeep()

	def iterativeDeep(self):
		deep = self.deep
		depth = 0
		bestMove = {"score":0}
		while depth<deep:
			newMove = search(depth, -10000, 10000, 0, 0)
			if newMove["move"]==-1:
				break
			if newMove["score"]>bestMove["score"]:
				bestMove = newMove
			depth+=1
		return bestMove