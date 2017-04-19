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
				grid.maxValueTime()*self.maxWeight+\
				len(grid.availableCells())*self.emptyWeight

	def search(self, depth, alpha, beta, moveCount, cutoffs):
		bestScore = 0
		bestMove = -1

		grid = self.grid
		result = {}

		if grid.playerTurn:
			return self.alpha_phase()			
		else:
			# computer's turn 
			badScore = beta

			


	def alpha_phase(self, depth, alpha, beta, moveCount, cutoffs):
		bestScore = alpha
		bestMove = -1
		grid = self.grid
		result = {}

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
						"score":newAI.eval(),
						"moveCount":moveCount
					}
				else:
					result = newAI.search(depth-1, bestScore, beta, moveCount, cutoffs)
					# if (result["score"]==self.MAXSCORE):
					moveCount = result["moveCount"]
					cutoffs = result["cutoffs"]

				if result["score"]>bestScore:
					bestScore = result["score"]
					bestMove = direction

				if bestScore > beta:
					cutoffs += 1
					# break
					return {
						"move" : bestMove,
						"score" : beta,
						"moveCount" : moveCount,
						"cutoffs" : cutoffs
						}
		return {
			"move" : bestMove,
			"score" : bestScore,
			"moveCount" : moveCount,
			"cutoffs" : cutoffs
			}

	def beta_phase(self, depth, alpha, beta, moveCount, cutoffs ):
		return worse_beta(depth, alpha, beta, moveCount, cutoffs)
		# return expect_beta(depth, alpha, beta, moveCount, cutoffs)
		# return badone_beta(depth, alpha, beta, moveCount, cutoffs)

	def worse_beta(self, depth, alpha, beta, moveCount, cutoffs  ):
		badScore = beta
		badMove = None
		grid = self.grid

		scores = [2, 4]
		cells = self.grid.availableCells()
		for val in scores:
			for cell in cells:	
				tile = Tile(cell, val)
				moveCount += 1
				# newGrid = this.grid.clone()
				# newGrid.setCell(tile)
				# newGrid.playerTurn = True
				# newAI = AI(self.grid)
				# newAI.search(depth, alpha, badScore, moveCount, cutoffs)
				self.grid.setCell(tile)
				self.grid.playerTurn = True
				result  = self.search(depth, alpha, badScore, moveCount, cutoffs)
				self.grid.removeCell(cell)
				self.grid.playerTurn = False
				moveCount = result["moveCount"]
				cutoffs = result["cutoffs"]

				if result["score"] < badScore:
					badScore = result["score"]

				# prun
				if badScore < alpha:
					cutoffs += 1
					return {
						"move":None,
						"score":alpha,
						"moveCount":moveCount,
						"cutoffs":cutoffs
					}
		return {
				"move":None,
				"score":badScore,
				"moveCount":moveCount,
				"cutoffs":cutoffs
			}


	def expect_beta(self,  depth, alpha, beta, moveCount, cutoffs ):
		badScore = beta
		grid = self.grid
		pass

	def badone_beta():
		badScore = beta
		grid = self.grid
		pass


	def nextMove(self):
		newGrid = self.grid.clone()
		newAI = AI(newGrid)
		return newAI.search(depth, -10000, 10000, 0, 0)

	def searchDeep(self):
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