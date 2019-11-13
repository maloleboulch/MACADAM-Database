#!/bin/bash
# This bash script downloads all RefSeq bacteria genomes.
#https://www.ncbi.nlm.nih.gov/genome/doc/ftpfaq/#allcomplete
#ftp://ftp.ncbi.nlm.nih.gov/genomes/README_assembly_summary.txt
# For genbank (not RefSeq) ftp://ftp.ncbi.nih.gov/genomes/genbank/bacteria/assembly_summary.txt
#Arguments:
#1 Reference genome (reference) only or all chromosome and complete genome (all)
#2 ptools-local path with /pgdbs/user/. ex: /home/user/ptools-local/pgdbs/user/*
#All python script are in python 3
# ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz take nodes.dmp & names.dmp & merged.dmp to download directory
# Download the IJSEM(IJSEM_pheno_db_v1.0.txt) (https://figshare.com/articles/International_Journal_of_Systematic_and_Evolutionary_Microbiology_IJSEM_phenotypic_database/4272392) and FAPROTAX.txt (http://www.zoology.ubc.ca/louca/FAPROTAX/lib/php/index.php?section=Home)  of Faprotax to the download directory
#Following file are needed: PT-tools v20.5 & 16.5
# ./classes16.5.dat
# ./classes.dat
# ./compounds16.5.dat
# ./compounds.dat
# ./enzrxns16.5.dat
# ./enzrxns.dat
# ./pathways16.5.dat
# ./pathways.dat
# ./reactions16.5.dat
# ./reactions.dat


#Delete all files in the downloads directory

module load system/Python-3.6.3

echo "Deleting old files"
rm -r downloads/*
mkdir downloads
rm -r gbff/*
mkdir gbff

#download the summary of RefSeq Bacteria
wget -nv -P downloads https://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt

python3 CompleteGenome.py

#Add to the ftp url the path to download all "_genomics.gbff.gz" files
awk 'BEGIN{FS=OFS="/";filesuffix="genomic.gbff.gz"}{ftpdir=$0;asm=$10;file=asm"_"filesuffix;print ftpdir,file}' downloads/ftpdirpaths.txt > downloads/ftpfilepaths.txt

#HTTPS are mandatory

sed -i 's/ftp:/https:/g' ./downloads/ftpfilepaths.txt

ftpurl=$(<downloads/ftpfilepaths.txt)
echo $ftpurl | xargs -n 1 -P 16 wget -P gbff

#Uncompress gz file
find ./gbff/* -name '*.gz*' -print0 | xargs -0 -I {} -P 8 gunzip {}

python3 Parallelize.py -n 30
