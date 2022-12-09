# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 23:17:41 2022

@author: xBubblex
"""

import re
import numpy as np

def load_files():
    fContent = []
    with open("input8.txt") as f:
        
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line):
                row = []
                row.extend(line.strip("\n"))
                fContent.append(row)
                    
    return(fContent)

# print(np.array(load_files()).shape)
class TreeHouse:
    def __init__(self):
        self.forest = np.array(load_files()).astype(int)
        self.visibleTrees = np.zeros(self.forest.shape)
        self.noVisibleTrees = 0
        
    def __look_around(self, rowIdx, treeIdx):
        if self.forest.shape[0] != self.forest.shape[1]:
            return print("FOREST NOT IN A SQUARE GRID")
        visibilityTable = []
        
        if rowIdx == self.forest.shape[0] - 1 or rowIdx == 0 or treeIdx == 0 or treeIdx == self.forest.shape[0] - 1:
            visibilityTable = [True]
            
        else:
            north = all(self.forest[:rowIdx, treeIdx] < self.forest[rowIdx, treeIdx])
            east = all(self.forest[rowIdx, treeIdx + 1:] < self.forest[rowIdx, treeIdx])
            south = all(self.forest[rowIdx + 1:, treeIdx] < self.forest[rowIdx, treeIdx])
            west = all(self.forest[rowIdx, :treeIdx] < self.forest[rowIdx, treeIdx])
            visibilityTable += [north, east, south, west]
            
        
        return visibilityTable
    
    
    def __count_trees(self):
        self.noVisibleTrees = sum(self.visibleTrees.flatten())
        
    def visible_trees(self):
        for rowIdx, row in enumerate(self.forest):
            for treeIdx, tree in enumerate(row):
                self.visibleTrees[rowIdx, treeIdx] = int(any(self.__look_around(rowIdx, treeIdx)))
        self.__count_trees()
        return self
    
def run():
    treeHouse = TreeHouse()
    
    # for row in treeHouse.visible_trees().forest:
    #     print(row)
    # for row in treeHouse.visible_trees().visibleTrees:
    #     print(row)
        
    return(treeHouse.visible_trees().noVisibleTrees)

print(run())
# a = np.array([3, 7, 2])
# print(all(a > 4))
# a = np.array([i for i in range(25)]).reshape((5, -1))
# print(a[:3 - 1, 2])
# print(a[3:, 2])

# print(a[2, 2])