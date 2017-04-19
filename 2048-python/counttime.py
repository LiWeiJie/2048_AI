#! /usr/bin/python3
# -*- coding:utf-8 -*-  

import datetime


class CountTime(object):
	"""docstring for CountTime"""
	def __init__(self):
		super(CountTime, self).__init__()
		self.cycle = False
		
	def start(self):
		self.cycle = False
		self.startTime = datetime.datetime.now()
		# print(self.startTime)

	def stop(self):
		self.cycle = True
		self.stopTime = datetime.datetime.now()
		# print(self.stopTime)

	def ct(self):	
		return (self.stopTime - self.startTime)

	def microseconds(self):
		if self.cycle==True:
			return self.ct().microseconds
		else:
			return 0		

	def milliseconds(self):
		if self.cycle==True:
			return self.microseconds()/1000
		else:
			return 0

	def seconds(self):
		if self.cycle==True:
			return self.ct().seconds
		else:
			return 0