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

	# Create a map from button to coordinates and vice versa
	# so that we can easily swap between hash maps
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

	deltas = {
		Move.Up: (0, -1),
		Move.Left: (-1, 0),
		Move.Right: (1, 0),
		Move.Down: (0, 1)
	}

	coordToButton = {coord: button for button, coord in buttonToCoord.items()}

	def _forceBound(coord):
		return (
			min(2, max(0, coord[0])),
			min(2, max(0, coord[1])))
		
	def moveFromButton(self, button, move):
		buttonCoord = Numpad.buttonToCoord[button]
		print("Coord for button {} is {}".format(button,
												 Numpad.buttonToCoord[button]))
		delta = Numpad.deltas[move]
		print("Delta for move {} is {}".format(move, delta))
		newCoord = Numpad._forceBound((delta[0] + buttonCoord[0], delta[1] + buttonCoord[1]))
		print("Coord after delta is {}".format(newCoord))
		return Numpad.coordToButton[newCoord]


def findButton(numpad, startButton, moves):
	button = startButton
	for move in moves:
		button = numpad.moveFromButton(button, Move[move])
		print("Move {} to button {}".format(move, button))
	return button


def findButtons(moveLines, numpad=None, startButton=5):
	if numpad is None:
		numpad = Numpad()

	button = startButton
	print("Starting at button {}".format(button))
	for i, moveLine in enumerate(moveLines):
		button = findButton(numpad, button, moveLine)
		print(CONSOLE_SEPARATOR)
		print("After line {0}, button was {1}".format(i, button))


if __name__ == "__main__":
	with open("input.txt") as inputFile:
		findButtons(map(lambda line: line.strip(), inputFile.readlines()))
