#!/usr/bin/python3
import math
from enum import Enum


CONSOLE_SEPARATOR = "=================================="


class Move(Enum):
	U = 0
	Up = 0
	L = 1
	Left = 1
	R = 2
	Right = 2
	D = 3
	Down = 3


class Numpad(object):

	deltas = {
		Move.Up: (0, -1),
		Move.Left: (-1, 0),
		Move.Right: (1, 0),
		Move.Down: (0, 1)
	}

	# Create a map from button to coordinates and vice versa
	# so that we can easily swap between hash maps
	buttonToCoord = {}

	coordToButton = {coord: button for button, coord in buttonToCoord.items()}

	def isInBounds(self, coord):
		return coord in self.coordToButton
		
	def moveFromButton(self, button, move):
		buttonCoord = self.buttonToCoord[button]
		delta = Numpad.deltas[move]
		newCoord = (delta[0] + buttonCoord[0], delta[1] + buttonCoord[1])

		# reset coord if the move pushes it out of bounds of the numpad
		if not self.isInBounds(newCoord):
			newCoord = buttonCoord

		return self.coordToButton[newCoord]


class SimpleNumpad(Numpad):
	
	buttonToCoord = {
		1: (0, 0),
		2: (1, 0),
		3: (2, 0),
		4: (0, 1),
		5: (1, 1),
		6: (2, 1),
		7: (0, 2),
		8: (1, 2),
		9: (2, 2)
	}

	coordToButton = {coord: button for button, coord in buttonToCoord.items()}

	def _forceBound(self, coord):
		return (
			min(2, max(0, coord[0])),
			min(2, max(0, coord[1])))


class ComplicatedNumpad(Numpad):

	buttonToCoord = {
		1: (2, 0),
		2: (1, 1),
		3: (2, 1),
		4: (3, 1),
		5: (0, 2),
		6: (1, 2),
		7: (2, 2),
		8: (3, 2),
		9: (4, 2),
		"A": (1, 3),
		"B": (2, 3),
		"C": (3, 3),
		"D": (2, 4)
	}

	coordToButton = {coord: button for button, coord in buttonToCoord.items()}


def findButton(numpad, startButton, moves):
	button = startButton
	for move in moves:
		button = numpad.moveFromButton(button, Move[move])
	return button


def findButtons(moveLines, numpad=None, startButton=5):
	if numpad is None:
		numpad = SimpleNumpad()

	button = startButton
	print("Starting at button {}".format(button))
	for i, moveLine in enumerate(moveLines):
		button = findButton(numpad, button, moveLine)
		print(CONSOLE_SEPARATOR)
		print("After line {0}, button was {1}".format(i, button))


if __name__ == "__main__":
	with open("input.txt") as inputFile:
		findButtons(map(lambda line: line.strip(), inputFile.readlines()), numpad=ComplicatedNumpad())
