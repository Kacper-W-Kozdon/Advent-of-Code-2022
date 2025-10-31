from hashlib import new
import math
import time
import re
import numpy as np
import random as rd
import functools as ft
import itertools
from dataclasses import dataclass, field
from typing import Union, OrderedDict, Mapping, Collection, Iterable, Dict, TypedDict
import cython
import time
from functools import wraps
import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def timer(func):

    @wraps(wrapped=func)
    def wrapped(*args, **kwargs):
        start_time = time.perf_counter()
        ret = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time

        print(f"{func.__name__=}; {duration=}")

        return ret
    return wrapped


def load_files() -> list[list[str]]:

    fContent = []
    with open("input16.txt") as f:
        
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line) and line != "\n":

                fContent.append(line.strip("\n").replace(",", "").replace(";", "").replace("Valve ", "").replace("has flow rate=", "").replace("tunnels lead to valves ", "").replace("tunnel leads to valve ", "").split())
    print(f"{fContent[:5]=}")
    return fContent


class Graph(TypedDict):
    distances: dict[str, int]
    weights: dict[str, list[int]]


@dataclass(unsafe_hash=True)
class Valve:
    name: str
    flow_rate: int
    paths: list[str]
    graph: Graph
    time_turned_on: int = -1


def compute_test_value(total_flow: int, time_remaining: int, flow_valves: list[Valve], path: list[Valve]) -> dict[str, int]:
    
    available_valves = [valve for valve in flow_valves if valve not in path]
    
    for test_valve in available_valves:

        test_value = (time_remaining - 1) * (total_flow + test_valve.flow_rate)

    raise NotImplementedError


@dataclass
class Flow_State:
    current_valve: str = "AA"
    best_path: list[str] = field(default_factory=list)
    best_total_flow: int = 0
    distances_dict: dict[str, int] = field(default_factory=dict)
    flow_valves: list[str] = field(default_factory=list)
    valves: OrderedDict[str, Valve] = field(default_factory=OrderedDict)
    time_available: int = 30
    cache: list[str] = field(default_factory=list)

    def update_state(self, num_updates: int = 100):

        for _ in range(num_updates):
            path = select_path(self.valves, self.flow_valves)
            path_flow = eval_path(path, self.valves, self.time_available)
            if path_flow > self.best_total_flow:
                self.best_total_flow = path_flow
                self.best_path = path

        return NotImplementedError

    def __post_init__(self):
        self.flow_valves = [valve[0] for valve in self.valves.items() if getattr(valve[1], "flow_rate") > 0]
        self.distances_dict = compute_distances(self.valves)
        

def select_path(valves, flow_valves) -> list[str]:

    remaining_valves: list[str] = []
    scaled_weights: list[float] = []
    selected_path = random.choices(remaining_valves, scaled_weights)
    raise NotImplementedError

    return selected_path


def eval_path(path: list[str], valves: dict[str, Valve], time_available: int) -> int:
    total_flow: int = 0
    time_elapsed: int = 0
    turning_on_time: int | list[int] = 1

    for valve in path:
        next_valve_index = path.index(valve) + 1
        if next_valve_index == len(path):
            break

        next_valve = path[next_valve_index]
                
        distances: dict[str, int] = valves[valve].graph["distances"]
        time_elapsed += distances[next_valve] + turning_on_time
        time_remaining = time_available - time_elapsed
        if time_remaining < 0:
            break

        total_flow += time_remaining * valves[valve].flow_rate

    return total_flow


def load_valves(prep_list: list[list[str]], *args, **kwargs) -> dict[str, Valve]:
    valves: dict[str, Valve] = OrderedDict()
    for element in prep_list:
        valves[element[0]] = Valve(element[0], int(element[1]), paths=element[2:], graph=Graph({"distances": {}, "weights": {}}))

    print(f"{list(valves.keys())[:5]=}")

    return valves


def graph_valves(valves: dict[str, Valve]) -> None:
    non_zero_flow_valves: OrderedDict[str, Valve] = OrderedDict([valve for valve in valves.items() if getattr(valve[1], "flow_rate") > 0])
    num_flow_valves = len(non_zero_flow_valves)
    distances_dict = compute_distances(valves)
    for valve in non_zero_flow_valves.values():
        graph = OrderedDict({path: {"distances": distances_dict[f"{valve.name}:{path}"], "weights": [1 for _ in range(num_flow_valves)]} for path in non_zero_flow_valves.keys() if path != valve.name})
        setattr(valve, "graph", graph)

    print(f"{list(non_zero_flow_valves.values())[0]=}")


# @timer
def pair_distance(valves: dict[str, Valve], start_valve_name: str, end_valve_name: str, *args, **kwargs) -> int:
    distance = 1
    next_valves: list[str] = valves[start_valve_name].paths
    valves_visited: list[str] = []

    while end_valve_name not in next_valves:
        distance += 1

        for valve in next_valves:
            if valve in valves_visited:
                next_valves.pop(next_valves.index(valve))
            else:
                valves_visited.append(valve)

        temp_valves = next_valves.copy()

        for _ in next_valves:
            checking_valve = temp_valves.pop(0)
            temp_valves.extend(valves[checking_valve].paths)

        next_valves = temp_valves

    return distance


# @cython.locals(n=cython.int)
@timer
def compute_distances(valves: dict[str, Valve], *args, **kwargs) -> dict[str, int]:

    distances_dict: dict[str, int] = {}
    last_valve = list(valves.keys())[-1]
    num_valves = len(list(valves.keys()))
    non_zero_flow_valves = OrderedDict({valve[0]: valve[1] for valve in valves.items() if valves[valve[0]].flow_rate > 0})
    non_zero_flow_valves["AA"] = valves["AA"]

    for start_valve_name, start_valve in non_zero_flow_valves.items():
        if start_valve_name == last_valve:
            break

        start_valve_idx = list(valves.keys()).index(start_valve_name)
        for end_valve_idx in range(start_valve_idx + 1, num_valves):
            end_valve_name = list(valves.keys())[end_valve_idx]
            distance = pair_distance(valves, start_valve_name, end_valve_name)
            distances_dict[f"{start_valve_name}:{end_valve_name}"], distances_dict[f"{end_valve_name}:{start_valve_name}"] = distance, distance

    # print(list(distances_dict.items()))
    print(f"{len(list(distances_dict.items()))=}")
    print(f"{len(list(non_zero_flow_valves.items()))=}")
    return distances_dict


def main() -> None:
    prep_list = load_files()
    valves = load_valves(prep_list=prep_list)
    graph_valves(valves)

    valves_list = list(valves.items())
    valves_num = len(valves_list)

    state = Flow_State(valves=valves)



if __name__ == "__main__":
    main()