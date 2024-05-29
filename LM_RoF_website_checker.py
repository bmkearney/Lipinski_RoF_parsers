import requests
import argparse
import os

def hmdb_checker(id,ofile):
    api_url = "https://www.lipidmaps.org/rest/compound/lm_id/"+id+"/hmdb_id"
    response = requests.get(api_url)
    try:
        if("hmdb_id" in response.json().keys()):
            print("HMDB exists")
            #print(id)
            ofile.write(id+'\n')
        else:
            print("no HMDB")
            rule_checker(id)
    except:
        print("Hard Error")
        rule_checker(id)

def rule_checker(id):
    api_url = "https://www.lipidmaps.org/rest/compound/lm_id/"+id+"/physchem"
    response = requests.get(api_url)
    flag_count=0 
    try:
        mw=float(response.json()['molecular_weight'])
    except:
        print("literally nothing")
        with open("HMDB_LM_missing.txt",'a') as ofile:
            ofile.write(id+'\n')
            ofile.close()
        return(2)#2 means I got literally nothing.        
    try:
        hdonor=int(response.json()['hbond_donors'])
    except:
        hdonor=0
        flag_count=flag_count+1
    try:
        hacceptor=int(response.json()['hbond_acceptors'])
    except:
        hacceptor=0
        flag_count=flag_count+1
    try:
        logp=float(response.json()['slogp'])
    except:
        logp=0
        flag_count=flag_count+1
    score=0
    if mw>500:
        score=score+1
    if hdonor>5:
        score=score+1
    if hacceptor>10:
        score=score+1
    if logp>5:
        score=score+1
    print(score)
    if score>1:
        print("failed screening")
        with open("LM_RoF_failed.txt",'a') as ofile:
            ofile.write(id+'\n')
            ofile.close()
    else:
        if(flag_count>1):
            print("missing data")
            with open("LM_RoF_except.txt","a") as ofile:
                ofile.write(id+'\n')
                ofile.close
        else:
            print("passed screening")
            with open("LM_RoF_pass.txt","a") as ofile:
                ofile.write(id+'\n')
                ofile.close()

#hmdb_checker("LMST01010008")
#hmdb_checker("LMPK12160027")
with open("HMDB_LM_duplicates.txt", 'w') as ofile:
    for file in os.listdir('.'):
        if(file.endswith('.pdbqt')):
            print(file.split('.')[0])
            hmdb_checker(file.split('.')[0],ofile)
            
    ofile.close()
