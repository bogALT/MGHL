# My Objects:
import getopt
import json

from CyclomaticComplexityAnalyzer import CyclomaticComplexityAnalyzer
from Downloader import Downlaoder
from FolderComparator import FolderComparator
from JARExtractor import JARExtractor
from JLCodeAnalyzer import JLCodeAnalyzer
from MavenRepositorySearcher import MavenRepositorySearcher
from GitManager import GitManager
import csv
import argparse
from Setup import Setup
from prettytable import PrettyTable
from Setup import Setup

from HTMLCreator import HTMLPage
from MyException import MyException
from XMLReader import XMLReader



report = {
        "GAV"                       : "ND - Not Defined", # ND = Not Defined
        "AVG Cyclomatic Complexity" : "NA - Not Analyzed", # NA = Not Analyzed
        "AVG LOCs per method"       : "NA - Not Analyzed",
        "Precedent version"         : "NA - Not Analyzed",
        "Number of changed files"   : "NA - Not Analyzed",
        "Number files examined"     : "NA - Not Analyzed",
        "GitHub repository"         : "NA - Not Analyzed",
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
    print(x)

def export_json(gav):
    json_report = json.dumps(report)
    jsonFile = open(f"json_reports/{gav[0]}_{gav[1]}_{gav[2]}.json", "w")
    jsonFile.write(json_report)
    jsonFile.close()

def terminate_app(e):
    print("\n--------- E N D   W I T H   E R R O R ---------\n")
    print_report()
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
    print("\nStarting Cyclomatic complexity analysis")
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

    report["Number files examined"]     = num_files_examined
    report["Number of changed files"]   = num_different_files

    # XML Reader -> return github url contained in the POM file
    try:
        xr = XMLReader()
        pom_file_name = "pom_jar/" + pom_file_name
    except MyException as me:
        terminate_app(me)
    urls = xr.get_github_url(pom_file_name)
    if len(urls) > 0:
        # create github manager object
        separator()
        print("Creating GitManager")
        gm = GitManager()

        # the POM file may contain more github urls, some may be documentation, some repositories and some other things
        # but i am looking only for repositories
        repo_dir = "gh_repos/"
        repo_name = ""
        valid_gh_url = False    # even if a gh url is present it may not be consistent (pointing to an empty page, old versions, and so on)
        for url in urls:
            if url.endswith('/'):
                url = url[:-1]
            if gm.is_valid_github_url(url):
                print("Cloning ", url)
                repo_dir = gm.clone_repository(url)
                repo_name = url.replace("http://github.com/", "")
                repo_name = repo_name.replace("https://github.com/", "")
                valid_gh_url = True     # cloning went fine so the gh url is OK
                continue  # first valid occurrence is enough
            else:
                print("This is not a valid url = ", url)

        # if I found a valid gh url and I managed to clone it: exe can continue
        if valid_gh_url:
            separator()
            # get code chunk
            try:
                code_churn = gm.get_code_churn(repo_dir)
            except MyException as me:
                terminate_app(me)
            print(f"Code churn (from the first version) = {code_churn}")

            report["Code Churn"] = code_churn
            try:
                versions = gm.get_prev_version(repo_name, v)
            except MyException as me:
                terminate_app(me)

            if versions != -1:  # I have found the version on gh
                v1 = precedent  # older
                v2 = v  # newer
                try:
                    changed_files = gm.get_changed_files(repo_name, v1, v2)
                    commits = gm.get_total_commits(repo_name, v1, v2)
                except MyException as me:
                    terminate_app(me)

                report["GitHub Nr. changed files"]  = changed_files
                report["GitHub Nr. commits"]        = commits
            else:
                text = f"No links to GitHub. GitHub parameters will not be examinated."
                report["GitHub repository"] = text
        else:
            text = f"No links to GitHub. GitHub parameters will not be examinated."
            report["GitHub repository"] = text

    else:
        text = f"No links to GitHub. GitHub parameters will not be examinated."
        report["GitHub repository"] = text

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
