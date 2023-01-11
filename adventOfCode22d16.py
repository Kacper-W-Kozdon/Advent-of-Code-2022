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
        
        
    def __preprocess1__(self, test = 0):
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
        self.permutations = list(itertools.permutations(self.nonZeroRate)) if test else 0 #Use lexicographic order and generate one by one the path
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
    
    def prep(self, test = 0):
        self.__preprocess1__(test)
        self.__preprocess2__()
        return self
    
    def __shortest_path__(self, start = "AA", end = "AA", test = 0):
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
            self.toEval[pathIdx] = path + [path[-1]]
            
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
        self.totalFlow = 0
        self.lastFlow = 0
        visited = []
        self.__reset_valves__()
        # print(path)
        iterPath = iter(path)
        valve = iter(order)
        valveToOpen = next(valve)
        # valveToOpen = next(valve)
        visited.append(valveToOpen)
        allOpen = False
        currentStep = "AA"
        # print(path, order)
        for moment in range(self.totalTime):
            
            
            
            try:
                currentStep = path[moment]
                previousStep = path[moment - 1]
                # print(previousStep, currentStep, valveToOpen, self.valvesObj[currentStep].on)
            except:
                pass
            
            if (previousStep == valveToOpen) or allOpen:
                try:   
                    # print(currentStep)
                    # print(self.valvesObj[currentStep].on)
                    # if self.valvesObj[previousStep].on:
                    if previousStep == currentStep and currentStep == valveToOpen and not allOpen:
                        tempFlow += self.valvesObj[currentStep].rate   #This line needs to get changed.
                        # print(tempFlow, self.valvesObj[currentStep].rate)
                    self.valvesObj[currentStep].on = True
                    # print(self.valvesObj[currentStep].on)
                    visited.append(currentStep)
                except:
                    pass
                
            if self.valvesObj[valveToOpen].on:
                try:
                    
                    valveToOpen = next(valve)
                    
                except:
                    allOpen = True
                    
                    
            # print(self.valvesObj["BB"].on)
            self.lastFlow += tempFlow
            self.totalFlow = self.lastFlow
        return self
  
    def total_pressure(self):
        self.flows = []
        for orderIdx, order in enumerate(self.permutations):
            # print(self.toEval)
            path = self.toEval[orderIdx]
            
            self.__calc_flow__(path, order)
            self.flows.append(self.totalFlow)
            # print()
            # print()
        print(max(self.flows))
        if max(self.flows) > self.solution1:
            self.solution1 = max(self.flows)
        return self   
    
    
    def __lex_ord__(self):   #Orders rates lexicographically.
        self.nonZeroRate.sort()
        self.permsFlag = True
        return self
    
    def __permute__(self, listToPermute):
        for idx in range(len(listToPermute) - 1, -1, -1):
            try:
                listToPermute[idx - 1]
            except:
                self.permsFlag = False
                return self.permsFlag
            if listToPermute[idx - 1] < listToPermute[idx]:
                idxToSwap1 = idx - 1
                valToSwap1 = listToPermute[idxToSwap1]
                break
        for idx in range(len(listToPermute) - 1, idxToSwap1, -1):
            if listToPermute[idx] > listToPermute[idxToSwap1]:
                idxToSwap2 = idx
                valToSwap2 = listToPermute[idxToSwap2]
                break
        
        listToPermute[idxToSwap1] = valToSwap2
        listToPermute[idxToSwap2] = valToSwap1
        listToPermute[idxToSwap1 + 1 : ] = listToPermute[ : idxToSwap1 : -1]
        return listToPermute
    
    def __gen_permutations__(self):   #Fill up self.permutations with 1000 new permutations.
        if self.permutations == []:
            self.permutations.append(self.nonZeroRate)
        else:
            while len(self.permutations) < 1000:
                if self.__permute__(self.permutations[-1]):
                    self.permutations.append(self.__permute__(self.permutations[-1]))
                else:
                    break
        return self
    
    def __clean_perms_and_paths__(self):
        while len(self.permutations) > 1:
            self.permutations.pop(0)
        while len(self.toEval) > 0:
            self.toEval.pop(0)
        return self
    
    def total_pressure2(self):  #Use the original function but generate permutations in steps (not all at once).
        self.prep()
        self.__lex_ord__()
        self.permutations = []
        self.solution1 = 0
        while self.permsFlag:
            self.__gen_permutations__()
            self.toEval()
            self.total_pressure()
            self.__clean_perms_and_paths__()
        print(self.solution1)
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
    print("TEST", valves.total_pressure2())
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