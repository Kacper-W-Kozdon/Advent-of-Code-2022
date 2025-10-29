from hashlib import new
import math
import time
import re
import numpy as np
import random as rd
import functools as ft
import itertools
from dataclasses import dataclass, field
from typing import Union, OrderedDict
import cython
import time
from functools import wraps


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


@dataclass(unsafe_hash=True)
class Valve:
    name: str
    flow_rate: int
    paths: list[str]
    time_turned_on: int = -1


@dataclass
class Flow_State:
    current_valve: str = "AA"
    paths_taken: list = field(default_factory=list)
    total_flow: int = 0
    summed_flow: int = 0
    time_elapsed: int = 0
    distances_dict: dict[str, int] = field(default_factory=dict)
    flow_valves: list = field(default_factory=list)
    valves: list = field(default_factory=list)
    time_available: int = 30

    def update_state(self):
        return NotImplementedError

    def compute_total_maximum(self) -> Union[int, type]:

        return NotImplementedError


def load_valves(prep_list: list[list[str]], *args, **kwargs) -> dict[str, Valve]:
    valves: dict[str, Valve] = OrderedDict()
    for element in prep_list:
        valves[element[0]] = Valve(element[0], int(element[1]), paths=element[2:])

    print(f"{list(valves.keys())[:5]=}")

    return valves


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
            distances_dict[f"{start_valve_name}:{end_valve_name}"] = distance

    # print(list(distances_dict.items()))
    print(f"{len(list(distances_dict.items()))=}")
    print(f"{len(list(non_zero_flow_valves.items()))=}")
    return distances_dict




def main() -> None:
    prep_list = load_files()
    valves = load_valves(prep_list=prep_list)

    valves_list = list(valves.items())
    valves_num = len(valves_list)
    non_zero_flow_valves = OrderedDict({valve[0]: valve[1] for valve in valves.items() if valves[valve[0]].flow_rate > 0})
    print(f"{non_zero_flow_valves=}")
    distances_dict = compute_distances(valves)

    state = Flow_State(distances_dict=distances_dict)



if __name__ == "__main__":
    main()