import  lizard
import os

class CyclomaticComplexityAnalyzer:
    '''
    This utility will calculate recursively Cyclomatic Complexity for every file in the directory oDir
    '''

    def __init__(self, oDir):
        self.code_directory = oDir
        print("Init cyclomatic complexity analyzer")

    def get_java_files(self):
        '''
        :param directory: path to the main directory of java files
        :return: list of java files found
        search for all .java files recursively in "directory"
        '''

        java_files = []
        for root, _, files in os.walk(self.code_directory):
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root, file))
        return java_files

    def start(self):
        jfs = self.get_java_files()
        avg_ccn_for_file = 0
        for jf in jfs:
            analyzed_files = lizard.analyze_file(jf)
            avg_ccn_for_file += round(analyzed_files.CCN, 2)
            #print(f"Whole file: {os.path.basename(jf)} has CCN = {analyzed_files.CCN}, and his methods:")

        avg_ccn = round(avg_ccn_for_file / len(jfs),2)
        return avg_ccn