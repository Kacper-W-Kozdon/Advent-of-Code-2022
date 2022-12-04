# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 20:49:55 2022

@author: xBubblex
"""

import numpy as np
import re
import time
import unicodedata
from sympy.combinatorics.partitions import Partition
from sympy.combinatorics.permutations import Permutation


def load_files():
    fContent = []
    with open("input4.txt") as f:
            for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
                if bool(line.strip("\n").split()):
                    # print(line.strip("\n").split("|"))
                    fContent.append(re.split("-|,", line.strip("\n")))  #splitting each entry into coordinates
    return(fContent)
# print(load_files())

class Cleanup:
    def __init__(self):
        self.ids = load_files()
        self.sections = []
        self.overlaps = []
        self.log = []
        
    def assign_sections(self):
        for idN in self.ids:
            pair1 = "".join([str(num) for num in range(int(idN[0]), int(idN[1]) + 1)])
            pair2 = "".join([str(num) for num in range(int(idN[2]), int(idN[3]) + 1)])
            self.sections.append([pair1, pair2])
        return self
    
    def find_full_overlaps(self):
        self.log = []
        self.overlaps = []
        overlapsFilled = len(self.overlaps) > 0
        for pairIdx, pair in enumerate(self.ids):
            overlap = False
            self.log.append([pair, pair[0] <= pair[2] and pair[1] >= pair[3], pair[0] >= pair[2] and pair[1] <= pair[3], (pair[0] <= pair[2] and pair[1] >= pair[3]) or (pair[0] >= pair[2] and pair[1] <= pair[3])])
            if (int(pair[0]) <= int(pair[2]) and int(pair[1]) >= int(pair[3])) or (int(pair[0]) >= int(pair[2]) and int(pair[1]) <= int(pair[3])):
    
                overlap = True
            if not overlapsFilled:
                self.overlaps.append(int(overlap))   
            else:
                self.overlaps[pairIdx] = int(overlap)
            if len(pair) < 3:
                self.sections[pairIdx].append("overlap: " + str(min(float(pair[1]), float(pair[0]))) if overlap else "no overlap")
        return self
    
    def find_all_overlaps(self):
        if len(self.log) == 0:
            self.find_full_overlaps()
        for pairIdx, pair in enumerate(self.ids):
            if self.overlaps[pairIdx] == 0:
                condition1 = int(pair[0]) in range(int(pair[2]), int(pair[3]) + 1)
                condition2 = int(pair[1]) in range(int(pair[2]), int(pair[3]) + 1)
                condition3 = int(pair[2]) in range(int(pair[0]), int(pair[1]) + 1)
                condition4 = int(pair[3]) in range(int(pair[0]), int(pair[1]) + 1)
                conditions = [condition1, condition2, condition3, condition4]
                if True in conditions:
                    self.overlaps[pairIdx] = 1
        return self
                    
    def count_overlaps(self):
        return sum(self.overlaps)
        
def run():
    cleaning = Cleanup()
    print(cleaning.assign_sections().find_all_overlaps().count_overlaps())
    
print(run())