#!/usr/bin/python3
"""adventofcode.com/2016/day/5

This puzzle seems to involve brute-forcing the correct code by
using an increasing index appended to our door id. The characters at the
6th index of the first 8 hashes that start with five zeroes becomes our
password and the solution to the first part of this puzzle.
"""
import hashlib


DOOR_ID = "reyedfim"


if __name__ == "__main__":
	password = []
	index = 0
	while len(password) < 8:
		tempBase = DOOR_ID + str(index)
		tempHash = hashlib.md5(tempBase.encode("utf-8")).hexdigest()
		if tempHash.startswith("00000"):
			password.append(tempHash[5])
			print(password)
		index += 1
	print("".join(password))
