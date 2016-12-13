#!/usr/bin/python3


FILENAME = "input.txt"


def isPossibleTriangle(triangle):
	"""Check if a triangle is possible given the three sides.

	Algorithm: sum up all sides and subtract each side from that sum.
	If any of those operations results in a number <= side, reject.
	"""
	cumsum = sum(triangle)
	for side in triangle:
		if cumsum - side <= side:
			return False
	return True


def checkPossibleTriangles(triangles):
	possible = 0
	for triangle in triangles:
		print("Triangle: {}".format(triangle))
		if isPossibleTriangle(triangle):
			possible += 1
		else:
			print("NOT POSSIBLE")
		print("---")
	return possible


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		possible = checkPossibleTriangles(map(lambda line: 
												tuple(int(side)
												for side 
												in line.strip().split()),
								   		  inputFile.readlines()))
		print("There are {} possible triangles.".format(possible))
