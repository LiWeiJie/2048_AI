#! /usr/bin/python3
# -*- coding:utf-8 -*-  

from grid import Grid



def main():
	grid = Grid()
	grid.gprint()
	print("input: w or s or a or d")
	while(grid.won==False):
		x = input()
		moved = False
		if x=="w":
			moved = grid.move(0)
		if x=="s":
			moved = grid.move(1)
		if x=="a":
			moved = grid.move(2)
		if x=="d":
			moved = grid.move(3)

		if moved:
			grid.computerMove()
			grid.gprint()
			grid.eval_print()
 
if __name__ == "__main__":
	main()