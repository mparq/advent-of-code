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


class Point:
	"""Data structure representing a point in the 2-d coordinate plane.

	Instance variables:
	x -- x coordinate
	y -- y coordinate
	"""
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, pointB):
		if not pointB or not isinstance(pointB, Point):
			return False
		return self.x == pointB.x and self.y == pointB.y

	def __str__(self):
		return "Point: x={0}, y={1}".format(self.x, self.y)

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

	def __init__(self, startPoint, xdelta=0, ydelta=0):
		self.startPoint = startPoint
		self.xcomponent = xdelta
		self.ycomponent = ydelta
		self.endPoint = Point(self.startPoint.x + xdelta, 
							  self.startPoint.y + ydelta)
		
	def concatenate(self, vectorB):
		"""Return the vector produced by appending given vector to this one.

		Might not be the correct name for this method. Can only add a vector
		which has the same start point as the end point of this vector. Will
		be used to build up the final vector.
		"""
		if not vectorB or not isinstance(vectorB, Vector):
			raise ValueError("argument given is not an instance of Vector.")

		if vectorB.startPoint != self.endPoint:
			raise ValueError("argument vector start point must match "
							 "this vector's end point to concatenate.")

		return Vector(
			self.startPoint, 
			self.xcomponent + vectorB.xcomponent,
			self.ycomponent + vectorB.ycomponent)

	def __str__(self):
		return "Vector: ({start.x}, {start.y}) {x:+}x {y:+}y".format(
			start=self.startPoint,
			x=self.xcomponent,
			y=self.ycomponent)

	def __repr__(self):
		return str(self)


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		rawInput = inputFile.readline()
		inputTurns = map(lambda raw: Turn(raw.strip()), rawInput.split(","))

	for turn in inputTurns:
		print(turn)
