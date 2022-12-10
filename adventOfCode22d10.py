# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 13:22:18 2022

@author: xBubblex
"""

import re
import numpy as np

def load_files():
    fContent = []
    with open("input10.txt") as f:
        
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line):
                fContent.append(line.strip("\n").split(" "))
    for lineIdx, line in enumerate(fContent):
        if len(fContent[lineIdx]) == 2:
            fContent[lineIdx][1] = int(line[1])
        if len(fContent[lineIdx]) != 2:
            fContent[lineIdx] += [0]
        
    return(fContent)

# print(load_files())

class Signal():
    def __init__(self):
        self.signal = load_files()
        self.signalStr = [1]
        self.totalStr = 0
        self.params = [20, 40]
        
    def find_str(self):
        # print(len(self.signal))
        # for line in self.signal:
            # print(line[1])
        toAdd1 = 0
        toAdd2 = 0
        for lineIdx, line in enumerate(self.signal):
            # print(self.signalStr[-1], line)
            
            if line[0] != "noop":
                toAdd1 = line[1]
                self.signalStr += [self.signalStr[-1]]
                self.signalStr += [self.signalStr[-1] + line[1]]
            if line[0] == "noop":
                self.signalStr += [self.signalStr[-1]]
                
    
        # self.signalStr.pop(0)
        # self.signalStr.pop(0)
        # print(self.signalStr)
        # print(self.signalStr[220])
        for lineIdx, line in enumerate(self.signalStr):

            self.signalStr[lineIdx] = line * (lineIdx + 1)
            
        # print(self.signalStr)
        # print(self.signalStr.index(21))
        # print(self.signalStr[20])
        # print(self.signalStr)
        # print(self.signalStr[self.params[0] - 1::self.params[1]])
        self.totalStr = sum(self.signalStr[self.params[0] - 1::self.params[1]])
        return self
    
def run():
    signal = Signal()
    signal.find_str()
    print(signal.totalStr)
    return signal.totalStr
    
print(run())

# x = [2 * i for i in range(20)]
# print(x)
# print(x[2::5])