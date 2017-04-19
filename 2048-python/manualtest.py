#! /usr/bin/python3
# -*- coding:utf-8 -*-  

from ai import AI
from grid import Grid
from counttime import CountTime

		

def test_ai():
	grid = Grid()
	grid.gprint()
	ct = CountTime()
	totalCT = 0
	while grid.won==False:
		# input()
		print("*******************************************")
		ai = AI(grid)
		ct.start()
		d = ai.nextMove()
		ct.stop()
		moved = grid.move(d["move"])
		if moved==True:
			grid.gprint()
			moveCount = d["moveCount"]
			cutoffs = d["cutoffs"]
			print("moveCount:%d\tcutoffs:%d"%(moveCount,cutoffs))
			nct = ct.milliseconds()
			totalCT += nct
			print("time consume:%d "%(nct))
			print("total time consume:%d "%(totalCT))
			if grid.won==False:
				grid.computerMove()
			else:
				grid.gprint()
		else:
			print("You fail")
			return


def main():
	test_ai()


if __name__=="__main__":
	main()