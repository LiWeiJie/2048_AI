#! /usr/bin/python3
# -*- coding:utf-8 -*-  

import random
from copy import deepcopy

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

	
	# // measures how smooth the grid is (as if the values of the pieces
	# // were interpreted as elevations). Sums of the pairwise difference
	# // between neighboring tiles (in log space, so it represents the
	# // number of merges that need to happen before they can merge). 
	# // Note that the pieces can be distant
	# Grid.prototype.smoothness = function() {
	#   var smoothness = 0;
	#   for (var x=0; x<4; x++) {
	#     for (var y=0; y<4; y++) {
	#       if ( this.cellOccupied( this.indexes[x][y] )) {
	#         var value = Math.log(this.cellContent( this.indexes[x][y] ).value) / Math.log(2);
	#         for (var direction=1; direction<=2; direction++) {
	#           var vector = this.getVector(direction);
	#           var targetCell = this.findFarthestPosition(this.indexes[x][y], vector).next;

	#           if (this.cellOccupied(targetCell)) {
	#             var target = this.cellContent(targetCell);
	#             var targetValue = Math.log(target.value) / Math.log(2);
	#             smoothness -= Math.abs(value - targetValue);
	#           }
	#         }
	#       }
	#     }
	#   }
	#   return smoothness;
	# }

	def smoothness():
		pass


	# Grid.prototype.monotonicity = function() {
	#   var self = this;
	#   var marked = [];
	#   var queued = [];
	#   var highestValue = 0;
	#   var highestCell = {x:0, y:0};
	#   for (var x=0; x<4; x++) {
	#     marked.push([]);
	#     queued.push([]);
	#     for (var y=0; y<4; y++) {
	#       marked[x].push(false);
	#       queued[x].push(false);
	#       if (this.cells[x][y] &&
	#           this.cells[x][y].value > highestValue) {
	#         highestValue = this.cells[x][y].value;
	#         highestCell.x = x;
	#         highestCell.y = y;
	#       }
	#     }
	#   }

	#   increases = 0;
	#   cellQueue = [highestCell];
	#   queued[highestCell.x][highestCell.y] = true;
	#   markList = [highestCell];
	#   markAfter = 1; // only mark after all queued moves are done, as if searching in parallel

	#   var markAndScore = function(cell) {
	#     markList.push(cell);
	#     var value;
	#     if (self.cellOccupied(cell)) {
	#       value = Math.log(self.cellContent(cell).value) / Math.log(2);
	#     } else {
	#       value = 0;
	#     }
	#     for (direction in [0,1,2,3]) {
	#       var vector = self.getVector(direction);
	#       var target = { x: cell.x + vector.x, y: cell.y+vector.y }
	#       if (self.withinBounds(target) && !marked[target.x][target.y]) {
	#         if ( self.cellOccupied(target) ) {
	#           targetValue = Math.log(self.cellContent(target).value ) / Math.log(2);
	#           if ( targetValue > value ) {
	#             //console.log(cell, value, target, targetValue);
	#             increases += targetValue - value;
	#           }
	#         } 
	#         if (!queued[target.x][target.y]) {
	#           cellQueue.push(target);
	#           queued[target.x][target.y] = true;
	#         }
	#       }
	#     }
	#     if (markAfter == 0) {
	#       while (markList.length > 0) {
	#         var cel = markList.pop();
	#         marked[cel.x][cel.y] = true;
	#       }
	#       markAfter = cellQueue.length;
	#     }
	#   }

	#   while (cellQueue.length > 0) {
	#     markAfter--;
	#     markAndScore(cellQueue.shift())
	#   }

	#   return -increases;
	# }

	# // measures how monotonic the grid is. This means the values of the tiles are strictly increasing
	# // or decreasing in both the left/right and up/down directions
	# Grid.prototype.monotonicity2 = function() {
	#   // scores for all four directions
	#   var totals = [0, 0, 0, 0];

	#   // up/down direction
	#   for (var x=0; x<4; x++) {
	#     var current = 0;
	#     var next = current+1;
	#     while ( next<4 ) {
	#       while ( next<4 && !this.cellOccupied( this.indexes[x][next] )) {
	#         next++;
	#       }
	#       if (next>=4) { next--; }
	#       var currentValue = this.cellOccupied({x:x, y:current}) ?
	#         Math.log(this.cellContent( this.indexes[x][current] ).value) / Math.log(2) :
	#         0;
	#       var nextValue = this.cellOccupied({x:x, y:next}) ?
	#         Math.log(this.cellContent( this.indexes[x][next] ).value) / Math.log(2) :
	#         0;
	#       if (currentValue > nextValue) {
	#         totals[0] += nextValue - currentValue;
	#       } else if (nextValue > currentValue) {
	#         totals[1] += currentValue - nextValue;
	#       }
	#       current = next;
	#       next++;
	#     }
	#   }

	#   // left/right direction
	#   for (var y=0; y<4; y++) {
	#     var current = 0;
	#     var next = current+1;
	#     while ( next<4 ) {
	#       while ( next<4 && !this.cellOccupied( this.indexes[next][y] )) {
	#         next++;
	#       }
	#       if (next>=4) { next--; }
	#       var currentValue = this.cellOccupied({x:current, y:y}) ?
	#         Math.log(this.cellContent( this.indexes[current][y] ).value) / Math.log(2) :
	#         0;
	#       var nextValue = this.cellOccupied({x:next, y:y}) ?
	#         Math.log(this.cellContent( this.indexes[next][y] ).value) / Math.log(2) :
	#         0;
	#       if (currentValue > nextValue) {
	#         totals[2] += nextValue - currentValue;
	#       } else if (nextValue > currentValue) {
	#         totals[3] += currentValue - nextValue;
	#       }
	#       current = next;
	#       next++;
	#     }
	#   }

	#   return Math.max(totals[0], totals[1]) + Math.max(totals[2], totals[3]);
	# }

	def monotonicity(self):
		pass

	def maxValue(self):
		ma = None
		for row in self.state:
			for x in row:
				if x!=None and (ma==None or x.value>ma.value):
					ma = x
		return ma

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

if __name__=="__main__":
	grid = Grid()
	grid.gprint()
	ava = grid.availableCells()
	print(ava)
