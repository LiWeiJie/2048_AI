#! /usr/bin/python3
# -*- coding:utf-8 -*-  

from copy import deepcopy

class Tile(object):
	"""docstring for Tile"""
	def __init__(self, position, value):
		super(Tile, self).__init__()
		self.x = position['x']
		self.y = position['y']
		self.value = value

		self.previous = None
		self.mergedTag = False

	def update(self, position, value, mergedTag=None):
		self.previous = {
			"x":self.x,
			"y":self.y,
			"value":self.value
		}

		self.x = position['x']
		self.y = position['y']
		self.value = value
		if mergedTag!=None:
			self.mergedTag = mergedTag

	def getPosition(self):
		return {
			"x":self.x,
			"y":self.y
		}

	def equal(self, newTile):
		return newTile!=None 	and\
			isinstance(newTile, Tile) and\
			newTile.x == self.x 	and\
			newTile.y == self.y 	and\
			newTile.value == self.value 	and\
			newTile.previous == self.previous 	and\
			newTile.mergedTag == self.mergedTag

	def __str__(self):
		return str(self.value)

	def clone(self):
		return deepcopy(self)
