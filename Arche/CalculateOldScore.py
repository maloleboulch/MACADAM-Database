#!/usr/bin/env python3
# -*- coding: utf-8 -*-

help_string = """
Extract the pwy-inference-description.data from the tar file and rename it by our conventionnal name (TAXID.catRefSeqNumberofccurenceShareoruniqueOriginofPGDBs). Only work for RefSeq PGDB. Needed for old Pathway-Tools Score
"""

import os
import tarfile
import pandas
import csv

#directories by defaults
PGDBsdirectory="./PGDBs/Uniq/"

listofPGDBsTar=[]

for file in os.listdir(PGDBsdirectory):
    if file.endswith("cyc.tsv"):
        print (file)
        listofPGDBsTar.append(file)

def convert_score(pathofthefile,dict,name):
    with open(pathofthefile,"r") as inputfile:
        lLineofPathwayReport=inputfile.readlines()[1:]
    lNewlines=[]
    for line in lLineofPathwayReport:
        line=line.split("\t")
        line[4]=str(round(dict[name][line[1]],9))
        lNewlines.append(line)
    outputfile=open(pathofthefile[:-3]+"tsv","w")
    outputfile.write("Pathway Name \t Pathway Frame-id \t Pathway Class Name \t Pathway Class Frame-id \t Pathway Score \t Pathway Frequency Score \t Pathway Abundance \t Reason to Keep \t Pathway URL\n")
    for item in lNewlines:
        item="\t".join(item)
        outputfile.write(item)



def process_old_score(pathofthefile):
    with open(pathofthefile,"r") as inputfile:
        lPWYDescription=inputfile.read().replace("\n","")

    lPWYDescription=lPWYDescription.split("(:")
    del lPWYDescription[0]

    dPWYtoScore={}
    for element in lPWYDescription:
        element="(:"+element
        lelement=element.split(":")
        del lelement[0]
        if lelement[1]=="KEEP? T ":
            #print (lelement)
            iPresentReaction=int(lelement[24].lstrip().split(" ")[1])
            iTotalReaction=int(lelement[23].lstrip().split(" ")[1])
            iOldscore=(iPresentReaction/iTotalReaction)
            #print (iOldscore)
            dPWYtoScore[lelement[0].lstrip().split(" ")[1]]=iOldscore
    return dPWYtoScore

def pathway_report_data_tar_to_linelist(tarArchives):
    #open a tar file, search the pwy-inference-description.data and put it in a buffer (list of readlines split by | without \n)
    #open tar
    tarArchives=tarfile.open(tarArchives)
    #get all files path
    namesTar=tarArchives.getnames()
    #search pathway-report-data
    for item in namesTar:
        if item.endswith("pwy-inference-description.data"):
            path=item
    #extract and readlines fron pathway-report-data
    pathway_report_data=tarArchives.extractfile(path)
    pathway_report_data=pathway_report_data.readlines()
    listlines=[]
    #decode bytes to string, clean lines and split each line like a csv file
    for line in pathway_report_data:
        line=line.decode("utf-8")
        listlines.append(line)
    return listlines

for file in listofPGDBsTar:
    file=file[:-4]+".tar.gz"
    if file.endswith("cyc.tar.gz"):
        pathway_report_data=pathway_report_data_tar_to_linelist(PGDBsdirectory+file)
        output=open(PGDBsdirectory+file[:-7]+"_data.txt","w")
        for item in pathway_report_data:
            output.write(item)
        output.close()

#Do a list of all pathway-report data name
listofPathwayreportData=[]
for file in os.listdir(PGDBsdirectory):
    if file.endswith("_data.txt"):
        listofPathwayreportData.append(file)

#Create a dict storing all old score for each PGDB ID
dIDtoAllOldScore={}

#Store in a dict all the new Score
for element in listofPathwayreportData:
    dIDtoAllOldScore[element[:-9]]=process_old_score(PGDBsdirectory+element)

###### Warning: After this line change the score of all RefSeq PGDBs
for element in listofPathwayreportData:
    convert_score(PGDBsdirectory+element[:-9]+".tsv",dIDtoAllOldScore,element[:-9])
