# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 13:24:13 2022

@author: xBubblex
"""

import re
import numpy as np

def load_files():
    fContent = []
    with open("inputtest.txt") as f:
        
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line):
                fContent.append(line.strip("\n").split(" "))

    return(fContent)

# print(load_files())

class Monkey:
    def __init__(self, number = 0, items = [], operation = ["+", "old, old"], test = [2, 0, 1], inspected = 0):
        self.number = number
        self.items = items
        self.operation = operation
        self.test = test
        self.inspected = inspected
    def check(self):
        # print("Monkey ", self.number)
        pass
        
        
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
        # print(self.rawMonkeys)
        number = 0
        items = []
        operation = []
        test = []
        numberFound = False
        itemsFound = False
        operationFound = False
        testFound = False
        for lineIdx, line in enumerate(self.rawMonkeys):
            # print(line)
            if "Monkey" in line:
                number = int(line[1].strip(": "))
                numberFound = True
            if "items:" in line:
                # print(line.index("items:") + 1)
                # print(line.index(line[-1]))
                # print([idx for idx in range(line.index("items:"), line.index(line[-1]) + 1)])
                items = [int(line[idx].strip(",")) for idx in range(line.index("items:") + 1, line.index(line[-1]) + 1)]
                itemsFound = True
            if "Operation:" in line:
                
               
                if bool("+" in line):
                    operation = ["+", line[line.index("+") - 1], line[line.index("+") + 1]]
            
         
                if bool("*" in line):
                    operation = ["*", line[line.index("*") - 1], line[line.index("*") + 1]]
                
                # print(operation)
                operationFound = True
            if "Test:" in line:
                test = [line[1 + line.index("by")], int(self.rawMonkeys[lineIdx + 1][-1]), int(self.rawMonkeys[lineIdx + 2][-1])]
                testFound = True
            if numberFound and itemsFound and operationFound and testFound:   
                numberFound = False
                itemsFound = False
                operationFound = False
                testFound = False
                monkey = Monkey(number, items, operation, test)
                # print(monkey.check())
                self.monkeys.append(monkey)
                
        return self
    
    def __monkey_business(self):
        monkeysBusinesses = [monkey.inspected for monkey in self.monkeys]
        print(monkeysBusinesses)
        monkey1 = monkeysBusinesses.pop(monkeysBusinesses.index(max(monkeysBusinesses)))
        monkey2 = monkeysBusinesses.pop(monkeysBusinesses.index(max(monkeysBusinesses)))
        
        self.monkeyBusiness = monkey1 * monkey2
        return self
    
    def rnd(self, rounds = 20):
        
        def worry_lvl(inspectedItem, operation):
            # print(inspectedItem, operation)
            worryLvl = inspectedItem
            # print(worryLvl) if worryLvl > 0 else 0
            # print(operation[1], operation[2])
            if operation[0] == "+":
                # print("add")
                worryLvl = (worryLvl if operation[1] == "old" else int(operation[1])) + (worryLvl if operation[2] == "old" else int(operation[2]))
            if operation[0] == "*":
                # print("multiply")
                worryLvl = (worryLvl if operation[1] == "old" else int(operation[1])) * (worryLvl if operation[2] == "old" else int(operation[2]))
            # print(worryLvl) if worryLvl > 0 else 0
            worryLvl = worryLvl // 3 if rounds == 20 else worryLvl
            return worryLvl
        for roundsIdx, rounds in enumerate(range(rounds)):
            print("\rRound %roundsIdx" % roundsIdx)
            # print("0", self.monkeys[0].items, "\n",  "1", self.monkeys[1].items, "\n", "2", self.monkeys[2].items, "\n", "2", self.monkeys[3].items)
            for monkeyIdx, monkey in enumerate(self.monkeys):                
                while len(monkey.items) > 0:
                    # print(monkey.items)
                    inspectedItem = monkey.items.pop(0)
                    # print(inspectedItem)
                    monkey.inspected += 1
                    # print(monkey.items)
                    worryLvl = worry_lvl(inspectedItem, monkey.operation)
                    self.monkeys[int(monkey.test[2])].items.append(worryLvl) if worryLvl % int(monkey.test[0]) else self.monkeys[int(monkey.test[1])].items.append(worryLvl)
        self.__monkey_business()                                        
            
        return self
    

def run():
    monkeys = Shenanigans()
    print(monkeys.prepare_monkeys().rnd(1000).monkeyBusiness)

print(run())
# x = [1, 2, 3]
# a = x.pop()
# print(a)
# print(x)

