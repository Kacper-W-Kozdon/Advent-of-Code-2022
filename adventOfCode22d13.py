# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 22:33:35 2022

@author: xBubblex
"""
# When comparing two values, the first value is called left and the second value is called right. Then:

# If both values are integers, the lower integer should come first. If the left integer is lower than the right integer, the inputs are in the right order. If the left integer is higher than the right integer, the inputs are not in the right order. Otherwise, the inputs are the same integer; continue checking the next part of the input.
# If both values are lists, compare the first value of each list, then the second value, and so on. If the left list runs out of items first, the inputs are in the right order. If the right list runs out of items first, the inputs are not in the right order. If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.
# If exactly one value is an integer, convert the integer to a list which contains that integer as its only value, then retry the comparison. For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2); the result is then found by instead comparing [0,0,0] and [2].

import re
import numpy as np
import random as rd
import functools as ft

def load_files():
    fContent = []
    with open("input13.txt") as f:
        
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line) and line != "\n" and type(eval(line.strip("\n"))) == list:
                fContent.append(eval(line.strip("\n")))

    return(fContent)

# print(load_files())

class Packets:
    def __init__(self):
        self.raw = load_files()
        self.packets = {"left": [], "right": []}
        self.order = []
        self.solution1 = 0
        self.orderedPackets = []
        self.decoderKey = 0
        
        
    def __extract_packets(self):
        self.packets = {"left": [], "right": []}
        for packetIdx, packet in enumerate(self.raw):
            key = "right" if packetIdx % 2 else "left"
            # print(packet)
            self.packets[key].append(packet)
            
        return self
        
    
    def analyse_packets(self, mode = "check"):
        
        def compare(leftC, rightC, order = "keepChecking", depth = 0):
            left = leftC.copy()
            right = rightC.copy()
            if order in ["right", "wrong"]:
                return order
            else:
                while bool(left) and bool(right) and order == "keepChecking":
                    options = ["right", "wrong", "keepChecking"]
                    l = left.pop(0)
                    r = right.pop(0)
                    if type(l) == list and type(r) == list:
                        depth += 1
                        # print(l, r)
                        order = compare(l, r, "keepChecking", depth)
                        # print(order)
                        depth = depth - 1
                        if order in ["right", "wrong"]:
                            
                            return order
                        
                    if type(l) == int and type(r) == int:
                        if l != r:
                            order = "right" if l < r else "wrong"
                            # print(l, r)
                            return order
                        if l == r:
                            order = "keepChecking"
                    if type(l) != type(r) and type(r) != None and type(l) != None:
                        if type(l) == int:
                            l = [l]
                        if type(r) == int:
                            r = [r]
                        depth += 1
                        order = compare(l, r, "keepChecking", depth)
                        depth = depth - 1
                        if order in ["right", "wrong"]:
                            return order
                        
                # if order == "keepChecking" and len(left) > len(right) and (len(left) == 0 or len(right) == 0):
                #     order = "right"
                # elif order == "keepChecking" and len(left) < len(right) and (len(left) == 0 or len(right) == 0):
                #     order = "wrong"
                if len(left) < len(right) and (len(right) == 0 or len(left) == 0) and order not in ["right", "wrong"]:
                    order = "right"
                    # print("SUS", left, right)
                elif len(left) > len(right) and (len(right) == 0 or len(left) == 0) and order not in ["right", "wrong"]:
                    order = "wrong"
                    # print("SUS", left, right)
                # else:
                    # print(left, right)
            # if order == "keepChecking":
            #     print(left, right)
            
            return order
        if mode == "check":
            self.__extract_packets()
            for left, right in zip(self.packets["left"], self.packets["right"]):
                # print(left, right)
                leftC = left.copy()
                rightC = right.copy()
                self.order.append(compare(leftC, rightC))
                # print(self.order[-1])
            # print(np.array(np.array(self.order) == "right").astype(int))
            self.solution1 = sum([orderIdx + 1 if orderVal != 0 else 0 for orderIdx, orderVal in enumerate(np.array(np.array(self.order) == "right").astype(int))])
        
        if mode == "order":
            
            dividerPackets = [[[2]], [[6]]]
            self.raw.append(dividerPackets[0])
            self.raw.append(dividerPackets[1])
            self.orderedPackets = self.raw.copy()
            
            self.order = [False]
            index = 0
            while not all(self.order):     
            # print(self.order)
                while len(self.order) > 0:                    
                    self.order.pop()              
                for packetIdx, packet in enumerate(self.orderedPackets): 
                    
                    # # print(packetIdx)
                    if packetIdx == len(self.orderedPackets) - 1:
                        break
                    # # print(packet, self.orderedPackets[packetIdx + 1])
                    packet1Copy = packet.copy()
                    packet2Copy = self.orderedPackets[packetIdx + 1].copy()
                    # print(packet1Copy, packet2Copy)
                    self.order.append(True if compare(packet1Copy, packet2Copy) == "right" else False)
                    # print(packet, self.orderedPackets[packetIdx + 1], "\n\n\n")
                    
                    if not self.order[-1]:
                        index = packetIdx
                        self.orderedPackets.insert(index, self.orderedPackets.pop(index + 1))
                        # print("After", self.orderedPackets[packetIdx], self.orderedPackets[packetIdx + 1], "\n\n")
                    #     break
                
                self.decoderKey = (self.orderedPackets.index(dividerPackets[0]) + 1) * (self.orderedPackets.index(dividerPackets[1]) + 1)
        return self
        
def run():
    packets = Packets()
    print(packets.analyse_packets().solution1)
    print(packets.analyse_packets(mode = "order").decoderKey)
    # for order, packetL, packetR in zip(packets.analyse_packets().order, packets.packets["left"], packets.packets["right"]):
        # print(packetL, "\n", packetR, "\n", order, "\n\n")
    
print(run())

# a = [1, 2, 3, 4]
# b = iter(a)
# print(next(b), next(b))
# a.insert(-1, a.pop())
# print(next(b), next(b))
# while True:
#     print(next(b))

# a = [1, 2, 3, 4]
# b = a.copy()
# b.pop()
# print(a, b)