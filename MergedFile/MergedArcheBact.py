import os

lListofFile=[]
for file in os.listdir("./Bact/"):
    lListofFile.append(file)

for element in lListofFile:
    bact="./Bact/"+element
    arch="./Arche/"+element
    result="./Temp/"+element
    lList=[bact,arch]
    with open(result,"w") as outfile:
        for fname in lList:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

for file in os.listdir("./Temp/"):
    lines_seen = set()
    outfile = open("./Results/"+file, "w")
    for line in open("./Temp/"+file, "r"):
        if line not in lines_seen:
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
