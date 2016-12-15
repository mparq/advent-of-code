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
			if c != s[i-1] and s[i-1] == s[i+2]
				abba
we have a very short pattern, worst case O(4n)
"""
import re


FILENAME = "input.txt"


def findAbba(haystack):
	index = 1
	while index < len(haystack) - 2:
		needle = haystack[index]
		if needle == haystack[index + 1]:
			if (needle != haystack[index - 1]
			   		and haystack[index - 1] == haystack[index + 2]):
				return haystack[index - 1 : index + 3]
		index += 1


def splitIpAddress(ipAddress):
	split = {"valid": [], "invalid": []}
	valid = True
	current = []
	for char in ipAddress:
		if valid and char == "[":
			split["valid"].append("".join(current))
			current = []
			valid = False
		elif not valid and char == "]":
			split["invalid"].append("".join(current))
			current = []
			valid = True
		else:
			current.append(char)
	if len(current) > 0:
		split["valid"].append("".join(current))
	return split


def findTLSSupported(ipAddresses):
	"""Parse and locate abbas in valid/invalid sections

	abba in invalid section means ip address is not supported.
	Otherwise, the ip address supports TLS if an abba is found in one
	of its valid sections.
	"""
	counter = 0
	for ipAddress in ipAddresses:
		split = splitIpAddress(ipAddress)
		print("Split for {} is {}".format(ipAddress, split))
		valid = True
		for hypernet in split["invalid"]:
			abba = findAbba(hypernet)
			if abba is not None:
				print("Abba found in invalid section {}: {}".format(hypernet, abba))
				valid = False
				break
		if not valid:
			print("Abba found in invalid section {}. {} does not support TLS".format(hypernet, ipAddress))
			continue

		valid = False
		for ip in split["valid"]:
			abba = findAbba(ip)
			if abba is not None:
				print("Abba found in valid section {}: {}".format(ip, abba))
				valid = True
				break
		if valid:
			print("IP address {} supports TLS".format(ipAddress))
			counter += 1
	return counter

if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		print("{} IP addresses support TLS.".format(
			findTLSSupported(line.strip() for line in inputFile)))
