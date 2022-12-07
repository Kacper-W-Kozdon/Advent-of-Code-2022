# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:04:29 2022

@author: xBubblex
"""

import re
import numpy as np

def load_files():
    fContent = []
    with open("input7.txt") as f:
        stacks = True
        for (lineIndex, line) in enumerate(f):  #loading the file into an np.array
            if bool(line):
                fContent.append(line.strip("\n").split(" "))
                    
    return(fContent)

class Device:
    def __init__(self):
        self.terminal = load_files()
        self.tree = {"/": dict({})}
        self.cmd = []
        self.args = []
        self.position = []
        self.currentDir = dict({})
        self.keywordsType = {"str": "dir", "int": "file"}
        self.files = []
        
        
    def __change_dir(self):
        print("cd: ", self.args)
        directory = self.args
        print("dir: ", directory)
        if directory[0] == "..":
            print("\ncurrent position: ", self.position, "\n")
            print("\n\n\ndown a dir\n\n\n")
            directory = self.tree
            for dirs in self.position:
                directory = directory[dirs]
            self.position.pop()
        else:
            print("\n\n\nUP A DIR \n\n\n")
            self.position.append(directory[0])
            print("\ncurrent position: ", self.position, "\n")
            print(self.tree["/"].keys())
            directory = self.tree
            print("last tree: ", self.tree)
            for dirs in self.position:
                print(dirs, dirs in list(directory.keys()))
                print(list(directory.keys()))
                directory = directory[dirs] 
                print("\n\n", directory, "\n\n")
 
        self.currentDir = directory
        self.args.pop()
        return self
    
    
    def __create_files(self):
        files = self.files
        print("files3: ", self.files, "\n\n\n")
        directory = self.tree
        print("CURRENT POSITION: ", self.position)
        for dirs in self.position:
            print("DIRSDIRS: ", dirs)
            print(self.tree)
            directory = directory[dirs]
            print("PROBLEM: ", type(directory))
            self.currentDir = directory
        print("\n\n\nFILES TO ADD: \n\n\n", files)
        for file in files:
            print(file[1], file[0] == "dir")
            if file[0] == "dir":
                # self.currentDir[files[1]] = {}
                print(file[0] == 'dir', file[1])
                self.currentDir.update({str(file[1]): dict({})})
            else:
                print("files2: ", files)
                print("PROBLEM: ", self.currentDir)
                if "files" not in list(self.currentDir.keys()):
                    self.currentDir.update({"files": []})
                self.currentDir["files"].append((file[0], file[1]))
        directory = self.currentDir
        self.args.pop()
        return self
    
    def create_tree(self):
        self.cmd = []
        def empty_files():
            print("clearing")
            while len(self.files) > 0:
                self.files.pop()
                print("POPPOPPOPPOPPOPPOP\n\n")
            return self
        
        
        def call_command():
            print("unpacked command: ", self.cmd[0][0])
            
            if self.cmd[0][0] == "cd":
                cd = lambda: self.__change_dir(); self.args.append(self.cmd[0][1]), print("dirargs: ", self.args) 
                print(self.cmd[0][0], self.cmd[0][0] == "cd")
                cd()
                print("changed dir")
            else:
                print("ADDING FILES \n\n\n")
                ls = lambda: self.__create_files(); self.args.append(self.files), print("order2 :", self.args)
                ls()
            return self
        ls = False
        for lineIdx, line in enumerate(self.terminal):
            print("line: ", line)
            print("line[0]: ", line[0])
            # print("current cmd: ", line[1:])
            
            
            if line[0] == "$" and line[1] == "cd" and not ls:
                print("command")
                self.cmd.append(line[1:])
                print("current cmd: ", self.cmd)
                call_command()
                try:
                    empty_files()
                except IndexError:
                    pass
                self.cmd.pop()
            elif line[0] == "$" and line[1] == "cd" and ls:
                print("command")
                self.cmd.append(["ls"])
                call_command()
                try:
                    empty_files()
                except IndexError:
                    pass
                self.cmd.pop()
                print("COMMANDS: ", self.cmd, "\n\n\n")
                self.cmd.append(line[1:])
                print("current cmd: ", self.cmd)
                
                  
                self.cmd.pop()
                ls = False
            elif line[0] == "$" and line[1] == "ls":
                print("command: 'ls'")
                ls = True
                pass
            else:
                print("not a command")
                self.files.append([line[0], line[1]])
                print("files: ", self.files)
            
            
                
            pass
            
        return self
    
    
def run():
    device = Device()
    x = "$"
    print("TREE: ", device.create_tree().tree)
    # print(device.create_tree().tree)



x = lambda: print("abc"); print("xyz"); print("123")
print(x())
print(run())


    

