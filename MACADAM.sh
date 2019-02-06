####### MACADAM script ######
####### see DLRefSeq.sh for more information #######


bash ./Bacteria/DLRefSeq.sh

rm -rf /work/mleboulch/PathT/ptools-local/pgdbs/user/

bash ./Archaea/DLRefSeq.sh

rm -rf /work/mleboulch/PathT/ptools-local/pgdbs/user/

cp -rf ./Archaea/DatabaseTSV/* MergedFile/Archaea/

cp -rf Bacteria/DatabaseTSV/* MergedFile/Bact/

python3 MergedFile/MergedArchaeaBact.py
python3 MergedFile/ImportSQLite.py
