import os
import sys
import subprocess

from MyException import MyException

class JARExtractor():

# -----------------------------------------------------------------------------
    def extract(self, jar_file):
        errorMessages = []
        if not isArchive(jar_file):           
            raise MyException(f"{jar_file} is not a valid jar archive")

        contentsDir = getExpandedDirName(jar_file)
        if os.path.exists(contentsDir):
            raise MyException(f"{contentsDir} needs to be removed")

        oDir = unzip(jar_file)
        return oDir

#-----------------------------------------------------------------------------
def unzip(fileName):
    #oDir = getExpandedDirName(fileName) # original
    oDir = "packages/" + fileName.replace(".jar", "")
    fileName = "pom_jar/" + fileName
    if os.path.exists(oDir):
        print(f"     Directory {oDir} already exists. Skipping extraction of {fileName}.")
    else:
        try:
            os.makedirs(oDir)
        except BaseException as be:
            raise MyException(f"Error while extracting files from the jar: {fileName}. Exceprion: {be}")

        try:
            #print(f"     Processing {fileName} into {oDir}")
            command = "unzip %s -d %s" % (fileName, oDir)
            process = subprocess.Popen(command, shell=True)
            status  = os.waitpid(process.pid, 0)[1]
        except BaseException as be:
            msg = f"An error ocured while executing subprocess.Popen({command}, shell=True): {be}"
            raise MyException(f"Error while extracting files from the jar: {fileName}. Error: {msg}")

    return oDir # return the directory
    #walkFiles(oDir) commented because rises an exception

#-----------------------------------------------------------------------------
def walkFiles(dirName):
   # print ("walking the files of %s" % dirName)
    dirs = os.walk(dirName)

    for (dirPath, dirNames, fileNames) in dirs:
        for fileName in fileNames:
            if isArchive(fileName):
                unzip(os.path.join(dirPath, fileName))

#-----------------------------------------------------------------------------
def getExpandedDirName(fileName):
    fileDir  = "packages/" + os.path.dirname(fileName)
    baseName = "%s.contents" % os.path.basename(fileName)

    return os.path.join(fileDir, baseName)

#-----------------------------------------------------------------------------
def isArchive(fileName):
    ext = fileName[-4:]

    if ext in [".zip", ".jar"]: return True
    return False

#-----------------------------------------------------------------------------

