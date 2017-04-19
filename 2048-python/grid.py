#! /usr/bin/python3
# -*- coding:utf-8 -*-  

import random
from copy import deepcopy
import math

from tile import Tile

class Grid(object):
	"""grid describe"""
	# def __init__(self):
	# 	self.grid = []
	size = 4
	startCell = 2
	score = 0
	won = False
	playerTurn = True

	def __init__(self, state = []):
		if len(state) == 0:
			self.state = []
			for _x in range(4):
				self.state.append([])
				for _y in range(4):
					self.state[-1].append(None)
			startCell = self.startCell
			for x in range(startCell):
				position = self.randomAvailableCell()
				self.setCell(self.newCell(position))
		else:
			self.state = []
			for x in range(self.size):
				self.state.append([])
				for y in range(self.size):
					if state[x][y]!=None:
						self.state[x].append(Tile({
											"x":x,
											"y":y
											}, state[x][y]))
					else:
						self.state[x].append(None)

	def gprint(self):
		for x in self.state:
			li = []
			columnStr = '['
			for y in x:
				if y==None:
					columnStr += ("     _")
					# li.append(None)
				else:
					columnStr += ("%6d"%y.value)
					# li.append(y.value)
			# print(li)
			columnStr += "]"
			print(columnStr)
			# print(x)

	def clone(self):
		return deepcopy(self)

	def availableCells(self):
		ava = []
		for row in range(self.size):
			for i in range(self.size):
				if self.state[row][i]==None :
					ava.append({'x':row, 'y':i})
		return ava

	def availableCell(self, position):
		if self.checkInBounds(position):
			return self.state[position['x']][position['y']]==None
		return False

	def available(self, ava=None):
		if ava==None:
			ava = self.availableCells()
		return len(ava)>0

	def randomAvailableCell(self):
		ava = self.availableCells()
		assert(self.available(ava))
		return ava[random.randint(0, len(ava)-1)]

	def checkCellValue(self, value):
		return isinstance(value, int) and value!=0 and (value & (value-1)==0) and value!=1

	def checkInBounds(self, position):
		return ((position['x']>=0) and (position['x']<self.size)
			and (position['y']>=0) and (position['y']<self.size))

	def newCell(self, position):
		rad = random.randint(0,9)
		if rad<8:
			return Tile(position, 2)
		else:
			return Tile(position, 4)

	def removeCell(self, position):
		if self.checkInBounds(position):
			self.state[position['x']][position['y']] = None

	def setCell(self, tile):
		if self.checkInBounds(tile.getPosition()) and self.checkCellValue(tile.value):
			self.state[tile.x][tile.y] = tile

	def getCell(self, position):
		if self.checkInBounds(position):
			return self.state[position['x']][position['y']]
		else:
			return None

	def cleanMergedFag(self):
		for x in self.state:
			for y in x:
				if y!=None:
					y.mergedTag = False

	def getVector(self, action):
		vectors = [
		{'x':-1, 'y':0},  	# up
		{'x':1, 'y':0},		# down
		{'x':0, 'y':-1},	# left
		{'x':0, 'y':1},		# right
		]
		return vectors[action]

	def findFarthestPosition(self, position, direction):
		flag = True
		nextPos = {
			"x":position["x"],
			"y":position["y"]
		}
		while flag:
			previous = {
				"x":nextPos["x"],
				"y":nextPos["y"]
			}
			nextPos = {
				"x":previous["x"]+direction["x"],
				"y":previous["y"]+direction["y"]
			}
			if (self.checkInBounds(nextPos)==False) or self.availableCell(nextPos)==False:
				flag = False

		return {
			"farthest":previous,
			"next":nextPos
		}

	# action = 0/1/2/3 
	def move(self, action):
		vector = self.getVector(action)
		tracks = self.getTracks(vector)
		moved = False
		for x in tracks[0]:
			for y in tracks[1]:
				position = {"x":x, "y":y}
				# print(position)
				tile = self.getCell(position)
				if tile!=None:
					tiles = self.findFarthestPosition(position, vector)
					# print(tiles)
					farthest = tiles["farthest"]
					farthestTile = self.getCell(farthest)
					nextTile = self.getCell(tiles["next"])

					if nextTile!=None and nextTile.value == tile.value and nextTile.mergedTag==False :
						tile.update(nextTile.getPosition(), tile.value*2, True)
						self.setCell(tile)
						self.removeCell(position)
						self.score += tile.value
						if tile.value==2048:
							self.won = True
					else:
						# print(tiles["farthest"])
						# print("%d,%d:%d"%(tile.x, tile.y, tile.value))

						if farthestTile==None:
							tile.update(farthest, tile.value)
							self.setCell(tile)
							self.removeCell(position)
					if position!=tile.getPosition():
						moved = True

		if moved==True:
			self.playerTurn = False
		self.cleanMergedFag()
		return moved

	def getTracks(self, direction):
		tracks = []
		for i in range(2):
			tracks.append([])
			for j in range(self.size):
				tracks[-1].append(j)

		if direction['x']==1:
			tracks[0].reverse()
		if direction['y']==1:
			tracks[1].reverse()

		return tracks



	def same(self, newGrid):
		for i in range(self.size):
			for j in range(self.size):
				if  (self.state[i][j]==None and newGrid.state[i][j]!=None) or \
					(self.state[i][j]!=None and self.state[i][j].equal(newGrid.state[i][j])==False):
					return False
		return True

	def addRandomTile(self):
		self.setCell( self.newCell( self.randomAvailableCell()))

	def computerMove(self):
		self.addRandomTile()
		self.playerTurn = True

	def mergeAvailable():
		for action in range(4):
			tryGrid = self.clone()
			if tryGrid.move(action):
				return True
		return False

	def moveAvailable(self):
		return len(self.availableCells())!=0 or mergeAvailable()

	# followed by some evaluation function

	def eval_print(self):
		print("smoothness:%d"%self.smoothness())
		print("monotonicity:%d"%self.monotonicity())
		print("empty tiles:%d"%len(self.availableCells()))


	def smoothness(self):
		smoothness = 0
		for i in range(self.size):
			for j in range(self.size):
				position = {
						"x":i,
						"y":j
					}
				tile = self.getCell(position)
				if (tile!=None):
					mergeTime = self.getCellValueTime(position)
					for d in [1,2]:
						vector = self.getVector(d)
						tiles = self.findFarthestPosition(position, vector)
						# print(tiles)
						farthest = tiles["farthest"]
						nextTile = self.getCell(tiles["next"])
						if nextTile!=None:
							nextTime = self.getCellValueTime(tiles["next"])
							smoothness -= abs(mergeTime-nextTime)

		return smoothness

	def monotonicity(self):
		scores = [0 for _x in range(4)]
		# up and down
		for x in range(self.size):
			for current in range(self.size):
				currentPosition = {
								"x": x,
								"y": current
								}
				if self.availableCell(currentPosition)==False:
					for next in range(current+1, self.size):
						currTime = self.getCellValueTime(currentPosition)
						nextPosition = {
									"x": x,
									"y": next
									}
						if self.availableCell(currentPosition)==False or next==(self.size-1):
							nextTime = self.getCellValueTime(nextPosition)
							if currTime > nextTime:
								scores[0] += currTime - nextTime
							else:
								scores[1] += nextTime - currTime
				
		# left and right
		for y in range(self.size):
			for current in range(self.size):
				for next in range(current+1, self.size):
					currTime = self.getCellValueTime({
							"x": current,
							"y": y
						})
					nextTime = self.getCellValueTime({
							"x": next,
							"y": y
						})
					if currTime > nextTime:
						scores[2] += currTime - nextTime
					else:
						scores[3] += nextTime - currTime
				
		return max(scores[0], scores[1]) + max(scores[2], scores[3])

	def islands(self):
		marked = {}
		islands = 0
		for row in self.state:
			for cell in row:
				if cell!=None:
					if cell.value in marked:
						marked[cell.value] = True
						islands += 1
		return islands
		

	def maxValue(self):
		ma = None
		for row in self.state:
			for x in row:
				if x!=None and (ma==None or x.value>ma.value):
					ma = x
		return ma

	def maxValueTime(self):
		return int(math.log2(self.maxValue().value))

	def getCellValue(self, position):
		cell = self.getCell(position)
		if cell==None:
			return 0
		else:
			return cell.value

	def getCellValueTime(self, position):
		val = self.getCellValue(position)
		if val==0:
			return 0
		else:
			return int(math.log2(val))


class TestGrid(object):

	def test_checkInBounds(self):
		grid = Grid()
		for x in range(Grid.size):
			for y in range(Grid.size):
				assert(grid.checkInBounds({'x':x, 'y':y}))

		assert(grid.checkInBounds({'x':Grid.size, 'y':0})==False)
		assert(grid.checkInBounds({'x':Grid.size, 'y':Grid.size})==False)
		assert(grid.checkInBounds({'x':0, 'y':Grid.size})==False)
		assert(grid.checkInBounds({'x':-1, 'y':Grid.size})==False)
		assert(grid.checkInBounds({'x':-1, 'y':0})==False)
		assert(grid.checkInBounds({'x':0, 'y':-1})==False)

	def test_checkCellValue(self):
		grid = Grid()
		num = 1
		for x in range(15):
			num = num*2
			assert(grid.checkCellValue(num))
		assert(grid.checkCellValue(1234)==False)
		assert(grid.checkCellValue(56)==False)
		assert(grid.checkCellValue(1)==False)
		assert(grid.checkCellValue(987)==False)
		assert(grid.checkCellValue(1023)==False)
		assert(grid.checkCellValue(1025)==False)


	# check in test_randomAvailableCell
	# def test_gprint(self):
	# 	grid = Grid()
	# 	grid.gprint()

	def test_clone(self):
		pass

	def test_availableCells(self):
		pass

	def test_availableCell(self):
		pass

	def test_available(self):
		pass

	# check in test_randomAvailableCell
	# def test_setCell(self):
	# 	pass

	def test_randomAvailableCell(self):
		grid = Grid()
		old = len(grid.availableCells())
		checknum = 10
		for x in range(checknum):
			grid.setCell( grid.newCell(grid.randomAvailableCell()))
		assert(old-len(grid.availableCells())==(checknum))
		grid.gprint()

	def test_newCell(self):
		pass

	def test_maxValue(self):
		grid = Grid()
		assert(grid.maxValue().value==2 or grid.maxValue().value==4)
		grid.setCell(Tile(grid.randomAvailableCell(), 1024))
		assert(grid.maxValue().value==1024)
		grid.setCell(Tile(grid.randomAvailableCell(), 512))
		assert(grid.maxValue().value==1024)

	def test_move(self):
		grid = Grid()
		grid.move(0)

	def test_getTracks(self):
		grid = Grid()
		vector1 = [ [0,1,2,3], [0,1,2,3]  ]
		vector2 = [ [3,2,1,0], [0,1,2,3]  ]
		vector3 = [ [0,1,2,3], [3,2,1,0]  ]
		assert(grid.getTracks(grid.getVector(0)) == vector1)
		assert(grid.getTracks(grid.getVector(1)) == vector2)
		assert(grid.getTracks(grid.getVector(2)) == vector1)
		assert(grid.getTracks(grid.getVector(3)) == vector3)

	def test_same(self):
		grid1 = Grid()
		grid2 = grid1.clone()
		grid3 = grid2.clone()
		grid4 = grid3.clone()
		grid2.setCell( Tile({"x":0, "y":0} , 8))
		grid3.setCell( Tile({"x":0, "y":0} , 8))

		# grid1.gprint()
		# grid2.gprint()
		# grid3.gprint()
		# grid4.gprint()


		assert(grid1.same(grid2)==False)
		assert(grid2.same(grid3)==True)
		assert(grid3.same(grid4)==False)
		assert(grid4.same(grid1)==True)

	def getVector(self):
		pass

	def test_findFarthestPosition(self):
		pass

	# def test_print(self):
	# 	grid = Grid()
	# 	checknum = 14
	# 	for x in range(checknum):
	# 		grid.setCell( grid.newCell(grid.randomAvailableCell()))

	# 	print(grid.state[0][0])

	def test_getCell(self):
		grid = Grid()
		grid.setCell( Tile({"x":0, "y":0} , 16))
		assert(grid.getCell({"x":0, "y":0}).value==16 )

	def test_addRandomTile(self):
		grid = Grid()
		le = len(grid.availableCells())
		grid.addRandomTile()
		assert((le-len(grid.availableCells()))==1)

	def test_mergeAvailable(self):
		pass

	def test_moveAvailable(self):
		pass

	def test_computerMove(self):
		pass

	def test_maxValueTime(self):
		pass

	def test_getCellValue(self):
		pass

	def test_getCellValueTime(self):
		pass

if __name__=="__main__":
	grid = Grid()
	grid.gprint()
	ava = grid.availableCells()
	print(ava)
