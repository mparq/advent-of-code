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
    queue.push(state, 0)
    current = null
    path_length = 0
    while queue.not_empty and not is_end_state(current):
        current, path_length = queue.pop()
        for neighbor in current.neighbors:
            queue.push(neighbor, path_length + 1)
    return path_length
'''
from collections import defaultdict


FILENAME = "input.txt"


class FloorState(object):

    def __init__(self, current_floor, floor_map):
        self.current_floor = current_floor
        self.floor_map = floor_map

    def is_end_state(self):
        return not any(self.floor_map[floor] for floor in range(1, len(self.floor_map)))

    def is_valid_state(self):
        for floor in self.floor_map:
            valid_dict = defaultdict(list)
            has_generator = False
            for component in self.floor_map[floor]:
                valid_dict[component.element].append(component.type)
                if component.type == "generator":
                    has_generator = True

            if has_generator:
                single_component_elements = (element for element in valid_dict
                                             if len(valid_dict[element]) < 2)
                for single_element in single_component_elements:
                    if valid_dict[single_element][0].type == "microchip":
                        return False
        return True

    def neighbors(self):
        '''Return all possible neighbors of the current floor state.

        It's up to the caller to filter out invalid states. We naively create
        a new state for each possible move of components which are moves to the
        upper and lower floors of 1 or 2 components.
        '''
        components_on_floor = self.floor_map[self.current_floor]
        for index, component in enumerate(components_on_floor):
            valid_floors = (floor for floor in (self.current_floor + 1, self.current_floor - 1)
                            if 1 <= floor <= len(self.floor_map))
            for floor in valid_floors:
                map_after_move = self.floor_map.copy()
                map_after_move[self.current_floor].remove(component)
                map_after_move[floor].append(component)
                yield FloorState(floor, map_after_move)

                for other_component in components_on_floor[index + 1:]:
                    map_after_move = self.floor_map.copy()
                    map_after_move[self.current_floor].remove(component)
                    map_after_move[self.current_floor].remove(other_component)
                    map_after_move[floor] += [component, other_component]
                    yield FloorState(floor, map_after_move)


if __name__ == "__main__":
    with open(FILENAME) as inputFile:
        for line in inputFile:
            print(line.strip())
