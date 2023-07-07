# My Objects:
import getopt

from CyclomaticComplexityAnalyzer import CyclomaticComplexityAnalyzer
from Downloader import Downlaoder
from FolderComparator import FolderComparator
from JARExtractor import JARExtractor
from JLCodeAnalyzer import JLCodeAnalyzer
from MavenRepositorySearcher import MavenRepositorySearcher
from GitManager import GitManager
import csv
import argparse

from HTMLCreator import HTMLPage
from XMLReader import XMLReader


def separator(type=None):
    if type == None:
        print("\n"+"-"*80)
    elif type == "results":
        print("-" * 80)
        print("-" * 80)

def read_csv():
    file_names = []
    with open('gav_input.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            g = row[0]
            a = row[1]
            file_names.append([g, a])
    return file_names

def start(gav=None, slimit=None):
    if gav != None:
        g = gav[0]
        a = gav[1]
        v = gav[2]

    if slimit == None:
        slimit = 1.0

    outputs = []
    outputs.append(f"RESULTS for {g}:{a}:{v} with Limit File Size = {slimit}:\n")
    mrs = MavenRepositorySearcher()

    # create an empty HTML page (outputs go here)
    page = HTMLPage()
    page.create_empty_page(g + " : " + a + " : " + v)
    page.add_css()

    # download the JAR and POM files of the specific GAV
    title = "Downloading JAR"
    text = f"I am downloading the JAR source file {g} : {a} : {v} from MVN"
    text += f"\nI am downloading the POM file for {g} : {a} : {v} from MVN"
    page.add_content(title, text)
    dl = Downlaoder()
    jar_file = dl.download(g, a, v)
    pom_file_name = dl.download(g, a, v, "pom")


    separator()
    # Extract java files from JAR to oDir
    je = JARExtractor()
    #jar_file = "packages/"+jar_file
    oDir = je.extract(jar_file)
    title = "Extracting java files from JAR source"
    text = f"Files extracted in {oDir}"
    page.add_content(title, text)

    separator()
    # count LOCs per method
    jlca = JLCodeAnalyzer(oDir)
    avg_locs_per_method = jlca.start(slimit)
    print(f"On average we have {avg_locs_per_method} locs per method\n")
    title = "LOCS per method"
    text = f"On average we have {avg_locs_per_method} locs per method"
    page.add_content(title, text)
    outputs.append(text)

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
    outputs.append(text)

    separator()

    # search the Maven Repository for version - 1
    print("Searching for version precedent to ", v)
    precedent = mrs.search_GAV(g, a, v)  # check what to do when incomplete parameters are set
    print(f"Version {v} has predecessor {precedent}")
    title = "Searching for v-1"
    text = f"Version {v} has predecessor {precedent}"
    page.add_content(title, text)
    outputs.append(text)

    separator()
    # download the precedent version
    # download the JAR file (version -1) from MVN repository
    # dl = Downlaoder()
    jar_file = dl.download(g, a, precedent)
    title = "Downloading JAR v-1"
    text = f"Downloading the JAR for the version {precedent}. " + "\n"

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
    text = f"Changed files: {num_different_files}" + "\n" + \
           f"Examined files: {num_files_examined}"
    page.add_content(title, text)
    outputs.append(text)

    #print(f"Changed files: {num_different_files}")
    #print(f"Examined files: {num_files_examined}")

    # XML Reader -> return github url contained in the POM file
    xr = XMLReader()
    pom_file_name = "pom_jar/" + pom_file_name
    urls = xr.get_github_url(pom_file_name)
    if len(urls) > 0:
        print("Possible urls = ", urls)

        # create github manager object
        separator()
        print("Creating GitManager")
        gm = GitManager()
        # print("Current dir = ", os.getcwd())

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
            code_churn = gm.get_code_churn(repo_dir)
            print(f"Code chunk = {code_churn}")
            title = "Code chunk"
            text = f"Code chunk = {code_churn}"
            page.add_content(title, text)
            outputs.append(text)
            versions = gm.get_prev_version(repo_name, v)
            print(versions)
            if versions != -1:  # I have found the version on gh
                v1 = precedent  # older
                v2 = v  # newer

                print(f"Comparing versions: v2 = {v2} and v1 = {v1}")
                changed_files = gm.get_changed_files(repo_name, v1, v2)
                commits = gm.get_total_commits(repo_name, v1, v2)
                print(f"     Changed files between {v2} and {v1} = {changed_files}")
                print(f"     Commits between {v2} and {v1} = {commits}")
            else:
                text = f"{g}:{a}:{v} has no valid version on github. GitHub parameter: diff commits will not be examinated."
                print(text)
                title = "GitHub"
                page.add_content(title, text)
                outputs.append(text)
        else:
            text = f"{g}:{a}:{v} has no valid links to github. GitHub parameters such as ode churn and diff commits will not be examinated."
            print(text)
            title = "GitHub"
            page.add_content(title, text)
            outputs.append(text)
    else:
        text = f"{g}:{a}:{v} has no links to github. GitHub parameters such as code churn and diff commits will not be examinated."
        print(text)
        title = "GitHub"
        page.add_content(title, text)
        outputs.append(text)

    # save to file
    page.save_to_file(f"{g}_{a}_{v}.html")
    print("\n")
    separator("results")
    for output in outputs:
        print(output)
    separator("results")

if __name__ == '__main__':
    # get GAV trom CL
    parser = argparse.ArgumentParser(description="description app",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-gav", help="insert group artefact and version")
    parser.add_argument("-slimit", help="files bigger than this will not be examined")
    args = parser.parse_args()
    slimit = args.slimit
    gav = (args.gav).split(":")
    print("Starting the program for GAV = ", args.gav)
    print("Slimit the program for GAV = ", args.slimit)
    start(gav, slimit)
