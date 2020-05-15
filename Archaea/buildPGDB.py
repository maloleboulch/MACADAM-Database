#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from optparse import OptionParser
import os
import shutil
from Bio import SeqIO
import subprocess
import time
import re


#Command line arguments
parser = OptionParser()
#Directory of the GBFF files
parser.add_option("-g" , "--gbff_directory" , dest="gbff_directory" , help="Directory of the REFSEQ GBFF files")
#Garder cette ligne?
#parser.add_option("-p" , "--pgdb_directory" , dest="pgdb_directory" , help="Path of the output of pathologic, normally in the location of the ptools-local directory" , default="/home/malo/ptools-local/pgdbs/user/")
#working directory
parser.add_option("-t" , "--working_directory" , dest="working_directory" , help="working directory")
(options, args) = parser.parse_args()
dpaths = vars(options)

#check if all path end with an os separator
for key in dpaths.keys():
    value=dpaths[key]
    if not value.endswith(os.sep):
        value=value+os.sep
    dpaths[key]=value

filesgbff=os.listdir(dpaths['gbff_directory'])
dirgbff=dpaths['gbff_directory']
dirtmp=dpaths['working_directory']



#creation of a tmp directory inside gbff directory
#if not os.path.exists("./tmp/"):
#    os.makedirs("./tmp/")

#creation of a file storing the 16S copy number
# f16Scopynumber=open("./downloads/16scopynumber.tsv","w")

#Open each file and create organism-params.dat, genetics-elements.dat and launch pathologic.
for file in filesgbff:
    print (file)
    #Take Assembly number from gbff name because not all gbff contain it
    sAssemblyAccesionNumber=file.split(".")[0]
    sAssemblyAccesionNumber=re.sub('[^0-9]','', sAssemblyAccesionNumber)
    if file.endswith(".gbff"):
        #delete and recreate dirtmp
        shutil.rmtree(dirtmp)
        os.makedirs(dirtmp)
        shutil.copy(dirgbff+file,dirtmp)

        #reset all list and iterator
        lTaxid=[]
        lNCnumber=[]
        lOrganism=[]
        lTopology=[]
        iNumberofGeneticsElement=0

        gbff=open(dirtmp+file,"r")
        #Use of Biopython for parse genbank file. Usefull for plasmid
        GenbankParse=SeqIO.parse(gbff,"genbank")

        #iterator for 16S copynumber. We only check in the bacterial genome not in the plasmid
        # k=0
        #
        try:
            for record in GenbankParse:
                #Store the taxid in lTaxid
                features=record.features
                for feat in features:
                    if feat.type=="source":
                        for tax in feat.qualifiers["db_xref"]:
                            if tax.startswith("taxon:"):
                                lTaxid.append(tax)

                #store accession number in lNCnumber
                lNCnumber.append(record.annotations["accessions"][0])
                #print (lNCnumber)

                #store the oragnism name's
                lOrganism.append(record.annotations["organism"])

                #check the topology of the genetic elements Ne marche pas sur le cluster. Topology absent de certains gbff?
                #lTopology.append(record.annotations["topology"])

                #number of genetics element in gbff file.
                iNumberofGeneticsElement+=1

                #create seperate files for differents genetics elements
                SeqIO.write(record,dirtmp+record.annotations["accessions"][0]+".gbff","genbank")
        except:
            print ("ERROR on file:"+file)

        #create the genetic-element.dat file
        i=0
        fGeneticelement=open(dirtmp+"genetic-elements.dat","w")
        while i<iNumberofGeneticsElement:
            fGeneticelement.write("ID\t"+lNCnumber[i]+"\n")
            if i==0:
                fGeneticelement.write("NAME\tgenome\n")
                fGeneticelement.write("TYPE\t:CHRSM\n")
            else:
                fGeneticelement.write("NAME\tplasmid"+str(i)+"\n")
                fGeneticelement.write("TYPE\t:PLASMID\n")
            #if lTopology[i]=='circular': ne marche pas sur le cluster
            fGeneticelement.write("CIRCULAR?\tY\n")
            #else:
            #    fGeneticelement.write("CIRCULAR?\tN\n")
            fGeneticelement.write("ANNOT-FILE\t"+lNCnumber[i]+".gbff\n")
            fGeneticelement.write("//\n")
            i+=1
        fGeneticelement.close()

        #create the organism-params.dat file. Other wau to open a file
        with open(dirtmp+"organism-params.dat","w") as fOrganismparams:
        #fOrganismparams=open(dirtmp+"organism-params.dat","w")
            #fOrganismparams.write("ID\t"+lNCnumber[0].replace("_","")+"\n") Old identifier
            fOrganismparams.write("ID\t"+"G"+sAssemblyAccesionNumber+"\n")
            fOrganismparams.write("STORAGE\tFILE\n")
            fOrganismparams.write("NAME\t"+lOrganism[0]+"\n")
            fOrganismparams.write("RANK\tSTRAIN\n")
            fOrganismparams.write("DOMAIN\tTAX-2157\n")
            fOrganismparams.write("NCBI-TAXON-ID\t"+(''.join(lTaxid[0])).replace("taxon:","")+"\n")
            fOrganismparams.write("CREATE?\tT\n")
            fOrganismparams.close()

        #launch pathway-tools on the file
        print ("start prediction for "+(''.join(lTaxid[0])).replace("taxon:",""))
        print (dirtmp)
        subprocess.call(["pathway-tools", "-lisp", "-no-cel-overview", "-no-web-cel-overview", "-nologfile", "-no-patch-download", "-disable-metadata-saving", "-patho", dirtmp])
        
