# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 22:05:20 2023

@author: xBubblex
"""

from hashlib import new
import time
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
        self.bestPath = []
        self.distances = {}
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
         #self.permutations = list(itertools.permutations(self.nonZeroRate)) if test else 0 #Use lexicographic order and generate one by one the path
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
        vars().update(myVars)

        # print(myVars)
        # print(myVars["AA"].to)
        # print("AA" in vars().keys())
        # print(vars(self))
        
        return self
    
    def __prep__(self, test = 0):
        self.__preprocess1__(test)
        self.__preprocess2__()
        return self
    
    def __eval_segments__(self):
        for start in self.nonZeroRate:
            for end in self.nonZeroRate:
                self.__shortest_path__(start = start, end = end)
                #if end == "HH" or end == "GG":
                    #print(self.distances)
        return self

    def __shortest_path__(self, start = "AA", end = "AA", test = 0):
        t1 = time.time()
        
        endFound = False
        self.paths = [[start]]
        starts = [start]
        oldPath = []
        nextStarts = starts
        keyFlag = False
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
                    if end == "HH":
                        print("\n\nFound 'HH'\n\n")
                    endFound = True
                    for pathIdx, path in enumerate(self.paths):
                        if end == "HH":
                            print(path)
                        #print(self.distances)
                        if path[-1] == start:
                            oldPath = self.paths.pop(pathIdx)
                            oldPath.append(end)
                            #print(str(oldPath[-1]))
                            #self.paths = oldPath
                            try:
                                #print(self.distances[str(oldPath[0])])
                                self.distances[str(oldPath[0])].update({str(oldPath[-1]): len(oldPath)})
                                #print(self.distances[str(oldPath[0])])

                            except KeyError:
                                self.distances[str(oldPath[0])] = {str(oldPath[-1]): len(oldPath)}
                                #print(self.distances) 
                                
                                             
                            #break
                    
                else:
                    pass
                    #print(myVars[start].to)
                    #print(self.paths)
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
                        if strt not in newPath:
                            newPath[-1] = strt
                            self.paths.append(newPath)
            pass
        # print(self.paths)
        t2 = time.time()
        # print(t2 - t1)
        return self  

    def __eval_path__(self):
        time = self.totalTime
        tempFlow = 0
        totalFlow = 0
        for idx, _ in enumerate(self.nonZeroRate):
            if idx == 0:
                pass
            else:
                stop = self.nonZeroRate[idx]
                #print(stop)
                start = self.nonZeroRate[idx - 1]
                #print(start)
                time += - self.distances[start][stop]
                tempFlow += self.valvesObj[start].rate
                if time >= 0:
                    totalFlow += tempFlow * self.distances[start][stop]
                else:
                    totalFlow += tempFlow * (self.distances[start][stop] - time)
                    break
        if time > 0:
            totalFlow += tempFlow * (time)
        return totalFlow




    #def __gen_permutations__(self):   #Fill up self.permutations with 1000 new permutations.
    #    # i = 1
    #    t1 = time.time()
    #    if self.permutations == []:
    #        # print(self.nonZeroRate)
    #        self.__lex_ord__()
    #        self.permutations.append(self.nonZeroRate)
    #        # print(self.permutations)
    #    if len(self.permutations) > 0:
    #        while len(self.permutations) < self.batchSize:
    #            # i += 1
    #            # print(i)
    #            if self.permsFlag:
    #                listToPermute = self.permutations[-1].copy()
    #                self.__permute__(listToPermute)
                    
    #                # print(len(self.permutations)) if len(self.permutations) % 100 == 0 else 0
    #            else:
    #                break
    #    if type(self.permutations[-1]) == bool:
    #        self.permutations.pop(-1)
    #    # print(self.permutations[0], self.permutations[-1])
    #    # print(len(self.permutations))
    #    # print("//////")
    #    t2 = time.time()
    #    # print(t2 - t1)
    #    return self

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
        #print(listToPermute)
        #self.permutations.append(listToPermute)
        # print(self.permutations[0] != self.permutations[-1])
        # print(self.permutations[-1], len(self.permutations))
        t2 = time.time()
        # print(t2 - t1)
        return self
    
    def __clean_perms_and_paths__(self):
        if len(self.permutations) > 1:
            self.permutations = [self.permutations[-1]]
        if len(self.toEval) > 0:
            self.toEval = []
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

    def get_distances(self):
        self.__prep__()
        self.__clean_perms_and_paths__()
        self.__reset_valves__()
        self.__eval_segments__()
        self.__lex_ord__()

        while(self.permsFlag):
            self.__permute__(listToPermute = self.nonZeroRate)
            self.lastFlow = self.__eval_path__()
            if self.lastFlow > self.totalFlow:
                self.totalFlow = self.lastFlow
                self.bestPath = self.nonZeroRate
        return self

    def test_run(self):
        self.__prep__()
        self.__clean_perms_and_paths__()
        self.__reset_valves__()
        self.__eval_segments__()
        self.__lex_ord__()
        print(self.distances)

        while(self.permsFlag):
            
            self.lastFlow = self.__eval_path__()
            if self.lastFlow > self.totalFlow:
                self.totalFlow = self.lastFlow
                self.bestPath = self.nonZeroRate
                print(self.totalFlow)
            self.__permute__(listToPermute = self.nonZeroRate)
        print(self.distances)
        return self
    
def run():
    valves = Valves()
    #print("TEST", valves.totalTime)
    valves.test_run()

    #print(myVars)
    #print(vars()["valves"].valvesObj)

    print()
    print()


print(run())
    