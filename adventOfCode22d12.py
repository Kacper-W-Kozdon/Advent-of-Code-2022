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
        self.deadEnds = []
        self.shortest = 0
        self.visited = set([])
        
    

    

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
        print(self.walks)
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
            if tuple(direction) in list(self.visited):
                directions.pop(directions.index(direction))
        
        if len(directions) == 0:
            self.deadEnds.append(self.walks.pop())  
        else:
            self.walks += [directions[0]]
            self.visited = set(list(self.visited) + [tuple(directions[0])])
        return self
        
    def choose_path2(self):
        #Need to add something to avoid the path looping around.
        self.__set_start_stop()
        self.__rel_heights()
        self.__find_ent_ex()
        rd.seed()
        
        
        
        start = [self.startStop[0][0][0], self.startStop[0][1][0]]
        finish = [self.startStop[1][0][0], self.startStop[1][1][0]]
        self.walks = [start]
        while finish not in self.walks:
            self.__step()
            print(len(self.walks))
            print(self.walks)
        self.shortest = len(self.walks) - 1 if finish in self.walks else 0
        lastL = self.longestWalkL
        print()
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
a = [1, 2, 3]
b = [4]
b.append(a.pop())
print(a, b)
