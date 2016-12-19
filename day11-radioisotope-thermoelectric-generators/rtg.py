#!/usr/bin/python3
'''adventofcode.com/2016/day/11

After move:
    check valid state:
        for each floor:
            if > 0 generators on floor:
                if any unmatched microchips on floor:
                    INVALID

Possible neighboring states:

Function of current floor and current map state. All combinations of 2 or 1 moves up or down.
(moving 2 or 1 components from current floor to lower or upper floor).

Seems like we need to do a search of the state space. Break out that AI textbook...

Before that, I'll try BFS.

Choosing BFS rather than DFS so I don't have to worry about detecting infinite loops and because
we're looking for the shortest path to the end state.

Algorithm:

bfs_search(state):
    queue = queue()
    for neighbor in state.neighbors:
        queue.push(neighbor, 1)
    current = null
    path_length = 0
    while queue.not_empty and not is_end_state(current):
        current, path_length = queue.pop()
        for neighbor in current.neighbors:
            queue.push(neighbor, path_length + 1)
    return path_length
'''


if __name__ == "__main__":
    print(0)