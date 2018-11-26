#!/usr/bin/env python3
# -*- coding: utf-8 -*-

help_string = """
A faire plus tard
"""

import os
import sys
import re


####### update namesremasteredImport.tsv with missing TaxID comming from Faprotax #####

with open("./downloads/names.dmp","r") as inputfile:
    lLinesNames=inputfile.readlines()

#create a dict with TaxID=[parent TaxID,Rank]
dTaxIDtoParentandRank={}
with open("./downloads/nodes.dmp","r") as inputfile:
    lLinesNodes=inputfile.readlines()
    for line in lLinesNodes:
        line=re.split("\t\|\t|\t|\n",line)
        dTaxIDtoParentandRank[line[0]]=[line[1],line[2]]

def lineage(TaxID):
    dLineage={}
    dLineage=dLineage.fromkeys(["superkingdom","phylum","class","order","family","genus","species"])
    rank=["superkingdom","phylum","class","order","family","genus","species"]
    dLineage[dTaxIDtoParentandRank[TaxID][1]]=TaxID
    sUniqueTaxID=set()
    lineage=[]
    lineage.insert(0,TaxID)
    while TaxID!="1":
        sUniqueTaxID.add(TaxID)
        value=dTaxIDtoParentandRank[TaxID]
        if value[1] in rank:
            dLineage[value[1]]=TaxID
            lineage.insert(0,TaxID)
        TaxID=value[0]

    return dLineage,sUniqueTaxID

#TaxId presents in Faprotax
#Open the FAPROTAXTable.tsv
with open("./DatabaseTSV/FAPROTAXTable.tsv","r") as inputfile:
    lLinesFaprotaxTable=inputfile.readlines()
    setTipTaxIDofFaprotax=set()
    for line in lLinesFaprotaxTable:
        line=line.split("\t")
        setTipTaxIDofFaprotax.add(line[1])


setofAllTaxIDFaprotax=set()
for item in setTipTaxIDofFaprotax:
    TaxIDs=lineage(item)[1]
    setofAllTaxIDFaprotax.update(TaxIDs)
#setofAllTaxIDFaprotax contains all Faprotax TaxID (includes no rank taxID)

#open namesremasteredimport.tsv for import all taxID all ready presents
with open("./DatabaseTSV/namesremasteredImport.tsv","r") as inputfile:
    setofPresentTaxID=set()
    lLines=inputfile.readlines()
    for line in lLines:
        line=line.split("\t")
        setofPresentTaxID.add(line[0])

setofUniqueTaxIDofFaprotax=set(setofAllTaxIDFaprotax-setofPresentTaxID)


#lineage of taxid unique to Faprotax
with open("./DatabaseTSV/namesremasteredImport.tsv","a") as outputfile:
    for line in lLinesNames:
        line=re.split("\t\|\t|\t|\n",line)
        if line[0] in setofUniqueTaxIDofFaprotax:
            outputfile.write(line[0]+"\t"+line[1]+"\t"+line[3]+"\t"+dTaxIDtoParentandRank[line[0]][0]+"\t"+dTaxIDtoParentandRank[line[0]][1]+"\n")




#add to nameremastered
