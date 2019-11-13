#This script take all uniq TaxiID from RefSeq (When an organism have a taxID different from the species TaxID ie the strain is plublicated) and try to find an occurence in Microcyc.

#Store Microcyc subtitution lines
with open("./downloads/MicrocycSubstitution.tsv","r") as inputfile:
    lLinesMicrocycSubstitution=inputfile.readlines()

#fMicrocycSubstitution corresponde a la suite du fichier substition. Donc a apenn au fichier
fMicrocycSubstitution=open("./downloads/MicrocycSubstitution.tsv","a")

fMicrocycRemainingRemastered=open("./downloads/MicrocycRemainingRemastered.tsv","w")

with open("./downloads/ShareIndex.tsv","r") as inputfile:
    lLinesShareIndex=inputfile.readlines()

#with open("PresentTaxID.tsv","r") as inputfile:
    #lLinesPresentTaxID=inputfile.readlines()

with open("./downloads/MicrocycRemaining.tsv","r") as inputfile:
    lLinesMicrocycRemaining=inputfile.readlines()


dTaxIDtoNameRefSeq={}
dTaxIDtoPGDBname={}
#store unique TaxID from our database to RefSeq name in a dict and for each uniq taxID store the PGDBname
for line in lLinesShareIndex:
    line=line.split("\t")
    ID=line[0].split(".")
    if "U" in ID[1]:
        dTaxIDtoNameRefSeq[ID[0]]=line[2]
        dTaxIDtoPGDBname[ID[0]]=line[0]



lMicrocycTaxID=[]
#Store TaxID of Microcyc element to a name in a dict
dTaxIDtoOidandName={}
for line in lLinesMicrocycRemaining:
    line=line.split("\t")
    if line[3] in line[2]:
        dTaxIDtoOidandName[line[1]]=[line[0],line[2]]
    else:
        dTaxIDtoOidandName[line[1]]=[line[0],line[2]+" "+line[3]]
    lMicrocycTaxID.append(line[1])

#Add an exception for 24 Thermotoga maritima	MSB8	243274	GENBANK	NC_000853.1. Why this one? because it's the sequence from RefSeq.
#dTaxIDtoOidandName['243274']=['24','Thermotoga maritima MSB8']




lUniq=[]
#Beware some are in double in Microcyc
for item in lMicrocycTaxID:
    if lMicrocycTaxID.count(item)==1:
        lUniq.append(item)

#Delete TaxID allready integrated of Microcyc Substitution (For the problem of the PRJNA )
lTaxIDSub=[]
for line in lLinesMicrocycSubstitution:
    sTaxIDSub=line.split("\t")[3]
    lTaxIDSub.append(sTaxIDSub)

setTaxIDSub=set(lTaxIDSub)

sUniq=set(lUniq)
sIntersection=set.intersection(sUniq,setTaxIDSub)
lUniq=list(sUniq-setTaxIDSub)

#exception for 243274
#lUniq.append('243274')

#find element who are in Microcyc and in RefSeq (same taxID) and extract these elements.
lDeleteOid=[]
for key in dTaxIDtoOidandName:
    if key in dTaxIDtoNameRefSeq:
        if key in lUniq:
            fMicrocycSubstitution.write(dTaxIDtoOidandName[key][1]+"\t"+dTaxIDtoNameRefSeq[key]+"\t"+dTaxIDtoPGDBname[key]+"\t"+key+"\t"+dTaxIDtoOidandName[key][0]+"\tUnique TaxID and PGDB"+"\n")
            lDeleteOid.append(dTaxIDtoOidandName[key][0])
        else:
            #identify double in Microcyc
            print (key)

#Add exception. delete this ID because we keep only the one from RefSeq
lDeleteOid.extend(('7342','7343'))


#update the Microcyc Remaining files with only the rest
for line in lLinesMicrocycRemaining:
    Oid=line.split("\t")[0]
    Otaxonomy=line.split("\t")[1]
    if Oid not in lDeleteOid:
        if Otaxonomy not in sIntersection:
            fMicrocycRemainingRemastered.write(line)
