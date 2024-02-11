# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 15:23:57 2022

@author: xBubblex
"""

'''

NEED TO ALLOCATE SEPARATE ARRAYS FOR SENSOR + BEACON PAIRS.

'''


import re
import numpy as np
import random as rd
import functools as ft

def load_files():
    fContent = []
    with open("input15.txt") as f:
        
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line) and line != "\n":
                fContent.append(line.strip("\n"))

    return(fContent)

# print(load_files())


class Beacons():
    def __init__(self, offset = [20, 20]):
        self.raw = load_files()
        self.data = {"sensors": [], "beacons": []}
        self.board = np.array([])
        self.translation = []
        self.boardOffset = offset
        self.preprocessingFinished = False
        self.solution1 = 0
        self.rowListOfHash = []
        self.beacon = []
        self.tuningFreq = 4000000
        self.row = np.array([], dtype = int)
        self.col = -1
    
    def __create_board__(self, shape0 = 0, shape1 = 0):
        
        self.board = np.empty((shape0 + self.boardOffset[0] * 2, shape1 + self.boardOffset[1] * 2), dtype = str)
        self.board[ : , : ] = "."
        return self
    
    def __place_s_b__(self, key = "", data = ([0], [0])):
        if key == "sensors":
            self.board[data] = "S"
        if key == "beacons":
            self.board[data] = "B"
        
        return self
    
    def __board_offset__(self):
        #list(dataForOffset)[0] print(list(zip(self.data["sensors"], self.data["beacons"])))
        dataForOffset = zip(self.data["sensors"], self.data["beacons"])
        # print(list(dataForOffset))
        # for sensor, beacon in list(dataForOffset):
            # print(sensor, beacon)
        # print(list(dataForOffset)[0] == ([2, 18], [-2, 15]))
        dataForOffsetList = list(dataForOffset)
        # print(dataForOffsetList[0])
        keyOffset = lambda sensorAndBeacon: abs(sensorAndBeacon[0][0] - sensorAndBeacon[1][0]) + abs(sensorAndBeacon[0][1] - sensorAndBeacon[1][1])
        # print(keyOffset(dataForOffsetList[0]))    
        boardOffset = sum(max(dataForOffsetList, key = keyOffset))
        # print(boardOffset)
        # print(boardOffset)
        self.boardOffset = [boardOffset + 1, boardOffset + 1]
    
    def __ping__(self, sensor):
        beaconFound = False
        step = 0
        SLocations = np.where(self.board == "S")
        try:
            pingedLocations = np.where(self.board == "#")
            self.board[pingedLocations] = "."
        except:
            pass
        while not beaconFound:
            if step == 0:
                # self.print_board()
                directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
                for direction in directions:
                    try:
                        if self.board[sensor[0] + direction[0], sensor[1] + direction[1]] == "B":
                            beaconFound = True
                        if self.board[sensor[0] + direction[0], sensor[1] + direction[1]] not in ["#", "B"]:
                            self.board[sensor[0] + direction[0], sensor[1] + direction[1]] = "#" 
                    except IndexError:
                        pass
                        
                nextY, nextX = np.where(self.board == "#")
                for nY, nX in zip(nextY, nextX):
                    for direction in directions:    
                        try:    
                            if self.board[nY + direction[0], nX + direction[1]] not in ["#", "B", ","]:
                                self.board[nY + direction[0], nX + direction[1]] = ","
                        except IndexError:
                            pass
                        
                # self.print_board()
            step += 1
            
            nextY, nextX = np.where(self.board == ",")
            self.board[np.where(self.board == ",")] = "#"
            if beaconFound == True:
                break
            for nY, nX in zip(nextY, nextX):
                for direction in directions: 
                    try:
                        if self.board[nY + direction[0], nX + direction[1]] not in ["#", "B", ","]:
                            self.board[nY + direction[0], nX + direction[1]] = ","
                        if self.board[nY + direction[0], nX + direction[1]] == "B":
                            beaconFound = True
                    except IndexError:
                        pass
        self.board[np.where(self.board == ",")] = "#"
        self.board[SLocations] = "S"
        self.board[pingedLocations] = "#"
        return self
    
    def print_board(self):
        for row in self.board:
            for column in row:
                print(column, end = "")
            print()
        print()
        print()
    
    def preprocess(self):
        
        if self.preprocessingFinished:
            self.data = {"sensors": [], "beacons": []}
            self.board = np.array([])
            self.translation = []
    
    
        for line in self.raw:
            line = line.split(": ")
            line = {"sensors": line[0], "beacons": line[1]}
            for key in self.data.keys():
                data = []
                readStart = line[key].index("=") + 1
                readEnd = line[key].index(",")
                data.append(int(line[key][readStart : readEnd]))
                readStart = line[key][readEnd : ].index("=") + readEnd + 1
                data.append(int(line[key][readStart : ]))
                self.data[key].append(data)
        
        allCoords = []
        allCoords += self.data["sensors"]
        allCoords += self.data["beacons"]
        # print(allCoords)
        # print(min(allCoords, key = lambda coords: coords[1])[1] - 1, min(allCoords, key = lambda coords: coords[0])[0] - 1)
        boardShape0 = max(allCoords, key = lambda coords: coords[1])[1] - min(allCoords, key = lambda coords: coords[1])[1] * sign(min(allCoords, key = lambda coords: coords[1])[1]) - 1
        boardShape1 = max(allCoords, key = lambda coords: coords[0])[0] - min(allCoords, key = lambda coords: coords[0])[0] * sign(min(allCoords, key = lambda coords: coords[0])[0]) - 1
        print(boardShape0, boardShape1)
        print(boardShape0, boardShape1)
        self.__create_board__(boardShape0, boardShape1)
        # print(self.board.shape)
        self.__board_offset__()
        
        midPointTranslation = [min([0, min(allCoords, key = lambda coords: coords[0])[0]]), min([0, min(allCoords, key = lambda coords: coords[1])[1]])]
        midPointTranslation = [midPointTranslation[0] - self.boardOffset[1], midPointTranslation[1] - self.boardOffset[0]]
        self.translation = [midPointTranslation[1], midPointTranslation[0]]
        print("TRANSLATION", self.translation)
        modifiedData = {}
        for key in self.data.keys():
            modifiedData[key] = np.array(self.data[key])
            modifiedData[key] = (np.array(modifiedData[key][ : , 1]) - midPointTranslation[1], np.array(modifiedData[key][ : , 0]) - midPointTranslation[0])
            # print(modifiedData[key])
        
            self.__place_s_b__(key, modifiedData[key])
        self.preprocessingFinished = True
        return self
    
    def ping_all(self):
        self.preprocess()
        # print("TRANSLATION", self.translation)
        sensors = [[sensor[1] - self.translation[0], sensor[0] - self.translation[1]] for sensor in self.data["sensors"]]
        # print("SENSORS", sensors)
        for sensorIdx, sensor in enumerate(sensors):
            self.__ping__([sensor[0], sensor[1]])
            # if sensorIdx == 5:
                # self.print_board()
        return self
    
    
    
    
    def ping_all_short(self, row = 10):
        
        #self.data[key][n][0/1] = x/y position of the key for nth + 1 example, 
        yToCheck = row
        
        
        return self
    
    def __count_hash_in_row__(self, row = 10, mode = "count", rangeS = [0, 20]):
       
        #Make one array with indices in rangeS and overwrite said indices with zeros when they are covered by sensors' range. Count zeros in array for a given row for
        #first part. Find non-zero value in rangeSxrangeS for second part.
        
        
        print("\rROW " + str(row), end = "")
        
        if mode == "count":
            self.rowListOfHash = np.array([], dtype = int)
            dataForDistances = zip(self.data["sensors"], self.data["beacons"])        
            dataForDistancesList = list(dataForDistances)
            for sAndB in dataForDistancesList:
                sensorX = sAndB[0][0]
                sensorY = sAndB[0][1]
                # print(sensorX)
                distance = lambda sensorAndBeacon: abs(sensorAndBeacon[0][0] - sensorAndBeacon[1][0]) + abs(sensorAndBeacon[0][1] - sensorAndBeacon[1][1])
                threshold = sensorY + distance(sAndB) - row if row >= sensorY else row - (sensorY - distance(sAndB))
                # print(threshold, distance(sAndB), sensorY)
                if row in range(sensorY, sensorY + distance(sAndB) + 1):
                    
                    # print("HASH", numHash)
                    # self.rowListOfHash += [colIdx for colIdx in range(sensorX - threshold, sensorX + threshold + 1)]
                    toConcat = [colIdx for colIdx in range(sensorX - threshold, sensorX + threshold + 1)]
                    self.rowListOfHash = np.concatenate((self.rowListOfHash, toConcat))
                if row in range(sensorY - distance(sAndB), sensorY):
                    
                    # self.rowListOfHash += [colIdx for colIdx in range(sensorX - threshold, sensorX + threshold + 1)]
                    toConcat = [colIdx for colIdx in range(sensorX - threshold, sensorX + threshold + 1)]
                    self.rowListOfHash = np.concatenate((self.rowListOfHash, toConcat))
                    
            self.rowListOfHash = list(set(self.rowListOfHash))
        # print(self.rowListOfHash)
        
        
            for beacon in self.data["beacons"]:
                if beacon[1] == row: #and beacon[0] in range(rangeS[0], rangeS[1] + 1):
                    try:
                        self.rowListOfHash.pop(self.rowListOfHash.index(beacon[0]))        
                    except:
                        pass
                   
            for sensor in self.data["sensors"]:
                if sensor[1] == row: #and sensor[0] in range(rangeS[0], rangeS[1] + 1):
                    self.rowListOfHash.append(sensor[0])
        
            self.rowListOfHash = np.array(list(set(self.rowListOfHash)))
            # print(row, self.rowListOfHash)
            self.solution1 = len(self.rowListOfHash.tolist()) if (mode == "count" or row == 10) else 0
        
        if mode == "find":
            # print("find")
            toZeroFull = []   
            dataForDistances = zip(self.data["sensors"], self.data["beacons"])        
            dataForDistancesList = list(dataForDistances)
            for sAndB in dataForDistancesList:
                
                # print(sAndB)
                sensorX = sAndB[0][0]
                sensorY = sAndB[0][1]
                # print(sensorX)
                distance = lambda sensorAndBeacon: abs(sensorAndBeacon[0][0] - sensorAndBeacon[1][0]) + abs(sensorAndBeacon[0][1] - sensorAndBeacon[1][1])
                threshold = sensorY + distance(sAndB) - row if row >= sensorY else row - (sensorY - distance(sAndB))
                # print(threshold)
                # print(threshold, distance(sAndB), sensorY)
                # print(row in range(sensorY, sensorY + distance(sAndB) + 1), row in range(sensorY - distance(sAndB), sensorY))
                if row in range(sensorY, sensorY + distance(sAndB) + 1):
                    
                    # print("HASH", numHash)
                    # self.rowListOfHash += [colIdx for colIdx in range(sensorX - threshold, sensorX + threshold + 1)]
                   
                    toZero = [sensorX - threshold if sensorX - threshold >= 0 else 0,  sensorX + threshold if sensorX + threshold <= rangeS[1] + 1 else rangeS[1] + 1]
                    toZeroFull += [toZero] 
                    # self.row[toZero[0] : toZero[1] + 1] = -1
                if row in range(sensorY - distance(sAndB), sensorY):
                    
                    # self.rowListOfHash += [colIdx for colIdx in range(sensorX - threshold, sensorX + threshold + 1)]
                    # toZero = [colIdx for colIdx in range(sensorX - threshold, sensorX + threshold + 1)]
                    toZero = [sensorX - threshold if sensorX - threshold >= 0 else 0, sensorX + threshold if sensorX + threshold <= rangeS[1] + 1 else rangeS[1] + 1]
                    toZeroFull += [toZero] 
                    # while toZero[0] < 0:
                    #     toZero.pop(0)
                    # while toZero[-1] > rangeS[1] + 1:
                    #     toZero.pop(-1)
                    # self.row[toZero[0] : toZero[1] + 1] = -1
            # print("ANY", any(np.array(self.row) != -1))
            toZeroFull = sorted(toZeroFull, key = lambda toZero: toZero[1])
            # print(toZeroFull)
            def connect(lists):
                newLists = []
            
                elem = lists[0]
                for lisT in lists:
                    if elem[1] in range(lisT[0] - 1, lisT[1] + 1):
                        elem = [min(elem[0], lisT[0]), lisT[1]]
                        # print("ELEM", elem)
                    else:
                        newLists.append(elem)
                        elem = [lisT[0], lisT[1]]
                
                
                newLists.append(elem)
                # print("NEW", newLists)               
                return newLists
            
            while toZeroFull != connect(toZeroFull):
                toZeroFull = connect(toZeroFull)    
            
            # print(len(toZeroFull))
            toZeroFullDif = []
            if len(toZeroFull) > 1:
                for elemIdx, elem in enumerate(toZeroFull):
                    if elemIdx + 1 == len(toZeroFull):
                        break
                    toZeroFullDif.append(((toZeroFull[elemIdx + 1][0] - elem[1]) > 1) * (elem[1] + 1 ))
                toZeroFullDif = np.array(toZeroFullDif)
                # print(toZeroFullDif)
                if any(toZeroFullDif > 0):
                        self.col = sum(toZeroFullDif)
        # print(self.solution1, row)
        
        return self
    

    def preprocess_short(self):
        # 
        if self.preprocessingFinished == True:
            return self
        
        if not self.preprocessingFinished:
            self.data = {"sensors": [], "beacons": []}
            self.board = np.array([])
            self.translation = []
    
    
        for line in self.raw:
            line = line.split(": ")
            line = {"sensors": line[0], "beacons": line[1]}
            for key in self.data.keys():
                data = []
                readStart = line[key].index("=") + 1
                readEnd = line[key].index(",")
                data.append(int(line[key][readStart : readEnd]))
                readStart = line[key][readEnd : ].index("=") + readEnd + 1
                data.append(int(line[key][readStart : ]))
                self.data[key].append(data)
        
        allCoords = []
        allCoords += self.data["sensors"]
        allCoords += self.data["beacons"]
        self.preprocessingFinished = True
        
        return self
    
    
    def find_short(self, row = 10, mode = "count", rangeS = [0, 20]):
        # print("prep")
        self.preprocess_short()
        # print("count")
        self.__count_hash_in_row__(row, mode, rangeS)
        return self
    
    def find_beacon(self, mode = "find", rangeS = [0, 20]):
        
        self.tuningFreq = 4000000
        for row in range(rangeS[0], rangeS[1] + 1):
            # print(row)   
            if self.col != -1:
                break
            self.find_short(row, mode, rangeS)
            # print(self.solution1)
            # print(row)    
            if self.col != -1:
                column = self.col
 
                self.beacon = [row, column]
        
            
                self.tuningFreq = self.tuningFreq * self.beacon[1] + self.beacon[0]
        print("TUNING FREQ", self.tuningFreq, "\n", self.beacon)
        
        return self
    
    def find_where_it_isnt(self, row = 10):
        row = row - self.translation[0]
        # print([location in ["#"] for location in self.board[row, : ]])
        # for rowV in range(row - 1, row + 2):
        #     for column in self.board[rowV]:
        #         print(column, end = "")
        #     print()
        # print()
        # print()
        self.solution1 = sum([location in ["#"] for location in self.board[row, : ]])
        print("SOLUTION 1: ", self.solution1)
        return self

# a = "abbbccc"
# print(a[a.index("d") + 1])

def run():
    beacons = Beacons()
    # print("SOLUTION1", beacons.find_short(row = 2000000).solution1)
    beacons.find_beacon(rangeS = [0, 4000000])
    # beacons.find_beacon(rangeS = [0, 20])
    
print(run())

# a = np.arange(25).reshape((5, -1))

# print(np.where(a > 4))

# print(a[([1, 1], [0, 1])])