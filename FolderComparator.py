import subprocess
import os

class FolderComparator:
    '''
        This is experimetal! It works actually but was not added to the working application. 
        This object is supposed to retrieve the number of changed files between two versions of a package from Maven repository.
    '''
    def __init__(self, folder1, folder2):
        self.folder1 = folder1
        self.folder2 = folder2

    def count_different_files(self):
        count = 0
        files_examined = 0

        # list recursively all files and directories
        for root, dirs, files in os.walk(self.folder1):
            for file in files:
                files_examined += 1
                file1 = os.path.join(root, file)

                # if file is not a java file: continue to the next one
                if not file1.endswith(".java"):
                    continue

                file2 = os.path.join(self.folder2, os.path.relpath(file1, self.folder1))

                # check if the file exists in the second folder
                if not os.path.exists(file2):
                    count += 1
                else:
                    # execute the diff command
                    cmd = ['diff', file1, file2]
                    diff_output = subprocess.run(cmd, capture_output=True, text=True)

                    # if the command diff returns a value different than 0 then the files are different
                    if diff_output.returncode != 0:
                        count += 1

        return count, files_examined

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