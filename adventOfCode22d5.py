# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 13:56:52 2022

@author: xBubblex
"""
import re
import numpy as np

def load_files():
    fContent = []
    with open("input5.txt") as f:
        stacks = True
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line):
                # print(line.strip("\n")) if "move" not in line else 0
                if line == ["\n"]:
                    stacks = False
                # print(line.strip("\n").split("|"))
                if stacks == True:
                    fContent.append(re.split("\] \[|    ", line.strip("\n")))
                else:
                    fContent.append(re.split(" ", line.strip("\n")))
                    
    return(fContent)
# print(load_files())

# print('[N]'.strip("[]"))

class Supplies:
    def __init__(self):
        self.data = load_files()
        self.crates = []
        self.instructions = []
        self.tops = []
        pass
    
    def load_crates(self):
        temporaryCrates = []
        if len(self.crates) != 0:
            self.crates = []
            print("emptying")
        
        stackComplete = False
        stack = self.data
        for crates in stack:
            if crates == [' 1   2   3   4   5   6   7   8   9 ']:
                stackComplete = True
            if not stackComplete:                  
                temporaryCrates.append(crates)
                
        for rowIdx, row in enumerate(temporaryCrates):
            for columnIdx, column in enumerate(row):
                if column != "":
                    if " [" in column:
                        temporaryCrates[rowIdx][columnIdx] = temporaryCrates[rowIdx][columnIdx].strip(" \[\]")
                        temporaryCrates[rowIdx].insert(columnIdx, "")
        temporaryCrates = np.array(temporaryCrates, dtype = object)
        shapeTempCrates = temporaryCrates.shape 
        temporaryCrates = np.array([el.strip("\[\]") for el in temporaryCrates.flatten()]).reshape(shapeTempCrates)
        temporaryCrates = np.rot90(temporaryCrates, k = 1, axes = (1, 0))
        temporaryCrates = temporaryCrates.tolist()
        for rowIdx, row in enumerate(temporaryCrates):
            while "" in temporaryCrates[rowIdx]:
                try:
                    temporaryCrates[rowIdx].remove("")
                    
                except ValueError:
                    pass
            
        self.crates = np.array(temporaryCrates, dtype = object)
                                
        return self
    
    def load_instructions(self):
        self.instructions = []
        instructions = self.data
        
        instructionsStarted = False
        for instruction in instructions:
            if instructionsStarted:
                self.instructions.append(instruction[0].split(" "))
            if instruction == ['']:
                instructionsStarted = True
                
        
        return self
    
    def move_boxes(self, newCrane = False):
        self.tops = []
        instructions = self.instructions
        crates = self.crates
        for instruction in instructions:
            number = int(instruction[1])
            fromStack = int(instruction[3]) - 1
            toStack = int(instruction[5]) - 1            
            crates[fromStack] = np.array(crates[fromStack])
            # print(crates[fromStack][1:])
            crates[toStack] = np.array(crates[toStack])
            topOfTheStack = crates[fromStack].shape[0]
            if not newCrane:
                pickUp = np.copy(crates[fromStack][topOfTheStack - number:])[::-1]
            else:
                pickUp = np.copy(crates[fromStack][topOfTheStack - number:])
            crates[toStack] = np.append(crates[toStack], pickUp)
            crates[fromStack] = np.delete(crates[fromStack], np.s_[topOfTheStack - number:])
        for rowIdx, row in enumerate(crates):
            crates[rowIdx] = row.tolist()
            self.tops.append(crates[rowIdx][-1])
        self.crates = crates
        return self
        
def run():
    supplies = Supplies()
    
    print("".join(supplies.load_crates().load_instructions().move_boxes().tops))
    print("".join(supplies.load_crates().load_instructions().move_boxes(newCrane = True).tops))
    
    pass

print(run())
