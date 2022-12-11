# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 13:24:13 2022

@author: xBubblex
"""

import re
import numpy as np

def load_files():
    fContent = []
    with open("input11.txt") as f:
        
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line):
                fContent.append(line.strip("\n").split(" "))

    return(fContent)

print(load_files())

class Monkey:
    def __init__(self, number = 0, items = [], operation = ["+", "old, old"], test = [2, 0, 1], inspected = 0):
        self.number = number
        self.items = items
        self.operation = operation
        self.test = test
        self.insepcted = inspected
        
class Shenanigans:
    def __init__(self):
        self.rawMonkeys = load_files()
        self.noMonkeys = 0
        self.monkeys = []
        self.monkeyBusiness = 0
        
        
    def __count_monkeys(self):
        for line in self.rawMonkeys:
            if "Monkey" in line:
                self.noMonkeys = int(line[1].strip(": ")) if int(line[1].strip(": ")) > self.noMonkeys else 0
        return self
    
    def prepare_monkeys(self):
        self.__count_monkeys()
        for lineIdx, line in enumerate(self.rawMonkeys):
            if "Monkey" in line:
                number = int(line[1].strip(": "))
            if "items:" in line:
                items = [int(line[idx]) for idx in range(line.index("item:"), line.index(line[-1]) + 1)]
            if "Operation:" in line:
                if "+" in line:
                    operation = ["+", line[line.index("+") - 1], line[line.index("+") + 1]]
                if "*" in line:
                    operation = ["*", line[line.index("+") - 1], line[line.index("+") + 1]]
            if "Test:" in line:
                test = [line[1 + line.index("by")], int(self.rawMonkeys[lineIdx + 1][-1]), int(self.rawMonkeys[lineIdx + 2][-1])]
            if number and items and operation and test:    
                self.monkeys.append(Monkey(number, items, operation, test))
        return self
    
    def __monkey_business(self):
        monkeysBusinesses = [monkey.inspected for monkey in self.monkeys]
        monkey1 = monkeysBusinesses.pop(monkeysBusinesses.index(max(monkeysBusinesses)))
        monkey2 = monkeysBusinesses.pop(monkeysBusinesses.index(max(monkeysBusinesses)))
        self.monkeyBusiness = monkey1 * monkey2
        return self
    
    def rnd(self, rounds = 20):
        
        def worryLvl(inspectedItem, operation):
            worryLvl = inspectedItem // 3
            if operation[0] == "+":
                worryLvl = (worryLvl if operation[1] == "old" else int(operation[1])) + (worryLvl if operation[1] == "old" else int(operation[1]))
            if operation[0] == "*":
                (worryLvl if operation[1] == "old" else int(operation[1])) * (worryLvl if operation[1] == "old" else int(operation[1]))
            return worryLvl
        for rounds in range(rounds):
            for monkey in self.monkeys:
                while len(monkey.items) > 0:
                    inspectedItem = monkey.items.pop()
                    monkey.inspected += 1
                    worryLvl = worryLvl(inspectedItem, monkey.operation)
                    self.monkeys[int(monkey.test[2])].items.append([worryLvl]) if worryLvl % int(monkey.test[0]) else self.monkeys[int(monkey.test[1])].items.append([worryLvl])
        self.__monkey_business()                                        
            
        return self
    

x = [1, 2, 3]
a = x.pop()
print(a)
print(x)

