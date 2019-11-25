import re
import os
import sys


with open("../MandatoryFile/names.dmp","r") as inputfile:
    lLinesNamesRemastered=inputfile.readlines()

#create a dict with TaxID=[parent TaxID,Rank]
dTaxIDtoParentandRank={}
with open("../MandatoryFile/nodes.dmp","r") as inputfile:
    lLinesNodesRemastered=inputfile.readlines()
    for line in lLinesNodesRemastered:
        line=re.split("\t\|\t|\t|\n",line)
        dTaxIDtoParentandRank[line[0]]=[line[1],line[2]]

dTaxIDtoParentandRank["2323"]=['2', 'phylum']

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

dAllLineage={}
for key in dTaxIDtoParentandRank:
    dAllLineage[key]=lineage(key)

dTemp={}
for key in dAllLineage:
    if dAllLineage[key][0]["phylum"]!="2323":
        dTemp[key]=dAllLineage[key]

dAllLineage=dTemp

setOfAllTaxIDofBacteria=set()
for key in dAllLineage:
    if dAllLineage[key][0]["superkingdom"]=="2157":
        setOfAllTaxIDofBacteria.update(dAllLineage[key][1])

setOfAllTaxIDofBacteria.update("1")
setOfAllTaxIDofBacteria.update("131567")

with open("./DatabaseTSV/allnamesremasteredImport.tsv","w") as outputfile:
    #No header for SQLite import
    #outputfile.write("taxID\tname\tparent\ttypeOfName\n")
    for line in lLinesNamesRemastered:
        line=re.split("\t\|\t|\t|\n",line)
        if line[0] in setOfAllTaxIDofBacteria:
            if line[0]!="1":
                ##Create Lineage
                lineage=str(dAllLineage[line[0]][0]["superkingdom"])+"."+str(dAllLineage[line[0]][0]["phylum"])+"."+str(dAllLineage[line[0]][0]["class"])+"."+str(dAllLineage[line[0]][0]["order"])+"."+str(dAllLineage[line[0]][0]["family"])+"."+str(dAllLineage[line[0]][0]["genus"])+"."+str(dAllLineage[line[0]][0]["species"])+"."
                while 1:
                    if lineage.endswith("None."):
                        lineage=lineage[:-5]
                    else:
                        break
                lineage=lineage.replace("None","NaN")
                #Write
                outputfile.write(line[0]+"\t"+line[1]+"\t"+line[3]+"\t"+dTaxIDtoParentandRank[line[0]][0]+"\t"+dTaxIDtoParentandRank[line[0]][1]+"\t"+lineage+"\n")
