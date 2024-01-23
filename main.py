# My Objects:
import json

from CyclomaticComplexityAnalyzer import CyclomaticComplexityAnalyzer
from Downloader import Downlaoder
# from FolderComparator import FolderComparator     # uncomment if using Folder Comparator
from GitManager import GitManager
from JARExtractor import JARExtractor
from JLCodeAnalyzer import JLCodeAnalyzer
from MavenRepositorySearcher import MavenRepositorySearcher
import argparse
from Setup import Setup
from prettytable import PrettyTable
from Setup import Setup

from MyException import MyException
from XMLReader import XMLReader


# Final report, its fields will be filled during the application execution below, in the start (method)
report = {
        "GAV"                       : "Not Defined",  
        "AVG Cyclomatic Complexity" : "Not Analyzed", 
        "AVG LOCs per method"       : "Not Analyzed",
        "Max Len LOCs method"       : "Not Analyzed",   # Nr. of LOCs in the longest method found in the pkg
        "Precedent version"         : "Not Analyzed",
        "Code Churn"                : "Not Analyzed",
        "GitHub Nr. changed files"  : "Not Analyzed",   # Nr. of changed files according to GH
        "GitHub Nr. commits"        : "Not Analyzed",   # Nr. of commits according to GH between vers. N and N-1
        "Nr. of contributors"       : "Not Analyzed",   # Nuber of contributors for the repo under analysis
        "AVG Contributions/user"    : "Not Analyzed"    # AVG contributions per contributor of a repository, 
                                                        # may be used as an AVG seniority of contributors for the repo
    }

def create_report():
    '''
    This method will create the report (the table to print on the screen) 
    and call export_json() that will create the JSON file with the results in the data/ folder
    '''

    # create the PrettyTable for aestetic terminal output
    x = PrettyTable()
    x.field_names = ["Metric", "Result"]

    for key in report:
        x.add_row([key, report[key]])
        #f"{key}: {report[key]}"
    x.align = "l"
    gav[0] = "ERROR__"+gav[0]

    # export the table in a JSON file and print it in the CL
    export_json(gav)
    print(x)

def export_json(gav):
    '''
    This method will export a JSON file (in the data/ folder) containing the results of the analysis
    '''
    json_report = json.dumps(report)
    jsonFile = open(f"data/{gav[0]}_{gav[1]}_{gav[2]}.json", "w")
    jsonFile.write(json_report)
    jsonFile.close()

def terminate_app(e):
    '''
    This method will terminate the app (after MyException propagation across the software), 
    print an error message, create a report and exit the application
    '''
    print("\n--------- E N D E D   W I T H    E R R O R ---------\n")
    print(f"Error thet raised the Exception:\n {e} \n")
    #report["Exception"] = str(e)
    create_report()
    exit(1)

def separator():
    # print a dashed line, I us it as a separator between outputs
    print("\n" + "-" * 80)


def start(gav=None, slimit=None):
    '''
    Default method for main.py. This executes each setep in the application 
    '''

    # split GroupID, ArtefactID and version from the input in command line (CL)
    if gav != None:
        g = gav[0]
        a = gav[1]
        v = gav[2]

    # check if custom max size limit has been set in CL, else set it to 0.1 MB
    if slimit == None:
        slimit = 1.0

    # start setup: creates folders
    setup = Setup()
    setup.crete_folders()

    # create object able to search Maven repository
    mrs = MavenRepositorySearcher()
    text = f"I am downloading the JAR source file and POM file for GAV: {g} : {a} : {v} from MVN"
    report["GAV"] = f"{g} : {a} : {v}"

    # create the downloader
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
        #print(oDir)
        jlca = JLCodeAnalyzer(oDir)
        avg_locs_per_method = jlca.start(slimit)
        longest_method = jlca.get_max_locs_len()
        #print("Longest_method = ",longest_method)
    except MyException as me:
        terminate_app(me)
   # print(f"On average we have {avg_locs_per_method} locs per method.\n")

    report["AVG LOCs per method"] = avg_locs_per_method
    report["Max Len LOCs method"] = longest_method

    separator()
    print("\nCyclomatic complexity analysis:")
    try:
        cca = CyclomaticComplexityAnalyzer(oDir)
        complexity = cca.start()
    except MyException as me:
        terminate_app(me)
   # print(f"AVG CCN per file = {complexity}. ")
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

    # --------------------------------------------------------------------------
    # ---------- UNCOMMENT ONLY IF YOU ARE USING DIRECTOY COMPARATOR -----------
    # --------------------------------------------------------------------------
    # download the precedent version
    # download the JAR file (version N-1) from MVN repository
    '''try:
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
'''
    '''
    Create Directory Comparator: 
    This is a manual comparator I created.
    Given a GAV vers. N on Maven repo: 
    1. it downloads vers. N and N-1 (downloaded from Maven repository))
    2. it compares files in directory version N and version N-1 
    3. it retrieves the number of changed files between ver. N and N-1
    
    Now you do not need a Github link in the POM file to perform this metric... 
    Just like the linux diff command would do
    '''
    '''
    try:
        # create the comparatore and compare oDir and oDir_precedent (N and  N-1)
        comparator = FolderComparator(oDir, oDir_precedent)
        num_different_files, num_files_examined = comparator.count_different_files()
    except MyException as me:
        terminate_app(me)
    
    #report["Number files examined"]     = num_files_examined
    #report["Number of changed files"]   = num_different_files
    '''
    # --------------------------------------------------------------------------
    # ----------------------------- UNTILL HERE --------------------------------
    # --------------------------------------------------------------------------

    
    urls = []   # init an empty list of (possible) urls to a GH repo
    try:
        # XML Reader: return github urls contained in a POM file (if any)
        xr = XMLReader()
        pom_file_name = "pom_jar/" + pom_file_name
        urls = xr.get_github_url(pom_file_name)
        print ("Analyzing possible GitHub URLs...")

        # start github manager
        try:
            gm = GitManager(urls, v, precedent)
            # DEPRECATED: get data from the GH repository, maybe this is not very human readable, consider implemnting it differently
            #report["Code Churn"], report["GitHub Nr. changed files"], report["GitHub Nr. commits"], report["AVG Contributions/user"], report["Nr. of contributors"] = gm.start()
            
            # if Github Manager successed retrieving information about the repository: put it in the report table
            if gm.start():
                report["Code Churn"]                = gm.get_code_churn()
                report["GitHub Nr. changed files"]  = gm.get_changed_files()
                report["GitHub Nr. commits"]        = gm.get_commits()
                report["AVG Contributions/user"]    = gm.get_avg_contributions()
                report["Nr. of contributors"]       = gm.get_nr_contributors()
        except MyException as me:
            terminate_app(me)
        # --------------------------------------------------------------------------

    except MyException as me:
        terminate_app(me)

    # create a report on screen (and on file) and save a JSON    
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
    
    # start application
    start(gav, slimit)
