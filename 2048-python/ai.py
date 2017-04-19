#! /usr/bin/python3
# -*- coding:utf-8 -*-  

from tile import Tile
import math
from counttime import CountTime

DEBUG = False

class AI(object):
	"""using Minimax search algorithm and Alpha-beta pruning to search a best move for 2048"""
	def __init__(self, grid):
		super(AI, self).__init__()
		self.grid = grid

	smoothWeight = 0.1
	maxWeight = 1.0
	monoWeight = 1.0
	emptyWeight = 2.7

	depth = 3

	MAXSCORE = 100000

	def eval(self):
		grid = self.grid
		return 	grid.smoothness()*self.smoothWeight +\
				grid.maxValueTime()*self.maxWeight+\
				grid.monotonicity()*self.monoWeight+\
				math.log(len(grid.availableCells()))*self.emptyWeight

	def search(self, depth, alpha, beta, moveCount, cutoffs):
		bestScore = 0
		bestMove = -1

		grid = self.grid
		result = {}

		if DEBUG:
			print("depth:%d"%depth)

		if grid.playerTurn:
			if DEBUG:
				print("\talpha phase")
				print("\tmoveCount:%d\tcutoffs:%d"%(moveCount,cutoffs))


			return self.alphaPhase(depth, alpha, beta, moveCount, cutoffs)			
		else:
			# computer's turn 
			if DEBUG:
				print("\tbeta phase")
				print("\tmoveCount:%d\tcutoffs:%d"%(moveCount,cutoffs))
			return self.betaPhase(depth, alpha, beta, moveCount, cutoffs)

			


	def alphaPhase(self, depth, alpha, beta, moveCount, cutoffs):
		bestScore = alpha
		bestMove = -1
		grid = self.grid
		result = {}

		for direction in range(4):
			newGrid = grid.clone()
			if newGrid.move(direction):
				moveCount = moveCount+1

				# if DEBUG:
				# 	print("\tmove:%d is ok"%direction)

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

	def betaPhase(self, depth, alpha, beta, moveCount, cutoffs ):
		# return self.searchAllBeta(depth, alpha, beta, moveCount, cutoffs)
		# return self.expectBeta(depth, alpha, beta, moveCount, cutoffs)
		return self.worstkBeta(depth, alpha, beta, moveCount, cutoffs)

	def searchAllBeta(self, depth, alpha, beta, moveCount, cutoffs  ):
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


	def expectBeta(self,  depth, alpha, beta, moveCount, cutoffs ):
		badScore = beta
		grid = self.grid
		pass

	def annoyingEval(self):
		return -self.grid.smoothness() + self.grid.islands()

	# worst k eval beta search
	def worstkBeta(self,  depth, alpha, beta, moveCount, cutoffs ):
		badScore = beta
		grid = self.grid
		k = 1
		candidates = []
		cells = self.grid.availableCells()
		values = [2, 4]
		for cell in cells:
			for value in values:
				tile = Tile(cell, value)
				self.grid.setCell(tile)
				ann = self.annoyingEval()
				candidates.append({
						"tile": tile,
						"annoyingEval":ann
					})
				self.grid.removeCell(cell)

		candidates.sort(key = lambda obj:obj.get('annoyingEval'), reverse= True)

		for i in range(k):
			candidate = candidates[i]
			tile = candidate["tile"]
			moveCount += 1
			self.grid.setCell(tile)
			self.grid.playerTurn = True
			result  = self.search(depth, alpha, badScore, moveCount, cutoffs)
			self.grid.removeCell(tile.getPosition())
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

	def nextMove(self):
		newGrid = self.grid.clone()
		newAI = AI(newGrid)
		# return newAI.fixSearch()
		return newAI.iterativeSearch()

	def fixSearch(self):
		return self.search(self.depth, -10000, 10000, 0, 0)

	def iterativeSearch(self):
		minSearchTime = 500
		ct = CountTime()
		ct.start()
		depth = 0
		bestMove = {"score":0}
		ct.stop()
		print(ct.milliseconds())
		while ct.milliseconds()<minSearchTime:
			newMove = self.search(self.depth, -10000, 10000, 0, 0)
			if newMove["move"]==-1:
				break
			else:
				bestMove = newMove
			depth+=1
			ct.stop()
		print("\tdepth:%d"%depth)
		return bestMove