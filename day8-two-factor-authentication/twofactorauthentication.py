#!/usr/bin/python3


FILENAME = "input.txt"


class TinyLED:
	"""Data structure representing the led screen specified in puzzle.

	Instance variables:
	board -- 2d list representing the led pixel screen
	width -- width of screen
	height -- height of screen
	numPixelsOn -- number of pixels that are ON in the screen

	Instance methods:
	rect -- turns on all pixels in a rectangle at top-left of screen
	rotateRow -- shifts pixels right in a row, rotating at boundary
	rotateColumn -- shifts pixels down in a column, rotating at boundary
	"""

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.board = [[False for j in range(width)] for i in range(height)]


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		for line in inputFile:
			print(line.strip())
