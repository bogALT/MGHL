# My Objects:
import getopt

from CyclomaticComplexityAnalyzer import CyclomaticComplexityAnalyzer
from Downloader import Downlaoder
from FolderComparator import FolderComparator
from JARExtractor import JARExtractor
from JLCodeAnalyzer import JLCodeAnalyzer
from MavenRepositorySearcher import MavenRepositorySearcher
import csv
import argparse

from HTMLCreator import HTMLPage


def separator():
    print("\n"+"-"*80)

def read_csv():
    file_names = []
    with open('gav_input.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            g = row[0]
            a = row[1]
            file_names.append([g, a])
    return file_names

def start(gav=None):
    if gav != None:
        g = gav[0]
        a = gav[1]
        v = gav[2]
    else:
        # define GAV - only for testing, later input from terminale
        g = "com.github.jnr"
        a = "jnr-posix"
        v = "3.1.0"

    mrs = MavenRepositorySearcher()

    '''# ----------------------------------------------------------------
    #               AUTOMATIZING THE ANALYSIS
    # only when you have no specific versions to look for
    #
    print("Searching for last version of ", g)
    last = mrs.search_last_version(g, a)
    print("Last version = ", last)
    v = last
    # ----------------------------------------------------------------'''

    # create an empty HTML page (outputs go here)
    page = HTMLPage()
    page.create_empty_page(g + " : " + a + " : " + v)
    page.add_css()

    # download the JAR file from MVN repository
    title = "Downloading JAR"
    text = f"I am downloading the JAR source file {g} : {a} : {v} from MVN"
    page.add_content(title, text)
    dl = Downlaoder()
    jar_file = dl.download(g, a, v)

    separator()
    # Extract java files from JAR to oDir
    je = JARExtractor()
    oDir = je.extract(jar_file)
    title = "Extracting java files from JAR source"
    text = f"Files extracted in {oDir}"
    page.add_content(title, text)

    separator()
    # count LOCs per method
    jlca = JLCodeAnalyzer(oDir)
    avg_locs_per_method = jlca.start()
    print(f"On average we have {avg_locs_per_method} locs per method\n")
    title = "LOCS per method"
    text = f"On average we have {avg_locs_per_method} locs per method"
    page.add_content(title, text)

    separator()
    print("\nStarting Cyclomatic complexity analysis")
    cca = CyclomaticComplexityAnalyzer(oDir)
    complexity = cca.start()
    print(f"AVG CCN per file = {complexity}. "
          f"For more detailed output uncomment code in CyclomaticComplexityAnalyzer.py::start()")
    title = "Cyclomatic complexity"
    text = f"AVG CCN per file = {complexity}. " \
           f"For more detailed output uncomment code in CyclomaticComplexityAnalyzer.py::start()"
    page.add_content(title, text)

    separator()

    # search the Maven Repository for version - 1
    print("Searching for version precedent to ", v)
    precedent = mrs.search_GAV(g, a, v)  # check what to do when incomplete parameters are set
    print(f"Version {v} has predecessor {precedent}")
    title = "Searching for v-1"
    text = f"Version {v} has predecessor {precedent}"
    page.add_content(title, text)

    separator()
    # download the precedent version
    # download the JAR file (version -1) from MVN repository
    # dl = Downlaoder()
    jar_file = dl.download(g, a, precedent)
    title = "Downloading JAR v-1"
    text = f"VDownloading the JAR for the version {precedent}. " + "<br>"

    # Extract java files from JAR to oDir
    # je = JARExtractor()
    oDir_precedent = je.extract(jar_file)
    text += f"saving in directory: {oDir_precedent}"
    page.add_content(title, text)

    separator()

    print(f"Comparing {oDir_precedent} and {oDir}:")

    # create Directory comparator
    comparator = FolderComparator(oDir, oDir_precedent)
    num_different_files, num_files_examined = comparator.count_different_files()
    title = f"Comparing {oDir_precedent} and {oDir}:"
    text = f"Changed files: {num_different_files}" + "<br>" + \
           f"Examined files: {num_files_examined}"
    page.add_content(title, text)
    print(f"Changed files: {num_different_files}")
    print(f"Examined files: {num_files_examined}")

    # save to file
    page.save_to_file(f"{g}_{a}_{v}.html")


if __name__ == '__main__':

    print("Starting the program..")
    '''gavs = []
    gavs = read_csv()    # automatize searching gavs -> fill an array with GAVs
    for gav in gavs:
        start(gav)
        '''

    # get GAV trom CL
    parser = argparse.ArgumentParser(description="description app",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-gav", help="insert group artefact and version")
    args = parser.parse_args()
    gav = (args.gav).split(":")

    start(gav)
