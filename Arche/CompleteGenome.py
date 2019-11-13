#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Select only latest complete Genome from assembly_summary
#Split unique species with unique

import os

print ("All complete genome")

#open assembly summary
f=open("downloads/assembly_summary.txt","r")

#open file for writing resultats
#Complete genomes=Assembly_summary remastered for containing only complete genomes
#ftpdirpaths is the file with the path of the gbff file of each genomes
#uniqueTaxID contains all refSeq entry with unique taxid
#sharedTaxID contains all RefSeq entry with a non unique taxID and ParentTaxID=Taxid of the strain

ftpdirpaths=open("downloads/ftpdirpaths.txt","w")
g=open("downloads/complete_genome_data.tsv","w")
uniqueTaxID=open("downloads/uniqueTaxID.tsv","w")
SharedTaxID=open("downloads/sharedTaxID.tsv","w")


#The first line is not read (line about the readme)
summary=f.readlines()[1:]
for line in summary:
    list=line.split("\t")
    #Only complete genomes are kept
    if list[0]=="# assembly_accession":
        g.write(line)
    if list[11]=="Complete Genome":
        if list[10]=="latest":
            g.write(line)
g.close()

###### Script for deleting duplicates Organims from complegenomes

fCompleteGenomes=open("downloads/complete_genome_data.tsv","r")
lCompleteGenomes=fCompleteGenomes.readlines()
fCompleteGenomes.close()


#All organisms which is duplicates except the reference and representative genomes
frejete=open("downloads/Rejected_entries.tsv","w")
#All duplicated organism in RefSeq but with no reference or reprensentative in the duplicates list
fDuplicateEntries=open("downloads/duplicate_Entries.tsv","w")
#New complete_genome_data.tsv
fhypotheticcomplete=open("downloads/complete_genome_data.tsv","w")

#write headers and delete from list
fhypotheticcomplete.write(lCompleteGenomes[0])
del lCompleteGenomes[0]



#create a dict Accesion Number = Liste(Line)
dAccesionNumbertoLine={}
for line in lCompleteGenomes:
    line=line.split("\t")
    dAccesionNumbertoLine[line[0]]=line

dTaxtoAccession={}

#create a dict with tax to acession and merged Species named with strain name
for key in dAccesionNumbertoLine:
    tax=[dAccesionNumbertoLine[key][7],dAccesionNumbertoLine[key][8],dAccesionNumbertoLine[key][9]]
    if "strain=" in tax[1]:
        tax[1]=tax[1].replace("strain=","")
    if tax[1] in tax[0]:
        if tax[0] in dTaxtoAccession:
            dTaxtoAccession[tax[0]].append(key)
        else:
            dTaxtoAccession[tax[0]]=[key]
    else:
        tax[0]=tax[0]+" "+tax[1]
        if tax[0] in dTaxtoAccession:
            dTaxtoAccession[tax[0]].append(key)
        else:
            dTaxtoAccession[tax[0]]=[key]



#keep reference and representative genomes and hold the others
#make a list for deleting entries in the dict after. To identify duplicate taxonomy with no representative or reference genomes
#Make a list with accession number
lDuplicatedAccession=[]
lGoodTax=[]
for key in dTaxtoAccession:
    if len(dTaxtoAccession[key]) >= 2:
        for item in dTaxtoAccession[key]:
            #add to the index if reference genome
            if "reference genome" in dAccesionNumbertoLine[item][4]:
                fhypotheticcomplete.write("\t".join(dAccesionNumbertoLine[item]))
                lGoodTax.append(key)
            #add to the index if representative genome
            elif "representative genome" in dAccesionNumbertoLine[item][4]:
                fhypotheticcomplete.write("\t".join(dAccesionNumbertoLine[item]))
                lGoodTax.append(key)
            else:
                frejete.write("\t".join(dAccesionNumbertoLine[item]))
                lDuplicatedAccession.append(dAccesionNumbertoLine[item][0])

    else:
        for item in dTaxtoAccession[key]:
            fhypotheticcomplete.write("\t".join(dAccesionNumbertoLine[item]))
            lGoodTax.append(str(key))

for item in lGoodTax:
    dTaxtoAccession.pop(item,None)

#delete entries with no strain name and no isolate name. Add the rest to complete genomes file and in a duplicated_entries files
for key in dTaxtoAccession:
    for item in dTaxtoAccession[key]:
        line=dAccesionNumbertoLine[item]
        if not (line[8] == '' and line[9] == ''):
            fDuplicateEntries.write("\t".join(dAccesionNumbertoLine[item]))
            fhypotheticcomplete.write("\t".join(dAccesionNumbertoLine[item]))
        else:
            if line[0] not in lDuplicatedAccession:
                frejete.write("\t".join(dAccesionNumbertoLine[item]))

frejete.close()
fDuplicateEntries.close()
fhypotheticcomplete.close()

################


g=open("downloads/complete_genome_data.tsv","r")
summary=g.readlines()[1:]
taxid=[]
for line in summary:
    line=line.split("\t")
    if line[5]!=line[6]:
        taxid.append(line[5])

uniq=set([x for x in taxid if taxid.count(x)==1])

for line in summary:
    split=line.split("\t")
    ftpdirpaths.write(split[19]+"\n")
    if split[5] in uniq:
        uniqueTaxID.write(line)
    else:
        SharedTaxID.write(line)
