#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#this script generate two files. the number of PGDBs for each TAXID and the others the number of PGDBs per Species TaxID

with open("./downloads/ShareIndexAfterLineage.tsv","r") as inputfile:
    lLineShareIndex=inputfile.readlines()

lID=[]
lSpeciesID=[]

for line in lLineShareIndex:
    line=line.replace("\n","")
    line=line.split("\t")
    ID=line[0].split(".")[0]
    lID.append(ID)
    lSpeciesID.append(line[11])

sID=set(lID)
sSpeciesID=set(lSpeciesID)

#dictionnaries for counting occurences
dID={}
dSpeciesID={}


for item in sID:
    occurencies=lID.count(item)
    dID[item]=occurencies

for item in sSpeciesID:
    occurencies=lSpeciesID.count(item)
    dSpeciesID[item]=occurencies

with open("./DatabaseTSV/CountTaxID.tsv","w") as outputfile:
    for key in dID:
        outputfile.write(key+"\t"+str(dID[key])+"\n")


with open("./DatabaseTSV/CountSpeciesID.tsv","w") as outputfile:
        for key in dSpeciesID:
            outputfile.write(key+"\t"+str(dSpeciesID[key])+"\n")
