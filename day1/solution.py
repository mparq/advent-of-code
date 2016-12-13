#!/usr/bin/python3
import sys
from enum import IntEnum, Enum


FILENAME = "input.txt"


class Direction(IntEnum):
	North = 0
	East = 1
	South = 2
	West = 3


class Turn(Enum):
	R = 0
	L = 1
	Right = 0
	Left = 1
	

class TurnStep:
	"""TurnStep represents an input of our algorithm.

	Instance variables:
	turn -- direction of the turn relative to facing direction
	steps -- number of steps taken after the turn
	"""

	def __init__(self, rawTurnStep):
		self.turn = Turn[rawTurnStep[0]]
		self.steps = int(rawTurnStep[1:])

	def __str__(self):
		return "TurnStep: turn - {0}, steps - {1}".format(self.turn,
														  self.steps)

	def __repr__(self):
		return str(self)	


class Point:
	"""Data structure representing a point in the 2-d coordinate plane.

	Instance variables:
	x -- x coordinate
	y -- y coordinate

	Instance methods:
	__eq__ -- Append given vector to instance vector to create new.
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

	Class methods:
	createVectorFromDirection -- creates a vector given facing direction.
	
	Instance variables:
	startPoint -- the starting point of the vector
	xcomponent -- the delta along X axis between start and end point
	ycomponent -- the delta along Y axis between start and end point
	endPoint -- the end point of the vector
	"""

	def __init__(self, startPoint, xdelta=0, ydelta=0):
		self.startPoint = startPoint
		self.xcomponent = xdelta
		self.ycomponent = ydelta
		self.endPoint = Point(self.startPoint.x + xdelta, 
							  self.startPoint.y + ydelta)

	def createVectorFromDirection(startPoint, direction, steps):
		xdelta = 0
		ydelta = 0

		if direction is Direction.North or direction is Direction.South:
			ydelta = steps if direction is Direction.North else -steps

		elif direction is Direction.East or direction is Direction.West:
			xdelta = steps if direction is Direction.East else -steps

		return Vector(startPoint, xdelta=xdelta, ydelta=ydelta)
		
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

	def __add__(self, vectorB):
		return self.concatenate(vectorB)

	def __str__(self):
		return "Vector: ({start.x}, {start.y}) {x:+}x {y:+}y".format(
			start=self.startPoint,
			x=self.xcomponent,
			y=self.ycomponent)

	def __repr__(self):
		return str(self)


def determineBlocksAway(turnSteps, startPosition=None, startDirection=None):
	"""Return the number of blocks away from starting position after turns.

	Solve part one of the puzzle asking for the number of blocks away from
	the starting position we end up from after taking all of the steps
	from the input.
	"""
	if startPosition is None:
		startPosition = Point(0, 0)

	if startDirection is None:
		startDirection = Direction.North

	direction = startDirection
	baseVector = Vector(startPosition, 0, 0)

	print("Facing North")

	for turnStep in turnSteps:
		print("============================")
		direction = _findDirectionAfterTurn(direction, turnStep.turn)
		tempVector = Vector.createVectorFromDirection(
			baseVector.endPoint,
			direction,
			turnStep.steps)
		baseVector += tempVector
		print("Input: {}".format(turnStep))
		print("Facing {}".format(direction.name))
		print("Base vector: {}".format(baseVector))
			
	return baseVector.xcomponent + baseVector.ycomponent
		
		
def _findDirectionAfterTurn(direction, turn):
	if turn is Turn.Right:
		return Direction((direction + 1) % 4)
	if turn is Turn.Left:
		return Direction((direction - 1) % 4)
	raise ValueError("Given direction must be left or right")


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		rawInput = inputFile.readline()
		inputTurnSteps = map(lambda raw: TurnStep(raw.strip()),
							 rawInput.split(","))

	print("We are {} blocks away from starting point.".format(
		determineBlocksAway(inputTurnSteps)))
