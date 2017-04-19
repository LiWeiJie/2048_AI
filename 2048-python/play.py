#! /usr/bin/python3
# -*- coding:utf-8 -*-  

from grid import Grid



def main():
	grid = Grid()
	grid.gprint()
	last = [grid.clone(), grid.clone()]
	print("input: w or s or a or d, r for undo")
	while(grid.won==False):
		x = input()
		moved = False
		reset = False
		
		if x=="w":
			moved = grid.move(0)
		if x=="s":
			moved = grid.move(1)
		if x=="a":
			moved = grid.move(2)
		if x=="d":
			moved = grid.move(3)
		if x=="r":
			reset = True
			grid = last[0]
			last[1] = grid.clone()
		
		if moved or reset:
			if reset==False:
				grid.computerMove()
				last[0] = last[1]
				last[1] = grid.clone()
			grid.gprint()
			grid.eval_print()
		else:
			if len(grid.availableCells())==0:
				print("You fail")
				return
 
if __name__ == "__main__":
	main()