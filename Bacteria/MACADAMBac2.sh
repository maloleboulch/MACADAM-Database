#!/bin/bash
#Following of the first script

#Compress all PGDBs in Pathway Tools export directory and copy in ./PDGBs directory

module load system/Python-3.6.3

#Warning! Absolute Path#

find /home/mleboulch/work/PathT23/ptools-local/pgdbs/user -maxdepth 1 -mindepth 1 -type d -print0 | xargs -t -0 -P 16 -I {} tar zcf {}.tar.gz {}

rm -r /home/mleboulch/work/PathT23/ptools-local/pgdbs/user/*/

rm -r /home/mleboulch/work/PathT23/ptools-local/pgdbs/user/PGDB-counter.dat

rm -r ./PGDBs/
mkdir ./PGDBs/
mkdir ./PGDBs/Uniq

cp /home/mleboulch/work/PathT23/ptools-local/pgdbs/user/*.tar.gz ./PGDBs/

rm /home/mleboulch/work/PathT23/ptools-local/pgdbs/user/*.tar.gz

#Dispatch PGBDs between unique and shared

python3 Delete_Double.py

python3 RenamePGDBs.py
python3 ExtractPathwayReport.py
python3 GenerateTaxonomyLineage.py

#MicroCyc part

python3 MicrocycIndexandSubstitution.py -N
python3 1%IntegrateUniqueTaxID.py
python3 2%deletesupword.py
python3 3%KeepOnlyTip.py

rm -r ./MicroCyc/
mkdir ./Microcyc/

python3 DLMicrocycandExtractOnlyDownloads.py
python3 DLMicrocycandExtractWithoutdownloads.py

##End of MicroCyc

python3 GenerateTaxonomyLineageAfterMicroCyc.py
python3 CalculateOldScore.py

rm -r ./DatabaseTSV/
mkdir ./DatabaseTSV/

python3 CountStrainPerSpecies.py
python3 PrepareTSVforDatabase.py
python3 getClassesOfPathway.py
python3 IntegrateFaproTax.py
python3 IntegrateIJSEMPDB.py
python3 IntegrateMetaboliteAndReaction.py
python3 RemasteredAllTax.py
