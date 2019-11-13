#!/usr/bin/env python3
# -*- coding: utf-8 -*-

help_string = """
Rename PGDBs to our standards.
"""
import os
import pandas as pd
import re
import math
import sys

PGDBsdirectory="./PGDBs/"
Uniqdirectory=PGDBsdirectory+"Uniq/"
ShareIndex=open("downloads/ShareIndex.tsv","w")

#List all PGDB in the folder
def listallPGDBs (directory):
    list=[]
    for files in os.listdir(directory):
        if files.endswith(".tar.gz"):
            list.append(files)
    return list
#change keys to match outpout of Pathologic for each Dictionnary
def matchpathologicoutput (dictionnary):
    temp={}
    for key in dictionnary:
        temp["g"+key[4:].split(".")[0]]=dictionnary[key]
    dictionnary=temp
    temp=None
    return dictionnary


#load Dataframe
CompleteGenomeDataframe=pd.read_csv("./downloads/complete_genome_data.tsv", sep="\t", header=0)
head=list(CompleteGenomeDataframe.columns.values)
UniqueGenomeDataframe=pd.read_csv("./downloads/uniqueTaxID.tsv", sep="\t", header=None)
UniqueGenomeDataframe.columns=head
ShareGenomeDataframe=pd.read_csv("./downloads/sharedTaxID.tsv", sep="\t", header=None)
ShareGenomeDataframe.columns=head

#list all uniq and shared taxID Pk?
uniqTaxID=UniqueGenomeDataframe["taxid"].tolist()
sharedTaxID=set(ShareGenomeDataframe["taxid"].tolist())

################# Begin workflow for PGDBS with unique TaxID

PGDBsnames=listallPGDBs(PGDBsdirectory)

#Dictionnary of Assembly name=TaxID for unique TaxID, Assembly=RefSeqCat and Assembly = Tax Name
dAssemblyTaxID=UniqueGenomeDataframe.set_index("# assembly_accession").to_dict()
dAssemblyTaxID=UniqueGenomeDataframe.set_index("# assembly_accession")['taxid'].to_dict()
dAssemblyCategory=UniqueGenomeDataframe.set_index("# assembly_accession").to_dict()
dAssemblyCategory=UniqueGenomeDataframe.set_index("# assembly_accession")['refseq_category'].to_dict()
dAssemblyTaxonomy=UniqueGenomeDataframe.set_index("# assembly_accession").to_dict()
dAssemblyTaxonomy=UniqueGenomeDataframe.set_index("# assembly_accession")['organism_name'].to_dict()
dAssemblyAssembly={}

for key in dAssemblyTaxonomy:
    dAssemblyAssembly[key]=key

dAssemblyTaxID=matchpathologicoutput(dAssemblyTaxID)
dAssemblyCategory=matchpathologicoutput(dAssemblyCategory)
dAssemblyTaxonomy=matchpathologicoutput(dAssemblyTaxonomy)
dAssemblyAssembly=matchpathologicoutput(dAssemblyAssembly)

#set abreviation for name of the file
for key in dAssemblyCategory:
    if dAssemblyCategory[key]=="representative genome":
        dAssemblyCategory[key]="rep"
    if dAssemblyCategory[key]=="reference genome":
        dAssemblyCategory[key]="ref"
    if dAssemblyCategory[key]=="na":
        dAssemblyCategory[key]="nan"

#Rename PGDBs if unique TaxID and move it to Uniq folder
for files in PGDBsnames:
    temp=files[:-10]
    if temp in dAssemblyTaxID:
        os.rename(PGDBsdirectory+files,Uniqdirectory+str(dAssemblyTaxID[temp])+"."+str(dAssemblyCategory[temp])+"1"+"Ucyc.tar.gz")
        ShareIndex.write(str(dAssemblyTaxID[temp])+"."+str(dAssemblyCategory[temp])+"1"+"Ucyc"+"\t1\t"+str(dAssemblyTaxonomy[temp])+"\t"+dAssemblyAssembly[temp]+"\tUniq\n")

################# Begin workflow for PGDBS with shared TaxID
PGDBsnames=listallPGDBs(PGDBsdirectory)

ShareGenomeDataframe["OccurencetaxID"]=1
ShareGenomeDataframe["infraspecific_name"]= ShareGenomeDataframe["infraspecific_name"].fillna('')

#Add a column to the dataframe for the number of occurence of the same taxID
dAssemblyOccurence={}
for item in sharedTaxID:
    i=1
    temp=ShareGenomeDataframe.loc[ShareGenomeDataframe['taxid'] == item]
    for index, row in temp.iterrows():
        dAssemblyOccurence[row["# assembly_accession"]]=i
        i+=1


for key in dAssemblyOccurence:
    index=ShareGenomeDataframe.loc[ShareGenomeDataframe["# assembly_accession"] == key].index.tolist()
    ShareGenomeDataframe.at[index[0],"OccurencetaxID"]=dAssemblyOccurence[key]
    #ShareGenomeDataframe.set_value(index[0],["OccurencetaxID"],dAssemblyOccurence[key])

#Dictionnaries of correspondances between name of the PGDBs and assembly names
dAssemblyNameofPGDS={}
lAssemblynumberforShared=ShareGenomeDataframe["# assembly_accession"].tolist()

for element in lAssemblynumberforShared:
    rework=element.split(".")[0]
    rework=re.sub('[^0-9]','', rework)
    rework="g"+rework
    dAssemblyNameofPGDS[rework]=element

#for each files rename it like: taxID.refseq_category/Numberofoccurenceof the taxID/Shared/cyc=PGDBmaison and print an index into downloads
for file in PGDBsnames:
	if file[:-10] in dAssemblyNameofPGDS:
		Assembly=dAssemblyNameofPGDS[file[:-10]]
		Rows=ShareGenomeDataframe.loc[ShareGenomeDataframe["# assembly_accession"] == Assembly]
		if Rows["refseq_category"].values[0]=="representative genome":
			cat="rep"
		if Rows["refseq_category"].values[0]=="reference genome":
			cat="ref"
		if Rows["refseq_category"].values[0]=="na":
			cat="nan"
		occ=Rows["OccurencetaxID"].values[0]
		taxID=Rows["taxid"].values[0]
		os.rename(PGDBsdirectory+file,Uniqdirectory+str(taxID)+"."+str(cat)+str(occ)+"Scyc.tar.gz")

		if Rows["infraspecific_name"].values[0].startswith("strain="):
			strain=str(Rows["infraspecific_name"].values[0]).replace("strain=","")
		else:
			strain=""
		#Check if the strain name is allready in the organisme name and adapt the output
		if strain.lower() in str(Rows["organism_name"].values[0]).lower():
			ShareIndex.write(str(taxID)+"."+str(cat)+str(occ)+"Scyc"+"\t"+str(Rows["OccurencetaxID"].values[0])+"\t"+str(Rows["organism_name"].values[0])+"\t"+dAssemblyNameofPGDS[file[:-10]]+"\tShared\n")
		else:
			ShareIndex.write(str(taxID)+"."+str(cat)+str(occ)+"Scyc"+"\t"+str(Rows["OccurencetaxID"].values[0])+"\t"+str(Rows["organism_name"].values[0])+" "+strain+"\t"+dAssemblyNameofPGDS[file[:-10]]+"\tShared\n")
	else:
		print (file[:-10])

for file in os.listdir("./PGDBs/"):
	if file.endswith(".tar.gz"):
		os.remove(os.path.join("./PGDBs/", file))
