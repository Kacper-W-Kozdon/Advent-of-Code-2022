from hashlib import new
import math
import time
import re
import numpy as np
import random as rd
import functools as ft
import itertools
from dataclasses import dataclass, field


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


def load_valves(prep_list: list[list[str]]) -> dict[str, Valve]:
    valves: dict[str, Valve] = {}
    for element in prep_list:
        valves[element[0]] = Valve(int(element[1]), state=False, paths=element[2:])

    print(f"{list(valves.keys())[:5]=}")

    return valves



def main() -> None:
    prep_list = load_files()
    valves = load_valves(prep_list=prep_list)



if __name__ == "__main__":
    main()