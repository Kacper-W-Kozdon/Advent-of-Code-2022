# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 15:31:52 2022

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
    
    '''
    __SHORTEST_PATH__ MIGHT NEED REWRITING FOR SPEED.
    
    '''
    
    
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
    
    '''
    EVAL_PATHS NEED TO BE CHECKED FOR SPEED. UPDATE- PROBLEM IS IN __SHORTEST_PATH__
    
    '''
    
    
    def eval_paths(self):
        # print(self.permutations)
        
        for perm in self.permutations:
            # print(perm)
            permPath = []
            t1 = time.time()
            for valveIdx, valve in enumerate(perm):
                
                # print(valveIdx)
                start = valve
                permPath.append(start)
                if valveIdx == len(perm) - 1:
                    break                
                end = perm[valveIdx + 1]
                t4 = time.time()
                self.__shortest_path__(start, end)
                
                for elem in self.paths:
                    permPath.append(elem)
                t5 = time.time()
            self.toEval.append(permPath)
            del permPath
            t2 = time.time()
        for pathIdx, path in enumerate(self.toEval):
            start = "AA"
            end = path[0]
            self.__shortest_path__(start, end)
            # print(self.paths)
            while len(self.paths) > 0:
                path.insert(0, self.paths.pop(-1))
            self.toEval[pathIdx] = path + [path[-1]]
        t3 = time.time()
        # print(t2 - t1, t3 - t2, t5 - t4)
        # print(self.toEval)    
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
            # print(self.totalFlow)
        return self
  
    def total_pressure(self):
        self.flows = []
        for orderIdx, order in enumerate(self.permutations):
            # print(self.toEval)
            path = self.toEval[orderIdx]
            # print(order)
            # print(self.permutations[orderIdx])
            # print()
            
            self.__calc_flow__(path, order)
            self.flows.append(self.totalFlow)
            # print()
            # print()
        # print(max(self.flows))
        # print((np.array(self.flows) == 1429).astype(int))
        if max(self.flows) > self.solution1:
            self.solution1 = max(self.flows)
        return self   
    
    
    def __lex_ord__(self):   #Orders rates lexicographically.
        self.nonZeroRate.sort()
        self.permsFlag = True
        return self
    
    def __permute__(self, listToPermute = [1, 2, 3, 4]):
        t1 = time.time()
        for idx in range(len(listToPermute) - 1, -1, -1):
            if idx - 1 == -1:
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
        # print(listToPermute)
        self.permutations.append(listToPermute)
        # print(self.permutations[0] != self.permutations[-1])
        # print(self.permutations[-1], len(self.permutations))
        t2 = time.time()
        # print(t2 - t1)
        return self
    
    def __gen_permutations__(self):   #Fill up self.permutations with 1000 new permutations.
        # i = 1
        t1 = time.time()
        if self.permutations == []:
            # print(self.nonZeroRate)
            self.__lex_ord__()
            self.permutations.append(self.nonZeroRate)
            # print(self.permutations)
        if len(self.permutations) > 0:
            while len(self.permutations) < self.batchSize:
                # i += 1
                # print(i)
                if self.permsFlag:
                    listToPermute = self.permutations[-1].copy()
                    self.__permute__(listToPermute)
                    
                    # print(len(self.permutations)) if len(self.permutations) % 100 == 0 else 0
                else:
                    break
        if type(self.permutations[-1]) == bool:
            self.permutations.pop(-1)
        # print(self.permutations[0], self.permutations[-1])
        # print(len(self.permutations))
        # print("//////")
        t2 = time.time()
        # print(t2 - t1)
        return self
    
    def __clean_perms_and_paths__(self):
        if len(self.permutations) > 1:
            self.permutations = [self.permutations[-1]]
        if len(self.toEval) > 0:
            self.toEval = []
        return self
    
    def total_pressure2(self):  #Use the original function but generate permutations in steps (not all at once).
        i = 0
        self.prep()
        self.__lex_ord__()
        self.permutations = []
        self.solution1 = 0
        self.permsFlag = 1
        t0 = time.time()
        t5 = time.time()
        while self.permsFlag:
            print(self.solution1, i, t5 - t0) if not i % 10 else 0
            i += 1
            t1 = time.time()
            self.__gen_permutations__()
            t2 = time.time()
            # print(self.permutations)
            # if self.permsFlag == 0:
            #     break
            # print(len(self.permutations))
            self.eval_paths()                   #EVAL PATHS NEED TO BE CHECKED FOR SPEED
            t3 = time.time()
            self.total_pressure()
            t4 = time.time()
            self.__clean_perms_and_paths__()
            t5 = time.time()
            # print(t2 - t1, t3 - t2, t4 - t3, t5 - t4)
            
        print(self.solution1)
        return self             
  
    
    def test_total_pressure2(self):
        self.prep()
        self.__lex_ord__()
        self.permutations = []
        self.solution1 = 0
        self.permsFlag = 1
        self.__gen_permutations__()
        # print(self.permutations)
        # self.__gen_permutations__()
        # print(self.permutations)
        # while self.permsFlag:
                       
            
        #     # print(self.permutations)
        #     # if self.permsFlag == 0:
        #     #     break
        #     # print(len(self.permutations))
        #     self.eval_paths()
        #     self.total_pressure()
        #     self.__clean_perms_and_paths__()
            
        print(self.solution1)
        return self   
                    
    
    

def run():
    valves = Valves()
    print("TEST", valves.total_pressure2().solution1)
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

'''
Need to look at the test_fun and correct what is returned and at what point permutations are added to the list. Or not- in fact, "while test_fun()" is the missing second call
of the function that was messing with me. Still need to change the "try/except" bit, because the current rule does not break the loop
since idx - 1 == -1 is a valid index.
'''


def test_fun(listToPermute = [1, 2, 3, 4], test = 1):
    print(listToPermute)
    for idx in range(len(listToPermute) - 1, -1, -1):
        if idx - 1 == -1:
            test = 0
            return test
        
        
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
    # print(listToPermute)
    return listToPermute

def test_fun_run():
    i = 1
    test = 1
    while test_fun():
        i += 1
        print(i)
        
        
# test_fun_run()