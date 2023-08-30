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
        self.shortestPaths = {}
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
        self.nonZeroRate.append("AA")
        for start in self.nonZeroRate:
            for end in self.nonZeroRate:
                self.__shortest_path__(start = start, end = end)
                #if end == "HH" or end == "GG":
                    #print(self.distances)
        self.nonZeroRate.pop()
        return self

    def __shortest_path__(self, start = "AA", end = "AA", test = 0):
        t1 = time.time()
        
        endFound = False
        self.paths = [[start]]
        starts = [start]
        inputStart = start
        oldPath = []
        nextStarts = starts
        keyFlag = False
        # print(len(starts))
        # print(myVars)
        if start == end:
            endFound = True
            oldPath = [start]
            try:
                #print(self.distances[str(oldPath[0])])
                self.distances[str(oldPath[0])].update({str(oldPath[-1]): len(oldPath)})
                self.shortestPaths[str(oldPath[0])].update({str(oldPath[-1]): oldPath})
                #print(self.distances[str(oldPath[0])])

            except KeyError:
                self.distances[str(oldPath[0])] = {str(oldPath[-1]): len(oldPath)}
                self.shortestPaths[str(oldPath[0])] = {str(oldPath[-1]): oldPath}
                #print(self.distances) 
                                
        while not endFound:   
            starts = nextStarts
            del nextStarts
            nextStarts = []
            #print(starts)
            # print(len(starts))   # <----- PROBLEM!
            for start in starts:
                #print(start)
                
                pass
                # print(starts)
                if end in myVars[start].to:
                    #if end == "HH" and inputStart == "BB":
                        #print("\n\nFound 'HH'\n\n")
                    endFound = True
                    for pathIdx, path in enumerate(self.paths):
                        
                        #print(self.distances)
                        if path[-1] == start:
                            oldPath = self.paths.pop(pathIdx)
                            oldPath.append(end)
                            #if end == "HH" and inputStart == "BB":
                                #print("path: ", path)
                            #print(str(oldPath[-1]))
                            #self.paths = oldPath
                            try:
                                #print(self.distances[str(oldPath[0])])
                                self.distances[str(oldPath[0])].update({str(oldPath[-1]): len(oldPath)})
                                self.shortestPaths[str(oldPath[0])].update({str(oldPath[-1]): oldPath})
                                #if end == "HH" and inputStart == "BB":
                                    #print(self.distances[str(oldPath[0])])

                            except KeyError:
                                self.distances[str(oldPath[0])] = {str(oldPath[-1]): len(oldPath)}
                                self.shortestPaths[str(oldPath[0])] = {str(oldPath[-1]): oldPath}
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
                    paths = self.paths
                    for pathIdx, path in enumerate(self.paths):   # <----- THIS PROBABLY CAN BE DONE MUCH BETTER.
                        
                        if path[-1] == start:
                            
                            
                            if any([strt not in path for strt in myVars[start].to]):
                                oldPath = paths.pop(pathIdx)
                                oldPath += ["TEMP"]
                                #print("\n\n\n")
                                for strt in myVars[start].to:
                                    if strt not in oldPath:
                                        newPath = oldPath.copy()
                                        newPath[-1] = strt
                                        paths.append(newPath)
                                        #print(newPath, strt)
                                #print("p1: ", paths)
                            
                    self.paths = paths
                    #print(inputStart, end, self.paths, "\n")
                        
                        
            pass
        # print(self.paths)
        t2 = time.time()
        # print(t2 - t1)
        return self  

    def __eval_path__(self, k = 0):
        time = self.totalTime
        tempFlow = 0
        totalFlow = 0
        start = "AA"
        stop = "AA"
        if not k:
            for idx, _ in enumerate(self.nonZeroRate):
         
                if idx == 0: 
                    start = "AA"
                    stop = self.nonZeroRate[idx]
                    tempFlow = self.valvesObj[start].rate
                    totalFlow += tempFlow * time
                    time += - (self.distances[start][stop])
                

                else:
                    tempFlow = self.valvesObj[stop].rate
                    start = self.nonZeroRate[idx - 1]
                    stop = self.nonZeroRate[idx]
                         

                
                    if time > 0:
                        totalFlow += tempFlow * time 
                    else:
                        totalFlow += tempFlow * (time + (self.distances[start][stop]))

                    time += - (self.distances[start][stop])
    
        
            if time > 0:
                start = self.nonZeroRate[-1]
                tempFlow = self.valvesObj[start].rate
                totalFlow += tempFlow * time
        
        if k == "rate":
            #Start with self.nonZeroRate ordered by rates (decreasing), on each segment:
            #1. check if any([valve in segment for valve in self.nonZeroRate])
            #2. if point 1 is True, for each such valve check if (time - self.distances[start][valve]) * self.valvesObj[valve].rate > (time - self.distances[start][stop]) * self.valvesObj[stop].rate
            #3. if yes, insert valve as the new stop and repeat.
            nonZeroRate = self.nonZeroRate
            switchedValves = []
            
            for idx, valve in enumerate(self.nonZeroRate):

                if idx == 0:
                    start = "AA"
                else:
                    start = self.nonZeroRate[idx - 1]
                stop = self.nonZeroRate[idx]
                pathSegment, bestResult, time = self.__find_opt__(self, start, stop, time)
                totalFlow += bestResult
                for valve in pathSegment:
                    if valve not in switchedValves:
                        switchedValves.append(valve)
                        nonZeroRate.pop(nonZeroRate.index(valve))
                        nonZeroRate.insert(nonZeroRate.index(stop), valve)
                switchedValves.append(stop)

            self.nonZeroRate = nonZeroRate
            if time > 0:
                start = self.nonZeroRate[-1]
                tempFlow = self.valvesObj[start].rate
                totalFlow += tempFlow * time
                
                    
            pass

        return totalFlow


    def __find_opt__(self, start, stop, time):
        #Need to try something similar but for the entire path: collect the nodes passed on the ordered way, then find all permutations of those extra nodes.

        remainingTime = time
        bestResult = 0
        flows = []
        pathSegment = []
        path = self.shortestPaths[start][stop]
        candidates = [valve in self.shortestPaths[start][stop] for valve in self.nonZeroRate]
        candidates.pop(candidates.index(start))
        candidates.pop(candidates.index(stop))
        numValves = sum(candidates) - 2
        if numValves > 0:
            valvesSequences = itertools.combinations_with_replacement([0, 1], numValves)

            for sequence in valvesSequences:
                flow = 0
                for idxValve, valve in enumerate(candidates):
                    remainingTime += -(path.index(valve) + sequence[idxValve])
                    flow += remainingTime * sequence[idxValve] * self.valvesObs[valve].rate
                remainingTime = time - sum([sequence]) - len(path)
                flow += remainingTime * self.valvesObj[stop].rate
                flows.append(flow)

                
                pass
            if flows:
                bestResult = max(flows)
                idxBest = flows.index(bestResult)
                sequence = valvesSequences[idxBest]
                for idxValve, valve in enumerate(sequence):
                    if valve:
                        pathSegment.append(candidates[idxValve])

            remainingTime += - self.distances[start][stop] - len(pathSegment) 

        return pathSegment, bestResult, remainingTime

        pass

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
    
    def __lex_ord__(self, k = 0):   #Orders rates lexicographically.
        if not k:
            self.nonZeroRate.sort()
            self.permsFlag = True
        if k == "rate":
            self.nonZeroRate.sort(key = lambda x: self.valvesObj[x].rate)
            foo = self.nonZeroRate[ : : -1]
            self.nonZeroRate = foo
        return self

    def get_distances(self):
        self.__prep__()
        self.__clean_perms_and_paths__()
        self.__reset_valves__()
        self.__eval_segments__()
        print(self.distances)
        print()
        print()
        print(self.shortestPaths)
        self.__lex_ord__()
        idx = 0
        total = np.math.factorial(len(self.nonZeroRate))
        #print(self.distances)
        t1 = time.time()
        while(self.permsFlag):
            
            self.lastFlow = self.__eval_path__()
            idx += 1
            t2 = time.time()
            if t2 - t1 >= 30:
                print(idx/total)
                t1 = t2
            if self.lastFlow > self.totalFlow:
                self.totalFlow = self.lastFlow
                self.bestPath = self.nonZeroRate
                #print(self.totalFlow)
            self.__permute__(listToPermute = self.nonZeroRate)
        self.solution1 = self.totalFlow
        print("Total flow: ", self.solution1)
        return self

    def get_distances2(self):
        self.__prep__()
        self.__clean_perms_and_paths__()
        self.__reset_valves__()
        self.__eval_segments__()
        print(self.distances)
        print()
        print()
        print(self.shortestPaths)
        self.__lex_ord__(k = "rate")
        
        #print(self.distances)
        
        
            
        self.lastFlow = self.__eval_path__(k = "rate")
            
        self.solution1 = self.totalFlow
        print("Total flow: ", self.solution1)
        return self
    


    
def run():
    valves = Valves()
    #print("TEST", valves.totalTime)
    valves.get_distances1()

    #print(myVars)
    #print(vars()["valves"].valvesObj)

    print()
    print()


print(run())
    