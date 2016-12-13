#!/usr/bin/python3
import sys

FILENAME = "input.txt"


class Turn:
	"""Turn represents an input of our algorithm.

	Instance variables:
	direction -- direction of the turn relative to facing direction
	steps -- number of steps taken after the turn
	"""
	def __init__(self, rawTurn):
		self.direction = rawTurn[0]
		self.steps = int(rawTurn[1:])

	def __str__(self):
		return "Turn: direction - {0}, steps - {1}".format(self.direction,
													self.steps)

	def __repr__(self):
		return str(self)	


class Vector:
	"""Vector used in geometric calculations to determine coordinates.

	VectorA + VectorB = VectorC where VectorC has start point of VectorA
	and end point of VectorB if VectorA endpoint = VectorB startpoint
	
	Instance variables:
	startPoint -- the starting point of the vector
	endPoint -- the end point of the vector
	"""

	def __init__(self, startPoint, endPoint):
		self.startPoint = startPoint
		self.endPoint = endPoint


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		rawInput = inputFile.readline()
		inputTurns = map(lambda raw: Turn(raw.strip()), rawInput.split(","))

	for turn in inputTurns:
		print(turn)
