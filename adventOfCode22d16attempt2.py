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


def load_files() -> list[list[str]]:

    fContent = []
    with open("input16.txt") as f:
        
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line) and line != "\n":

                fContent.append(line.strip("\n").replace(",", "").replace(";", "").replace("Valve ", "").replace("has flow rate=", "").replace("tunnels lead to valves ", "").split())
    print(f"{fContent[:5]=}")
    return fContent


@dataclass(unsafe_hash=True)
class Valve:
    flow_rate: int
    state: bool
    paths: list[str]


@dataclass
class Flow_State:
    current_valve: str = "AA"
    path_taken: list = field(default_factory=list)
    total_flow: int = 0
    summed_flow: int = 0
    time_elapsed: int = 0

    def update_state(self):
        pass


def load_valves(prep_list: list[list[str]]) -> dict[str, Valve]:
    valves: dict[str, Valve] = OrderedDict()
    for element in prep_list:
        valves[element[0]] = Valve(int(element[1]), state=False, paths=element[2:])

    print(f"{list(valves.keys())[:5]=}")

    return valves


def pair_distance(valves: dict[str, Valve], start_valve_name: str, end_valve_name: str) -> int:
    distance = 1
    next_valves: list[str] = valves[start_valve_name].paths

    while end_valve_name not in next_valves:
        distance += 1
        temp_valves = next_valves.copy()

        for _ in next_valves:
            checking_valve = temp_valves.pop(0)
            temp_valves.extend(valves[checking_valve].paths)

        next_valves = temp_valves

    return distance


def compute_distances(valves: dict[str, Valve]) -> dict[str, int]:

    distances_dict: dict[str, int] = {}
    last_valve = list(valves.keys())[-1]
    num_valves = len(list(valves.keys()))

    for start_valve_name, start_valve in valves.items():
        if start_valve_name == last_valve:
            break

        start_valve_idx = list(valves.keys()).index(start_valve_name)
        for end_valve_idx in range(start_valve_idx + 1, num_valves):
            end_valve_name = list(valves.keys())[end_valve_idx]
            distance = pair_distance(valves, start_valve_name, end_valve_name)
            distances_dict[f"{start_valve_name}:{end_valve_name}"] = distance

    return distances_dict




def main() -> None:
    prep_list = load_files()
    valves = load_valves(prep_list=prep_list)
    non_zero_flow_valves = [valve[0] for valve in valves.items() if valves[valve[0]].flow_rate > 0]
    print(f"{non_zero_flow_valves=}")
    distances_dict = compute_distances(valves)

    state = Flow_State()



if __name__ == "__main__":
    main()