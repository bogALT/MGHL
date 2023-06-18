import os
import sys
import subprocess

class JARExtractor():
    def __init__(self):
        print("JAR Extractor created")

# -----------------------------------------------------------------------------
    def extract(self, jar_file):
        errorMessages = []
        if not isArchive(jar_file):
            errorMessages.append("file is not an archive:        %s" % jar_file)

        contentsDir = getExpandedDirName(jar_file)
        if os.path.exists(contentsDir):
            errorMessages.append("directory needs to be removed: %s" % contentsDir)

        if len(errorMessages) > 0:
            for errorMessage in errorMessages:
                print(errorMessage)
            sys.exit()

        oDir = unzip(jar_file)
        return oDir #return the directory

#-----------------------------------------------------------------------------
def unzip(fileName):
    #oDir = getExpandedDirName(fileName) # original
    oDir = fileName.replace(".jar", "")

    if os.path.exists(oDir):
        print(f"Directory {oDir} already exists. Skipping extraction of {fileName}.")
    else:
        try:
            os.makedirs(oDir)
        except BaseException as be:
            print("Base Exception = ", be)

        try:
            print ("Processing: %s into: %s" % (fileName, oDir))
            command = "unzip %s -d %s" % (fileName, oDir)
            process = subprocess.Popen(command, shell=True)
            status  = os.waitpid(process.pid, 0)[1]
        except BaseException as be:
            print(f"An error ocured while executing subprocess.Popen({command}, shell=True):\n{be}")

    return oDir # return the directory
    #walkFiles(oDir) commented because rises an exception

#-----------------------------------------------------------------------------
def walkFiles(dirName):
    print ("walking the files of %s" % dirName)
    dirs = os.walk(dirName)

    for (dirPath, dirNames, fileNames) in dirs:
        for fileName in fileNames:
            if isArchive(fileName):
                unzip(os.path.join(dirPath, fileName))

#-----------------------------------------------------------------------------
def getExpandedDirName(fileName):
    fileDir  = os.path.dirname(fileName)
    baseName = "%s.contents" % os.path.basename(fileName)

    return os.path.join(fileDir, baseName)

#-----------------------------------------------------------------------------
def isArchive(fileName):
    ext = fileName[-4:]

    if ext in [".zip", ".jar"]: return True
    return False

#-----------------------------------------------------------------------------

