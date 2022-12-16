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
    with open("input12.txt") as f:
        
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
        self.stepsData = np.zeros(self.map.shape)
        
    

    

    def __set_start_stop(self):
        while len(self.startStop) > 0:
            self.startStop.pop()
        self.startStop.append(np.where(self.map == "S"))
        self.startStop.append(np.where(self.map == "E"))

        self.map[self.startStop[0]] = "a"
        self.map[self.startStop[1]] = "z"
        self.pathLimit = ord("z") + 1 - ord("a")
        # print(self.map.shape)
        # print(len([inf for i in range((self.map.shape[0] + 2) * (self.map.shape[1] + 2))]))
        
        self.mapWBorders = np.array([1000 for i in range((self.map.shape[0] + 2) * (self.map.shape[1] + 2))]).reshape((self.map.shape[0] + 2, -1))
        
        self.map = np.array([ord(height) for height in self.map.flatten()]).reshape(self.map.shape)
        
                
        self.mapWBorders[1 : -1, 1 : -1] = self.map
        
        return self
    
    def __rel_heights(self):
        # print(self.map)
        # print(self.mapWBorders[1 : -1,  : -2])
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
     
    
    def find_path_lee(self):
        #Need to add something to avoid the path looping around.
        self.__set_start_stop()
        self.__rel_heights()
        self.__find_ent_ex()
        self.deadEnds = []
        self.stepsData = np.zeros(self.map.shape)
        start = [self.startStop[0][0][0], self.startStop[0][1][0]]
        finish = [self.startStop[1][0][0], self.startStop[1][1][0]]
        self.shortest = 0
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        while self.stepsData[finish[0], finish[1]] == 0:
            
            if self.shortest == 0:
                self.shortest += 1
                for direction in directions:       
                    if self.map[direction[0] + start[0] + 1, direction[1] + start[1] + 1] - self.map[start[0], start[1]] <= 1:
                        self.stepsData[direction[0] + start[0] + 1, direction[1] + start[1] + 1] = self.shortest 
            
            currentStepLocRaw = np.where(self.stepsData == self.shortest)
            currentStep = [location for location in zip(currentStepLocRaw[0], currentStepLocRaw[1])]
            self.shortest += 1
            for location in currentStep:
                for direction in directions:
                    # print([direction[0] + location[0], direction[1] + location[1]])
                    locCond = (direction[0] + location[0]) in range(self.map.shape[0]) and (direction[1] + location[1]) in range(self.map.shape[1])
                    if locCond:
                        valCond = self.map[direction[0] + location[0], direction[1] + location[1]] - self.map[location[0], location[1]] <= 1
                        notVisitedCond = self.stepsData[direction[0] + location[0], direction[1] + location[1]] == 0
                    else:
                        valCond = False
                        notVisitedCond = False
                    # print(locCond, valCond, notVisitedCond)
                    
                    if valCond and notVisitedCond and locCond:
                        self.stepsData[direction[0] + location[0], direction[1] + location[1]] = self.shortest
            
        return self    
        
#use a sum and u product for each point with entries/exits in the format [pm1 or 0, pm1 or 0, pm1 or 0, pm1 or 0] for [r, d, l, u] directions.
#map relative heights in the same manner as line above.

def run():
    maps = Map()
    maps.find_path_lee()
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
# a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# b = a.copy()
# a.pop()
# print(b)
# b = np.where(a > 4)
# print([a[i] for i in zip(b[0], b[1])])