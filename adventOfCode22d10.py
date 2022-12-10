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
        self.coursor = [1]
        self.totalStr = 0
        self.params = [20, 40]
        
    def find_str(self):

        toAdd1 = 0
        toAdd2 = 0
        for lineIdx, line in enumerate(self.signal):
            # print(self.signalStr[-1], line)
            
            if line[0] != "noop":
                toAdd1 = line[1]
                self.coursor += [self.coursor[-1]]
                self.coursor += [self.coursor[-1] + line[1]]
            if line[0] == "noop":
                self.coursor += [self.coursor[-1]]
                
        self.signalStr = self.coursor.copy()

        for lineIdx, line in enumerate(self.signalStr):

            self.signalStr[lineIdx] = line * (lineIdx + 1)
            
        self.totalStr = sum(self.signalStr[self.params[0] - 1::self.params[1]])
        return self
    def printer(self):
        for cycle, pix in enumerate(self.coursor):
            crtLine = ["." for i in range(41)]
            for i in [i - 1 for i in range(3)]:
                crtLine[i + pix] = "#"
            if cycle % 40 == 0:
                print()
            print(crtLine[cycle % 40], end = "")
             
    
def run():
    signal = Signal()
    signal.find_str()
    print(signal.totalStr)
    signal.printer()
    return signal.totalStr
    
print(run())

