#!/usr/bin/python3
import re


FILENAME = 'input.txt'


class Graph(object):

    def __init__(self, width, height, nodes):
        self.width = width
        self.height = height
        self.graph = {}
        for node in nodes:
            self.graph[(node.x, node.y)] = node
        print(self.graph)


class Node(object):
    def __init__(self, name, size, used, avail):
        self.name = name
        self.x, self.y = re.findall(r"x(\d+)-y(\d+)", self.name)[0]
        self.size = size
        self.used = used
        self.avail = avail

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return '({}, {}): {} {} {}'.format(self.x, self.y, self.size, self.used, self.avail)

    def __repr__(self):
        return str(self)


def parse_nodes():
    with open(FILENAME) as inputFile:
        inputFile.readline()
        inputFile.readline()
        used_nodes = []
        avail_nodes = []
        for line in inputFile:
            split = line.split()
            used_nodes.append(Node(split[0], int(split[1][:-1]), int(split[2][:-1]), int(split[3][:-1])))
            avail_nodes.append(Node(split[0], int(split[1][:-1]), int(split[2][:-1]), int(split[3][:-1])))
        used_nodes.sort(key=lambda node: node.used, reverse=True)
        avail_nodes.sort(key=lambda node: node.avail, reverse=True)

        avail_visited = set()
        pairs = []
        used_pos = 0
        avail_pos = 0
        while used_pos < len(used_nodes):
            used = used_nodes[used_pos]
            if used.used == 0:
                break
            while avail_pos < len(avail_nodes) and avail_nodes[avail_pos].avail >= used.used:
                avail_visited.add(avail_nodes[avail_pos])
                avail_pos += 1
            pairs.extend((used, avail) for avail in (avail_visited - {used}))
            print(pairs)
            print("==========================")
            used_pos += 1

        print(len(pairs))


if __name__ == "__main__":
     parse_nodes()


