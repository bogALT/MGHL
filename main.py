# My Objects:
import getopt
import json

from CyclomaticComplexityAnalyzer import CyclomaticComplexityAnalyzer
from Downloader import Downlaoder
from FolderComparator import FolderComparator
from GitManager import GitManager
from JARExtractor import JARExtractor
from JLCodeAnalyzer import JLCodeAnalyzer
from MavenRepositorySearcher import MavenRepositorySearcher
import csv
import argparse
from Setup import Setup
from prettytable import PrettyTable
from Setup import Setup

from HTMLCreator import HTMLPage
from MyException import MyException
from XMLReader import XMLReader



report = {
        "GAV"                       : "ND - Not Defined",  # ND = Not Defined
        "AVG Cyclomatic Complexity" : "NA - Not Analyzed", # NA = Not Analyzed
        "AVG LOCs per method"       : "NA - Not Analyzed",
        "Precedent version"         : "NA - Not Analyzed",
        "Code Churn"                : "NA - Not Analyzed",
        "GitHub Nr. changed files"  : "NA - Not Analyzed",
        "GitHub Nr. commits"        : "NA - Not Analyzed"
    }

def create_report():
    x = PrettyTable()
    x.field_names = ["Metric", "Result"]

    for key in report:
        x.add_row([key, report[key]])
        #f"{key}: {report[key]}"
    x.align = "l"
    gav[0] = "ERROR__"+gav[0]
    export_json(gav)
    print(x)

def export_json(gav):
    json_report = json.dumps(report)
    jsonFile = open(f"data/{gav[0]}_{gav[1]}_{gav[2]}.json", "w")
    jsonFile.write(json_report)
    jsonFile.close()

def terminate_app(e):
    print("\n--------- E N D E D   W I T H    E R R O R ---------\n")
    print(f"Error Message thet raised the Exception:\n {e} \n")
    report["Exception"] = str(e)
    create_report()
    exit(1)

def separator():
    print("\n" + "-" * 80)


def start(gav=None, slimit=None):
    if gav != None:
        g = gav[0]
        a = gav[1]
        v = gav[2]

    if slimit == None:
        slimit = 1.0

    setup = Setup()
    setup.crete_folders()
    mrs = MavenRepositorySearcher()

    # download the JAR and POM files of the specific GAV
    text = f"I am downloading the JAR source file {g} : {a} : {v} from MVN"
    text += f"\nI am downloading the POM file for {g} : {a} : {v} from MVN"

    report["GAV"] = f"{g} : {a} : {v}"
    dl = Downlaoder()
    try:
        jar_file = dl.download(g, a, v)
        pom_file_name = dl.download(g, a, v, "pom")
    except MyException as me:
        terminate_app(me)
        
    separator()
    # Extract java files from JAR to oDir
    try:
        je = JARExtractor()
        oDir = je.extract(jar_file)
        print(jar_file)
    except MyException as me:
        terminate_app(me)

    separator()
    # count LOCs per method
    try:
        print(oDir)
        jlca = JLCodeAnalyzer(oDir)
        avg_locs_per_method = jlca.start(slimit)
    except MyException as me:
        terminate_app(me)
    print(f"On average we have {avg_locs_per_method} locs per method\n")

    report["AVG LOCs per method"] = avg_locs_per_method

    separator()
    print("\nCyclomatic complexity analysis:")
    try:
        cca = CyclomaticComplexityAnalyzer(oDir)
        complexity = cca.start()
    except MyException as me:
        terminate_app(me)
    print(f"AVG CCN per file = {complexity}. ")
    report["AVG Cyclomatic Complexity"] = complexity

    separator()
    # search the Maven Repository for version - 1
    print("Searching for version precedent to ", v)
    try:
        precedent = mrs.search_GAV(g, a, v)  # check what to do when incomplete parameters are set
    except MyException as me:
        terminate_app(me)

    report["Precedent version"] = precedent
    print("Found v = ", precedent)

    separator()
    # download the precedent version
    # download the JAR file (version -1) from MVN repository
    # dl = Downlaoder()
    try:
        jar_file = dl.download(g, a, precedent)
    except MyException as me:
        terminate_app(me)

    # Extract java files from JAR to oDir
    # je = JARExtractor()
    try:
        oDir_precedent = je.extract(jar_file)
        text += f"saving in directory: {oDir_precedent}"
    except MyException as me:
        terminate_app(me)

    separator()

    # create Directory comparator
    try:
        comparator = FolderComparator(oDir, oDir_precedent)
        num_different_files, num_files_examined = comparator.count_different_files()
    except MyException as me:
        terminate_app(me)

    #report["Number files examined"]     = num_files_examined
    #report["Number of changed files"]   = num_different_files

    # XML Reader -> return github url contained in the POM file
    urls = []
    try:
        xr = XMLReader()
        pom_file_name = "pom_jar/" + pom_file_name
        urls = xr.get_github_url(pom_file_name)
        print ("Analyzing possible GitHub URLs...")

        # start net github manager -------------------------------------------------
        try:
            gm = GitManager(urls, v, precedent)
            report["Code Churn"], report["GitHub Nr. changed files"], report["GitHub Nr. commits"] = gm.start()
        except MyException as me:
            terminate_app(me)
        # --------------------------------------------------------------------------

    except MyException as me:
        terminate_app(me)
        
    # if urls has links, start github research and analysis
    

    create_report()
    export_json(gav)
    

if __name__ == '__main__':
    # get GAV trom CL
    try:
        parser = argparse.ArgumentParser(description="MVN repo anlayzer",
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("-gav", help="insert group artefact and version")
        parser.add_argument("-slimit", help="files bigger than this will not be examined")
        args = parser.parse_args()
        slimit = args.slimit
        gav = (args.gav).split(":")
    except BaseException as be:
        print("Correct Usage: usage: main.py [-h] [-gav GAV] [-slimit SLIMIT]")
        exit(1)
    print("Starting the program for GAV = ", args.gav)
    print("Slimit the program for GAV = ", args.slimit)
    
    start(gav, slimit)
