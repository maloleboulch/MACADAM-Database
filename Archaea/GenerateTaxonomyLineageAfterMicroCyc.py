#!/usr/bin/env python3
# -*- coding: utf-8 -*-

help_string = """
A faire plus tard
"""

import os
import sys

#Attention! nodes.dmp et names.dmp doit être dans le dossier downloads. Ils viennent du NCBI taxonomy
#open nodes.dmp
fNodes=open("downloads/nodes.dmp","r")
lineNodes=fNodes.readlines()
fNames=open("downloads/names.dmp","r")
lineNames=fNames.readlines()
fShareIndex=open("downloads/ShareIndex2.tsv","r")
lineShareIndex=fShareIndex.readlines()
fNamesRemastered=open("downloads/namesremastered.dmp","w")
fNodesRemastered=open("downloads/nodesremastered.dmp","w")
fShareIndexAfterLineage=open("downloads/ShareIndexAfterLineage.tsv","w")

#create a dictionary to store [taxID]=[parent,rank]
dNodes={}

for line in list(lineNodes):
    line=line.split("\t|\t")
    dNodes[line[0]]=[line[1],line[2]]



#search lineage for a taxID
#Careful the dict has a string as key and not a int
def lineage(TaxID):
    dLineage={}
    dLineage=dLineage.fromkeys(["superkingdom","phylum","class","order","family","genus","species"])
    rank=["superkingdom","phylum","class","order","family","genus","species"]
    dLineage[dNodes[TaxID][1]]=TaxID
    sUniqueTaxID=set()
    lineage=[]
    lineage.insert(0,TaxID)
    print (TaxID)
    while TaxID!="1":
        sUniqueTaxID.add(TaxID)
        value=dNodes[TaxID]
        if value[1] in rank:
            dLineage[value[1]]=TaxID
            lineage.insert(0,TaxID)
        TaxID=value[0]

    return dLineage,sUniqueTaxID

#Shareindex.tsv extract all unique TaxID of PGDBs
lTaxID=[]
for item in list(lineShareIndex):
    lTaxID.append(item.split(".")[0])

sTaxID=set(lTaxID)

#print ("218495" in sTaxID)

#make a dict with the lineage of all unique taxID and make a set of all
dLineageTaxID={}
sAllTaxID=set()
for item in sTaxID:
    temp=lineage(item)
    dLineageTaxID[item]=temp[0]
    sAllTaxID=sAllTaxID.union(temp[1])

#Add Root to set
sAllTaxID.add("1")

#write different nodes.dmp and names.dmp with only TaxID of our database for decreasing calculations
for line in list(lineNodes):
    if line.split("\t|\t")[0] in sAllTaxID:
        fNodesRemastered.write(line)
for line in list(lineNames):
    if line.split("\t|\t")[0] in sAllTaxID:
        fNamesRemastered.write(line)

#Write Lineage for Share Index:
for line in list(lineShareIndex):
    TaxID=line.split(".")[0]
    dTemp=dLineageTaxID[TaxID]
    for key in dTemp:
        if dTemp[key] is None:
            dTemp[key]="NaN"
    newline=line[:-2]+"\t"+dTemp['superkingdom']+"\t"+dTemp['phylum']+"\t"+dTemp['class']+"\t"+dTemp['order']+"\t"+dTemp['family']+"\t"+dTemp['genus']+"\t"+dTemp['species']+"\n"
    fShareIndexAfterLineage.write(newline)
