import math
import sys
import time
import numpy

import datetime
import os
import itertools
import shutil

class Atom:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z


flagged_files=[]
writefile=open("flagged.txt",'w')
if(not os.path.exists('flagged/')):
    os.makedirs('flagged/')

def distance(x1,x2,y1,y2,z1,z2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** .5

def checker(atoms):
    for i,j in itertools.combinations(atoms,2):
        if (distance(float(i.x),float(j.x),float(i.y),float(j.y),float(i.z),float(j.z))<0.9):
            return -1

filenames = os.listdir(os.getcwd())
count=0
for f in filenames:
    if (f[-6:] == '.pdbqt'):
        count=count+1
        if(count%1000==0):
            print(count)
        file = open(f,'r')
        atoms=[]
        for line in file:
            if line.startswith("ATOM"):
                if("H" not in line.split()[-1]):
                    atoms.append(Atom(line.split()[5],line.split()[6],line.split()[7]))
            if line.startswith("ENDMDL"):
                if(checker(atoms) == -1):
                    file.close()
                    writefile.write(f + '\n')
                    shutil.move(f, 'flagged/')
                else:
                    file.close()
                break

writefile.close()
