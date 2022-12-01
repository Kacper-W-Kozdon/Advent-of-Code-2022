# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 14:28:44 2022

@author: xBubblex
"""

import numpy as np
import re
import time

def load_files():
    fContent = []
    with open("input1.txt") as f:
            for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
                if bool(line):
                    # print(line.strip("\n").split("|"))
                    fContent.append(line.strip("\n"))  #splitting each entry into coordinates
    return(fContent)

def elf_shares(fContent = load_files()):
    shares = []
    elf = []
    for share in fContent:
        if share == "":
            shares.append(elf)
            elf = []
        else:   
            elf.append(int(share))
    return shares

def fattest_elf(shares = elf_shares()):
    fattestElf = max(shares, key = lambda elf: sum(elf))
    fattestElfTotal = sum(fattestElf)
    return fattestElf, fattestElfTotal

def fattest_3_elves(shares = elf_shares()):
    sharesCopy = shares.copy()
    fattest3Elves = []
    for elfN in range(3):
        fattestElf = fattest_elf(sharesCopy)[0]
        fattest3Elves.append(fattestElf)
        sharesCopy.remove(fattestElf)
    fattest3ElvesTotal = sum(sum(fattest3Elves))
    return fattest3ElvesTotal
    
def run():
    fContent = load_files()
    shares = elf_shares(fContent)
    fattestElfTotal = fattest_elf(shares)[1]
    fattest3ElvesTotal = fattest_3_elves(shares)
    return(fattestElfTotal, fattest3ElvesTotal)

# print(load_files())
# print(elf_shares())
# print(fattest_elf())
print(run())