import os
import re
import subprocess
from MyException import MyException

import git
from github import Github
from github import Auth
import requests
from git import Repo
import shlex

from Login import Login

# for retrieving files changed
from urllib.request import urlopen

class GitManager:
    def __init__(self):
        self.github_api_url = "https://api.github.com"
        l = Login()
        self.api_username = "BogAlt"
        self.access_token = "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"

    def query_github(self, repo_path):
        try:
            gh_session = requests.Session()
            headers = {'Authorization': "Token " + self.access_token}
            url = self.github_api_url + repo_path
            response = requests.get(url, headers=headers, auth=(self.api_username, self.access_token))
        except BaseException as be:
            msg = f"Something went wrong while quering github at url: {url} "\
                  f"and the following exception was raised: {be}. "\
                  f"This operation is mandatory, "
            raise MyException(msg)
        return response

    def get_locs_from_repo(self, repo_path):
        #print("\n-------------------------------------------------")
        #print("Retrieving LOCs of code per language of : ", repo_path)
        response = self.query_github(repo_path + "/languages")
        locs_per_lang = response.json()
        return locs_per_lang

    '''def get_contributors_of_repo(self, repo_path):
        #print("List of contributors for ", repo_path)
        repo_path = repo_path + "/contributors"
        #print("Queueing for contributors at: ", repo_path)
        response = self.query_github(repo_path)
        contributors = response.json()
        return contributors

    def get_all_repos_contrributed_by(self, user):
        user_path = "/users/" + user + "/repos"

        # get all repos of the user
        #print("\n-------------------------------------------------")
        #print(f"{user} is also working in the following repo:")
        url = self.github_api_url + user_path
        #print("quering for contribution of ", url)
        response = self.query_github(user_path)
        repos_contributed = response.json()
        return repos_contributed
'''
    def get_user_contributions(self, user):
        # get contributions of user
        #print(f"Let's get contribution of: {user}")
        url = "https://github-contributions-api.deno.dev/" + user + ".json"
        try:
            headers = {'Authorization': "Token " + self.access_token}
            response = requests.get(url, headers=headers, auth=(self.api_username, self.access_token))
            contributions = response.json()
        except Exception as e:
            raise MyException(e)
        return contributions

    

    def clone_repository(self, url):
        """
            This method checks if the repo does exist in local and if not
            clones the repository and save it in local
        """
        path = url.replace("http://github.com", "")
        path = path.replace("https://github.com", "")
        print("path = ", path)
        dir = os.getcwd() + "/gh_repos" + path
        print("Cloning in directory =", dir)
        if os.path.exists(dir):
            print(f"The repository {url} already exists in directory: {dir}. Not going to clone.")
        else:
            print(f"Cloning {url} to {dir}")
            try:
                Repo.clone_from(url, dir)
            except git.exc.InvalidGitRepositoryError as ghe:
                msg = f"Something went wrong while cloning repository {url} and the following exception was raised: {ghe}. "
                #self.exceptions.append(msg)
                raise MyException(msg)
            except BaseException as be:
                msg = f"Something went wrong while cloning repository {url} and the following exception was raised: {be}. "
                #self.exceptions.append(msg)
                raise MyException(msg)
        return dir

    def get_code_churn(self, dir):
        '''
        This function execute the command provided in git-churn.sh in order to compute the code chunk. 
        It needed futher code to be executed due to some limitation on some machines: analyze of too many files is denied. 
        This is why I manually incremented merge.renameLimit to 999999
        :param dir: directory that contains the code to analyze
        :return: sum of chunks of all files
        '''

        command = "git config merge.renameLimit 999999 && set -e && git log --all -M -C --name-only --format='format:' \"$@\" | sort | grep -v '^$' | uniq -c | sort -n"
        task = subprocess.Popen(command,
                                shell=True,
                                cwd=dir,
                                stdout=subprocess.PIPE)
        command_output = task.stdout.read()
        lines = command_output.splitlines()
        #lines       # WHAT THE HELL IS THIS ??  # WHAT THE HELL IS THIS ??  # WHAT THE HELL IS THIS ??  # WHAT THE HELL IS THIS ??  # WHAT THE HELL IS THIS ??
        count = 0
        sum = 0
        for l in lines:
            l = l.decode('UTF-8')
            l = re.findall(r'\b\d+\b', l)
            count += 1
            sum += int(l[0])
            #print(f"[{count}] = {l}, Sum = {sum}")
        #print(dir)
        return sum

    def get_versions_of_repo(self, repo_path):
        '''
        This function retrieve all versions (releases) of a repository
        :param repo_name: the name of a repository
        :return: list of all versions available on GitHub
        '''

        print("Quering forversions of: ", repo_path)
        # Access token or username and password can be used to access a private repository
        auth = Auth.Token(self.access_token)
        g = Github(auth = auth)
        relases = []
        versions = []

        # Fetch the repository object using the extracted name
        try:
            repo = g.get_repo("PyGithub/PyGithub")
            releases = repo.get_releases()
            #populate an array
            for release in releases:
                print(f"Adding Release: {release.tag_name} to the versions array")
                versions.append(release.tag_name)
            versions.sort()
        
        except BaseException as be:
            msg = f"Something went wrong when retrieving repository {repo_path} in order to obtain all "\
                  f"repository versions and the following exception was raised: {be}. "\
                  f"This values are mandatory, "

            raise MyException(msg)
        print("GH-----", versions)
        return versions

    def get_prev_version(self, repo_path, v):
        '''
        This function takes in input a version and returns its precedent version.
        :param v: version
        :return: precedent version
        '''

        print("Looking for precedent of version = ",v)
        precedent_version = -1
        versions = self.get_versions_of_repo(repo_path)
        if len(versions) > 0:
            try:
                current_version_index = versions.index(v)
                print(f"{v} is at {current_version_index}pos and v-1 is {versions[current_version_index+1]}")
                precedent_version = {versions[current_version_index+1]} # GH ordering is from biggest to smallest number of version
            except BaseException as be:
                msg = (f"I wasn't able to find version {v} in the list of versions retrieved from git repo "
                      f"for repository {repo_path}. This may happen because github does not contain all versions that are contained on maven repo."
                      f"The following exception was raised: {be}. "
                      f"Skipping this step")
                self.exceptions.append(msg)
                raise MyException(msg)

        return precedent_version


    def get_changed_files(self, repo_path, v1, v2):
        '''
        This functions retrieves the total number of files changed between v1 and v2 requesting the diff file
        and counting occurrences of "diff --git". Note that using APIs has limit of 300 files so larger changes
        won't be correct.
        :param repo_path: part of the repo in form: owner/repo
        :param v1: first version to be compared
        :param v2: second version to be compared
        :return: number of files changed
        '''
        print(f"Getting number of changed files for repository {repo_path} and v1 = {v1}, v2 = {v2}")
        repo_info = repo_path.split("/")
        headers = {'Authorization': "Token " + self.access_token}
        url = f"https://github.com/{repo_info[0]}/{repo_info[1]}/compare/{v1}...{v2}.diff"
        print("Comparing url = ", url)
        try:
            response = requests.get(url, headers=headers, auth=(self.api_username, self.access_token))
        except BaseException as be:
            msg = f"Something went wrong when retrieving number of changed files between {v1} and {v2} "\
                  f"for repository {repo_path} and the following exception was raised: {be}. "\
                  f"This value is mandatory, "
            self.exceptions.append(msg)
            raise MyException(msg)

        diff = response.content
        count = diff.count(b"diff --git")   # count() uses byte, so "b" is needed
        #print("Count via diff file = ", count)
        return count

    def get_total_commits(self, repo_path, v1, v2):
        '''
        This function counts total commits between version 1 and version 2 of a repository
        :param repo_path: path of the repository (to be split into owner and name of the repo)
        :param v1: first version to be compared
        :param v2: second version to be compared
        :return: number of commits
        '''
        print(f"Getting number of commits for repository {repo_path} and v1 = {v1}, v2 = {v2}")
        repo_info = repo_path.split("/")    #repo_info[0] = user, repo_info[1] = repo name
        # calculating the number of files changed between v1 and v2
        try:
            g = Github(self.access_token)
            repo = g.get_user(repo_info[0]).get_repo(repo_info[1])
            comp = repo.compare(v1, v2)
        except BaseException as be:
            msg = f"Something went wrong when retrieving total commits between {v1} and {v2} "\
                  f"for repository {repo_path} and the following exception was raised: {be}. "\
                  f"This value is mandatory, "
            self.exceptions.append(msg)
            raise MyException(msg)

        return comp.total_commits
