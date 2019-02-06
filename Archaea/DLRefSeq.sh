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

echo "Deleting old files"
rm -r downloads/*
rm -r gbff/*


#download the summary of RefSeq Bacteria
wget -nv -P downloads ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/archaea/assembly_summary.txt

python3 CompleteGenome.py

#Add to the ftp url the path to download all "_genomics.gbff.gz" files
awk 'BEGIN{FS=OFS="/";filesuffix="genomic.gbff.gz"}{ftpdir=$0;asm=$10;file=asm"_"filesuffix;print ftpdir,file}' downloads/ftpdirpaths.txt > downloads/ftpfilepaths.txt


#Old downloads line
#time wget -nv -P gbff -i downloads/ftpfilepaths.txt

ftpurl=$(<downloads/ftpfilepaths.txt)
echo $ftpurl | xargs -n 1 -P 24 wget -q -P gbff

#time gunzip -d ./gbff/*
find ./gbff/* -name "*gz*" -print0 | parallel -q0 gunzip

time python3 Parallelize.py -n 20

#Load library for pathway tools for genotoul only (Now in Parallelize output)
#export LD_LIBRARY_PATH=/tools/libraries/glibc/glibc-2.14/build/:$LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=/tools/libraries/jpeg/jpegv8/jpeg-8c/.libs/:$LD_LIBRARY_PATH


#Qarray all the gbff files
qarray -l mem=4G -l h_vmem=32G -sync y qarray.sh

#Reset Path
unset LD_LIBRARY_PATH
source /etc/profile

#copy all PGDB from the ptools-local directory to current directory
for d in /work/mleboulch/PathT/ptools-local/pgdbs/user/*; do tar -zcf ${d:0:${#d}}.tar.gz $d; done

rm -rf /work/mleboulch/PathT/ptools-local/pgdbs/user/*/

cp -r  /work/mleboulch/PathT/ptools-local/pgdbs/user/*.tar.gz ./PGDBs/

#Dispatch PGBDs between unique and shared

python3 Deletedouble.py
python3 RenamePGDBs.py
python3 ExtractPathwayReport.py
python3 GenerateTaxonomyLineage.py


if [ $1 == Microcyc ]; then
	python3 MicrocycIndexandSubstitution.py -N
	python3 1%IntegrateUniqueTaxID.py
	python3 2%deletesupword.py
	python3 3%KeepOnlyTip.py
	python3 DLMicrocycandExtractOnlyDownloads.py
	python3 DLMicrocycandExtractWithoutdownloads.py
fi
python3 GenerateTaxonomyLineageAfterMicroCyc.py
python3 CalculateOldScore.py
python3 CountStrainPerSpecies.py
python3 PrepareTSVforDatabase.py
python3 getClassesOfPathwayremake.py
python3 IntegrateFaproTax.py
python3 IntegrateIJSEMPDB.py
python3 IntegrateMetaboliteAndReaction.py
python3 RemasteredAllTax.py
