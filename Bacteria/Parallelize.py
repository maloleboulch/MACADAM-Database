#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from optparse import OptionParser
import os

parser = OptionParser()
#Directory of the GBFF files
parser.add_option("-n" , "--number" , dest="number" , help="Number of gbff per directory")
(options, args) = parser.parse_args()
dnumber = vars(options)
number=int(dnumber["number"])


#path of the GBFF
gbff_global_directory="./gbff/"
lgbfffiles=[]


# list all file with gbff extension
for file in os.listdir(gbff_global_directory):
    if file.endswith(".gbff"):
        lgbfffiles.append(file)

i=0
k=1

#Browse all file
for item in lgbfffiles:
    #If iterator a 0 create a new directery in gbff: ./gbffk
    if i==0:
        os.makedirs(gbff_global_directory+"gbff"+str(k)+"/")
        pathtotemporarygbfffile=gbff_global_directory+"gbff"+str(k)+"/"
        os.makedirs(pathtotemporarygbfffile+"tmp/")
        os.rename(gbff_global_directory+item,pathtotemporarygbfffile+item)
        k+=1
        i+=1
        continue
    if i==number:
        os.rename(gbff_global_directory+item,pathtotemporarygbfffile+item)
        i=0
        continue
    else:
        os.rename(gbff_global_directory+item,pathtotemporarygbfffile+item)
        i+=1
        continue

qarrayfile=open("sarray.sh","w")

for file in os.listdir(gbff_global_directory):
    #change path (Needed on genotoul cluster for pathway tools) + +command for pathway
    qarrayfile.write("module load system/Python-3.6.3;time python3 buildPGDB.py " "-g ./gbff/"+file+"/ "+"-t ./gbff/"+file+"/tmp/ "+"\n")

qarrayfile.close
