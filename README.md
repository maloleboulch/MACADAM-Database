# MACADAM URL
# [macadam.toulouse.inra.fr](macadam.toulouse.inra.fr)

# MACADAM Dependancy
- Pathway Tools v23 installed and in your path. (http://bioinformatics.ai.sri.com/ptools/ to have a licence)
  - You must launch Pathway Tools manually one time before executing the full pipeline. Thanks to that Pathway-Tools can download patches.
- Python 3 with pandas (https://pandas.pydata.org/), biopython (https://biopython.org/)
- MetaCyc Datafiles (https://biocyc.org/download-flatfiles.shtml to have a license)
- NCBI Taxonomy flatfiles (ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip)
- MetaCyc 16.5 datafiles

# MACADAM scripts:
Master scripts: MACADAM.sh
MASTER scripts in bacteria and archaea: MACADAMBac1.sh, MACADAMBac2.sh, MACADAMArch1.sh, MACADAMArch2.sh
MACADAM-test.sh: Launch only on Archaea for testing.

Some scripts have absolute path to change be fore launching:
  - MACADAMBac2.sh
  - MACADAMArch2.sh
  - MACADAM.sh

To create MACADAM launch the MACADAM.sh script.

# MACADAM ressources
Maximum space usage: 750 GB
Optimized for SLURM
3 parameters can be changed for the parralel computing of the PGDBs:
  - inside MACADAM.sh (-c 1: number of cores and --%=50 : number of simultaneous jobs )
  - option in MACADAMArch1 and MACADAMBac1 when Parallelize.py is called: -n 20 : number of genomes per jobs.
Be carrefull to optimize these numbers to limit disk access during PGDBS generation.

# MicroCyc
If MicroCyc doesn't work anymore you can comment all the MicroCyc scripts in the MicroCyc part in MACADAMBac2 and MACADAMArch2.

#Errors
If pathway tools cannot create some PGDBs, the script RenamePGDBs.py or ExtractPathwayReport.py will crash and show the PGDBs names.
getClassesOfPathway.py will crashed if some pathways are unknown in MetaCyc 23.1 or 16.5. Yout must find the hierarchy on internet and add it to the UnknownPathway.tsv file.
ShareIndexAfterLineage.tsv is the main intermediary files. You can follow changes at each steps of MACADAM inside it



# MACADAM Database
Progress in genome sequencing and bioinformatics opens up new possibilities, including that of correlating genome annotations with functional information such as metabolic pathways. Thanks to the development of functional annotation databases, scientists are able to link genome annotations with functional annotations. Here we present MACADAM (MetAboliC pAthways DAtabase for Microbial taxonomic groups), a user-friendly database that allows finding presence/absence/completeness statistics for metabolic pathways at a given microbial taxonomic position. MACADAM, for each 13,509 (11,794) prokaryotic “RefSeq complete genomes”, builds a PGDB (Pathway Genome DataBase) thanks to Pathway-tools software based on MetaCyc data that includes metabolic pathways as well as associated metabolites, reactions, enzymes. To ensure the highest quality of the genome functional annotation data, MACADAM contains also MicroCyc, a manually curated collection of PGDBs, FAPROTAX (Functional Annotation of Prokaryotic Taxa) manually curated functional annotation database and IJSEM phenotypic database. The MACADAM database contains 13,195 bacterial organisms, 314 archaea organisms, 1260 unique metabolic pathways, completed with 82 functional annotations from FAPROTAX and 16 from the IJSEM phenotypic database. A total of 7921 metabolites, 592 enzymatic reactions, 2134 EC numbers and 7440 enzymes are collected in MACADAM. MACADAM can be queried at any ranks of the NCBI taxonomy (from phyla to species). It provides the possibility to explore functional information completed with metabolites, enzymes, enzymatic reactions and EC numbers. MACADAM returns a tabulated file containing a list of pathways with two scores (pathway score and pathway frequency score) that are presents in the queried taxa. The file contains also the names of the organisms in which the pathways are found and the metabolic hierarchy associated to the pathways. Finally, MACADAM can be downloaded as a single file and queried with SQLite or python command lines or explored through a web interface.

# MACADAM Database Repository

How: MACADAM database is built from a pipeline of python scripts. The update process takes around 2 days, depending on the parallelization capacities. MACADAM needs, as dependencies, Python 3, the Pandas package and a valid license of Pathway Tools that have to be installed. All other dependencies are included by default in python 3 setup. MACADAM can be updated at each RefSeq release (i.e. addition of new high-quality annotated genomes). MACADAM automatically downloads the new index summary from RefSeq. Then, MACADAM building script downloads and process all the genomes that matched our quality standards and launches Pathway Tools on each one of them. This is the crucial part in terms of computing power. In order to save time, the process is parallelized on the cluster of GenoToul Bioinformatics platform (http://bioinfo.genotoul.fr/) that provides access to high-performance computing resources. To do so, we process genomes by batch of 50 genomes and this whole step is done approximatively in one day. This step needs a least 8GB of RAM for each batch. The generation of the unique ID and the calculation of the PS take around 6 hours each one, due to file movements and extraction of archives. MACADAM can take up to 600 GB of disk space during the construction of the PGDBs, it is the most critical part. After compressing, this file takes 150 GB of space disk.

Who: MACADAM database benefits from GenoToul Bioinformatics platform facilities including permanent staff and technical support. The database will be available for downloading and querying as long as it demonstrates its utility for research community. Moreover, python script pipeline is available on GitHub repository (GitHub URL: https://github.com/maloleboulch/MACADAM-Database.
