import os
import subprocess
import shlex
import re
import string
import json

def randomfunc():
    #Testing import
    print("Printing from txtfileprocessing.py!")

#To append the vectors into vectors.txt

def symbolizeAndVectorizeToFile(filevectors,path):
    randomfile = "vector.txt"
    rf = open(path+"/"+randomfile,"a+")
    #rf.write(json.dumps(numdict))
    for i in range(0,len(filevectors)-1):
        rf.write("%s," % str(filevectors[i]))
    rf.write(str(filevectors[len(filevectors)-1]))
    rf.write("\n")
    #data = json.load(rf)
    rf.close()

def symbolizeAndVectorize(filetoopen,path):
    keywordsfile = "keywordsdict.txt"
    kfdread = open(keywordsfile,"r+")
    keywords = json.load(kfdread)
    
    content = []
    opcodes = []
    filevectors = []
    with open(path+"/"+filetoopen) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        #content - an array of lines from the file that was opened
    for line in content:
        if not ("\t" in line):
            continue
        templist = line.split("\t")
        tempstr = templist[2]
        tempstr = " ".join(tempstr.split())
        templist = re.split(',',tempstr)
        for i in range(0,len(templist)):
            try:
                hexnum = int(templist[i],16)
                templist[i] = "num"
            except ValueError:
                continue
        templist2 = templist[0].split()
        opcodestr = templist2.pop(0)
        opcodes.append(opcodestr)
        
        tempstr2 = " ".join(templist2)
        templist[0] = tempstr2
        templist.insert(0,opcodestr)
        operand1 = templist[1].split()
        
        operand2 = []
        try:
            operand2 = templist[2].split()
        except IndexError:
            operand2.append('')
        lines = opcodes+operand1+operand2
        opcodes = []
        
        for i in range(0,len(lines)):
            if str(lines[i]).startswith("<"):
                lines[i] = "num"
            elif str(lines[i]).startswith("["):
                lines[i] = "num"
            try:
                hexnum = int(lines[i],16)
                lines[i] = "num"
            except ValueError:
                continue
        
        for j in range(len(lines)):
            if lines[j] in keywords:
                lines[j] = keywords[lines[j]]
            if lines[j] != '':
                filevectors.append(lines[j])
        
        
    kfdread.close()
    symbolizeAndVectorizeToFile(filevectors,path)

