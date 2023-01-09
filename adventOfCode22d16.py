# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 15:31:52 2022

@author: xBubblex
"""

import re
import numpy as np
import random as rd
import functools as ft
import itertools


def load_files():
    fContent = []
    with open("inputtest.txt") as f:
        
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
    def __init__(self):
        super().__init__()
        self.raw = load_files()
        self.valves = []
        # self.valvesObj = []
        self.valvesObj = {}
        self.nonZeroRate = []
        self.permutations = []
        self.paths = []
        self.toEval = []
        self.totalTime = 29
        self.flows = []
        self.lastFlow = 0
        
        
    def __preprocess1__(self):
        self.nonZeroRate = []
        self.valves = []
        for line in self.raw:
            valveStart = line.index(" ") + 1
            # print(valveStart, line[valveStart + 1 : ].index(" ") )           
            valveStop = line.index("has") - 1            
            # print(line[valveStart : valveStop], valveStart, valveStop, line[valveStart : valveStop])            
            rateStart = line.index("=") + 1
            rateStop = line.index(";")             
            # print(rateStart, rateStop)
            tempLine = line[rateStop : ]
            # print(tempLine)
            valves = tempLine.index("valve") + len("valve") + 1 + (1 if line[line.index("valve") +  len("valve")] == "s" else 0)
            # print(tempLine[valves : ])
            valves = tempLine[valves : ]
            self.valves += [[line[valveStart : valveStop], int(line[rateStart : rateStop]), valves.split(", ")]]
            if int(line[rateStart : rateStop]) > 0 and [line[valveStart : valveStop]] != "AA":
                self.nonZeroRate += [line[valveStart : valveStop]]  
        # print(self.nonZeroRate)
        self.permutations = list(itertools.permutations(self.nonZeroRate))
        # print(self.permutations)
        return self
    
    
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
    
    def prep(self):
        self.__preprocess1__()
        self.__preprocess2__()
        return self
    
    def __shortest_path__(self, start = "AA", end = "AA"):
        endFound = False
        self.paths = [[start]]
        starts = [start]
        oldPath = []
        nextStarts = starts
        # print(myVars)
        while not endFound:   
            starts = nextStarts
            del nextStarts
            nextStarts = []
            for start in starts:
                pass
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
                    nextStarts += myVars[start].to
                    for pathIdx, path in enumerate(self.paths):
                        if path[-1] == start:
                            oldPath = self.paths.pop(pathIdx)
                            oldPath += ["TEMP"]
                            break
                    for strt in myVars[start].to:
                        newPath = oldPath.copy()
                        newPath[-1] = strt
                        self.paths.append(newPath)
            pass
            
        return self  
    
    def eval_paths(self):
        # print(self.permutations)
        for perm in self.permutations:
            # print(perm)
            permPath = []
            for valveIdx, valve in enumerate(perm):
                start = valve
                permPath.append(start)
                if valveIdx == len(perm) - 1:
                    break                
                end = perm[valveIdx + 1]
                self.__shortest_path__(start, end)
                for elem in self.paths:
                    permPath.append(elem)
                
            self.toEval.append(permPath)
            del permPath
            
        for pathIdx, path in enumerate(self.toEval):
            start = "AA"
            end = path[0]
            self.__shortest_path__(start, end)
            # print(self.paths)
            while len(self.paths) > 0:
                path.insert(0, self.paths.pop(-1))
            self.toEval[pathIdx] = path
            
        return self
    
    
    
    '''
    Need to: count total time all valves are open and the count the flow for the period the valves are getting opened
    
    '''
    
    def __reset_valves__(self):
        for valve in self.valvesObj:
            # print("VALVE", valve)
            self.valvesObj[valve].on = False
        return self
    
                    
    def __calc_flow__(self, path, order):
        tempFlow = 0
        self.lastFlow = 0
        self.__reset_valves__()
        
        iterPath = iter(path)
        valve = iter(order)
        valveToOpen = next(valve)
        allOpen = False
        currentStep = "AA"
        
        for moment in range(self.totalTime):
            if self.valvesObj[valveToOpen].on:
                try:
                    valveToOpen = next(valve)
                except:
                    allOpen = True
            
            try:
                currentStep = path[moment]
            except:
                pass
            
            if currentStep == valveToOpen or allOpen:
                try:                
                    if self.valvesObj[currentStep].on:
                        tempFlow += self.valvesObj[currentStep].rate
                    self.valvesObj[currentStep].on = True
                except:
                    pass
            
            self.lastFlow += tempFlow
        return self
  
    def total_pressure(self):
        self.flows = []
        for orderIdx, order in enumerate(self.permutations):
            # print(self.toEval)
            path = self.toEval[orderIdx]
            
            self.__calc_flow__(path, order)
            self.flows.append(self.lastFlow)
        print(max(self.flows))
        return self                
  
    
    def test_meth(self):
        # print(self.permutations)
        for perm in self.permutations:
            # print(perm)
            permPath = []
            for valveIdx, valve in enumerate(perm):
                start = valve
                permPath.append(start)
                if valveIdx == len(perm) - 1:
                    break                
                end = perm[valveIdx + 1]
                self.__shortest_path__(start, end)
                for elem in self.paths:
                    permPath.append(elem)
                
            self.toEval.append(permPath)
            del permPath
            
        for pathIdx, path in enumerate(self.toEval):
            start = "AA"
            end = path[0]
            self.__shortest_path__(start, end)
            # print(self.paths)
            while len(self.paths) > 0:
                path.insert(0, self.paths.pop(-1))
            self.toEval[pathIdx] = path
            
        return self
                    
    
    

def run():
    valves = Valves()
    print("TEST", valves.prep().eval_paths().total_pressure())
    # print(valves.permutations)
    print()
    print()
    # print([var for var in vars()["valves"].valvesObj])
    # print(vars()["valves"].valvesObj["AA"].name)
    # print([item for item in locals().items()])
    print()
    print()
    # print(vars(valves)["valvesObj"])
    # print()
    # print(vars())
    
    
print(run())

a = "strings string"
print(a[a.index(" ") : ])
b = list(itertools.permutations([1, 2, 3]))
print(b)
c = iter(a)
next(c)
d = next(c)
print(next(c), next(c), d)