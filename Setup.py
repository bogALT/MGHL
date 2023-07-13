import os
from MyException import MyException


class Setup:
    '''
        This class will initialize some basic data like directories and data structures
    '''
    def crete_folders(self):
        # create folders
        dirs = ["gh_repos", "HTML_Reports", "packages", "pom_jar", "json_reports"]
        for dir in dirs:
            if not os.path.exists(dir):
                try:
                    os.makedirs(dir)
                    print("Creating directory: ", dir)
                except Exception as e:
                    raise MyException(e)
    