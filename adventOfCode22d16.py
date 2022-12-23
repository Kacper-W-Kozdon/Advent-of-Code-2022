# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 15:31:52 2022

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
            if bool(line) and line != "\n":
                fContent.append(line.strip("\n"))

    return(fContent)

# print(load_files())


class Valve():
    def __init__(self):
        self.name = ""
        self.from_ = []
        self.to = []
        self.rate = 0
        self.on = False


class Valves(Valve):
    def __init__(self):
        super().__init__()
        self.raw = load_files()
        self.valves = []
        self.valvesObj = []
        
        
        
    def preprocess1(self):
        for line in self.raw:
            valveStart = line.index(" ") + 1
            # print(valveStart, line[valveStart + 1 : ].index(" ") )           
            valveStop = line.index("has") - 1            
            # print(line[valveStart : valveStop], valveStart, valveStop, line[valveStart : valveStop])            
            rateStart = line.index("=") + 1
            rateStop = line.index(";")             
            # print(rateStart, rateStop)
            tempLine = line[rateStop : ]
            # print(tempLine)
            valves = tempLine.index("valve") + len("valve") + 1 + (1 if line[line.index("valve") +  len("valve")] == "s" else 0)
            # print(tempLine[valves : ])
            valves = tempLine[valves : ]
            self.valves += [[line[valveStart : valveStop], int(line[rateStart : rateStop]), valves.split(", ")]]
        return self
    
    def preprocess2(self):
        myVars = vars()
        self.valvesObj = []
        for valve in self.valves:
            myVars.__setitem__(valve[0], Valve())
            myVars[valve[0]].name = valve[0]
            myVars[valve[0]].to = valve[2]
            myVars[valve[0]].rate = valve[1]
            myVars[valve[0]].from_ = []
            for val in self.valves:
                if valve[0] in val[2]:
                    myVars[valve[0]].from_.append(val[0])
            self.valvesObj.append(myVars[valve[0]])
            
        # print(vars()["valves"])
        return self

def run():
    valves = Valves()
    print(valves.preprocess1().preprocess2().valvesObj)
    
    
print(run())

a = "strings string"
print(a[a.index(" ") : ])