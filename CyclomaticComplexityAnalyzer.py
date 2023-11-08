import  lizard
import os

from MyException import MyException

class CyclomaticComplexityAnalyzer:
    '''
    This utility will calculate recursively Cyclomatic Complexity for every file in the directory oDir
    '''

    def __init__(self, oDir):
        self.code_directory = oDir

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
        if not jfs:
            msg = "I have not found any java file to work on."
            raise MyException(msg)
            return 0
        avg_ccn_for_file = 0
        for jf in jfs:
            analyzed_files = lizard.analyze_file(jf)
            avg_ccn_for_file += round(analyzed_files.CCN, 2)
            
        try:
            avg_ccn = round(avg_ccn_for_file / len(jfs),2)
            self.result = avg_ccn
        except Exception as e:
            raise MyException(e)
        return avg_ccn