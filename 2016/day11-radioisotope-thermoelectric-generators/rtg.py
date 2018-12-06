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

jk... BFS is not sufficient here. number of states explodes

heuristic?
'''
from collections import defaultdict, namedtuple
import heapq
import copy
import re


FILENAME = "input.txt"
NUM_FLOORS = 4


Component = namedtuple("Component", ["element", "component_type"])


class FloorState(object):
    '''Encapsulates the state logic of the building floors.

    The possible state neighbors depend on the current floor and what components
    are on the surrounding floors.

    Instance variables:
    current_floor -- current floor that you are on
    floor_map -- information about which components are on each floor

    Instance methods:
    neighbors -- returns generator of all valid neighbor states
    is_end_state -- returns true if at final state
    is_valid_state -- returns true only if there are no unmatched microchips on a floor
    '''

    def __init__(self, current_floor, floor_map):
        self.current_floor = current_floor
        self.floor_map = floor_map

    def is_end_state(self):
        '''Return True if all components are on the top floor.'''
        return not any(self.floor_map[floor] for floor in range(1, len(self.floor_map)))

    def is_valid_state(self):
        '''Return true if there are no unmatched microchips on any floor.'''
        for floor in self.floor_map:
            valid_dict = defaultdict(list)
            has_generator = False
            for component in self.floor_map[floor]:
                valid_dict[component.element].append(component.component_type)
                if component.component_type == "generator":
                    has_generator = True

            if has_generator:
                single_component_elements = (element for element in valid_dict
                                             if len(valid_dict[element]) < 2)
                for single_element in single_component_elements:
                    if valid_dict[single_element][0] == "microchip":
                        return False
        return True

    @property
    def estimated_distance_from_end(self):
        '''Return the h(s) in f(s) = g(s) + h(s) of the a* algorithm.

        This is the heuristic estimate of the estimated cost of the remaining
        path. The heuristic must be admissable meaning that it should never overestimate
        the cost of the path. Have to choose a good heuristic to arrive at the correct
        answer quickly though.

        Intuitively, I'd prefer the generators get to the top floor quickest. If all
        generators are on the top floor, we merely need to move microchips to arrive at the
        final end state, since no microchip will be unmatched at the top.
        '''
        estimated_cost = 0
        for floor in range(1, len(self.floor_map) + 1):
            floor_generators = [component for component in self.floor_map[floor]
                                if component.component_type == "generator"]
            floor_microchips = [component for component in self.floor_map[floor]
                                if component.component_type == "microchip"]
            lower_unmatched_generators = []
            for lower_floor in range(1, floor):
                lower_floor_components = self.floor_map[lower_floor]
                for lower_component in lower_floor_components:
                    if (lower_component.component_type == "generator"
                            and lower_component.element in (chip.element
                                                            for chip in floor_microchips)):
                        lower_unmatched_generators.append(lower_component)
            unmatched_generators = len(lower_unmatched_generators)

            floor_cost = floor_generators * 5 * floor
            floor_cost += (len(floor_microchips) - 1) * (len(self.floor_map) - floor)
            estimated_cost += floor_cost
        return estimated_cost

    def neighbors(self):
        '''Return all possible neighbors of the current floor state.

        It's up to the caller to filter out invalid states. We naively create
        a new state for each possible move of components which are moves to the
        upper and lower floors of 1 or 2 components.
        '''
        components_on_floor = self.floor_map[self.current_floor]
        valid_floors = [floor for floor in (self.current_floor + 1, self.current_floor - 1)
                        if 1 <= floor <= len(self.floor_map)]
        for index, component in enumerate(components_on_floor):
            for floor in valid_floors:
                map_after_move = copy.deepcopy(self.floor_map)
                map_after_move[self.current_floor].remove(component)
                map_after_move[floor].append(component)
                potential_floor_state = FloorState(floor, map_after_move)
                if potential_floor_state.is_valid_state():
                    yield potential_floor_state

                for other_component in components_on_floor[index + 1:]:
                    map_after_move = copy.deepcopy(self.floor_map)
                    map_after_move[self.current_floor].remove(component)
                    map_after_move[self.current_floor].remove(other_component)
                    map_after_move[floor] += [component, other_component]
                    potential_floor_state = FloorState(floor, map_after_move)
                    if potential_floor_state.is_valid_state():
                        yield potential_floor_state

    def __hash__(self):
        return hash((self.current_floor, frozenset((floor, frozenset(components))
                                                   for floor, components
                                                   in self.floor_map.items())))

    def __str__(self):
        floor_strings = ["Current floor: {}".format(self.current_floor)]
        for floor in self.floor_map:
            floor_string = ", ".join("{} {}".format(component.element, component.component_type)
                                     for component
                                     in self.floor_map[floor])
            floor_strings.append("Floor {}: {}".format(floor, floor_string))
        return "\n".join(str(floor_string) for floor_string in floor_strings)

    def __repr__(self):
        return str(self)

    def __eq__(self, other_state):
        return (self.floor_map == other_state.floor_map
                and self.current_floor == other_state.current_floor)

    def __lt__(self, other_state):
        return self.estimated_distance_from_end < other_state.estimated_distance_from_end


def find_shortest_radioactive_path(raw_floors):
    '''Find shortest path to bring all components to top floor.'''
    initial_floor_map = {floor: [] for floor in range(1, NUM_FLOORS + 1)}
    all_components = []
    for index, raw_floor in enumerate(raw_floors):
        current_floor_components = initial_floor_map[index + 1]
        print(raw_floor)
        generator_match_pattern = r"(\w+) generator"
        microchip_match_pattern = r"(\w+)-compatible microchip"
        matched_generators = re.finditer(generator_match_pattern, raw_floor)
        matched_microchips = re.finditer(microchip_match_pattern, raw_floor)
        for element in (match.group(1) for match in matched_generators):
            component = Component(element=element, component_type="generator")
            current_floor_components.append(component)
            all_components.append(component)
        for element in (match.group(1) for match in matched_microchips):
            component = Component(element=element, component_type="microchip")
            current_floor_components.append(component)
            all_components.append(component)
    initial_state = FloorState(1, initial_floor_map)

    end_floor_map = {floor: [] for floor in range(1, NUM_FLOORS)}
    end_floor_map[NUM_FLOORS] = all_components
    goal_state = FloorState(4, end_floor_map)
    return bfs_search(initial_state, goal_state)


class ToVisitQueue:
    '''A priority queue implementation that allows for efficient updating of priorities.

    Modeled after http://code.activestate.com/recipes/522995-priority-dict-a-priority-queue-with-updatable-prio/
    Basically just a  wrapper around a python heap and a dictionary.
    The dictionary keeps track of the current priorities of all elements in the queue
    and allows for O(1) priority updating. The heap keeps our priority invariant.
    '''

    def __init__(self):
        self._queue = []
        self._priority = {}

    def _rebuild_heap(self):
        self._queue = [(val, key) for key, val in self._priority.items()]
        heapq.heapify(self._queue)

    def __setitem__(self, key, val):
        if key not in self._priority:
            self._priority[key] = None
        self._priority[key] = val

        # don't worry about removing from heap - high cost
        # if our heap gets too big, rebuild it from priority dictionary
        if len(self._queue) < 2 * len(self._priority):
            heapq.heappush(self._queue, (val, key))
        else:
            self._rebuild_heap()

    def __getitem__(self, key):
        return self._priority[key]

    def __len__(self):
        return len(self._priority)

    def peek_smallest(self):
        '''Return item with smallest priority.'''
        heap = self._queue
        val, key = heap[0]
        while key not in self._priority or self._priority[key] != val:
            heapq.heappop(heap)
            val, key = heap[0]
        return key

    def pop_smallest(self):
        '''Return item with smallest priority and remove from queue.'''
        heap = self._queue
        val, key = heapq.heappop(heap)
        while key not in self._priority or self._priority[key] != val:
            val, key = heapq.heappop(heap)
        del self._priority[key]
        return key


def bfs_search(initial_state, goal_state):
    to_visit = ToVisitQueue()
    to_visit[initial_state] = 0
    visited = set()
    cost_to_get_to = defaultdict(lambda: float('inf'))
    estimated_total_cost = defaultdict(lambda: float('inf'))
    cost_to_get_to[initial_state] = 0
    estimated_total_cost[initial_state] = initial_state.estimated_distance_from_end

    current = None
    while len(to_visit) > 0:
        print("f(s) of next state is: {}".format(to_visit._priority[to_visit.peek_smallest()]))
        current = to_visit.pop_smallest()
        print(current)
        print("path to get to this state: {}".format(cost_to_get_to[current]))
        if current == goal_state:
            return cost_to_get_to[current]

        visited.add(current)

        for neighbor in current.neighbors():
            if neighbor in visited:
                continue
            tentative_cost = cost_to_get_to[current] + 1
            if cost_to_get_to[neighbor] >= tentative_cost:
                cost_to_get_to[neighbor] = tentative_cost
                to_visit[neighbor] = tentative_cost + neighbor.estimated_distance_from_end
        print(len(to_visit))


if __name__ == "__main__":
    with open(FILENAME) as inputFile:
        print(find_shortest_radioactive_path(line.strip() for line in inputFile))
