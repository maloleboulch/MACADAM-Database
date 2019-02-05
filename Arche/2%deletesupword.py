#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Ce script permet de substituer quelques PGDB supplémentaire en virant les mots joker.

with open("./downloads/MicrocycSubstitution.tsv","r") as inputfile:
    lMicrocycSubstitution=inputfile.readlines()
    lPGDBAllreadyPresent=[]
    for line in lMicrocycSubstitution:
        line=line.split("\t")
        lPGDBAllreadyPresent.append(line[2])



#funique corresponde a la suite du fichier substition. Donc a apenn au fichier
funique=open("./downloads/MicrocycSubstitution.tsv","a")
fMicrocycRemainingRemastered=open("./downloads/MicrocycRemainingRemasteredAfter2.tsv","w")

with open("./downloads/ShareIndex.tsv","r") as inputfile:
    lLinesShareIndex=inputfile.readlines()

#open remaining from Microcyc
with open("./downloads/MicrocycRemainingRemastered.tsv","r") as inputfile:
    lLinesRemaining=inputfile.readlines()

#Goal is to compare name without the strain and with the deletion of sp. strain ssp subsp spp.

#List of word
lWord=[" sp. "," sp "," str. "," str "," spp. "," spp "," subsp "," pv "," pv. "," genomovar. "," genomovar "," bv. "," bv "," serovar "," serovar. "," var "," var. "," substr. "," substr "," strain "]

#Rules:
#No space, no species etc...
#No [], "",'',/,-
#For Sino rhizobium no _2
#No Bioproject ID




#dict Name=PGDB name from RefSeq and one dict for original name
dPGDBNametoName={}
dNametoOriginalName={}
for line in lLinesShareIndex:
    line=line.lower()
    line=line.split("\t")
    dNametoOriginalName[line[0]]=line[2]
    for ch in lWord:
        if ch in line[2]:
            line[2]=line[2].replace(ch," ")
    if "[" in line[2].split(" ")[0]:
        line[2]=line[2].replace("[","")
        line[2]=line[2].replace("]","")
    if "'" in line[2]:
        line[2]=line[2].replace("'","")
    if "/" in line[2]:
        line[2]=line[2].replace("/"," ")
    if "-" in line[2]:
        line[2]=line[2].replace("-"," ")
    line[2]=line[2].replace(" ","")

    dPGDBNametoName[line[2]]=line[0]

#dict Oid = [species,strain] and all in small letter and one dic for original name
dOidtoNameAndStrain={}
dOidtoOriginalName={}
dOidtoTaxID={}
for line in lLinesRemaining:
    line=line.lower()
    line=line.replace("\n","")
    line=line.split("\t")
    dOidtoOriginalName[line[0]]=line[2]+" "+line[3]
    dOidtoTaxID[line[0]]=line[1]
    for ch in lWord:
        if ch in line[2]:
            line[2]=line[2].replace(ch," ")
        if ch in line[3]:
            line[3]=line[3].replace(ch," ")
    if line[3].endswith("_2"):
        line[3]=line[3][:-2]
    if line[3] in line[2]:
        sNameandStrain=line[2]
    else:
        sNameandStrain=(line[2]+" "+line[3])
    if "[" in sNameandStrain.split(" ")[0]:
        sNameandStrain=sNameandStrain.replace("[","")
        sNameandStrain=sNameandStrain.replace("]","")
    if "'" in sNameandStrain:
        sNameandStrain=sNameandStrain.replace("'","")
    if "/" in sNameandStrain:
        sNameandStrain=sNameandStrain.replace("/"," ")
    if "-" in sNameandStrain:
        sNameandStrain=sNameandStrain.replace("-"," ")
    if "prjna" in sNameandStrain:
        sNameandStrain=sNameandStrain.split("prjna")[0]
    sNameandStrain=sNameandStrain.replace(" ","")
    dOidtoNameAndStrain[line[0]]=sNameandStrain

lLeft=[]

for key in dOidtoNameAndStrain:
    if dOidtoNameAndStrain[key] in dPGDBNametoName:
        #Check if we change a second time a PGDB
        if dPGDBNametoName[dOidtoNameAndStrain[key]].replace('u','U').replace('s','S') not in lPGDBAllreadyPresent:
            funique.write(dOidtoOriginalName[key]+"\t"+dNametoOriginalName[dPGDBNametoName[dOidtoNameAndStrain[key]]]+"\t"+dPGDBNametoName[dOidtoNameAndStrain[key]].replace('u','U').replace('s','S')+"\t"+dOidtoTaxID[key]+"\t"+key+"\tToken Word\n")
    else:
        lLeft.append(key)
i=0

for line in lLinesRemaining:
    sOid=line.split("\t")[0]
    if sOid in lLeft:
        fMicrocycRemainingRemastered.write(line)
