#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

def Append_one():
    #this script take one of the duplicates if the duplicate have a species name

    dLineDuplicates={}
    lDeletedPGDBs=[]
    #create a dict to link Accession to line
    with open("downloads/duplicate_Entries.tsv","r") as fDuplicateEntries:
        for line in fDuplicateEntries:
            linesplit=line.split("\t")
            if linesplit[8]:
                dLineDuplicates[linesplit[0]]=line
            else:
                lDeletedPGDBs.append(linesplit[0])

    dTaxtoAccession={}
    i=0
    #create a dict to link Tax to acession number
    for key in dLineDuplicates:
        line=dLineDuplicates[key].split("\t")
        tax=[line[7],line[8],line[9]]
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

    lChoosen=[]
    #If all the duplicates have the same taxID so take the first one (arbitrary)
    #Else if different taxID so take the most precise one (TaxID!=ParentTaxID)
    for key in dTaxtoAccession:
        lTaxId=[]
        lParentTaxId=[]
        for item in dTaxtoAccession[key]:
            lTaxId.append(dLineDuplicates[item].split("\t")[5])
        #if same taxID
        if len(set(lTaxId))==1:
            lChoosen.append(dTaxtoAccession[key][0])
        #if not:
        else:
            #store Parent TaxID
            for item in dTaxtoAccession[key]:
                lParentTaxId.append(dLineDuplicates[item].split("\t")[6])
            #take the one without the same as parent. Attention le cas ou il y a deux taxID précis n'est pas géré.
            for item in lTaxId:
                if item not in lParentTaxId:
                    for assembly in dTaxtoAccession[key]:
                        if dLineDuplicates[assembly].split("\t")[5]==item:
                            lChoosen.append(assembly)
    return lChoosen

lChoosen=Append_one()

lAccessionDouble=[]
#Store accesion number of duplicated organism
with open("downloads/duplicate_Entries.tsv","r") as fDuplicateEntries:
    for line in fDuplicateEntries:
        sAccessionDouble=line.split("\t")[0]
        lAccessionDouble.append(sAccessionDouble)



lSharedTaxID=[]
#Store accesion number of organisms with shared TaxID
with open("downloads/sharedTaxID.tsv","r") as fSharedTaxID:
    for line in fSharedTaxID:
        sAccession=line.split("\t")[0]
        if sAccession not in lAccessionDouble:
            lSharedTaxID.append(sAccession)

lSharedTaxID.extend(lChoosen)

luniqueTaxID=[]
#Store accesion number of organisms with uniq TaxID
with open("downloads/uniqueTaxID.tsv","r") as funiqueTaxID:
    for line in funiqueTaxID:
        sAccession=line.split("\t")[0]
        if sAccession not in lAccessionDouble:
            luniqueTaxID.append(sAccession)

luniqueTaxID.extend(lChoosen)

dcomplete_genome_data={}
#store all lines of complete genome
with open("downloads/complete_genome_data.tsv","r") as fcomplete_genome_data:
    for line in fcomplete_genome_data:
        sAccession=line.split("\t")[0]
        dcomplete_genome_data[sAccession]=line
        # if sAccession in lAccessionDouble:
        #     lcomplete_genome_data.append(sAccession)
        #     i+=1

#remake the complete genomes data files without duplicates
fSharedTaxID=open("downloads/sharedTaxID.tsv","w")
funiqueTaxID=open("downloads/uniqueTaxID.tsv","w")

#generate new shareindex+uniqindex+completegenomedata without duplicates
with open("downloads/complete_genome_data.tsv","w") as fcomplete_genome_data:
    fcomplete_genome_data.write(dcomplete_genome_data["# assembly_accession"])
    for key in dcomplete_genome_data:
        #for the new sharedTaxID file and complete genome data
        if key in lSharedTaxID:
            fcomplete_genome_data.write(dcomplete_genome_data[key])
            fSharedTaxID.write(dcomplete_genome_data[key])
        elif key in luniqueTaxID:
            #for the new UniqID file
            fcomplete_genome_data.write(dcomplete_genome_data[key])
            funiqueTaxID.write(dcomplete_genome_data[key])
        #uncomment this line for delete all duplicates!
        elif key !="# assembly_accession" :
            os.remove("PGDBs/g"+key[4:-2]+"cyc.tar.gz")
