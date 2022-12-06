# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 14:51:08 2022

@author: xBubblex
"""

import re
import numpy as np

def load_files():
    fContent = []
    with open("input6.txt") as f:
        stacks = True
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line):
                fContent.append(line.strip("\n"))
                    
    return(fContent)

# print(load_files())

class Signal:
    def __init__(self):
        self.rawSignal = load_files()[0]
        self.preprocessedSig = []
        self.marker = ""
        self.markerName = "packet"
        self.markerIdx = 0
        self.log = []
        
    def split_signal(self):
        markerName = self.markerName
        self.preprocessedSig = []
        for symbolIdx, symbol in enumerate(self.rawSignal):
            if symbolIdx < (lambda mrkr: 4 if mrkr == "packet" else 14)(markerName):
                self.preprocessedSig.append(symbol)
            elif symbolIdx == (lambda mrkr: 4 if mrkr == "packet" else 14)(markerName):
                self.preprocessedSig.append(self.preprocessedSig[:])
                for itr in range((lambda mrkr: 4 if mrkr == "packet" else 14)(markerName)):
                    self.preprocessedSig.remove(self.preprocessedSig[0])                
                self.preprocessedSig.append(self.preprocessedSig[-1][1:] + [symbol])
            else:
                self.preprocessedSig.append(self.preprocessedSig[-1][1:] + [symbol])
        self.preprocessedSig = list(map(lambda entry: "".join(entry), self.preprocessedSig))
        
        return self
        
    def find_marker(self):
        markerName = self.markerName
        self.marker = ""
        for entry in self.preprocessedSig:
            self.marker += entry if all([letter not in entry.replace(letter, "", 1) for letter in entry]) else ""
            if self.marker != "":
                self.markerIdx = np.where(np.array(self.preprocessedSig) == self.marker)[0][0] + (lambda mrkr: 4 if mrkr == "packet" else 14)(markerName) if np.where(np.array(self.preprocessedSig) == self.marker)[0][0] != 0 else 1
                self.log = (np.array(self.preprocessedSig) == self.marker).astype(int)
                return self
        return self
    
def run():
    signal = Signal()
    print(len(signal.rawSignal))
    print(signal.split_signal().find_marker().markerIdx)
    signal.markerName = "message"
    print(signal.split_signal().find_marker().markerIdx)
    
print(run())