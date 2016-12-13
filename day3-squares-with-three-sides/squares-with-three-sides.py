#!/usr/bin/python3


FILENAME = "input.txt"


def checkPossibleTriangles(triangles):
	for triangle in triangles:
		print(triangle)


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		checkPossibleTriangles(map(lambda line: tuple(int(side)
												 	  for side 
												 	  in line.strip().split()),
								   inputFile.readlines()))
