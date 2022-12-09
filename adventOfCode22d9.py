# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 18:49:57 2022

@author: xBubblex
"""

import re
import numpy as np

def load_files():
    fContent = []
    with open("input9.txt") as f:
        
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line):
                fContent.append(line.strip("\n").split(" "))
    for lineIdx, line in enumerate(fContent):
        fContent[lineIdx][1] = int(line[1])
    return(fContent)

# print(load_files())

class Rope():
    def __init__(self):
        self.motions = load_files()
        self.board = np.array([])
        self.startingPosition = []
    
    def __find_board_sizes(self):
        vertical = 0
        maxVertical = 0
        maxHorizontal = 0
        horizontal = 0
        hFound = False
        vFound = False
        for motion in self.motions:
            
            if not hFound or not vFound:
               
                if (motion[0] == "R" or motion[0] == "L") and not hFound: 
                    hFound = motion[0]
                    print("H Found", hFound)
                if (motion[0] == "U" or motion[0] == "D") and not vFound: 
                    vFound = motion[0]
                    print("V Found", vFound)
                
            if motion[0] == "R" or motion[0] == "L":
                horizontal += int(hFound == motion[0]) * motion[1] + (int(hFound == motion[0]) - 1) * motion[1]
                
                if abs(horizontal) >= maxHorizontal:
                    maxHorizontal = abs(horizontal)
            if motion[0] == "U" or motion[0] == "D":
                vertical += int(vFound == motion[0]) * motion[1] + (int(vFound == motion[0]) - 1) * motion[1]
                
                if abs(vertical) >= maxVertical:
                    maxVertical = abs(vertical)
            
        self.startingPosition = [maxVertical - 1 if vFound == "U" else 0, maxHorizontal - 1 if hFound == "L" else 0]
        print("Starting position: ", self.startingPosition)
        print("Board sizes: ", (maxVertical * 2, maxHorizontal * 2))
        return (maxVertical * 2, maxHorizontal * 2)
    
    def __update_board(self, tail):
        updater = np.zeros(self.board.shape)
        updater[tail[0], tail[1]] = 1
        self.board += updater
        # print(self.board[tail[0], tail[1]])
        # print("BOARD UPDATE: ", self.board[tail])
        # print(sum(self.board > 0))
        return self
    
    def create_board(self):
        print("Creating the board")
        self.board = np.zeros(self.__find_board_sizes())        
        return self
    
    def simulate_rope(self):
        
        def tail_step(head, tail):
            step = [0, 0]
            dist = list(map(lambda x: abs(x), [head[0] - tail[0], head[1] - tail[1]]))
            condition = any([dist == [1, 1], dist == [0, 1], dist == [1, 0], dist == [0, 0]])
            step = [0, 0] if condition else [sign(head[0] - tail[0]), sign(head[1] - tail[1])]
            return step
        
        head = self.startingPosition
        tail = self.startingPosition
        print("TAIL: ", tail)
        for motion in self.motions:
            instruction = [motion[1] if motion[0] in ["U", "D"] else 0, motion[1] if motion[0] in ["L", "R"] else 0, ]
            if motion[0] == "L":
                instruction = [instruction[0], -instruction[1]]
            if motion[0] == "U":
                instruction = [-instruction[0], instruction[1]]
            
            # print(instruction)
            while instruction != [0, 0]:
                head = [head[0] + sign(instruction[0]), head[1] + sign(instruction[1])]
                instruction = [instruction[0] - sign(instruction[0]) * 1, instruction[1] - sign(instruction[1]) * 1, ]
                step = tail_step(head, tail)
                tail = [tail[0] + step[0], tail[1] + step[1]]
                # print("STEP", head, tail)
                self.__update_board(tail)
        return self
    
def run():
    ropeBridge = Rope()
    ropeBridge.create_board().simulate_rope()
    
    print(ropeBridge.board)
    noVisitedPlaces = sum((ropeBridge.board > 0).astype(int))
    return noVisitedPlaces

print(run())
    
# def fun():
#     return (3, 3)
# a = np.ones(fun())
# print(a)
a = 5
print(sign(a))