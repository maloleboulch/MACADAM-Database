#Store all Data of Faprotax in our Format
#there are 4692 differents taxonomy in the database (but maybe some of the same and some non bacteria)
#90 fonctions
#434 mauvaise Taxonomy
#412 after rules
#4203 reconnu
#3991 Taxonomie de bactérie
#3843 TaxID différent (82%)


with open("../MandatoryFile/FAPROTAX.txt","r") as inputfile:
    lFaprotaxLine=inputfile.readlines()


#Load all Names and TaxID in a Dict
with open("../MandatoryFile/names.dmp","r") as inputfile:
    lLinesNames=inputfile.readlines()
    dNameToTaxID={}
    for line in lLinesNames:
        line=line.split("\t|\t")
        dNameToTaxID[line[1]]=line[0]

#Create a Dict with TaxID= Parent TaxID
with open("../MandatoryFile/nodes.dmp","r") as inputfile:
    lLinesNodes=inputfile.readlines()
    dTaxIDToParentComplete={}
    lBacteriaTaxID=[]
    for line in lLinesNodes:
        line=line.split("\t|\t")
        dTaxIDToParentComplete[line[0]]=[line[1],line[2]]
    for item in dTaxIDToParentComplete:
        sTaxID=item
        while sTaxID!="1":
            if sTaxID=="2157":
                lBacteriaTaxID.append(item)
            sTaxID=dTaxIDToParentComplete[sTaxID][0]


#function for the lineage
def lineage(TaxID):
    dLineage={}
    dLineage=dLineage.fromkeys(["superkingdom","phylum","class","order","family","genus","species"])
    rank=["superkingdom","phylum","class","order","family","genus","species"]
    dLineage[dTaxIDToParentComplete[TaxID][1]]=TaxID
    sUniqueTaxID=set()
    lineage=[]
    lineage.insert(0,TaxID)
    while TaxID!="1":
        sUniqueTaxID.add(TaxID)
        value=dTaxIDToParentComplete[TaxID]
        if value[1] in rank:
            dLineage[value[1]]=TaxID
            lineage.insert(0,TaxID)
        TaxID=value[0]
    return dLineage,sUniqueTaxID


#Function for the add group in certain function
def AddGroup(item,dictionnary):
    lResults=[]
    lSubFonction=[]
    item=item.replace("add_group:","")
    lSubFonction.append(item)
    listofOrganism=dictionnary[item]
    for element in listofOrganism:
        if element.startswith("add_group:"):
            lResults=lResults+AddGroup(element,dictionnary)[0]
            lSubFonction=lSubFonction+AddGroup(element,dictionnary)[1]
        else:
            lResults.append(element)
    return [lResults,lSubFonction]



dFunctionToOrganism={}

for line in lFaprotaxLine:
    #Line starting with # are comments. Some organism begin with ###. Some line explain how the category are done
    if line.startswith("#"):
        pass
    #Function come with metadata in line so if there are metadata in line:
    elif "; light_dependent:" in line:
        sFunction=line.split("\t")[0]
        sFunction=sFunction.rstrip()
        dFunctionToOrganism[sFunction]=[]
    #Species or Genus begin with * normally. But for some exemple there are no * but it begins with an uppercase
    elif line.startswith("*") or line[0].isupper():
        sTax=line.split("\t")[0]
        sTax=sTax.replace("\n","")
        sTax=sTax.rstrip()
        dFunctionToOrganism[sFunction].append(sTax)
    elif line.startswith("add_group"):
        sAddGroup=line.split("\t")[0]
        sAddGroup=sAddGroup.replace("\n","")
        sAddGroup=sAddGroup.rstrip()
        dFunctionToOrganism[sFunction].append(sAddGroup)
    else:
        if not line=="\n":
            print (line)


dTemp={}
dFunctionHierarchy={}


#create a dict with all Taxonomy for all function (No more add group only tax)
for key in dFunctionToOrganism:
    for element in dFunctionToOrganism[key]:
        if element.startswith("add_group:"):
            if key in dTemp:
                dTemp[key]=AddGroup(element,dFunctionToOrganism)[0]+dTemp[key]
            else:
                dTemp[key]=AddGroup(element,dFunctionToOrganism)[0]
                dFunctionHierarchy[key]=(AddGroup(element,dFunctionToOrganism)[1])
        else:
            if key in dTemp:
                dTemp[key]=[element]+dTemp[key]
            else:
                dTemp[key]=[element]
    if key not in dFunctionHierarchy:
        dFunctionHierarchy[key]=[]



#delete stars in taxonomy name and transform lists into sets.

dFunctionToOrganism={}

for key in dTemp:
    setOfTax=set()
    for element in dTemp[key]:
        sTax=element.replace("*"," ")
        sTax=sTax.strip()
        setOfTax.add(sTax)
    dFunctionToOrganism[key]=setOfTax

#Compute number of organism in database

setofAllOrganism=set()

for key in dFunctionToOrganism:
    for element in dFunctionToOrganism[key]:
        setofAllOrganism.add(element)


#Find TaxId for each Organism. Len = 1 for the genus/family name

dTaxonomytoTaxID={}
#Create a new dict to update Taxonomy
dFunctionToOrganismNewTax={}
lBadTax=[]
for key in dFunctionToOrganism:
    dFunctionToOrganismNewTax[key]=[]
    for element in dFunctionToOrganism[key]:
        sTax=element.split(" ")
        if len(sTax)==1:
            if sTax[0] in dNameToTaxID:
                dTaxonomytoTaxID[sTax[0]]=dNameToTaxID[sTax[0]]
                dFunctionToOrganismNewTax[key].append(sTax[0])
            else:
                lBadTax.append(" ".join(sTax))
        elif len(sTax)==2:
            sTemp=list(sTax)
            #Check if first letter of second word is an uppercase
            if sTax[1][0].isupper():
                sTemp[1]=sTemp[1].lower()
                #Some taxonomy with an upper case are not Family Genus but Genus species
                if " ".join(sTemp) in dNameToTaxID:
                    dTaxonomytoTaxID[" ".join(sTemp)]=dNameToTaxID[" ".join(sTemp)]
                    dFunctionToOrganismNewTax[key].append(" ".join(sTemp))
                #If the first letter of the second item in the list is an upper case = genus level
                elif sTax[1] in dNameToTaxID:
                    dTaxonomytoTaxID[sTax[1]]=dNameToTaxID[sTax[1]]
                    dFunctionToOrganismNewTax[key].append(sTax[1])
                #Else test if the species exist without modification
                else:
                    sTax=" ".join(sTax)
                    if sTax in dNameToTaxID:
                        dTaxonomytoTaxID[sTax]=dNameToTaxID[sTax]
                        dFunctionToOrganismNewTax[key].append(sTax)
                    else:
                        lBadTax.append(sTax)
            #General for Genus species
            else:
                sTax=" ".join(sTax)
                if sTax in dNameToTaxID:
                    dTaxonomytoTaxID[sTax]=dNameToTaxID[sTax]
                    dFunctionToOrganismNewTax[key].append(sTax)
                else:
                    lBadTax.append(sTax)
        elif len(sTax)>=3:
            sTax=" ".join(sTax)
            if sTax in dNameToTaxID:
                if sTax in dNameToTaxID:
                    dTaxonomytoTaxID[sTax]=dNameToTaxID[sTax]
                    dFunctionToOrganismNewTax[key].append(sTax)
                else:
                    lBadTax.append(sTax)
            else:
                lBadTax.append(sTax)


lTemp=[]
#This dict update the taxonomy for the next function
dNewGoodTax={}
#Allows us to correct some mistake in Faprotax (Upper case on species name and subsp.)
for element in lBadTax:
    sTax=element.split(" ")
    if len(sTax)==2:
        sTax[1]=sTax[1].lower()
        sTax=" ".join(sTax)
        if sTax in dNameToTaxID:
            dTaxonomytoTaxID[sTax]=dNameToTaxID[sTax]
            dNewGoodTax[element]=sTax
        else:
            lTemp.append(element)
    elif len(sTax)==3:
        sTax.insert(2,"subsp.")
        sTax=" ".join(sTax)
        if sTax in dNameToTaxID:
            dTaxonomytoTaxID[sTax]=dNameToTaxID[sTax]
            dNewGoodTax[element]=sTax
        else:
            lTemp.append(element)
    else:
        lTemp.append(element)

lBadTax=lTemp



#update dFunctionToOrganismNewTax with the new taxonomy recover:
for key in dFunctionToOrganismNewTax:
    for idx, item in enumerate(dFunctionToOrganism[key]):
        if item in dNewGoodTax:
            dFunctionToOrganismNewTax[key].append(dNewGoodTax[item])



#Delete all element who are not bacteria
dTemp={}
for key in dTaxonomytoTaxID:
    if dTaxonomytoTaxID[key] in lBacteriaTaxID:
        dTemp[key]=dTaxonomytoTaxID[key]

dTaxonomytoTaxID=dTemp


#Create a dict who associate fonction to organism
dOrganismtoListFunction={}
for key in dFunctionToOrganismNewTax:
    for element in dFunctionToOrganismNewTax[key]:
        if element in dOrganismtoListFunction:
            dOrganismtoListFunction[element].append(key)
        else:
            dOrganismtoListFunction[element]=[key]
a=0
b=0

#
dTaxIDtoFunction={}

#Create a dict who associate TaxID to function
for key in dTaxonomytoTaxID:
    if key in dOrganismtoListFunction:
        if dTaxonomytoTaxID[key] in dTaxIDtoFunction:
            dTaxIDtoFunction[dTaxonomytoTaxID[key]]=dTaxIDtoFunction[dTaxonomytoTaxID[key]]+dOrganismtoListFunction[key]
        else:
            dTaxIDtoFunction[dTaxonomytoTaxID[key]]=dOrganismtoListFunction[key]
    else:
        print ("BadTax:"+key)


#Use sets to delete double in function list for each TaxID
dTemp={}
a=0
b=0


for key in dTaxIDtoFunction:
    settemp=set(dTaxIDtoFunction[key])
    for element in dTaxIDtoFunction[key]:
        a+=1
    dTemp[key]=settemp
    b+=len(settemp)

dTaxIDtoFunction=dTemp


#Warning there are subspecies!
with open("./DatabaseTSV/FAPROTAXTable.tsv","w") as outputfile:
    for key in dTaxIDtoFunction:
        dTaxID={}
        dTaxID=lineage(key)[0]
        for item in dTaxID:
            if dTaxID[item] is None:
                dTaxID[item]="NaN"
        for element in dTaxIDtoFunction[key]:
            outputfile.write(dTaxID["superkingdom"]+"."+dTaxID["phylum"]+"."+dTaxID["class"]+"."+dTaxID["order"]+"."+dTaxID["family"]+"."+dTaxID["genus"]+"."+dTaxID["species"]+".\t"+key+"\t"+element.replace("_"," ")+"\n")

# possibilité de faire un taxize python sur les mauvaises taxonomies mais il faut l'installer! A verifier l'installation et les scores 0.75?
# pytaxize.gnr_resolve(names="Thermotoga neopolitana" , source=4, best_match_only='true')
# Attention plusieurs string ont le même TAXID! A faire attention pour le fichier de sortie (ex: Achromobacter xylosoxidans & Achromobacter xylosoxidans subsp. xylosoxidans)
# for element in set(lBadTax):
#    request=pytaxize.gnr_resolve(names=element , source=4, best_match_only='true')
#    if len(request[0])>0:
#        request=request[0][0]
#        if type(request)==dict:
#        #if request["score"]>0.9:
#            print (element+"\t"+request["name_string"])
