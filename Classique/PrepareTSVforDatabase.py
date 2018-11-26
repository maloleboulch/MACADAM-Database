#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#remastered file for correspondance between TaxID and Name

import re
import os
import sys


with open("./downloads/namesremastered.dmp","r") as inputfile:
    lLinesNamesRemastered=inputfile.readlines()

#create a dict with TaxID=[parent TaxID,Rank]
dTaxIDtoParentandRank={}
with open("./downloads/nodesremastered.dmp","r") as inputfile:
    lLinesNodesRemastered=inputfile.readlines()
    for line in lLinesNodesRemastered:
        line=re.split("\t\|\t|\t|\n",line)
        dTaxIDtoParentandRank[line[0]]=[line[1],line[2]]




#Write the file ready to import: TaxID Name Type of Name
with open("./DatabaseTSV/namesremasteredImport.tsv","w") as outputfile:
    #No header for SQLite import
    #outputfile.write("taxID\tname\ttypeOfName\n")
    for line in lLinesNamesRemastered:
        line=re.split("\t\|\t|\t|\n",line)
        outputfile.write(line[0]+"\t"+line[1]+"\t"+line[3]+"\t"+dTaxIDtoParentandRank[line[0]][0]+"\t"+dTaxIDtoParentandRank[line[0]][1]+"\n")

#write the file needed for the other table:

#First list all Pathway reports files in the PGDBs/Uniq directory and insert it in a dictionnary.
temp=os.listdir("./PGDBs/Uniq/")
lListOfPathwayReportsFiles=[]

#take only TSV files
for element in temp:
    if element.endswith(".tsv"):
        lListOfPathwayReportsFiles.append(element)


# Load all lines of each ID in a dic
dUniqIDtoPathway={}

for element in lListOfPathwayReportsFiles:
    with open("./PGDBs/Uniq/"+element,"r") as inputfile:
        lLinesPathwayReports=inputfile.readlines()[1:]
        dUniqIDtoPathway[element[:-4]]=lLinesPathwayReports

#Count the number of pathway of each ID
dIdLineCount={}

for key in dUniqIDtoPathway:
    sCount=str(len(dUniqIDtoPathway[key]))
    dIdLineCount[key]=sCount
    lListofLines=[]
    for line in dUniqIDtoPathway[key]:
        line=line.split("\t")
        del line[-1]
        del line[3]
        del line[2]
        del line[0]
        lListofLines.append("\t".join(line))
    dUniqIDtoPathway[key]=lListofLines

print (dUniqIDtoPathway)



#Load ShareIndexAfterLineage into a dict with uniq ID as key
with open("./downloads/ShareIndexAfterLineage.tsv","r") as inputfile:
    lLineShareIndex=inputfile.readlines()

dShareIndex={}

for line in lLineShareIndex:
    line=line.split("\t")
    dShareIndex[line[0]]=line

#Open the count of different PGDB per Species TaxID
with open("./DatabaseTSV/CountSpeciesID.tsv","r") as inputfile:
    lLineCountSpecies=inputfile.readlines()

dCountperSpecies={}
for line in lLineCountSpecies:
    line=line.split("\t")
    dCountperSpecies[line[0]]=line[1].replace("\n","")



#Generate lines for the table
with open("./DatabaseTSV/PathwayTable.tsv","w") as outputfile:
    #No header for SQLite import
    #outputfile.write("taxonomy\tId\tstrainName\tnumberOfPGDBInSpecies\tnumberOfPathway\tpathwayName\tpathwayFrameId\tpathwayClassName\tpathwayClassFrameId\tpathwayScore\tpathwayFrequencyScore\tpathwayAbundance\treasonToKeep\tpathwayURL\n")
    for key in dShareIndex:
        listShareIndex=dShareIndex[key]
        sTaxonomy=".".join(listShareIndex[5:])
        sTaxonomy=sTaxonomy.replace("\n","")+"."
        sSpeciesTaxID=listShareIndex[11].replace("\n","")
        sStrainName=listShareIndex[2]
        for line in dUniqIDtoPathway[key]:
            line=line.split("\t")
            line.pop(3)
            line="\t".join(line)
            outputfile.write(sTaxonomy+"\t"+key+"\t"+sStrainName+"\t"+dCountperSpecies[sSpeciesTaxID]+"\t"+dIdLineCount[key]+"\t"+line+"\n")
