#!/usr/bin/python3


FILENAME = "input.txt"


def parseInput(line):
	split = line.strip().split("-")
	encrypted = "".join(split[:-1])
	last = split[-1]
	sectorId = int(last[:last.find("[")])
	checkSum = last[last.find("[") + 1 : -1]
	return encrypted, sectorId, checkSum


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		for line in inputFile:
			print(parseInput(line))
