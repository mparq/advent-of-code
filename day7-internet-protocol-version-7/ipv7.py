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

Part two
--

This time we need to search the valid sequences first to build up
a set of aba's and in turn a set of corresponding bab's to search in
the hypernet sequences. I think Rabin-Karp would be ideal for searching
for a set of patterns, but it might be overkill here especially since
our patterns and strings to search through are small and frequently
changing.
"""
import re


FILENAME = "input.txt"


def findAbas(ip):
	abas = set()
	for index, char in enumerate(ip[:-2]):
		# only consider possible abas
		if char != ip[index + 2] or char == ip[index + 1]:
			continue
		abas = abas.union({ip[index : index + 3]})
	return abas


def parallelFindBab(haystack, babs, memTempSets):
	"""Search through the given string for any of the given patterns.

	Assumption is that all patterns are babs. This function is not
	general. If a general function is needed, we'll be better off
	re-implementing a known string searching algorithm like Rabin-Karp
	with multiple pattern searching. Don't need that here.

	Just for fun, I included a memory dictionary hashing from
	characters to possible babs for that character within an ipaddress.
	I realized that this probably wouldn't be used as often as I
	originally though, but left it in anyway.
	"""
	for index, char in enumerate(haystack[:-2]):
		# only start search if we have a possible bab
		if char != haystack[index + 2] or char == haystack[index + 1]:
			continue

		if char not in memTempSets:
			memTempSets[char] = {bab for bab in babs if bab.startswith(char)}
		tempSet = memTempSets[char]

		for bab in tempSet:
			if bab[1] == haystack[index + 1]:
				return bab


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


def findSSLSupported(ipAddresses):
	counter = 0
	for ipAddress in ipAddresses:
		split = splitIpAddress(ipAddress)
		abas = set()
		print("ipAddress {} split into {}".format(ipAddress, split))
		for ip in split["valid"]:
			abas = abas.union(findAbas(ip))
		print("abas found in {}: {}".format(ipAddress, abas))
		babs = {aba[1] + aba[0] + aba[1] for aba in abas}
		print("babs to search for: {}".format(babs))
		memTempSets = {}
		for hypernet in split["invalid"]:
			bab = parallelFindBab(hypernet, babs, memTempSets)
			print("searching for babs {} in hypernet {}".format(babs, hypernet))
			if bab is not None:
				print("bab found searching in hypernet {} out of possible babs {}: {}".format(hypernet, babs, bab))
				counter += 1
				break
	return counter


if __name__ == "__main__":
	with open(FILENAME) as inputFile:
		print("{} IP addresses support SSL.".format(
			findSSLSupported(line.strip() for line in inputFile)))
