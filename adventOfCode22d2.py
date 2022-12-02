# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 16:30:56 2022

@author: xBubblex
"""

import numpy as np
import re
import time
import unicodedata
from sympy.combinatorics.partitions import Partition
from sympy.combinatorics.permutations import Permutation


def load_files():
    fContent = []
    with open("input2.txt") as f:
            for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
                if bool(line.strip("\n").split()):
                    # print(line.strip("\n").split("|"))
                    fContent.append(line.strip("\n").split(" | "))  #splitting each entry into coordinates
    return(fContent)

# print("".join(load_files()[0][0].split(" "))[0])

class RockPaperScissors:
    def __init__(self, gamesData = load_files()):
        self.firstP = ["".join(line[0].split(" "))[0] for line in gamesData]
        self.secondP = ["".join(line[0].split(" "))[1] for line in gamesData]
        self.noGames = len(self.firstP)
        self.translate = {"X": "A", "Y": "B", "Z": "C"}
        self.plays = ["A", "B", "C"]
        self.results = []
        self.score = 0
        
     
    def reset(self):
        self.results = []
        self.score = 0
        return self
     
    def games(self):
        return [[self.firstP[idx], self.secondP[idx]] for idx in range(self.noGames)]
        
    def translated(self):
        self.secondP = list(map(lambda pick: self.translate[pick], self.secondP)) if self.secondP[0] not in ["A", "B", "C"] else self.secondP
        return self
        
    def play(self, ruleset = 0):
        
        test_rules = lambda gRound: [0, 3, 6][gRound[1] - gRound[0]] + gRound[1]
        # The one-liner above and the function below should be equivalent for ruleset == 0
        def rules(game):
            score = [0, 3, 6]
            win = score[2]
            draw = score[1]
            lose = score[0]
            gameResult = game[1] - game[0]
            gameResultSign = [-1, 0, 1]
            loseWin = [lose, draw, win] if ruleset == 1 else [draw, win, lose]
            winningPlay = game[0] + gameResultSign[game[1]]
            winningPlay = winningPlay % 3 if winningPlay == 3 else winningPlay
            roundScore = loseWin[game[1]] + [1, 2, 3][winningPlay] if ruleset == 1 else loseWin[gameResult] + game[1] + 1 
            
            return roundScore
            
        self.translated()
        minValGame = ord("A")
        games = self.games()
        for game in games:
            # print("game: ", game)
            # print(game)
            game = list(map(lambda ltr: ord(ltr), game))
            game = (np.array(game) - minValGame).tolist()
            # print(game)
            self.results.append(rules(game))
        return self
    
    # def play2(self):
        
    #     test_rules = lambda gRound: [0, 3, 6][gRound[1] - gRound[0]] + gRound[1]
    #     # The one-liner above and the function below should be equivalent
    #     def rules(game):
    #         score = [0, 3, 6]
    #         win = score[2]
    #         draw = score[1]
    #         lose = score[0]
    #         gameResult = game[1] - game[0]
    #         gameResultSign = [-1, 0, 1]
    #         loseWin = [lose, draw, win]
    #         winningPlay = game[0] + gameResultSign[game[1]]
    #         winningPlay = winningPlay % 3 if winningPlay == 3 else winningPlay
    #         # print(game[1], game[0], winningPlay, "points: ", loseWin[game[1]], "+", [1, 2, 3][winningPlay])
    #         roundScore = loseWin[game[1]] + [1, 2, 3][winningPlay]
            
    #         return roundScore
            
        self.translated()
        minValGame = ord("A")
        games = self.games()
        for game in games:
            # print("game: ", game)
            # print(game)
            game = list(map(lambda ltr: ord(ltr), game))
            game = (np.array(game) - minValGame).tolist()
            # print(game)
            self.results.append(rules(game))
        return self
    
    def total_score(self):
        self.score = sum(self.results)
        return self
    
        
def run():
    playGames = RockPaperScissors()
    # print(playGames.secondP)
    # print(playGames.translated().games())
    print(playGames.reset().play().total_score().score)
    print(playGames.reset().play(1).total_score().score)

    # print(playGames.secondP)
    # print(playGames.secondP)

print(run())

# print(ord("A"))
# print(list(map(lambda x: ord(x), ["A", "C", "D"])))