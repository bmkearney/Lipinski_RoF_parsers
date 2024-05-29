import math
import sys
import time
import numpy

import datetime
import os
import itertools
import shutil

from itertools import islice

wfile = open("RoF_HMDB2.txt", "w")
counter=0
for file in os.listdir("."):
    if file.endswith('.sdf'):
        counter=counter+1
        index = 0
        with open(file, "r") as f:
            for line in f:
                index += 1
                if "> <JCHEM_RULE_OF_FIVE>" in line:
                    f.seek(0)
                    value="".join(islice(f, index, index + 1))
                    #print(value.strip())
                    if(value.strip()=="1"):
                        wfile.write(file[:-4]+"_out.pdbqt\n")
                    break
        if(counter%1000==0):
            print(counter)
wfile.close()
        
