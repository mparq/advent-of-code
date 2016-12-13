#!/usr/bin/python3
import sys

FILENAME = "input.txt"


class Turn:
	def __init__(self, rawTurn):
		self.direction = rawTurn[0]
		self.steps = int(rawTurn[1:])

	def __str__(self):
		return "Turn: direction - {0}, steps - {1}".format(self.direction,
													self.steps)

	def __repr__(self):
		return str(self)	


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		rawInput = inputFile.readline()
		inputTurns = map(lambda raw: Turn(raw.strip()), rawInput.split(","))
		print(list(inputTurns))
