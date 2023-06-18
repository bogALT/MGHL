import subprocess
import os

class FolderComparator:
    def __init__(self, folder1, folder2):
        self.folder1 = folder1
        self.folder2 = folder2

    def count_different_files(self):
        count = 0
        files_examined = 0

        # Attraversa ricorsivamente la prima cartella
        for root, dirs, files in os.walk(self.folder1):
            for file in files:
                files_examined += 1
                file1 = os.path.join(root, file)
                if not file1.endswith(".java"):
                    #print(f"{file1} is not a java file")
                    continue

                #print(f"Examinating {file1}")
                file2 = os.path.join(self.folder2, os.path.relpath(file1, self.folder1))

                # Controlla se il file esiste nella seconda cartella (ma solo se sono file .Java)
                if not os.path.exists(file2):
                    count += 1
                else:
                    # Esegui il comando diff per confrontare i file
                    cmd = ['diff', file1, file2]
                    diff_output = subprocess.run(cmd, capture_output=True, text=True)

                    # Se il comando diff restituisce un codice diverso da 0, i file sono diversi
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