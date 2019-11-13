#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import csv

def Connection_to_DB(db_file):
    #connect to the db and place the cursor
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None



#Create the DB and put the cursor
dbTools=Connection_to_DB("../MACADAM/MACADAMdatabase.db")
dbToolsCursor=dbTools.cursor()

############## DROP TABLES ###############
dbToolsCursor.execute('''DROP TABLE IF EXISTS pathway;''')
dbToolsCursor.execute('''DROP TABLE IF EXISTS taxonomy;''')
dbToolsCursor.execute('''DROP TABLE IF EXISTS hierarchy;''')
dbToolsCursor.execute('''DROP TABLE IF EXISTS faprotax;''')
dbToolsCursor.execute('''DROP TABLE IF EXISTS PWYRXN;''')
dbToolsCursor.execute('''DROP TABLE IF EXISTS RXNName;''')
dbToolsCursor.execute('''DROP TABLE IF EXISTS RXNMTB;''')
dbToolsCursor.execute('''DROP TABLE IF EXISTS MTBName;''')
dbToolsCursor.execute('''DROP TABLE IF EXISTS RXNENZ;''')
dbToolsCursor.execute('''DROP TABLE IF EXISTS EnzName;''')
dbToolsCursor.execute('''DROP TABLE IF EXISTS IJSEMPhenoDB;''')
dbToolsCursor.execute('''DROP TABLE IF EXISTS RXNECNumber;''')


############## DROP TABLES ###############



dbToolsCursor.execute('''CREATE TABLE IF NOT EXISTS taxonomy(
            taxID INTEGER,
            name TEXT COLLATE NOCASE,
            typeOfName TEXT,
            parentTaxID INTEGER,
            taxonomicRank TEXT,
            taxonomy TEXT
            );''')
dbToolsCursor.execute('''CREATE TABLE IF NOT EXISTS pathway(
            taxonomy TEXT,
            ID TEXT,
            strainName TEXT,
            numberOfPGDBInSpecies INTEGER,
            numberOfPathway INTEGER,
            pathwayFrameID TEXT,
            pathwayScore REAL,
            pathwayFrequencyScore REAL,
            reasonToKeep TEXT
            );''' )
dbToolsCursor.execute('''CREATE TABLE IF NOT EXISTS hierarchy(
            pathwayFrameID TEXT,
            PathwayHierarchy TEXT,
            pathwayName TEXT
            );''')
dbToolsCursor.execute('''CREATE TABLE IF NOT EXISTS faprotax(
            taxonomy TEXT,
            taxID INTEGER,
            pathwayName TEXT
            );''')

dbToolsCursor.execute('''CREATE TABLE IF NOT EXISTS PWYRXN(
            PWY TEXT,
            RXN TEXT
            );''')

dbToolsCursor.execute('''CREATE TABLE IF NOT EXISTS RXNName(
            RXN TEXT,
            Name TEXT
            );''')

dbToolsCursor.execute('''CREATE TABLE IF NOT EXISTS RXNMTB(
            RXN TEXT,
            MTB TEXT
            );''')

dbToolsCursor.execute('''CREATE TABLE IF NOT EXISTS MTBName(
            MTB TEXT,
            Name TEXT
            );''')

dbToolsCursor.execute('''CREATE TABLE IF NOT EXISTS RXNENZ(
            ENZ TEXT,
            RXN TEXT
            );''')

dbToolsCursor.execute('''CREATE TABLE IF NOT EXISTS ENZName(
            ENZ TEXT,
            Name TEXT
            );''')

dbToolsCursor.execute('''CREATE TABLE IF NOT EXISTS RXNECNumber(
            RXN TEXT,
            ECNumber TEXT
            );''')

dbToolsCursor.execute('''CREATE TABLE IF NOT EXISTS IJSEMPhenoDB(
            taxonomy TEXT,
            taxID INTEGER,
            strainName TEXT,
            pathway TEXT,
            substrat TEXT,
            habitat TEXT
            );''')

dbTools.commit()

#Open CSV files
with open("./Results/allnamesremasteredImport.tsv","r") as inputfile:
    csvTaxonomy=csv.reader(inputfile,delimiter='\t')
    for t in csvTaxonomy:
        dbToolsCursor.execute('INSERT INTO  taxonomy VALUES (?,?,?,?,?,?)', t)

with open("./Results/PathwayTable.tsv","r") as inputfile:
    csvPathway=csv.reader(inputfile,delimiter='\t')
    for t in csvPathway:
        dbToolsCursor.execute('INSERT INTO  pathway VALUES (?,?,?,?,?,?,?,?,?)', t)

with open("./Results/PathwayHierarchy.tsv","r") as inputfile:
    csvPathway=csv.reader(inputfile,delimiter='\t')
    for t in csvPathway:
        dbToolsCursor.execute('INSERT INTO  hierarchy VALUES (?,?,?)', t)

with open("./Results/FAPROTAXTable.tsv","r") as inputfile:
    csvPathway=csv.reader(inputfile,delimiter='\t')
    for t in csvPathway:
        dbToolsCursor.execute('INSERT INTO  faprotax VALUES (?,?,?)', t)

with open("./Results/PWY.RXN.tsv","r") as inputfile:
    csvPathway=csv.reader(inputfile,delimiter='\t')
    for t in csvPathway:
        dbToolsCursor.execute('INSERT INTO  PWYRXN VALUES (?,?)', t)

with open("./Results/RXN.Name.tsv","r") as inputfile:
    csvPathway=csv.reader(inputfile,delimiter='\t')
    for t in csvPathway:
        dbToolsCursor.execute('INSERT INTO  RXNName VALUES (?,?)', t)

with open("./Results/RXN.CPD.tsv","r") as inputfile:
    csvPathway=csv.reader(inputfile,delimiter='\t')
    for t in csvPathway:
        dbToolsCursor.execute('INSERT INTO  RXNMTB VALUES (?,?)', t)

with open("./Results/CPD.Name.tsv","r") as inputfile:
    csvPathway=csv.reader(inputfile,delimiter='\t')
    for t in csvPathway:
        dbToolsCursor.execute('INSERT INTO  MTBName VALUES (?,?)', t)

with open("./Results/RXN.ENZ.tsv","r") as inputfile:
    csvPathway=csv.reader(inputfile,delimiter='\t')
    for t in csvPathway:
        dbToolsCursor.execute('INSERT INTO  RXNENZ VALUES (?,?)', t)

with open("./Results/ENZName.tsv","r") as inputfile:
    csvPathway=csv.reader(inputfile,delimiter='\t')
    for t in csvPathway:
        dbToolsCursor.execute('INSERT INTO  ENZName VALUES (?,?)', t)

with open("./Results/RXNECNumber.tsv","r") as inputfile:
    csvPathway=csv.reader(inputfile,delimiter='\t')
    for t in csvPathway:
        dbToolsCursor.execute('INSERT INTO  RXNECNumber VALUES (?,?)', t)

with open("./Results/IJSEMphenodb.tsv","r") as inputfile:
    csvPathway=csv.reader(inputfile,delimiter='\t')
    for t in csvPathway:
        dbToolsCursor.execute('INSERT INTO  IJSEMPhenoDB VALUES (?,?,?,?,?,?)', t)

dbToolsCursor.execute('''CREATE INDEX index_lineage ON pathway(taxonomy);''')
dbToolsCursor.execute('''CREATE INDEX index_name ON taxonomy(name);''')
dbToolsCursor.execute('''CREATE INDEX index_taxID ON taxonomy(taxID);''') #Usefull? Not in use i think
dbToolsCursor.execute('''CREATE INDEX index_faprotax ON faprotax(taxonomy);''')
dbToolsCursor.execute('''CREATE INDEX index_ENZname ON ENZName(Name);''')
dbToolsCursor.execute('''CREATE INDEX index_MTB ON RXNMTB(MTB);''')
dbToolsCursor.execute('''CREATE INDEX index_ENZ ON RXNENZ(ENZ);''')
dbToolsCursor.execute('''CREATE INDEX index_PWY ON PWYRXN(RXN);''')
dbToolsCursor.execute('''CREATE INDEX index_FrameID ON pathway(pathwayFrameID);''')
dbToolsCursor.execute('''CREATE INDEX index_MTBname ON MTBName(Name);''')
dbToolsCursor.execute('''CREATE INDEX index_RXNname ON RXNName(Name);''')
dbToolsCursor.execute('''CREATE INDEX index_RXNECNumber ON RXNECNumber(ECNumber);''')
dbToolsCursor.execute('''CREATE INDEX index_IJSEMPhenoDB ON IJSEMPhenoDB(taxonomy);''')

dbTools.commit()
dbTools.close()
