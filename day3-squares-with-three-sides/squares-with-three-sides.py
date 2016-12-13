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
	for i, triangle in enumerate(triangles):
		print("Triangle: {}".format(triangle))
		if isPossibleTriangle(triangle):
			possible += 1
		else:
			print("NOT POSSIBLE")
		print("---")
	print("Out of {} total.".format(i))
	return possible


def convertToTriangles(rawInput):
	"""Convert raw input into triangles for parsing by algorithm.

	Basically, we are reading in each line, keeping up a small data
	structure which keeps track of the running triangles in each
	column. After three lines have been read, we yield each of the
	triangles which we have built for each column and proceed to
	null out the data structure. In this way, we avoid double-reading
	lines with some small book-keeping overhead.
	"""
	triangleSlice = None
	for i, line in enumerate(rawInput):

		row = tuple(int(side) for side in line.strip().split())

		if i != 0 and i % 3 == 0:
			for triangle in triangleSlice:
				yield tuple(triangle)

		if i % 3 == 0:
			triangleSlice = [[] for column in row]
			
		for i, side in enumerate(row):
			triangleSlice[i].append(side)

	for triangle in triangleSlice:
		yield tuple(triangle)


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		possible = checkPossibleTriangles(convertToTriangles(inputFile.readlines()))
		print("There are {} possible triangles.".format(possible))
