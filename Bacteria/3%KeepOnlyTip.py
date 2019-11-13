#Essayons de ne garder uniquement les noeuds au bout de la classification. pas les autres.

def onlybacteria(setOfTaxID,dTaxIDtoparent):
    #check and discard TaxID who are not bacteria
    setTemp=set()
    for element in setOfTaxID:
        temp=element
        while temp!="1":
            temp=dTaxIDtoparent[temp]
            if temp=="2":
                setTemp.add(element)
    return setTemp


#open remaining from Microcyc
with open("./downloads/MicrocycRemainingRemasteredAfter2.tsv","r") as inputfile:
    lLinesRemaining=inputfile.readlines()

with open("../MandatoryFile/merged.dmp","r") as inputfile:
    lLinesMergedTaxID=inputfile.readlines()

with open("../MandatoryFile/nodes.dmp","r") as inputfile:
    lLinesNodes=inputfile.readlines()

################################### Nodes remastered
with open("./downloads/nodesremastered.dmp","r") as inputfile:
    lLinesNodesRemastered=inputfile.readlines()

setTaxIDNodes=set()
for line in lLinesNodesRemastered:
    line=line.split("\t")[0]
    line=line.split(".")[0]
    setTaxIDNodes.add(line)

#######################################

fTipOnly=open("./downloads/TipOnly.tsv","w")
fReMainingafterTip=open("./downloads/FinalRemaining.tsv","w")
fTipSubstition=open("./downloads/MicrocycSubstitution.tsv","a")

#Store all Microcyc TaxID
lTaxIDMicrocyc=[]

for line in lLinesRemaining:
    lTaxIDMicrocyc.append(line.split("\t")[1])

#Create a dict for Merged TaxID
dOldTaxIDtoNew={}
for line in lLinesMergedTaxID:
    line=line.replace("\t|\n","")
    line=line.split("\t|\t")
    dOldTaxIDtoNew[line[0]]=line[1]

#Check if old TaxID is used in Microcyc
setTaxIDMicrocyc=set(lTaxIDMicrocyc)
setTemp=set()
for element in setTaxIDMicrocyc:
    if element in dOldTaxIDtoNew:
        setTemp.add(dOldTaxIDtoNew[element])
    else:
        setTemp.add(element)

setTaxIDMicrocyc=setTemp

#find in the NCBI Taxonomy the tip's nodes (i.e Nodes never parents to others)
dTaxIDtoRank={}
dTaxIDtoparent={}
setTipTaxID=set()
setParentTaxID=set()

for line in lLinesNodes:
    line=line.split("\t|\t")
    setTipTaxID.add(line[0])
    setParentTaxID.add(line[1])
    dTaxIDtoRank[line[0]]=line[2]
    dTaxIDtoparent[line[0]]=line[1]

setTipTaxID=setTipTaxID-setParentTaxID

#Keep only nodes inside Bacteria
setTipTaxIDbacteria=onlybacteria(setTipTaxID,dTaxIDtoparent)
#setTipTaxIDbacteria contains tip for only the bacteria Domain now

#quality control of Microcyc
setTaxIDMicrocyc=onlybacteria(setTaxIDMicrocyc,dTaxIDtoparent)


setTaxIDMicrocycTip=setTaxIDMicrocyc-setTaxIDNodes
setTaxIDMicrocycTip=setTaxIDMicrocycTip.intersection(setTipTaxIDbacteria)

#Write lines of interests
for line in lLinesRemaining:
    sTaxID=line.split("\t")[1]
    if sTaxID in setTaxIDMicrocycTip:
        fTipOnly.write(line)
    else:
        fReMainingafterTip.write(line)
fTipOnly.close()

####### Add to substitution file ####

with open("./downloads/TipOnly.tsv","r") as inputfile:
    lLinesTipOnly=inputfile.readlines()

#Detect double taxID
lTaxIdTip=[]
setDouble=[]

for line in lLinesTipOnly:
    TaxID=line.split("\t")[1]
    lTaxIdTip.append(TaxID)

setDouble=set([x for x in lTaxIdTip if lTaxIdTip.count(x) > 1])

#Good Oid. We use preferentially sequence from in order: RefSeq(4370,6669), Genbank, JGI, 2nd version (1140001,4822). Len=20 nowadays Same Oid have the same sequences (5675,6375). 2510, 5625, 3829 is an improved quality draft. Bad tax (778)
#Competibacter are an artifact (1501,1502) More plasmid(2537) Scaffold (3370)
lGood=["7371","3838","6773","4416","6080","5675","2510","5625","3829","4370","778","6375","2537","5887","4822","6669","4888","3370","7364"]

for line in lLinesTipOnly:
    line=line.split("\t")
    if line[1] not in setDouble:
        if line[3] not in line[2]:
            fTipSubstition.write(line[2]+" "+line[3]+"\t"+"NaN"+"\t"+line[1]+".nan1Umic"+"\t"+line[1]+"\t"+line[0]+"\tTip of the taxonomy\n")
        else:
            fTipSubstition.write(line[2]+"\t"+"NaN"+"\t"+line[1]+".nan1Umic"+"\t"+line[1]+"\t"+line[0]+"\tTip of the taxonomy\n")
    else:
        if line[1] in setDouble:
            if line[0] in lGood:
                fTipSubstition.write(line[2]+" "+line[3]+"\t"+"NaN"+"\t"+line[1]+".nan1Umic"+"\t"+line[1]+"\t"+line[0]+"\tTip of the taxonomy\n")
        #else:
        #    print (line)
