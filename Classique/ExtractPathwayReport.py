#!/usr/bin/env python3
# -*- coding: utf-8 -*-

help_string = """
Extract the pathway report from the tar file and rename it by our conventionnal name (TAXID.catRefSeqNumberofccurenceShareoruniqueOriginofPGDBs). Only work for RefSeq PGDB
"""

import os
import tarfile
import pandas
import csv

#directories by defaults
PGDBsdirectory="./PGDBs/Uniq/"

listofPGDBsTar=os.listdir(PGDBsdirectory)


def pathways_report_tar_to_linelist(tarArchives):
    #open a tar file, search the pathway-reports.txt and put it in a buffer (list of readlines split by | without \n)
    #open tar
    tarArchives=tarfile.open(tarArchives)
    #get all files path
    namesTar=tarArchives.getnames()
    #search pathway-reports
    for item in namesTar:
        if item.endswith("/pathways-report.txt"):
            path=item
    #extract and readlines fron pathway-reports
    pathways_report=tarArchives.extractfile(path)
    pathways_report=pathways_report.readlines()
    listlines=[]
    #decode bytes to string, clean lines and split each line like a csv file
    for line in pathways_report:
        line=line.decode("utf-8")
        line=line.replace("\n","")
        #delete commentary lines from pathways_report
        if line.startswith("#"):
            pass
        else:
            line=line.split("|")
            listlines.append(line)
    #filter empty strings
    listlines = [x for x in listlines if x != ['']]
    return listlines

for file in listofPGDBsTar:
    if file.endswith("cyc.tar.gz"):
        try:
            pathway_report=pathways_report_tar_to_linelist(PGDBsdirectory+file)
            output=open(PGDBsdirectory+file[:-7]+".tsv","w")
            for item in pathway_report:
                line = "\t".join(item)
                line = line + "\n"
                output.write(line)
        except:
            print ("Missing Pathway report: "+file)
