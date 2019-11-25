#!/bin/sh
####### MACADAM script ######
####### see DLRefSeq.sh for more information #######

#Load Python on SLURM
module load system/Python-3.6.3 #Python3.6.3 have Biopython in it.

#Launch a first time on Archaea

cd Archaea/

MACADAMArch1=$(sbatch -c 1 --mem=16G --wait MACADAMArch1.sh)


MACADAMArray=$(sarray -c 1 --mem-per-cpu=8G  -o ./Pt-Tools_%J_%A.out -e ./Pt-Tools_%J_%A.err --wait --%=20 sarray.sh)

rm -r ./gbff/*

MACADAMArch2=$(sbatch -c 1 --mem=16G --wait MACADAMArch2.sh)


#Launch on Bacteria

cd ..

cd Bacteria/

MACADAMBac1=$(sbatch -c 1 --mem=16G --wait MACADAMBac1.sh)


MACADAMBacArray=$(sarray -c 1 --mem-per-cpu=8G  -o ./Pt-Tools_%J_%A.out -e ./Pt-Tools_%J_%A.err --wait --%=50 sarray.sh)

rm -r ./gbff/*

MACADAMBac2=$(sbatch -c 1 --mem=16G --wait MACADAMBac2.sh)


#Merged files

cd ..

rm -rf /work/mleboulch/PathT/ptools-local/pgdbs/user/

cp -rf ./Archaea/DatabaseTSV/* MergedFile/Archaea/

cp -rf Bacteria/DatabaseTSV/* MergedFile/Bact/

cd MergedFile

python3 MergedArcheBact.py
python3 ImportSQLite.py
