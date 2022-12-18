# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 17:41:44 2022

oauthor: xBubblex
"""

import re
import numpy as np
import random as rd
import functools as ft

def load_files():
    fContent = []
    with open("input14.txt") as f:
        
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line) and line != "\n":
                fContent.append(line.strip("\n").split(" -> "))

    return(fContent)

# print(load_files())

class Stone:
    def __init__(self):
        self.raw = load_files()
        self.lines = []
        self.board = np.array([])
        self.maxH = 0
        self.maxV = 0
        self.minH = 0
        self.minV = 0
        self.boardReady = False
        
    def __preprocess__(self):
        self.lines = []
        for lineIdx, line in enumerate(self.raw):
            lineCoords = {"ver": [], "hor": []}
            for coordsIdx, coords in enumerate(line):
                
                coord = coords.split(",")
                lineCoords["ver"].append(int(coord[1]))
                lineCoords["hor"].append(int(coord[0]))
            self.lines.append(lineCoords)
        return self
    
    def __prepare_board__(self):
        allCoords = {"ver": [], "hor": []}
        for line in self.lines:
            allCoords["ver"] += line["ver"]
            allCoords["hor"] += line["hor"]
        maxH = max(allCoords["hor"])
        maxV = max(allCoords["ver"])
        minH = min(allCoords["hor"])
        minV = min(allCoords["ver"])
        self.maxH = maxH
        self.maxV = maxV
        self.minH = minH
        self.minV = minV
        self.board = np.zeros((maxV + 3, maxH + 2), dtype = object)
        return self
    
    def __prepare_stones__(self):
        for line in self.lines:
            prevCoord = ["v", "h"]
            for coordIdx, coord in enumerate(zip(line["ver"], line["hor"])):
                coordV = coord[0]
                coordH = coord[1]
                if prevCoord == ["v", "h"]:
                    prevCoord = [coordV, coordH]
                else:
                    self.board[min(prevCoord[0], coordV) : max(prevCoord[0], coordV) + 1, min(prevCoord[1], coordH) : max(prevCoord[1], coordH) + 1] = "#"
                    prevCoord = [coordV, coordH]                
                
        return self
    
    def board_ready(self, mode = "void"):
        if not self.boardReady:
            self.__preprocess__()
            self.__prepare_board__()
            self.__prepare_stones__()
            self.board[np.where(self.board == 0)] = "."
            if mode == "noVoid":
                # print(self.board.shape)
                for counter in range(2 * self.maxV):
                    self.entry[1] += 1
                    self.board = np.insert(self.board, 0, ".", axis=1)
                    self.board = np.insert(self.board, -1, ".", axis=1)
                self.board[-1, :] = "#"
                # print(self.board.shape)
                # print(self.board[-1, :])
            self.boardReady = True
        return self
    
class Sand(Stone):
    def __init__(self, entry = [0, 500]):
        super().__init__()
        self.entry = entry
        self.grainCounter = 0
        self.limReached = False
        
    def __add_grain__(self):
        prevPos = self.entry
        canMove = True
        
        # print(self.grainCounter)
        if self.board[prevPos[0], prevPos[1]] == "o":
            return self
        
        self.board[prevPos[0], prevPos[1]] = "o"
        
        
        while canMove:
            # print(prevPos)
            try:
                self.board[prevPos[0], prevPos[1]]
                
                if self.board[prevPos[0] + 1, prevPos[1]] not in ["#", "o"]:
                    self.board[prevPos[0] + 1, prevPos[1]] = "o"
                    self.board[prevPos[0], prevPos[1]] = "."
                    prevPos = [prevPos[0] + 1, prevPos[1]]
                elif self.board[prevPos[0] + 1, prevPos[1] - 1] not in ["#", "o"]:
                    self.board[prevPos[0] + 1, prevPos[1] - 1] = "o"
                    self.board[prevPos[0], prevPos[1]] = "."
                    prevPos = [prevPos[0] + 1, prevPos[1] - 1]
                elif self.board[prevPos[0] + 1, prevPos[1] + 1] not in ["#", "o"]:
                    self.board[prevPos[0] + 1, prevPos[1] + 1] = "o"
                    self.board[prevPos[0], prevPos[1]] = "."
                    prevPos = [prevPos[0] + 1, prevPos[1] + 1]
                else:
                    canMove = False
                    if prevPos == self.entry:
                        self.grainCounter += 1
                        self.limReached = True
                        return self
            except:
                self.limReached = True
                # print("BREAK")
                return self
            
        self.grainCounter += 1
        # print(self.grainCounter)
        return self
        
    def simulate_sand(self, mode = "void"):
        self.board_ready(mode)
        # if mode == "noVoid":
            # entry = [0, 500 + self.maxH]
        
        self.grainCounter = 0
        self.limReached = False
        while not self.limReached:
            self.__add_grain__()
        
        return self
    
    def print_sand(self, rangeView = 40):
        for line in self.board:
            for symbol in line[self.entry[1] - rangeView : self.entry[1] + rangeView]:
                print(symbol, end = "")
            print()
        print()
    
def run():
    stonePath = Stone()
    stonePath.board_ready()
    sand = Sand()
    # for line in sand.board_ready().board:
        # print(line[490 : 520])
    # sand.board_ready(mode = "noVoid").print_sand()
    grainNo = sand.simulate_sand(mode = "noVoid").grainCounter
    sand.print_sand()
    return grainNo
print(run())

# a = np.arange(25).reshape((5, -1))
# a[1 : 2, 1 : -1] = 0
# print(a)
