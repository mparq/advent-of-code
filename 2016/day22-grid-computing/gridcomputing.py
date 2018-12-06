#!/usr/bin/python3
'''adventofcode.com/2016/day/22

Part One
--
All we had to do was read in node inputs and sort two lists by used and avail.
From this we can deduce that there is a viable pair for each node in the used
list paired with every higher node from the avail list. This can be determined
with one pass through each list.

Part Two
--
Looks like we'll need to do another state-space searching algorithm.

I want to try implementing IDA* (Iterative deepening A*).
Simple heuristic function might be the number of steps it would take
to send the current goal data to start along with the number of moves
it would take to off-load the start's data.
'''
import re


FILENAME = 'input.txt'


class Graph(object):
    '''Graph object stores state of all nodes and represents a state in our state search.'''

    def __init__(self, nodes, start=None, goal=None, width=37, height=25):
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal
        self.graph = {}
        for node in nodes:
            self.graph[(node.x, node.y)] = node

    def __str__(self):
        row_strings = []
        cutoff = 5
        header_string = ('    ' + '    '.join('{:^9d}'.format(col) for col in range(cutoff))
                         + ' ' * 17
                         + '    '.join('{:^9d}'.format(col)
                                       for col in range(self.width - (cutoff + 1), self.width)))
        for row in range(self.height):
            col_strings = []
            for col in range(cutoff):
                node = self.graph[(col, row)]
                format_string = ('({:3d}/{:3d})' if node == self.start
                                 else '[{:3d}/{:3d}]' if node == self.goal
                                 else ' {:3d}/{:3d} ')
                col_strings.append(format_string.format(node.used, node.size))
            col_strings.append('    ..   ')
            for col in range(self.width - (cutoff + 1), self.width):
                node = self.graph[(col, row)]
                format_string = ('({:3d}/{:3d})' if node == self.start
                                 else ('[{:3d}/{:3d}]' if node == self.goal
                                       else ' {:3d}/{:3d} '))
                col_strings.append(format_string.format(node.used, node.size))
            row_strings.append('{:<4d}{}'.format(row, ' -- '.join(col_strings)))
        row_separator = '\n{}\n'.format('    '
                                        + '    '.join('    |    ' for col in range(cutoff * 2)))
        table_body = row_separator.join(row_strings)
        return header_string + '\n\n' + table_body


class Node(object):
    '''Node of the memory grid.'''

    def __init__(self, name, size, used, avail):
        self.name = name
        match = re.findall(r"x(\d+)-y(\d+)", self.name)[0]
        self.x, self.y = int(match[0]), int(match[1])
        self.size = size
        self.used = used
        self.avail = avail

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return '({}) - {}/{}'.format(self.name, self.used, self.size)

    def __repr__(self):
        return '{}/{}'.format(self.used, self.size)

    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]
        return self.x == other.x and self.y == other.y


def parse_nodes():
    with open(FILENAME) as inputFile:
        inputFile.readline()
        inputFile.readline()
        nodes = []
        for line in inputFile:
            split = line.split()
            nodes.append(Node(split[0], int(split[1][:-1]), int(split[2][:-1]), int(split[3][:-1])))
        graph = Graph(nodes, start=(0, 0), goal=(36, 0))
        print(graph)


if __name__ == "__main__":
     parse_nodes()


