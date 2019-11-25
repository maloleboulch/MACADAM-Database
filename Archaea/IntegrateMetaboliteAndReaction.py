#This script export reaction and compound associated to a pathway name
#Create the table Raction and Compoundself.#Need all the pathways.dat, compound.dat and reaction.dat from each versions used of Metacyc


#########Function ########
def RetrieveReaction(RXNlist,dPWYtoRXN):
    ListOfReact=[]
    for value in RXNlist:
        if value in dPWYtoRXNOut:
            ListOfReact.append(RetrieveReaction(dPWYtoRXNOut[value],dPWYtoRXN))
        else:
            ListOfReact.append(value)
    return ListOfReact

with open("../MandatoryFile/pathways.dat","r",encoding="iso-8859-14") as inputfile:
    lLinePathway=inputfile.readlines()
with open("../MandatoryFile/pathways16.5.dat","r",encoding="iso-8859-14") as inputfile:
    lOldLinePathway=inputfile.readlines()

#Formating files
lLinePathway="".join(lLinePathway)
lLinePathway=lLinePathway.split("//")
del lLinePathway[0]
#Create a dict PWY to (RXN,OPD)
dPWYtoRXN={}
lOfNewPathay=[]
for entry in lLinePathway:
    entry=entry.split("\n")
    dRXNtoCPD={}
    sPWY=0
    for item in entry:
        if item.startswith("UNIQUE-ID - "):
            item=item.replace("UNIQUE-ID - ","")
            sPWY=item.replace(" ","")
            lOfNewPathay.append(sPWY)
        if item.startswith("REACTION-LAYOUT - ("):
            item=item.replace("REACTION-LAYOUT - (","")
            item=item.replace("RIGHT-PRIMARIES ","")
            item=item.replace("LEFT-PRIMARIES ","")
            item=item.replace("))","")
            item=item.replace(") ","")
            item=item.split("(:")
            dRXNtoCPD[item[0].replace(" ","")]=item[1].split(" ")+item[3].split(" ")
    if sPWY!=0:
        dPWYtoRXN[sPWY]=dRXNtoCPD

#add Old Pathway
lOldLinePathway="".join(lOldLinePathway)
lOldLinePathway=lOldLinePathway.split("//")
del lOldLinePathway[0]
dOldPWYtoRXN={}
del lOldLinePathway[0]
for entry in lOldLinePathway:
    entry=entry.split("\n")
    dRXNtoCPD={}
    sPWY=0
    for item in entry:
        if item.startswith("UNIQUE-ID - "):
            item=item.replace("UNIQUE-ID - ","")
            sPWY=item
            lOfNewPathay.append(sPWY)
        if item.startswith("REACTION-LAYOUT - ("):
            item=item.replace("REACTION-LAYOUT - (","")
            item=item.replace("RIGHT-PRIMARIES ","")
            item=item.replace("LEFT-PRIMARIES ","")
            item=item.replace("))","")
            item=item.replace(") ","")
            item=item.split("(:")
            dRXNtoCPD[item[0].replace(" ","")]=item[1].split(" ")+item[3].split(" ")
    if sPWY!=0:
        dOldPWYtoRXN[sPWY]=dRXNtoCPD
###Add all PWY to PWYtoRXN
for item in dOldPWYtoRXN:
    if item in dPWYtoRXN:
        pass
    else:
        dPWYtoRXN[item.replace(" ","")]=dOldPWYtoRXN[item]


#PWY to RXN for output file
dPWYtoRXNOut={}
for item in dPWYtoRXN:
    tmp=[]
    sPWY=item
    for key in dPWYtoRXN[item]:
        tmp.append(key.replace(" ",""))
    dPWYtoRXNOut[item]=tmp

#Some RXN are pathway, translate pathway to RXN
dTemp={}
for key in dPWYtoRXNOut:
    tmplist=RetrieveReaction(dPWYtoRXNOut[key],dPWYtoRXNOut)
    #flat the list
    tmplist = repr(tmplist)
    flat = []
    for i in tmplist:
      if i != ',' and i != '[' and i != ']' and i != ' ':
          flat.append(i)
    tmplist="".join(flat).split("\'")
    tmplist=filter(None,tmplist)
    tmplist=set(tmplist)
    dTemp[key]=tmplist
dPWYtoRXNOut=dTemp



#Some CPD are class. Need to import classes.dat for some name
#RXN to CPD. Create a dict: React to CPD
dRXNtoCPD={}
for key in dPWYtoRXN:
    for item in dPWYtoRXN[key]:
        if item in dRXNtoCPD:
            if dRXNtoCPD[item]!=dPWYtoRXN[key][item]:
                dRXNtoCPD[item].append(dPWYtoRXN[key][item])
            # print (item)
            # print (dPWYtoRXN[key][item])
            # print (dRXNtoCPD[item])
        else:
            dRXNtoCPD[item]=dPWYtoRXN[key][item]

dTemp={}
for element in dRXNtoCPD:
    tmplist=dRXNtoCPD[element]
    #flat the list
    tmplist = repr(tmplist)
    flat = []
    for i in tmplist:
        if i != ',' and i != '[' and i != ']' and i != ' ':
            flat.append(i)
    tmplist="".join(flat).split("\'")
    tmplist=filter(None,tmplist)
    tmplist=list(tmplist)
    templist=[]
    for item in tmplist:
        templist.append(item.replace("|",""))
    dTemp[element]=set(templist)

dRXNtoCPD=dTemp


############### ID to Name ##############

###############For compounds file #########
with open ("../MandatoryFile/compounds.dat","r",encoding="iso-8859-14") as inputfile:
    lLineCompound=inputfile.readlines()
with open ("../MandatoryFile/compounds16.5.dat","r",encoding="iso-8859-14")  as inputfile:
    lOldLineCompound=inputfile.readlines()

lLineCompound="".join(lLineCompound)
lLineCompound=lLineCompound.split("//")
del lLineCompound[0]
#Create a dict PWY to (RXN,CPD)
dCPDtoName={}
for entry in lLineCompound:
    entry=entry.split("\n")
    lNames=[]
    for item in entry:
        if item.startswith("UNIQUE-ID - "):
            item=item.replace("UNIQUE-ID - ","")
            CPD=item.replace(" ","")
        if item.startswith("COMMON-NAME - "):
            item=item.replace("COMMON-NAME - ","")
            lNames.append(item)
        if item.startswith("SYNONYMS - "):
            item=item.replace("SYNONYMS - ","")
            lNames.append(item)
    dCPDtoName[CPD]=lNames

#Old Compounds
lOldLineCompound="".join(lOldLineCompound)
lOldLineCompound=lOldLineCompound.split("//")
del lOldLineCompound[0]
#Create a dict PWY to (RXN,OPD)
dOldCPDtoName={}
for entry in lOldLineCompound:
    entry=entry.split("\n")
    lNames=[]
    for item in entry:
        if item.startswith("UNIQUE-ID - "):
            item=item.replace("UNIQUE-ID - ","")
            CPD=item.replace(" ","")
        if item.startswith("COMMON-NAME - "):
            item=item.replace("COMMON-NAME - ","")
            lNames.append(item)
        if item.startswith("SYNONYMS - "):
            item=item.replace("SYNONYMS - ","")
            lNames.append(item)
    dOldCPDtoName[CPD]=lNames

#addOldCPD
for element in dOldCPDtoName:
    if element in dCPDtoName:
        pass
    else:
        dCPDtoName[element]=dOldCPDtoName[element]

############# For Class Compounds ############
with open ("../MandatoryFile/classes.dat","r",encoding="iso-8859-14") as inputfile:
    lLineClasses=inputfile.readlines()
with open ("../MandatoryFile/classes16.5.dat","r",encoding="iso-8859-14")  as inputfile:
    lOldLineClasses=inputfile.readlines()

lLineClasses="".join(lLineClasses)
lLineClasses=lLineClasses.split("//")
del lLineClasses[0]
#Create a dict PWY to (RXN,OPD)
dCLtoName={}
for entry in lLineClasses:
    entry=entry.split("\n")
    lNames=[]
    for item in entry:
        if item.startswith("UNIQUE-ID - "):
            item=item.replace("UNIQUE-ID - ","")
            CPD=item.replace(" ","")
        if item.startswith("COMMON-NAME - "):
            item=item.replace("COMMON-NAME - ","")
            lNames.append(item)
        if item.startswith("SYNONYMS - "):
            item=item.replace("SYNONYMS - ","")
            lNames.append(item)
    dCLtoName[CPD]=lNames

#Old Compounds
lOldLineClasses="".join(lOldLineClasses)
lOldLineClasses=lOldLineClasses.split("//")
del lOldLineClasses[0]
#Create a dict PWY to (RXN,OPD)
dOldCLtoName={}
for entry in lOldLineClasses:
    entry=entry.split("\n")
    lNames=[]
    for item in entry:
        if item.startswith("UNIQUE-ID - "):
            item=item.replace("UNIQUE-ID - ","")
            CPD=item.replace(" ","")
        if item.startswith("COMMON-NAME - "):
            item=item.replace("COMMON-NAME - ","")
            lNames.append(item)
        if item.startswith("SYNONYMS - "):
            item=item.replace("SYNONYMS - ","")
            lNames.append(item)
    dOldCLtoName[CPD]=lNames

#addOldCPD
for element in dOldCLtoName:
    if element in dCLtoName:
        pass
    else:
        dCLtoName[element]=dOldCLtoName[element]

####### Name of Reaction ##########
with open ("../MandatoryFile/reactions.dat","r",encoding="iso-8859-14") as inputfile:
    lLineReaction=inputfile.readlines()
with open ("../MandatoryFile/reactions16.5.dat","r",encoding="iso-8859-14")  as inputfile:
    lOldLineReaction=inputfile.readlines()

lLineReaction="".join(lLineReaction)
lLineReaction=lLineReaction.split("//")
del lLineReaction[0]
#Create a dict PWY to (RXN,OPD)
dRXNtoName={}
dRXNtoECNumber={}
for entry in lLineReaction:
    entry=entry.split("\n")
    lNames=[]
    lECNumber=[]
    for item in entry:
        if item.startswith("UNIQUE-ID - "):
            item=item.replace("UNIQUE-ID - ","")
            CPD=item.replace(" ","")
        if item.startswith("COMMON-NAME - "):
            item=item.replace("COMMON-NAME - ","")
            lNames.append(item)
        if item.startswith("SYNONYMS - "):
            item=item.replace("SYNONYMS - ","")
            lNames.append(item)
        if item.startswith("EC-NUMBER - "):
            item=item.replace("EC-NUMBER - EC-","")
            lECNumber.append(item)
    dRXNtoName[CPD]=lNames
    dRXNtoECNumber[CPD]=lECNumber

#Old Compounds
lOldLineReaction="".join(lOldLineReaction)
lOldLineReaction=lOldLineReaction.split("//")
del lOldLineReaction[0]
#Create a dict PWY to (RXN,OPD)
dOldRXNtoName={}
dOldRXNtoECNumber={}
for entry in lOldLineReaction:
    entry=entry.split("\n")
    lNames=[]
    lECNumber=[]
    for item in entry:
        if item.startswith("UNIQUE-ID - "):
            item=item.replace("UNIQUE-ID - ","")
            CPD=item.replace(" ","")
        if item.startswith("COMMON-NAME - "):
            item=item.replace("COMMON-NAME - ","")
            lNames.append(item)
        if item.startswith("SYNONYMS - "):
            item=item.replace("SYNONYMS - ","")
            lNames.append(item)
        if item.startswith("EC-NUMBER - "):
            item=item.replace("EC-NUMBER - EC-","")
            lECNumber.append(item)
    dOldRXNtoName[CPD]=lNames
    dOldRXNtoECNumber[CPD]=lECNumber

#addOldCPD
for element in dOldRXNtoName:
    if element in dRXNtoName:
        pass
    else:
        dRXNtoName[element]=dOldRXNtoName[element]

for element in dOldRXNtoECNumber:
    if element in dRXNtoECNumber:
        pass
    else:
        dRXNtoECNumber[element]=dOldRXNtoECNumber[element]


### Read present pathway #####
with open("./DatabaseTSV/PathwayTable.tsv","r") as inputfile:
    lPathway=inputfile.readlines()
setOfPresentPathwayinDatabase=set()
for element in lPathway:
    setOfPresentPathwayinDatabase.add(element.split("\t")[5])

########### Enzyme.Reaction ################

with open ("../MandatoryFile/enzrxns.dat","r",encoding="iso-8859-14") as inputfile:
    lLineENZ=inputfile.readlines()
with open ("../MandatoryFile/enzrxns16.5.dat","r",encoding="iso-8859-14")  as inputfile:
    lOldLineENZ=inputfile.readlines()

lLineENZ="".join(lLineENZ)
lLineENZ=lLineENZ.split("//")
del lLineENZ[0]
#Create a dict PWY to (RXN,OPD)
dENZtoName={}
dENZtoRXN={}
for entry in lLineENZ:
    entry=entry.split("\n")
    lNames=[]
    lRXN=[]
    for item in entry:
        if item.startswith("UNIQUE-ID - "):
            item=item.replace("UNIQUE-ID - ","")
            ENZ=item.replace(" ","")
        if item.startswith("COMMON-NAME - "):
            item=item.replace("COMMON-NAME - ","")
            lNames.append(item)
        if item.startswith("SYNONYMS - "):
            item=item.replace("SYNONYMS - ","")
            lNames.append(item)
        if item.startswith("REACTION - "):
            item=item.replace("REACTION - ","")
            lRXN.append(item)
    dENZtoName[ENZ]=lNames
    dENZtoRXN[ENZ]=lRXN

#Old Compounds
lOldLineENZ="".join(lOldLineENZ)
lOldLineENZ=lOldLineENZ.split("//")
del lOldLineENZ[0]
#Create a dict PWY to (RXN,OPD)
doldENZtoName={}
doldENZtoRXN={}
for entry in lOldLineENZ:
    entry=entry.split("\n")
    lNames=[]
    lRXN=[]
    for item in entry:
        if item.startswith("UNIQUE-ID - "):
            item=item.replace("UNIQUE-ID - ","")
            ENZ=item.replace(" ","")
        if item.startswith("COMMON-NAME - "):
            item=item.replace("COMMON-NAME - ","")
            lNames.append(item)
        if item.startswith("SYNONYMS - "):
            item=item.replace("SYNONYMS - ","")
            lNames.append(item)
        if item.startswith("REACTION - "):
            item=item.replace("REACTION - ","")
            lRXN.append(item)
    doldENZtoName[ENZ]=lNames
    doldENZtoRXN[ENZ]=lRXN


for element in doldENZtoName:
    if element in dENZtoName:
        pass
    else:
        dENZtoName[element]=doldENZtoName[element]

for element in doldENZtoRXN:
    if element in dENZtoRXN:
        pass
    else:
        dENZtoRXN[element]=doldENZtoRXN[element]

# for element in dENZtoRXN:
#     print (element)
#     print (dENZtoRXN[element])

########### Creates File ################
lListofBadString=["<i>","</i>","<I>","</I>","<sub>","</sub>","<SUB>","</SUB>","<sup>","</sup>","<em>","</em>","<small>","</small>","<SUP>","</SUP>"]
lECnumberBadstring=["EC-NUMBER - ","|","EC-"]

with open("./DatabaseTSV/PWY.RXN.tsv","w") as PWYRXN:
    with open("./DatabaseTSV/RXN.Name.tsv","w") as RXNName:
        with open("./DatabaseTSV/RXN.CPD.tsv","w") as RXNCPD:
            with open("./DatabaseTSV/CPD.Name.tsv","w") as CPDName:
                with open("./DatabaseTSV/RXN.ENZ.tsv","w") as RXNENZ:
                    with open("./DatabaseTSV/ENZName.tsv","w") as EnzName:
                        with open("./DatabaseTSV/RXNECNumber.tsv","w") as ECName:
                            setofRXN=set()
                            setofCPD=set()
                            setofENz=set()
                            for element in dPWYtoRXNOut:
                                if element in setOfPresentPathwayinDatabase:
                                    for item in dPWYtoRXNOut[element]:
                                        PWYRXN.write(element+"\t"+item+"\n")
                                        setofRXN.add(item)
                            for item in setofRXN:
                                if item in dRXNtoName:
                                    for element in dRXNtoName[item]:
                                        for ch in lListofBadString:
                                            if ch in element:
                                                element=element.replace(ch,"")
                                        RXNName.write(item+"\t"+element+"\n")
                                if item in dRXNtoECNumber:
                                        for element in dRXNtoECNumber[item]:
                                            for ch in lECnumberBadstring:
                                                if ch in element:
                                                    element=element.replace(ch,"")
                                            ECName.write(item+"\t"+element+"\n")
                                for CPD in dRXNtoCPD[item]:
                                    RXNCPD.write(item+"\t"+CPD+"\n")
                                    setofCPD.add(CPD)
                            for CPD in setofCPD:
                                if CPD in dCPDtoName:
                                    for Name in dCPDtoName[CPD]:
                                        for ch in lListofBadString:
                                            if ch in Name:
                                                Name=Name.replace(ch,"")
                                        CPDName.write(CPD+"\t"+Name+"\n")
                            for element in dENZtoRXN:
                                for item in dENZtoRXN[element]:
                                    if item in setofRXN:
                                        RXNENZ.write(element+"\t"+item+"\n")
                                        setofENz.add(element)
                            for element in dENZtoName:
                                if element in setofENz:
                                    for item in dENZtoName[element]:
                                        for ch in lListofBadString:
                                            if ch in item:
                                                item=item.replace(ch,"")
                                        EnzName.write(element+"\t"+item+"\n")
