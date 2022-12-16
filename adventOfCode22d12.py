# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 14:32:58 2022

@author: xBubblex
"""

import re
import numpy as np
import random as rd
import functools as ft

def load_files():
    fContent = []
    with open("inputtest.txt") as f:
        
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line):
                fContent.append(list(line.strip("\n")))

    return(fContent)

print(np.array(load_files()).shape)




class Map():
    def __init__(self):
        rd.seed()
        self.raw = np.array(load_files())
        self.map = self.raw.copy()
        self.mapWBorders = np.array(load_files())
        self.entrances = np.zeros(self.map.shape, dtype = object)
        self.exits = np.zeros(self.map.shape, dtype = object)
        self.enex = np.zeros(self.map.shape, dtype = object)
        self.startStop = []
        self.longestWalkL = self.map.shape[0] * self.map.shape[1]
        self.pathLimit = self.longestWalkL
        self.relH = np.zeros(self.map.shape, dtype = object)
        self.walks = []
        self.deadEnds = list([])
        self.shortest = 0
        self.visited = set([])
        self.shortestW = []
        self.shortestWDirs = []
        
    

    

    def __set_start_stop(self):
        while len(self.startStop) > 0:
            self.startStop.pop()
        self.startStop.append(np.where(self.map == "S"))
        self.startStop.append(np.where(self.map == "E"))

        self.map[self.startStop[0]] = "a"
        self.map[self.startStop[1]] = "z"
        self.pathLimit = ord("z") + 1 - ord("a")
        print(self.map.shape)
        print(len([inf for i in range((self.map.shape[0] + 2) * (self.map.shape[1] + 2))]))
        
        self.mapWBorders = np.array([float(inf) for i in range((self.map.shape[0] + 2) * (self.map.shape[1] + 2))]).reshape((self.map.shape[0] + 2, -1))
        
        self.map = np.array([ord(height) for height in self.map.flatten()]).reshape(self.map.shape)
        
                
        self.mapWBorders[1 : -1, 1 : -1] = self.map
        
        return self
    
    def __rel_heights(self):
        print(self.map)
        print(self.mapWBorders[1 : -1,  : -2])
        l = self.map - self.mapWBorders[1 : -1,  : -2]
        r = self.map - self.mapWBorders[1 : -1, 2 : ]
        u = self.map - self.mapWBorders[ : -2, 1 : -1]
        d = self.map - self.mapWBorders[2 : , 1 : -1]
        for rowIdx, row in enumerate(self.map):
            for colIdx, col in enumerate(row):
                self.relH[rowIdx, colIdx] = [r[rowIdx, colIdx], d[rowIdx, colIdx], l[rowIdx, colIdx], u[rowIdx, colIdx]]
            
        return self
    

     
    def __find_ent_ex(self):
        conditionEnt = 1
        conditionEx = -1
        self.enex = map(lambda dirs: np.array([(dir_ <= conditionEnt) * "en" + (dir_ >= conditionEx) * "ex" for dir_ in dirs]), self.relH)
        cond = [np.array(["enex", "", "", ""]), np.array(["enex", "", "", ""]), np.array(["", "", "enex", ""]), np.array(["", "", "", "enex"])]
        deadEndsMatrix = (self.enex == cond[0]).astype(int) + (self.enex == cond[1]).astype(int) + (self.enex == cond[2]).astype(int) + (self.enex == cond[3]).astype(int)
        self.deadEnds = np.where(deadEndsMatrix == 1)
        
        return self
     
    def choose_path(self):
        #Need to add something to avoid the path looping around.
        self.__set_start_stop()
        self.__rel_heights()
        self.__find_ent_ex()
        
        
        heights = self.relH
        
        start = [self.startStop[0][0][0], self.startStop[0][1][0]]
        finish = [self.startStop[1][0][0], self.startStop[1][1][0]]
        print(heights[start[0], start[1]])
        self.walks = [[start]]
        # print(self.walks)
        finished = False
        while not finished:
            print(len(self.walks))
            
            copyWalks = self.walks.copy()
            # print(copyWalks)
            for walk in copyWalks:
                # finished = True if finish in walk else 0
                if len(walk) < self.longestWalkL:
                    coords = walk[-1]
                    
                    r = [walk[-1][0], walk[-1][1] + 1] if [walk[-1][0], walk[-1][1] + 1] not in walk and heights[coords[0], coords[1]][0] >= -1 else 0
                    d = [walk[-1][0] + 1, walk[-1][1]] if [walk[-1][0] + 1, walk[-1][1]] not in walk and heights[coords[0], coords[1]][1] >= -1 else 0
                    l = [walk[-1][0], walk[-1][1] - 1] if [walk[-1][0], walk[-1][1] - 1] not in walk and heights[coords[0], coords[1]][2] >= -1 else 0
                    u = [walk[-1][0] - 1, walk[-1][1]] if [walk[-1][0] - 1, walk[-1][1]] not in walk and heights[coords[0], coords[1]][3] >= -1 else 0
                directions = [r, d, l, u]
                # print(directions)
                # print(directions)
                while 0 in directions:
                    
                    directions.pop(directions.index(0))
                    # print("dirs0:", directions)
            # print("dirs:", directions)
            # print(len(directions))
            # print(len(directions) > 0)
            # print(len(directions) > 0)
            # if len(directions) > 0:
                if len(directions) == 0:
                    self.walks.pop(self.walks.index(walk))
                else:
                    walk = self.walks.pop(self.walks.index(walk))
                # print(walk)
                # print(directions)
                # print(self.walks)
                    
                    
                    for direction in directions:
                        
                        # print(direction)
                        walk.append(direction)
                        # print(walk)
                        self.walks += [walk]
                        walk = walk[ : -1]
                        if direction == finish:
                            # print("MIN: ", min(self.walks, key = lambda walk: len(walk)))
                            finished = True
                            # print(finished)
        
        self.shortest = len(min(self.walks, key = lambda walk: len(walk))) - 1  
   
    def __step(self):    

        heights = self.relH          
        start = [self.startStop[0][0][0], self.startStop[0][1][0]]
        finish = [self.startStop[1][0][0], self.startStop[1][1][0]]
        oldCoords = self.walks[-1]
        step = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        
        r = [self.walks[-1][0], self.walks[-1][1] + 1] if [self.walks[-1][0], self.walks[-1][1] + 1] not in self.deadEnds and [self.walks[-1][0], self.walks[-1][1] + 1] not in self.walks and heights[oldCoords[0], oldCoords[1]][0] >= -1 else 0
        d = [self.walks[-1][0] + 1, self.walks[-1][1]] if [self.walks[-1][0] + 1, self.walks[-1][1]] not in self.deadEnds and [self.walks[-1][0] + 1, self.walks[-1][1]] not in self.walks and heights[oldCoords[0], oldCoords[1]][1] >= -1 else 0
        l = [self.walks[-1][0], self.walks[-1][1] - 1] if [self.walks[-1][0], self.walks[-1][1] - 1] not in self.deadEnds and [self.walks[-1][0], self.walks[-1][1] - 1] not in self.walks and heights[oldCoords[0], oldCoords[1]][2] >= -1 else 0
        u = [self.walks[-1][0] - 1, self.walks[-1][1]] if [self.walks[-1][0] - 1, self.walks[-1][1]] not in self.deadEnds and [self.walks[-1][0] - 1, self.walks[-1][1]] not in self.walks and heights[oldCoords[0], oldCoords[1]][3] >= -1 else 0
        directions = [r, d, l, u] 
        while 0 in directions:
            directions.pop(directions.index(0))
        for direction in directions:
            # print(tuple(direction) in list(self.visited))
            # print(tuple(direction), direction)
            if tuple(direction) in list(self.visited):
                directions.pop(directions.index(list(direction)))
                
        if len(directions) == 0 and self.walks[-1] != start:
            # print(self.walks[-1])
            # print(type(self.deadEnds))
            # print(self.deadEnds)
            self.deadEnds.append(self.walks.pop())  
        elif len(directions) != 0:
            direction = rd.choice(directions)
            self.walks += [direction]
            self.visited = list(self.visited)
            self.visited.append(tuple(direction))
            self.visited = set(self.visited)
            # print(self.visited)
        else:
            pass
        return self
     
    def __optim(self):
        start = [self.startStop[0][0][0], self.startStop[0][1][0]]
        finish = [self.startStop[1][0][0], self.startStop[1][1][0]]
        self.shortestWDirs = []
        for stepIdx in range(1, len(self.shortestW)):
            self.shortestWDirs.append([self.shortestW[stepIdx][0] - self.shortestW[stepIdx - 1][0], self.shortestW[stepIdx][1] - self.shortestW[stepIdx - 1][1]])
        oldL = len(self.shortestWDirs) + 1
        
        
        
        def walk_the_path(testPath):
            finish = [self.startStop[1][0][0], self.startStop[1][1][0]]
            start = [self.startStop[0][0][0], self.startStop[0][1][0]]
            state = True
            for step in testPath:
                end = [start[0] + step[0], start[1] + step[1]]
                print("END", end)
                condition = True if self.map[end[0], end[1]] - self.map[start[0], start[1]] <= 1 else False
                # print(self.map[end[0], end[1]], self.map[start[0], start[1]], condition)
                if not condition:
                    
                    state = False
                    # print(state)
                    break
                start = end
            
            if end != finish:
                print("END", end, finish)
                state = False
            return state
        
        
        testPath = self.shortestWDirs
        print(all(testPath[-1] == testPath[-2]))
        
        # print(testPath)
        condMet = False
        while oldL != len(testPath):
            # print(oldL, len(testPath))
            testStep1Idx = 0
            testStep2Idx = 0
            testStep1 = np.array([])
            testStep2 = np.array([])
            
            found = False
            
            newPathState = True
            # print(len(testPath))
            
            for stepIdx, step in enumerate(testPath):
                # print(stepIdx)
                if not stepIdx < len(testPath):
                    break
                if stepIdx > 0 and stepIdx < len(testPath) - 1 and not condMet:
                    # print(step != testPath[stepIdx - 1])
                    # print(testStep2Idx == testStep1Idx)
                    if any(step != testPath[stepIdx - 1]) and testStep2Idx == testStep1Idx and not condMet and not found:
                        
                        testStep1Idx = stepIdx
                        testStep1 = np.array(testPath[stepIdx - 1])
                        testStep2 = testStep1
                        testStep2Idx = testStep1Idx
                        found = True
                        condMet = False
                    # print(all(step != testPath[stepIdx - 1]) and found and not condMet)
                    # print(step, testPath[stepIdx - 1])
                    if any(step != testPath[stepIdx - 1]) and found and not condMet:
                        testStep2 = np.array(step)
                        testStep2Idx = stepIdx
                        # print(testStep1, testStep2)
                        # print("COND", [testStep2[0], testStep2[1]] == [-testStep1[0], -testStep1[1]])
                        if [testStep2[0], testStep2[1]] == [-testStep1[0], -testStep1[1]]:
                            # print(testStep1, testStep2)
                            condMet = True
                            # oldL = len(testPath)  
                            # found = False
                            # break
                            safety = testPath
                            
                            
                            idxFromStart = testStep1Idx
                            idxFromEnd = -(len(testPath) - testStep2Idx) - 1
                            while condMet:
                               print(len(testPath))
                               if not newPathState:
                                   print(oldL != len(testPath), oldL, len(testPath))
                                   condMet = False
                                   testStep1 = testStep2.copy()
                                   testStep1Idx = testStep2Idx
                                   # print("BREAK")
                                   break
                                   # print(len(testPath), oldL)
                                   
                               testPath = safety
                               idxFromStart = idxFromStart - 1
                               idxFromEnd = idxFromEnd + 1
                                   
                               
                               print(idxFromStart, idxFromEnd)
                               safety = testPath.copy()
                               safety.pop(idxFromStart)
                               safety.pop(idxFromEnd)
                               newPathState = walk_the_path(safety)
                               if newPathState:
                                   print("NEW PATH")
                                   oldL = len(testPath)
                            
                            
                            
                    
               
            
                        
                        
                        
                        
                        
        self.shortestWDirs = testPath
       
        self.shortest = len(self.shortestWDirs) 
        return self
    
    def choose_path2(self):
        #Need to add something to avoid the path looping around.
        self.__set_start_stop()
        self.__rel_heights()
        self.__find_ent_ex()
        self.deadEnds = []
        start = [self.startStop[0][0][0], self.startStop[0][1][0]]
        rd.seed()
        lastL = self.longestWalkL
        lastWalkL = self.longestWalkL
        
        
        
        start = [self.startStop[0][0][0], self.startStop[0][1][0]]
        finish = [self.startStop[1][0][0], self.startStop[1][1][0]]
        for i in range(5000):
            # print(i)
            attrition = 0
            self.walks = [start]
            while finish not in self.walks:
                self.__step()
                if len(self.walks) == lastWalkL:
                    attrition += 1
                if attrition == 5:
                    break
                lastWalkL = len(self.walks)
                # print(len(self.walks))
                # print(self.walks)
            self.shortest = len(self.walks) - 1 if finish in self.walks else -1
            if self.shortest < lastL and self.shortest != -1:
                self.shortestW = self.walks
                lastL = self.shortest
        
        print(self.shortestW[-1], finish)        
        self.shortest = lastL
        
        self.__optim()
        print()
        return self
    
    def __level(self):
        
        return self
    
    def choose_path3(self):
        #Need to add something to avoid the path looping around.
        self.__set_start_stop()
        self.__rel_heights()
        self.__find_ent_ex()
        self.deadEnds = []
        start = [self.startStop[0][0][0], self.startStop[0][1][0]]
        rd.seed()
        lastL = self.longestWalkL
        lastWalkL = self.longestWalkL
        
        
        
        start = [self.startStop[0][0][0], self.startStop[0][1][0]]
        finish = [self.startStop[1][0][0], self.startStop[1][1][0]]
            
        return self    
        
#use a sum and u product for each point with entries/exits in the format [pm1 or 0, pm1 or 0, pm1 or 0, pm1 or 0] for [r, d, l, u] directions.
#map relative heights in the same manner as line above.

def run():
    maps = Map()
    maps.choose_path2()
    print("shortest: ", maps.shortest)
    return maps.shortest

print(run())

# a = np.array([i for i in range(25)]).reshape((5, -1))
# print(a)
# print(sum(abs(np.array(np.where(a == 0)) - np.array(np.where(a == 24)))))
# print(list(np.where(a == 12))[1])
# print(np.where(a == 12))
# print(np.where(a == 12)[0][0], np.where(a == 12)[1][0])

# b = True
# c = False
# print([b] + [c])
# a = np.array([inf for i in range(9)]).reshape((3, -1))
# a[1 : -1, 1 : -1] = np.array([-inf])
# print(a - 5)
# def fun(x):
#     return x if x%2 else -x
# print(fun(2), fun(3))
# a = [1, 2, 3]
# b = [4]
# b.append(a.pop())
# print(a, b)
a = [1, 2, 3]
# b = a.copy()
# a.pop()
# print(b)