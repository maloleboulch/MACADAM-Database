#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#this script integrate Microcyc in your database. See readme

import urllib.request
import json
from argparse import ArgumentParser

#Output File
fSubstitution=open("./downloads/MicrocycSubstitution.tsv","w")
fSubstitution.write("#Microcyc Name\t#RefSeq Name\t#PGDB Name\t#Microcyc TaxID\t#Microcyc ID\t#Reason to keep\n")

fRemainingData=open("./downloads/MicrocycRemaining.tsv","w")

#option
parser = ArgumentParser()

parser.add_argument("-N", "--New Summary", dest="bNewSummary", action="store_true",default=False,help="If specify then Create a new Microcyc summary")
parser.add_argument("-R", "--RefSeq", dest="bRefSeq", action="store_true",default=False,help="If specify then Microcyc script is not execute")


args = parser.parse_args()

def CreateMicrocycIndex ():
    #Create summary file
    fMicrocycIndex=open("./downloads/MicrocycIndex.tsv","w")

    #get the list of Microcyc organism
    page_source=urllib.request.urlopen("https://www.genoscope.cns.fr/agc/microscope/export/tojson.php?type=organism&value=list")
    print (type(page_source))
    page_source=page_source.read().decode('utf-8')
    print (type(page_source))
    JsonContent=json.loads(page_source)


    fMicrocycIndex.write("Oid\tOtaxon\tOname\tOstrain\tOpgdbname\tOsynonym\n")

    #create a new dict with only bacteria. Arche bacteria or others are discarded. Create a Dict for storing for each Oid the name of the PGDB
    #To access to the PGDB you must request this URL http://www.genoscope.cns.fr/agc/microscope/search/export.php?format=microcyc&O_id=<organisms_identifier>
    #If the organism identifier do not exist or there are no PGDB associate with it, it returns the same file (ACIAD31cyc) and only this (tested by the script analyse.py)
    #Example: 37 doesn't exist and return the PGDB ACIAD31cyc
    #31 Is the real entry of ACIAD31cyc
    #This exception is hardcoded be carreful!
    #Two entries are bad according to Microcyc (1780 and 2780). Create a list for this two number
    lBadOid=["1780","2780"]



    dOidtoPGDBname={}
    for item in JsonContent:
        print (str(item['O_id']))
        if str(item['O_id']) not in lBadOid:
            if item['O_kingdom']=='arc':
                temp=urllib.request.urlopen("https://www.genoscope.cns.fr/agc/microscope/search/export.php?format=microcyc&O_id="+str(item['O_id']))
                #access to the name of the PGDB
                temp=temp.info().get('Content-Disposition')
                temp=temp.split("filename=")[1]
                dOidtoPGDBname[item['O_id']]=temp
                if str(dOidtoPGDBname[item['O_id']])!="ACIAD31cyc.tar.gz":
                    fMicrocycIndex.write(str(item['O_id'])+"\t"+str(item["O_taxon"])+"\t"+str(item["O_name"])+"\t"+str(item["O_strain"])+"\t"+dOidtoPGDBname[item['O_id']]+"\t"+str(item["O_synonym"])+"\n")
                else:
                    if str(item['O_id'])=="31":
                        fMicrocycIndex.write(str(item['O_id'])+"\t"+str(item["O_taxon"])+"\t"+str(item["O_name"])+"\t"+str(item["O_strain"])+"\t"+dOidtoPGDBname[item['O_id']]+"\t"+str(item["O_synonym"])+"\n")
    fMicrocycIndex.close()

#if new summary
if args.bNewSummary:
    CreateMicrocycIndex()
    fMicrocycIndex=open("./downloads/MicrocycIndex.tsv","r")
    lineMicrocycIndex=fMicrocycIndex.readlines()[1:]

else:
    fMicrocycIndex=open("./downloads/MicrocycIndex.tsv","r")
    lineMicrocycIndex=fMicrocycIndex.readlines()[1:]

#Open Share Index which is the file with all the refseq genome
fShareIndex=open("./downloads/ShareIndex.tsv","r")
lineShareIndex=fShareIndex.readlines()


#######Begin the script for check if a Microcyc entry is allready in the database

#Store MicrocycIndex in a Dic[oid]={Oname,Ostrain,Otaxon,Opgdbname,Osynonym}
dMicrocycIndex={}
dtemp={}
for line in lineMicrocycIndex:
    line=line.split("\t")
    dtemp["Oname"]=line[2]
    #Some organism have no species
    if line[3]!="None":
        dtemp["Ostrain"]=line[3]
    else:
        dtemp["Ostrain"]=""
    dtemp["Otaxon"]=line[1]
    dtemp["Opgdbname"]=line[4]
    dtemp["Osynonym"]=line[5]
    dtemp["Oid"]=line[0]
    dMicrocycIndex[line[0]]=dtemp
    dtemp={}

#Change some wrong TaxID:
#dMicrocycIndex["6575"]["Otaxon"]="1408888"

#Store ShareIndex in a Dic[id]= Name and Name to ID.
dShareIndexNametoAssembly={}
dShareIndexNametoId={}
lGenus=[]

for line in lineShareIndex:
    line=line.split("\t")
    dShareIndexNametoAssembly[line[2]]=line[3]
    dShareIndexNametoId[line[2].lower()]=line[0]
    lGenus.append(line[2].split(" ")[0])

sGenus=set(lGenus)
lRemainingOid=[]
lGoodOid=[]

#Introduct a list for the double. This list contains bad Oid (Not RefSeq Sequences)
#Why? 4677: 4678 same organism but annoted by JGI. 4678 is the same sequence as our from RefSeq
#2313,2314: Wrong annoted strain, 2350 is the same sequence as us.
#"6575","6576": not the same strain as 6573. Change the taxID of 6575 because it's not 66712 but 1408888
#"7342","7343": 24 is coming from RefSeq
#187: 2900 is the second version of the same sequence
#4651 :174 is the same sequence that we use in RefSeq
#6408 :5774 is the same sequence that we use in RefSeq
#6609: 869 is the same sequence that we use in RefSeq
#528: 6293 is the updated version
#6608: 6607 is the full sequence

lBadDouble=["1294","5536","5606","242","2415","4677","6576","7342","7343","187","4651","6408","6609","6608","528","2313","2314"]

#Check if some name are the same in each dict: if Oname+Ostrain == Name RefSeq
#Some entry in Microcyc are duplicated (Example: TW20)
lMicrocycGenus=[]
for key in dMicrocycIndex:
    #Delete Bad Oid (Double only keep RefSeq Sequence)
    if dMicrocycIndex[key]["Oid"] not in lBadDouble:
        if (dMicrocycIndex[key]["Ostrain"].lower()=="none") or (dMicrocycIndex[key]["Ostrain"].lower()=="null"):
            sOrganismName=dMicrocycIndex[key]["Oname"].lower()
        else:
            sOrganismName=(dMicrocycIndex[key]["Oname"]+" "+dMicrocycIndex[key]["Ostrain"]).lower()
        #Delete end of trail spaces
        sOrganismName=sOrganismName.rstrip()
        #If the organism name are the same in Microcyc and RefSeq
        if sOrganismName in dShareIndexNametoId:
            #if the tax ID are the same.
            if dMicrocycIndex[key]["Otaxon"]==dShareIndexNametoId[sOrganismName].split(".")[0]:
                fSubstitution.write(sOrganismName+"\t"+sOrganismName+"\t"+dShareIndexNametoId[sOrganismName]+"\t"+dMicrocycIndex[key]["Otaxon"]+"\t"+dMicrocycIndex[key]["Oid"]+"\tSame ID Same Tax ID\n")
                #if the taxID are different
            else:
                fSubstitution.write(sOrganismName+"\t"+sOrganismName+"\t"+dShareIndexNametoId[sOrganismName]+"\t"+dMicrocycIndex[key]["Otaxon"]+"\t"+dMicrocycIndex[key]["Oid"]+"\tSame ID Different Tax ID\n")

        #It compare first the taxID. If same taxID then keep the entry if Microcyc name is in RefSeq Name
        else:
            for item in dShareIndexNametoId:
                if dShareIndexNametoId[item].split(".")[0]==dMicrocycIndex[key]["Otaxon"]:
                    #Split all taxonomy
                    lRefSeqName=item.split(" ")
                    lMicrocycName=sOrganismName.split(" ")
                    #Discard taxonomy with a length < 2
                    if len(lMicrocycName)>2 and len(lRefSeqName)>2:
                        #If Microcyc Name is a subset of the refseq name then keep it. Just checkin the taxID for more infos
                        if set(lMicrocycName).issubset(set(lRefSeqName)):
                            if dShareIndexNametoId[item].split(".")[0]==dMicrocycIndex[key]["Otaxon"]:
                                lGoodOid.append(key)
                                fSubstitution.write(sOrganismName+"\t"+item+"\t"+dShareIndexNametoId[item]+"\t"+dMicrocycIndex[key]["Otaxon"]+"\t"+dMicrocycIndex[key]["Oid"]+"\tMicrocyc Name in RefSeq Name and Same TaxID\n")
                else:
                    lRemainingOid.append(key)


sGoodOid=set(lGoodOid)
sRemainingOid=set(lRemainingOid)-sGoodOid

for key in sRemainingOid:
    fRemainingData.write(dMicrocycIndex[key]["Oid"]+"\t"+dMicrocycIndex[key]["Otaxon"]+"\t"+dMicrocycIndex[key]["Oname"]+"\t"+dMicrocycIndex[key]["Ostrain"]+"\t"+dMicrocycIndex[key]["Opgdbname"]+"\t"+dMicrocycIndex[key]["Osynonym"])
