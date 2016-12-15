#!/usr/bin/python3


FILENAME = "input.txt"


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		for line in inputFile:
			print(line.strip())
