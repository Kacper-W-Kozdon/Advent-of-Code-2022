# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 22:05:20 2023

@author: xBubblex
"""

import time
import re
import numpy as np
import random as rd
import functools as ft
import itertools


def load_files():
    fContent = []
    with open("input16.txt") as f:
        
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line) and line != "\n":
                fContent.append(line.strip("\n"))

    return(fContent)

# print(load_files())


class Valve():
    def __init__(self):
        self.name = ""
        self.from_ = []
        self.to = []
        self.rate = 0
        self.on = False 


class Valves(Valve):
    def __init__(self, test = 0):
        super().__init__()
        self.raw = load_files()
        self.valves = []
        # self.valvesObj = []
        self.valvesObj = {}
        self.nonZeroRate = []
        self.permutations = []
        self.paths = []
        self.toEval = []
        self.totalTime = 30
        self.flows = []
        self.lastFlow = 0
        self.totalFlow = 0
        self.solution1 = 0
        self.permsFlag = True
        self.batchSize = 2**10
        
        
    # def __preprocess1__(self, test = 0):
    #     self.nonZeroRate = []
    #     self.valves = []
    #     for line in self.raw:
    #         valveStart = line.index(" ") + 1
    #         # print(valveStart, line[valveStart + 1 : ].index(" ") )           
    #         valveStop = line.index("has") - 1            
    #         # print(line[valveStart : valveStop], valveStart, valveStop, line[valveStart : valveStop])            
    #         rateStart = line.index("=") + 1
    #         rateStop = line.index(";")             
    #         # print(rateStart, rateStop)
    #         tempLine = line[rateStop : ]
    #         # print(tempLine)
    #         valves = tempLine.index("valve") + len("valve") + 1 + (1 if line[line.index("valve") +  len("valve")] == "s" else 0)
    #         # print(tempLine[valves : ])
    #         valves = tempLine[valves : ]
    #         self.valves += [[line[valveStart : valveStop], int(line[rateStart : rateStop]), valves.split(", ")]]
    #         if int(line[rateStart : rateStop]) > 0 and [line[valveStart : valveStop]] != "AA":
    #             self.nonZeroRate += [line[valveStart : valveStop]]  
    #     # print(self.nonZeroRate)
    #     self.permutations = list(itertools.permutations(self.nonZeroRate)) if test else 0 #Use lexicographic order and generate one by one the path
    #     # print(self.permutations)
    #     return self
    
    
    def __preprocess2__(self):
        global myVars
        myVars = vars()
        # self.valvesObj = []
        self.valvesObj = {}
        for valve in self.valves:
            myVars.__setitem__(valve[0], Valve())
            myVars[valve[0]].name = valve[0]            
            myVars[valve[0]].to = valve[2]
            myVars[valve[0]].rate = valve[1]
            myVars[valve[0]].from_ = []
            for val in self.valves:
                if valve[0] in val[2]:
                    myVars[valve[0]].from_.append(val[0])
            # print(myVars[valve[0]].from_)
            del val
            # self.valvesObj.append(myVars[valve[0]])
            self.valvesObj[valve[0]] = myVars[valve[0]]
        
        # print(myVars)
        # print(myVars["AA"].to)
        # print("AA" in vars().keys())
        # print(vars(self))
        
        return self
    
    def prep(self, test = 0):
        # self.__preprocess1__(test)
        self.__preprocess2__()
        return self
    
    def __shortest_path__(self, start = "AA", end = "AA", test = 0):
        t1 = time.time()
        
        endFound = False
        self.paths = [[start]]
        starts = [start]
        oldPath = []
        nextStarts = starts
        # print(len(starts))
        # print(myVars)
        while not endFound:   
            starts = nextStarts
            del nextStarts
            nextStarts = []
            # print(len(starts))   # <----- PROBLEM!
            for start in starts:
                
                pass
                # print(starts)
                if end in myVars[start].to:
                    endFound = True
                    for pathIdx, path in enumerate(self.paths):
                        if path[-1] == start:
                            oldPath = self.paths.pop(pathIdx)
                            self.paths = oldPath
                            break
                    break
                else:
                    pass
                    # print(myVars[start].to)
                    for elem in myVars[start].to:
                        # print(elem)
                        if elem not in nextStarts:
                            nextStarts += [elem]
                    # print(len(nextStarts))
                    for pathIdx, path in enumerate(self.paths):   # <----- THIS PROBABLY CAN BE DONE MUCH BETTER.
                        if path[-1] == start:
                            oldPath = self.paths.pop(pathIdx)
                            oldPath += ["TEMP"]
                            break
                    for strt in myVars[start].to:
                        newPath = oldPath.copy()
                        newPath[-1] = strt
                        self.paths.append(newPath)
            pass
        # print(self.paths)
        t2 = time.time()
        # print(t2 - t1)
        return self  
    
    def __reset_valves__(self):
        for valve in self.valvesObj:
            # print("VALVE", valve)
            self.valvesObj[valve].on = False
        return self
    
    def __lex_ord__(self):   #Orders rates lexicographically.
        self.nonZeroRate.sort()
        self.permsFlag = True
        return self
    
    