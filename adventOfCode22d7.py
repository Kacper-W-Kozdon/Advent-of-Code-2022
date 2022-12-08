# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:04:29 2022

@author: xBubblex
"""

import re
import numpy as np

def load_files():
    fContent = []
    with open("input7.txt") as f:
        
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line):
                fContent.append(line.strip("\n").split(" "))
                    
    return(fContent)

class Device:
    def __init__(self):
        self.terminal = load_files()
        self.paths = [["/"]]
        self.tape = []  
        self.lsContent = []
        self.cd = ""
        self.currentPaths = []
        self.maxPathLen = 0
        
    def __update_paths(self):
        while len(self.currentPaths) > 0:
            self.currentPaths.pop()
        for path in self.paths:
            if all(list(map(lambda element: element in path, self.tape))):
                self.currentPaths.append(path)
        return self
        
    def __cd(self):
        if self.cd == "..":
            self.tape.pop()
            self.__update_paths()
        else:
            self.tape.append(self.cd)
            self.__update_paths()
        return self
            
    def __ls(self):
        if len(self.currentPaths) == 1:  
            # print("\n", len(self.lsContent), "\n")
            self.paths.pop(self.paths.index(self.currentPaths[0]))
            for item in self.lsContent:
                path = self.currentPaths[0].copy()
                try:
                    path.append((int(item[0]), item[1]))
                except ValueError:
                    path.append(item[1])
                                
                self.paths.append(path)
            pass
        return self
    
    def __remove_duplicates(self):
        test = self.paths.copy()
        for path in self.paths:
            test.pop(test.index(path))            
            if path in test:
                pass
            else:
                test.append(path)
        self.paths = test
        return self
    
    def create_tree(self):
        for lineIdx, line in enumerate(self.terminal):
            # print("Line " + str(lineIdx) + ": ", line) if lineIdx % 100 == 0 else 0
            if line[0] == "$":
                pass
                if line[1] == "cd":
                    self.cd = line[2]
                    self.__cd()
                if line[1] == "ls":
                    for item in self.terminal[lineIdx + 1:]:
                        if item[0] != "$":
                            self.lsContent.append([item[0], item[1]])
                        else:
                            break
                            # print(item)
                    self.__ls()
                    self.lsContent = []
                            
            else:
                pass
            pass
        self.__remove_duplicates()
        return self
    
    def size_check(self):
        self.maxPathLen = max(list(map(lambda path: len(path), self.paths)))
        return self
    
def run():
    device = Device()
    paths = device.create_tree().size_check().paths
    # print(paths)
    print("max: ", device.maxPathLen)
    # for path in paths:
        # print(path) if "bgzdv" in path else 0
    
print(run())





print(list(map(lambda x: x in [1, 2, 3, 4], [1, 2, 3])))
    
a = [1, 2, 3, 5]
print(a[2:])

