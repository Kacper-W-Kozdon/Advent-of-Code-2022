# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 12:53:29 2022

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
    with open("input3.txt") as f:
            for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
                if bool(line.strip("\n").split()):
                    # print(line.strip("\n").split("|"))
                    fContent.append(line.strip("\n").split(" | ")[0])  #splitting each entry into coordinates
    return(fContent)
# print(load_files())

class Rucksacks:
    def __init__(self):
        self.load = []
        self.priorities = [priority + 1 for priority in range(52)]
        self.items = [chr(ord("a") + uni) for uni in range(26)] + [chr(ord("A") + uni) for uni in range(26)]
        self.listDict = {}
        self.suspiciousItems = []
        self.log = []
        pass
    
    def loader(self):
        self.load = load_files()
        for (backpack, item) in enumerate(self.load):
            load_compartments = lambda item: (item[:int((len(item)/2))], item[(int(len(item)/2)):])
            self.load[backpack] = load_compartments(item)
        return self
    
    def inspect(self, backpack = 0):
        return self.load[backpack]
    
    def make_list(self):
        for (item, priority) in zip(self.items, self.priorities):
            self.listDict[item] = priority
        return self
    
    def recheck_rucksacks(self):
        self.suspiciousItems = []
        self.log = []
        for compartmentIdx, compartments in enumerate(self.load):
            appended = False
            for item1 in compartments[0]:       
                for item2 in compartments[1]:
                    if item1 == item2 and not appended:
                        self.log.append(["Compartment" + str(compartmentIdx), compartments, "item: ", item1, self.listDict[item1]])
                        self.suspiciousItems.append(item1)
                        appended = True

        return self
    
    def authenticate(self):
        self.suspiciousItems = []
        self.log = []
        group = []
        groupFull = False
        for bpIndex, backpack in enumerate(self.load):            
            badgeFound = False
            group.append(backpack[0] + backpack[1])
            if len(group) == 3:
                groupFull = True                
                self.log.append(["groupNo: ", bpIndex//3, "groupFull: ", groupFull, "group members: ", [group[0], group[1], [group[2]]]])
                for item in group[0]:                    
                    if not badgeFound:                        
                        if item in group[1] and item in group[2]:
                            badgeFound = True
                            self.log.append(["badge found: ", badgeFound, "badge: ", item])
                            self.suspiciousItems.append(item)                                         
                            groupFull = False
                            group = []                                        
            
        return self
    
    
    def translate_to_priorities(self):
        for (index, item) in enumerate(self.suspiciousItems):
            self.suspiciousItems[index] = self.listDict[item]
        return self
        
def run():
    elfBps = Rucksacks()
    print(elfBps.loader().make_list().recheck_rucksacks().translate_to_priorities().suspiciousItems)
    sumOfSusItems = sum(elfBps.loader().make_list().recheck_rucksacks().translate_to_priorities().suspiciousItems)
    # print(elfBps.log)
    print(elfBps.loader().make_list().authenticate().translate_to_priorities().suspiciousItems)
    sumOfBadges = sum(elfBps.loader().make_list().authenticate().translate_to_priorities().suspiciousItems)
    # print(elfBps.log)
    return sumOfSusItems, sumOfBadges

print(run())