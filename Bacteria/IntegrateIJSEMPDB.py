#Integrate the IJSEM Database to Macadam. https://figshare.com/articles/International_Journal_of_Systematic_and_Evolutionary_Microbiology_IJSEM_phenotypic_database/4272392
#Need the IJSEM_pheno_db_v1.0.txt or newer version in the downloads directory and thee NCBI taxonomy too.

###Load NCBI taxonomy####
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
            if sTaxID=="2":
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






with open("../MandatoryFile/IJSEM_pheno_db_v1.0.txt","r", encoding="ISO-8859-14") as inputfile:
    lListofLines=inputfile.readlines()[1:]
    #For each taxonomy (Genus+species+strain) connect to: Genus, Species, Strain, Metabolic Pathway, Substrate, Habitat
    dTaxonomytoInfos={}
    lAllTax=[]
    for line in lListofLines:
        line=line.split("\t")
        line[11]=line[11].strip()
        line[12]=line[12].strip()
        line[13]=line[13].strip()
        if line[11]+" "+line[12]+" "+line[13] in dTaxonomytoInfos:
            dTaxonomytoInfos[line[11]+" "+line[12]+" "+line[13]][3].update(line[10].split(", "))
            dTaxonomytoInfos[line[11]+" "+line[12]+" "+line[13]][4].update(line[25].split(", "))
            if line[0]=="other":
                temp=set()
                temp.add(line[28])
                dTaxonomytoInfos[line[11]+" "+line[12]+" "+line[13]][-1].update(temp)
            else:
                temp=set()
                temp.add(line[0])
                dTaxonomytoInfos[line[11]+" "+line[12]+" "+line[13]][-1].update(temp)
                if line[28]!='':
                    temp=set()
                    temp.add(line[28])
                    dTaxonomytoInfos[line[11]+" "+line[12]+" "+line[13]][-1].update(temp)
        else:
            dTaxonomytoInfos[line[11]+" "+line[12]+" "+line[13]]=[line[11],line[12],line[13],set(line[10].split(", ")),set(line[25].split(", "))]
            if line[0]=="other":
                temp=set()
                temp.add(line[28])
                dTaxonomytoInfos[line[11]+" "+line[12]+" "+line[13]].append(temp)
            else:
                temp=set()
                temp.add(line[0])
                dTaxonomytoInfos[line[11]+" "+line[12]+" "+line[13]].append(temp)
                if line[28]!='':
                    temp=set()
                    temp.add(line[28])
                    dTaxonomytoInfos[line[11]+" "+line[12]+" "+line[13]][-1].update(temp)


# for item in dTaxonomytoInfos:
#     print (item)
#     print (dTaxonomytoInfos[item])



###Create lineage ####
i=0
j=0
dTaxonomytoInfosPresent={}
for item in dTaxonomytoInfos:
    #### Test if full name is in NCBI Tax #####
    tax=dTaxonomytoInfos[item][0].title()+" "+dTaxonomytoInfos[item][1].lower()
    if tax in dNameToTaxID:
        i+=1
        if dTaxonomytoInfos[item][0].title()+" "+dTaxonomytoInfos[item][1].lower()==dTaxonomytoInfos[item][2]:
            name=dTaxonomytoInfos[item][0].title()+" "+dTaxonomytoInfos[item][1].lower()
        else:
            name=dTaxonomytoInfos[item][0].title()+" "+dTaxonomytoInfos[item][1].lower()+" "+dTaxonomytoInfos[item][2]
        dTaxonomytoInfosPresent[name]=dTaxonomytoInfos[item]
        dTaxonomytoInfosPresent[name].append(dNameToTaxID[tax])
    else:
        ####### Some Have the complete Name has species Name
        tax=dTaxonomytoInfos[item][1]
        if tax in dNameToTaxID:
            if dTaxonomytoInfos[item][1]==dTaxonomytoInfos[item][2]:
                name=dTaxonomytoInfos[item][1]
            else:
                name=dTaxonomytoInfos[item][1]+" "+dTaxonomytoInfos[item][2]
            dTaxonomytoInfosPresent[name]=dTaxonomytoInfos[item]
            dTaxonomytoInfosPresent[name].append(dNameToTaxID[tax])
            j+=1

print (i)
print (j)

k=0
#### generate lineage #####
with open("./DatabaseTSV/IJSEMphenodb.tsv","w") as outputfile:
    for item in dTaxonomytoInfosPresent:
        sTaxID=dTaxonomytoInfosPresent[item][-1]
        dTaxID=lineage(sTaxID)[0]
        if dTaxID["superkingdom"]=="2":
            for element in dTaxID:
                if dTaxID[element]==None:
                    dTaxID[element]="NaN"
            tmpset=set()
            for element in dTaxonomytoInfosPresent[item][4]:
                tmpset.add(element.replace("\"",""))
                dTaxonomytoInfosPresent[item][4]=tmpset
            tmpset=set()
            for element in dTaxonomytoInfosPresent[item][5]:
                tmpset.add(element.replace("\"",""))
                dTaxonomytoInfosPresent[item][5]=tmpset
            for element in dTaxonomytoInfosPresent[item][3]:
                element=element.replace("\"","")
                outputfile.write(dTaxID["superkingdom"]+"."+dTaxID["phylum"]+"."+dTaxID["class"]+"."+dTaxID["order"]+"."+dTaxID["family"]+"."+dTaxID["genus"]+"."+dTaxID["species"]+".\t"+dTaxonomytoInfosPresent[item][-1]+"\t"+item)
                outputfile.write("\t"+element+"\t"+", ".join(list(dTaxonomytoInfosPresent[item][4]))+"\t"+", ".join(list(dTaxonomytoInfosPresent[item][5]))+"\n")
        else:
            k+=1

# print (k)
# print (len(dTaxonomytoInfos))
#4873 Organisme 4623 à la fin
