#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json
import tarfile
import os
from io import BytesIO


with open("./downloads/MicrocycSubstitution.tsv","r") as fSubtitution:
    lineMicrocyc=fSubtitution.readlines()[1:]

#Create a dic Microcyc ID to PGDBs Name and a list of all PGDBsName
dMicrocycIdtoPGDBnames={}
lPGDBsNames=[]

for line in lineMicrocyc:
    line=line.split("\t")
    dMicrocycIdtoPGDBnames[line[4]]=line[2]
    lPGDBsNames.append(line[2])

#for each Microcyc ID, put the PGDBs associate with the Oid in a buffer and fin the pathway report.
for item in dMicrocycIdtoPGDBnames:
    print (item)
    #Create a byte buffer to store the tar.gz
    tmpfile = BytesIO()
    #request the http object
    request=urllib.request.urlopen("https://www.genoscope.cns.fr/agc/microscope/search/export.php?format=microcyc&O_id="+str(item))

    #Store the tar gz inside the buffer
    while True:
        # Download a piece of the file from the connection
        s = request.read(16384)

        # Once the entire file has been downloaded, tarfile returns b''
        # (the empty bytes) which is a falsey value
        if not s:
            break

        # Otherwise, write the piece of the file to the temporary file.
        tmpfile.write(s)
    request.close()

    # Now that the FTP stream has been downloaded to the temporary file,
    # we can ditch the FTP stream and have the tarfile module work with
    # the temporary file.  Begin by seeking back to the beginning of the
    # temporary file.
    tmpfile.seek(0)

    #open the tar.gz file in the buffer. r:gz allow to search backwards
    Tar=tarfile.open(fileobj=tmpfile, mode="r:gz")
    #Obtain all path file in the tar.gz and find the pathway-report
    namesTar=Tar.getnames()
    for names in namesTar:
        if names.endswith("/pathways-report.txt"):
            path=names

    #extract and readlines fron pathway-reports
    pathways_report=Tar.extractfile(path)
    pathways_report=pathways_report.readlines()
    #open a file with the name of the PGDB to replace
    with open("./Microcyc/"+dMicrocycIdtoPGDBnames[item]+".tsv","w") as outputfile:
        i=0
        for line in pathways_report:
            #decodes bytes to string
            line=line.decode("utf-8")
            #delete empty lines
            if not line=="\n":
                line=line.split("|")
                #for the first line we need to change some of the column's name and position as well as add some extra column
                if i==0:
                    line[4],line[5]=line[5],line[4]
                    line[2]=" Pathway Class Name "
                    line.insert(6," Reason to Keep ")
                    line.insert(6," Pathway Abundance ")
                #for the others lines, change position names and add column with values
                else:
                    line[4],line[5]=line[5],line[4]
                    line.insert(6,"MICROCYC")
                    line.insert(6,"1")
                line="\t".join(line)
                outputfile.write(line)
                i+=1
