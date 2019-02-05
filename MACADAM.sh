####### MACADAM script ######
####### see DLRefSeq.sh for more information #######


bash ./Bacteria/DLRefSeq.sh

rm -rf /work/mleboulch/PathT/ptools-local/pgdbs/user/

bash ./Arche/DLRefSeq.sh

rm -rf /work/mleboulch/PathT/ptools-local/pgdbs/user/

cp -rf ./Arche/DatabaseTSV/* MergedFile/Arche/

cp -rf Bacteria/DatabaseTSV/* MergedFile/Bact/

python3 MergedFile/MergedArcheBact.py
python3 MergedFile/ImportSQLite.py
