# Ce script permet d'extraire la classe de toutes les Pathway de Metacyc
# Nécéssite 2 fichiers dans les fichiers plats de Metacyc (Classes.dat et Pathways.dat)
# Chaque Pathay de pathway.dat est associé à un TYPE qui est associé un autre auter type dans classes.dat
# UNIQUE-ID - Pathways TYPES - Generalized-Reactions est la racine de l'arbre des classes
#Attention certains Unique-ID ont plusieurs Type

#Input File: classes.dat & pathway.dat from the current MetaCyc Database and MetaCyc 16.5 for MicroCyc
#You can find these files on BioCyc website
#Pathway Table must be all ready done!

with open("../MandatoryFile/classes.dat","r",encoding="iso-8859-14") as inputfile:
    lLineClasses=inputfile.readlines()


with open("../MandatoryFile/pathways.dat","r",encoding="iso-8859-14") as inputfile:
    lLinePathway=inputfile.readlines()


#Fonction that allow us to create the the path of all PWY in Metacyc.
def create_paths(root_name,dictio):
    paths = []
    recursive(root_name,[],dictio,paths)
    return paths

def recursive(current_node_name,current_path,dictio,paths):
    if current_node_name in dictio:
        current_path_copy = current_path.copy()
        current_path_copy.append(current_node_name)
        for node in dictio[current_node_name]:
            recursive(node,current_path_copy,dictio,paths)
    else:
        current_path_copy = current_path.copy()
        current_path_copy.append(current_node_name)
        paths.append(current_path_copy)

#Formating files
lLineClasses="".join(lLineClasses)
lLineClasses=lLineClasses.split("//")

dParenttoSon={}
dIDtoCommonName={}

a=0

#Create a dict Parent => list of Son
for entry in lLineClasses:
    entry=entry.split("\n")
    lParents=[]
    sonID=0
    sCommonName=0
    for item in entry:
        if item.startswith("UNIQUE-ID - "):
            item=item.replace("UNIQUE-ID - ","")
            sonID=item
        elif item.startswith("TYPES - "):
            item=item.replace("TYPES - ","")
            lParents.append(item)
        elif item.startswith("COMMON-NAME - "):
            item=item.replace("COMMON-NAME - ","")
            sCommonName=item
    if sonID!=0:
        for Class in lParents:
            if Class in dParenttoSon:
                dParenttoSon[Class].append(sonID)
            else:
                dParenttoSon[Class]=[sonID]
        dIDtoCommonName[sonID]=sCommonName


#we do that for Lines Pathway too

lLinePathway="".join(lLinePathway)
lLinePathway=lLinePathway.split("//")

dPathwaytoParentClass={}

for entry in lLinePathway:
    entry=entry.split("\n")
    lParents=[]
    sonID=0
    sCommonName=0
    for item in entry:
        if item.startswith("UNIQUE-ID - "):
            item=item.replace("UNIQUE-ID - ","")
            sonID=item
        elif item.startswith("TYPES - "):
            item=item.replace("TYPES - ","")
            lParents.append(item)
        elif item.startswith("COMMON-NAME - "):
            item=item.replace("COMMON-NAME - ","")
            sCommonName=item
    if sonID!=0:
        for Class in lParents:
            if Class in dParenttoSon:
                dParenttoSon[Class].append(sonID)
            else:
                dParenttoSon[Class]=[sonID]
        dIDtoCommonName[sonID]=sCommonName

#We use the fonction for the Pathways ("Pathways" is a frame. So it's our root)

lPath=create_paths("Pathways",dParenttoSon)

#Write a file with all the pathway

with open("./downloads/PathwayHierarchy.tsv","w") as outputfile:
    for element in lPath:
        outputfile.write("\t".join(element)+"\n")

########### Some pathway of Microcyc are not our version of Metacyc (20.5). Microcyc use the 16.5 version ##############


# Compute Pathway that are in our database and those who are not in Microcyc 20.5 ####


with open("./downloads/PathwayHierarchy.tsv","r") as inputfile:
    lLinePathway=inputfile.readlines()
    lListOfPathway=[]
    for line in lLinePathway:
        line=line.replace("\n","")
        line=line.split("\t")
        lListOfPathway.append(line[-1])

with open("./DatabaseTSV/PathwayTable.tsv","r") as inputfile:
    lLinePathway=inputfile.readlines()
    lListOfDatabase=[]
    dPathwaytoName={}
    for line in lLinePathway:
        line=line.replace("\n","")
        line=line.split("\t")
        lListOfDatabase.append(line[5])
        dPathwaytoName[line[6]]=line[5]

setDatabasePathway=set(lListOfDatabase)
setPathway=set(lListOfPathway)

print (setDatabasePathway-setPathway)
setUnknown=setDatabasePathway-setPathway


#Create Pathway for the other Metacyc 16.5
with open("../MandatoryFile/classes16.5.dat","r",encoding="iso-8859-14") as inputfile:
    lLineClasses=inputfile.readlines()


with open("../MandatoryFile/pathways16.5.dat","r",encoding="iso-8859-14") as inputfile:
    lLinePathway=inputfile.readlines()

lLineClasses="".join(lLineClasses)
lLineClasses=lLineClasses.split("//")

dParenttoSon={}
dIDoldtoCommonName={}

a=0

#Create a dict Parent => list of Son
for entry in lLineClasses:
    entry=entry.split("\n")
    lParents=[]
    sonID=0
    sCommonName=0
    for item in entry:
        if item.startswith("UNIQUE-ID - "):
            item=item.replace("UNIQUE-ID - ","")
            sonID=item
        elif item.startswith("TYPES - "):
            item=item.replace("TYPES - ","")
            lParents.append(item)
        elif item.startswith("COMMON-NAME - "):
            item=item.replace("COMMON-NAME - ","")
            sCommonName=item
    if sonID!=0:
        for Class in lParents:
            if Class in dParenttoSon:
                dParenttoSon[Class].append(sonID)
            else:
                dParenttoSon[Class]=[sonID]
        dIDoldtoCommonName[sonID]=sCommonName


#we do that for Lines Pathway too

lLinePathway="".join(lLinePathway)
lLinePathway=lLinePathway.split("//")

dPathwaytoParentClass={}

for entry in lLinePathway:
    entry=entry.split("\n")
    lParents=[]
    sonID=0
    sCommonName=0
    for item in entry:
        if item.startswith("UNIQUE-ID - "):
            item=item.replace("UNIQUE-ID - ","")
            sonID=item
        elif item.startswith("TYPES - "):
            item=item.replace("TYPES - ","")
            lParents.append(item)
        elif item.startswith("COMMON-NAME - "):
            item=item.replace("COMMON-NAME - ","")
            sCommonName=item
    if sonID!=0:
        for Class in lParents:
            if Class in dParenttoSon:
                dParenttoSon[Class].append(sonID)
            else:
                dParenttoSon[Class]=[sonID]
        dIDoldtoCommonName[sonID]=sCommonName

#We use the fonction for the Pathways ("Pathways" is a frame. So it's our root)

lPath=create_paths("Pathways",dParenttoSon)

#Make a dict of all Pathway ID with path

with open("./downloads/PathwayHierarchy.tsv","a") as outputfile:
    for element in lPath:
        if element[-1] in setUnknown:
            outputfile.write("\t".join(element)+"\n")

#Keep only The common name used
for element in setUnknown:
    if element in dIDoldtoCommonName:
        dIDtoCommonName[element]=dIDoldtoCommonName[element]

###### Unique ID to common names ######

#make a set of all ID used in PathwayHierarchy.tsv
with open("./downloads/PathwayHierarchy.tsv","r") as inputfile:
    lLinesPathwayHierarchy=inputfile.readlines()
    lAllUniqueID=[]
    for line in lLinesPathwayHierarchy:
        line=line.replace("\n","")
        line=line.split("\t")
        lAllUniqueID=lAllUniqueID+line

lAllUniqueID=list(set(lAllUniqueID))

#correct empty dict values
for key in dIDtoCommonName:
    if dIDtoCommonName[key]==0:
        dIDtoCommonName[key]=key


lListofBadString=["<i>","</i>","<I>","</I>","<sub>","</sub>","<SUB>","</SUB>","<sup>","</sup>","<em>","</em>","<small>","</small>","<SUP>","</SUP>"]
for ch in lListofBadString:
    for key in dIDtoCommonName:
        if ch in dIDtoCommonName[key]:
            dIDtoCommonName[key]=dIDtoCommonName[key].replace(ch,"")

with open("./DatabaseTSV/PathwayIDtoName.tsv","w") as outputfile:
    for item in lAllUniqueID:
        outputfile.write(item+"\t"+dIDtoCommonName[item]+"\n")

### Rewrite Pathway Hierarchy
with open("./DatabaseTSV/PathwayHierarchy.tsv","w") as inputfile:
    for line in lLinesPathwayHierarchy:
        line=line.split("\t")
        ending=line[-1].replace("\n","")
        inputfile.write(ending+"\t"+".".join(line).replace("\n","")+".\t"+dIDtoCommonName[ending]+"\n")


#Some Pathways are not in our files. We add them manually
with open("./DatabaseTSV/PathwayHierarchy.tsv","a") as outputfile:
    with open("../MandatoryFile/UnknownPathways.tsv","r") as inputfile:
        lLines=inputfile.readlines()
        for line in lLines:
            outputfile.write(line)
