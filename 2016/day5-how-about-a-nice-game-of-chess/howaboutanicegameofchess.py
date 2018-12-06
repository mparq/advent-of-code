#!/usr/bin/python3
"""adventofcode.com/2016/day/5

This puzzle seems to involve brute-forcing the correct code by
using an increasing index appended to our door id. The characters at the
6th index of the first 8 hashes that start with five zeroes becomes our
password and the solution to the first part of this puzzle.

Second part of the puzzle. More brute forcing. But more intense...
"""
import hashlib


DOOR_ID = "reyedfim"


if __name__ == "__main__":
	password = [None for i in range(8)]
	index = 0
	while None in password:
		tempBase = DOOR_ID + str(index)
		tempHash = hashlib.md5(tempBase.encode("utf-8")).hexdigest()
		if tempHash.startswith("00000"):
			print("Interesting hash: {}".format(tempHash))
			position = int(tempHash[5]) if tempHash[5].isdigit() else None

			if position is not None and 0 <= position < len(password) and password[position] is None:
				password[position] = tempHash[6]
			
			print(" ".join("_" if letter is None else letter for letter in password))
		index += 1
	print("".join(password))
