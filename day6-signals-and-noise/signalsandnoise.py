#!/usr/bin/python3
"""adventofcode.com/2016/day/6

Part one of the puzzle seems like it will require the same operations
we already implemented for the day 4 puzzle but distributed across the
different columns of our input. I didn't use a heap in that puzzle, but
part one of this puzzle looks ripe for one, since we'll only be caring
about the "best" letter in each column to construct our final output.
I'll use a dictionary and min-heap (with negative counts) for each
column to keep track of the most-frequent letter.
"""


FILENAME = "input.txt"


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		for line in inputFile:
			print(line.strip())

