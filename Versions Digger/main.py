import os
import re

import requests
from Downloader import Downlaoder

# base url for maven search
base = "https://repo1.maven.org/maven2/"

# "versions/" directory contains one file for each GgoupID and AnchorID (syntax: GroupID_AnchorID.txt)
# which contains a list of versions for that G:A as published on maven repository (may be many).
# From each file, read all the versions available, construct a GAV link to the POM file on maven
# download it and search inside for github links 
files_list = os.listdir("versions/")
#files_list.sort()

# create a downloader
dl = Downlaoder()

# create loggers
found = open("found.csv", "w")
not_found = open("not_found.csv", "w")

# start opening GA files
for f_gav in files_list:
    try: 
        file = open("versions/" + f_gav, 'r')
    except BaseException as be:
        print(f"Trying to read {f_gav} and got error: {be}")
    
    # read versions of f_gav and order them (newer first)
    versions = []
    try:
        versions = file.readlines()
        versions.sort(reverse=True)
    except BaseException as be:
        print(f"Trying to read versions from {f_gav} and got error: {be}")

    # format GroupID and ArtefactID 
    gav = os.path.basename(f_gav).replace('.txt', '').split('_')
    g = gav[0]
    a = gav[1]

    # get the filename
    file_name = os.path.basename(f_gav).replace('_', '/').replace('.txt', '/').replace('.', '/')

    print(f"Analyzing: {g} : {a} ...")

    # init the counter: a G:A will be signed as not found only when all versions have been processed 
    # and no gh links were found
    count = 0

    # start iterating on all G:A's versions until a github link is found, then breake
    for v in versions:

        count += 1

        # some formating on url
        gid = g.replace(".", "/")
        url = re.sub(r'\n', '', (base + gid + "/" + a + "/" + v + "/" + a + "-" + v + "." + "pom")) 
        try:
            # query
            response = requests.get(url, allow_redirects=True)
            if b"github.com" in response.content:
                #open("pom/"+f_gav+"_"+v, "wb").write(response.content)
                # found "github.com", sign as found and break the cycle to start wit the next G:A
                found.write(g+","+a+","+v)
                print(f"    - Found {g} : {a} : {v}")
                break
            else:
                #open("pom/_"+f_gav+"_"+v, "wb").write(response.content)
                # last version examinated and didn't find "github.com": insert the G:A amount not found
                if count >= len(versions):
                    print(f"Adding to not found: {g}:{a}")
                    not_found.write(g+","+a+",NONE")          
        except Exception as e:
            print("UPS: {e}")

            
        