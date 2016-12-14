#!/usr/bin/python3
import heapq
from string import ascii_lowercase


FILENAME = "input.txt"
LETTER_TO_INDEX = {letter: index for index, letter in enumerate(ascii_lowercase)}


def parseInput(line):
	split = line.strip().split("-")
	encrypted = "".join(split[:-1])
	last = split[-1]
	sectorId = int(last[:last.find("[")])
	checkSum = last[last.find("[") + 1 : -1]
	return encrypted, sectorId, checkSum


def checkValid(encrypted, checkSum):
	counter = {}
	ordered = []
	for letter in encrypted:
		if letter not in counter:
			counter[letter] = 0
		counter[letter] += 1
	ordered = sorted((-count, letter) for letter, count in counter.items())
	realSum = "".join(map(lambda tup: tup[1], ordered[:5]))
	return realSum == checkSum
	

def sumSectorIds(lines):
	total = 0
	for line in lines:
		print(line.strip())
		encrypted, sectorId, checkSum = parseInput(line)
		if checkValid(encrypted, checkSum):
			print("Check sum was valid")
			total += sectorId
	return total


def shiftCipher(encrypted, shift):
	newString = []
	for letter in encrypted:
		newIndex = (LETTER_TO_INDEX[letter] + shift) % 26
		newLetter = ascii_lowercase[newIndex]
		newString.append(newLetter)
	return "".join(newString)


def solveCiphers(lines):
	for line in lines:
		encrypted, sectorId, checkSum = parseInput(line)
		if checkValid(encrypted, checkSum):
			solved = shiftCipher(encrypted, sectorId)
			print("{} sectorID: {}".format(solved, sectorId))


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		# grep output for northpole to solve
		solveCiphers(inputFile.readlines())
