#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json
import tarfile
import os
from io import BytesIO
from shutil import copyfile


with open("./downloads/MicrocycSubstitution.tsv","r") as fSubtitution:
    lineMicrocyc=fSubtitution.readlines()[1:]

#Create a dic Microcyc ID to PGDBs Name and a list of all PGDBsName
dMicrocycIdtoPGDBnames={}
lPGDBsNames=[]

for line in lineMicrocyc:
    line=line.split("\t")
    dMicrocycIdtoPGDBnames[line[4]]=line[2]
    lPGDBsNames.append(line[2])

#open the ShareIndex and stock the lines.
with open("./downloads/ShareIndex.tsv","r") as fShareindex:
    lineShareIndex=fShareindex.readlines()


#Rewrite ShareIndex with the substitute PGDBs and move and rename pathway reports of this PGDBs.
with open("./downloads/ShareIndex2.tsv","w") as outputfile:
    for line in lineShareIndex:
        line = line.split("\t")
        if line[0] in lPGDBsNames:
            PGDBsNameforPop=line[0]
            FileName=line[0]
            #Add the proper suffix to Microcyc pathway reports name
            line[0]=line[0][:-3]+"mic"
            #move the file and rename it
            os.rename("./Microcyc/"+FileName+".tsv","./PGDBs/Uniq/"+FileName+".tsv")
            os.rename("./PGDBs/Uniq/"+FileName+".tsv","./PGDBs/Uniq/"+line[0]+".tsv")
            line="\t".join(line)
            outputfile.write(line)
            #pop the occurence in lPGDBsNames for later
            print (PGDBsNameforPop)
            lPGDBsNames.remove(PGDBsNameforPop)
        else:
            line="\t".join(line)
            outputfile.write(line)

#Integrate other file who are new (not substitution)
#Store in a dict all infos for the PGDB of the tip of taxonomy
dPGDBtiptoInfos={}

for line in lineMicrocyc:
    line=line.split("\t")
    if line[2] in lPGDBsNames:
        if line[5]=="Tip of the taxonomy\n":
            dPGDBtiptoInfos[line[2]]=[line[0],line[4]]

#Append to share Index
ftest=open("./downloads/ShareIndex2.tsv","a")

for item in dPGDBtiptoInfos:
    sTax=dPGDBtiptoInfos[item][0]
    sOid=dPGDBtiptoInfos[item][1]
    ftest.write(item+"\t1\t"+sTax+"\t"+"Microcyc: "+sOid+"\t"+"Uniq\n")
    os.rename("./Microcyc/"+item+".tsv","./PGDBs/Uniq/"+item+".tsv")
