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
import heapq
from collections import defaultdict


FILENAME = "input.txt"


class FrequencyCollector(object):
	"""Data structure which keeps track of letter frequencies

	Internally, we use a dictionary and a heap to keep track of letter
	frequencies and "most frequent" letter.

	Instance variables:
	mostFrequent -- The most frequent letter.

	Instance methods:
	addLetter -- Adding a letter and updating inner data structures.
	"""

	def __init__(self):
		self.counter = defaultdict(int)
		self.pq = []

	def addLetter(self, letter):
		self.counter[letter] += 1
		heapq.heappush(self.pq, (-self.counter[letter], letter))

	@property
	def mostFrequent(self):
		return self.pq[0][1]


def decodeFrequencySignals(signals):
	columnFrequencies = None
	for i, signal in enumerate(signals):
		if i == 0:
			columnFrequencies = [FrequencyCollector()
								 for i in range(len(signal))]
		for freq, letter in zip(columnFrequencies, signal):
			freq.addLetter(letter)
			print("Added letter: {}".format(letter))
			print("Top 5 {}".format(freq.pq[:5]))
	return "".join(freq.mostFrequent for freq in columnFrequencies)


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		print(decodeFrequencySignals(line.strip() for line in inputFile))

