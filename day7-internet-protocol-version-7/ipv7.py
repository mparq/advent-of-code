#!/usr/bin/python3
"""adventofcode.com/2016/day/7

Part One
--
Need to split input up into valid and invalid sections. If an abba
exists in an invalid section, the ip address is invalid. O/w if an
abba axists in a valid section, the ip address is valid. Seems like
a good time to research some string searching algorithms.

My abba-finding algorithm: 
findabba(s)
	i = 1
	while i < len(s) - 2
		c = s[i]
		if c == s[i+1]
			if s[i-1] == s[i+2]
				abba
we have a very short pattern, worst case O(4n)
"""
import re


FILENAME = "input.txt"


def findTLSSupported(ipAddresses):
	for ipAddress in ipAddresses:
		print(ipAddress)


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		findTLSSupported(line.strip() for line in inputFile)
