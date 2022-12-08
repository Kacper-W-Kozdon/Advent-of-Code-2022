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
        self.maxFolderSize = 100000
        self.totalPaths = 0
        self.bigFolders = []
        
    def __update_paths(self):
        while len(self.currentPaths) > 0:
            self.currentPaths.pop()
        for path in self.paths:
            if all(list(map(lambda element: element in path, self.tape))):
                self.currentPaths.append(path)
        # print(self.currentPaths) if len(self.currentPaths) > 1 else 0
        return self
        
    def __cd(self):
        if self.cd == "..":
            self.tape.pop()
            self.__update_paths()
        else:
            self.tape.append(self.cd)
            self.__update_paths()
        # print(self.tape) if len(self.tape) != len(set(self.tape)) else 0
        return self
            
    def __ls(self):
        # print(self.currentPaths) if len(self.currentPaths) > 1 else 0
        if len(self.currentPaths) >= 0:  
            # print("\n", len(self.lsContent), "\n")
            # print(self.currentPaths)

            for item in self.lsContent:
                print("Found: ", item) if item[1] == "nnrd.zrj" else 0
                path = self.tape.copy()
                # print(path) if item[1] == "nnrd.zrj" else 0
                try:
                    path.append((int(item[0]), item[1]))
                    # print(item)
                except ValueError:
                    path.append(item[1])
                    # print(item)
                # print(path) if item[1] == "nnrd.zrj" else 0                
                self.paths.append(path)
                # print(path in self.paths) if item[1] == "nnrd.zrj" else 0 
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
                    print(self.lsContent) if (len(self.lsContent) == 1 and 'nnrd.zrj' in self.lsContent[0]) else 0
                    
                    print(['/', 'fhhwv', 'jngvpc', 'jbc', 'htczftcn', 'nflgvsgz', (208092, 'nnrd.zrj')] in self.paths) if (len(self.lsContent) == 1 and 'nnrd.zrj' in self.lsContent[0]) else 0 
                    self.lsContent = []        
            else:
                pass
            pass
        self.__remove_duplicates()
        self.totalPaths = len(self.paths)
        return self
    
    def size_check(self, mod = 1):
        self.maxPathLen = max(list(map(lambda path: len(path), self.paths)))
        for depth in range(0, self.maxPathLen):
            temporaryPaths = []
            setOfFolders = []
            for path in self.paths:
                if len(path) > depth:
                    # print(tuple(path[:depth + 1]))
                    setOfFolders.append(tuple(path[:depth + 1])) if type(path[depth]) != tuple else 0
                    temporaryPaths.append(path) if type(path[depth]) != tuple else 0
            setOfFolders = set(setOfFolders)
            

            # print(setOfFolders, depth)
            # print(temporaryPaths, "\n") if depth == 11 else 0
            for folder in setOfFolders:
                folderSize = 0
                # print("FOLDER: ", folder)
                for path in temporaryPaths:
                    if type(path[-1]) == tuple and tuple(path[:depth + 1]) == folder:
                        folderSize += path[-1][0]
                self.bigFolders.append((folderSize, folder[-1]))
        bigFolders = sorted(self.bigFolders.copy(), key = lambda folder: folder[0])
        # print("BIG FOLDERS: ")
        # print(bigFolders)
        # print("\n\n\n")
        # for folder in bigFolders:
        #     if folder[0] > self.maxFolderSize:
        #         self.bigFolders.pop(self.bigFolders.index(folder))
        
        if mod == 1:
            bigFolders = []
            for folder in self.bigFolders:
                if folder[0] <= self.maxFolderSize:
                    bigFolders.append(folder)
                self.bigFolders = bigFolders
        if mod != 1:
            folderToDel = []
            maxTakenSpace = 70000000 - 30000000
            takenSpace = max(bigFolders, key = lambda folder: folder[0])[0]
            toFreeUp = takenSpace - maxTakenSpace
            for folder in bigFolders:
                if folder[0] > toFreeUp and len(folderToDel) == 0:
                    folderToDel.append(folder)
            self.bigFolders = folderToDel
        return self
    
def run():
    device = Device()
    paths = device.create_tree().size_check().paths
    # print(device.bigFolders)
    # print(paths)
    # size = 0
    # numberFiles = 0
    # files0 = []
    # for path in device.paths:
    #     # print(path[-1]) if type(path[-1]) == tuple else 0
    #     size += path[-1][0] if type(path[-1]) == tuple else 0
    #     numberFiles += 1 if type(path[-1]) == tuple else 0
    #     files0.append((int(path[-1][0]), path[-1][1])) if type(path[-1]) == tuple else 0
    # print(size, numberFiles)
    # # print(files0)
    files = []
    numberFiles = 0
    size = 0
    for line in device.terminal:
        try:
            int(line[0])
            numberFiles += 1
            size += int(line[0])
            files.append((int(line[0]), line[1]))
        except ValueError:
            pass
    numberFiles = len(set(files))
    print(size, numberFiles)
    # print("max: ", device.maxPathLen)
    # for file in files:
    #     print("Missing file: ", file) if file not in set(files0) else 0
    # # print(device.bigFolders)
    solution = 0
    for folder in device.bigFolders:
        solution += folder[0]
    # for path in paths:
        # print(path) if "bgzdv" in path else 0
    for path in device.paths:
        if (303757, 'gglsqjbz.ffb') in path:
            print("AYE")
            print(path)
            print("\n")
    device2 = Device()
    solution2 = device2.create_tree().size_check(0).bigFolders
    return solution, solution2
    
print(run())

# x = [4, 2, 3, 1]
# a = sorted(x)
# print(x, a)



print(list(map(lambda x: x in [1, 2, 3, 4], [1, 2, 3])))
    
a = [(1, "a"), (3, "b")]


