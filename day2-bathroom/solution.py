#!/usr/bin/python3
from enum import Enum


class Move(Enum):
	U = 0
	L = 1
	R = 2
	D = 3


class Numpad(object):
	pass


def findButton(numpad, startButton, moves):
	return startButton


if __name__ == "__main__":
	with open("input.txt") as inputFile:
		numpad = Numpad()
		for line in inputFile:
			print(findButton(numpad, 5, line.strip()))

	
