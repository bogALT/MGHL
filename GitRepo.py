import os
import pathlib
import re
import shutil
import subprocess
import git

from MyException import MyException


class GitRepo:
    def __init__(self):
        print(f"\nGit Repo manager created --------------\n")
        self.versions = []
        self.dir = ""
        self.repo_path = ""
        self.changed_files = -1
        self.commits = -1

    #---------------------------------------------------------------------------------------------------------------------

    def find_repo_url(self, urls):
        '''
            This function takes in input a list of urls and returns the first one that is actually linking to a repository on GH
        '''
        for url in urls:
            #print("Examinating = ", url)
            url = url[:-1] if url.endswith('/') else url                # get rid of the ending "/"
            if self.is_valid_github_url(url):
                print(f"{url} looks to be a valid gh repo url. Returning!")
                return url
            else:
                #print(f"{url} is not a valid repo url")
                continue

        #print(f"I wasnt ble to retrieve a valig gh repo url from {urls}.")
        return []           # return the first valid url
                            # if no valid url found -> return empty array

    #---------------------------------------------------------------------------------------------------------------------

    def is_valid_github_url(self, url):
        """
            Checks if a URL is a valid GitHub repository URL. Returns True if the URL is valid, False otherwise.
        """
        # Regular expression for a GitHub repository URL
        github_regex = r'^https?://github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)$'
        return bool(re.match(github_regex, url))

    #---------------------------------------------------------------------------------------------------------------------
    
    def clone_repository(self, url):
        """
            This method checks if the repo does exist in local and if not clones the repository and save it in local
        """
        
        try:
            # remove the unvonted part of url to obtain only the repo path
            path = url.replace("http://github.com", "").replace("https://github.com", "")
            dir = os.getcwd() + "/gh_repos" + path
            self.repo_path = path   # save the repository name like ORAGANIZATION/REPOSITORY so I can use it in GIT User
            self.dir = dir
        
        except Exception as e:
            raise MyException(e)

        if os.path.exists(dir):    
            return dir
        else:
            print(f"Cloning {url} to {dir}")
            try:
                repo = git.Repo.clone_from(url, dir)       # clone repo function
            except git.exc.InvalidGitRepositoryError as ghe:
                msg = f"Something went wrong while cloning repository {url} and the following exception was raised: {ghe}. "
                #self.exceptions.append(msg)
                raise MyException(msg)
            except BaseException as be:
                try:
                    shutil.rmtree(dir)
                    print("Directory removed successfully = ",dir)
                except Exception as o:
                    print(f"Error, {o.strerror}: {path}")

                msg = f"Something went wrong while cloning repository {url} and the following exception was raised: {be}. "
                raise MyException(msg)
        return dir
    
    #---------------------------------------------------------------------------------------------------------------------

    def get_commits_and_changed_files_between_versions(self, repo_dir, current, precedent):
        """
            This method will produce the number of commits between two versions
        """
        try:
            repo = git.Repo(repo_dir)
            commits = list(repo.iter_commits(f'{precedent}..{current}'))
            files_list = []
            # get files for every commit
            for c in commits:
                files_list.extend(list(set(c.stats.files.keys())))
            
            # remove duplicates
            files_list = set(files_list)
            #for f in files_list:
                #print(f)
            #self.changed_files = sum(len(c.stats.files) for c in commits)
            self.changed_files = len(files_list)
            self.commits = len(commits)
            #print(" comits - ", len(commits))
            return self.commits, self.changed_files
        except Exception as e:
            msg = f"I wasn't abe tro retrieve the number of commits between {current} and {precedent}: {e}"
            # RAISE EXCEPTION
            raise MyException(msg)
        return -1

    #---------------------------------------------------------------------------------------------------------------------

    def get_versions(self, version):
        """
        This method will retrieve all available version of a repository and look if can find the desired version
        """
        repo = git.Repo(self.dir)       # clone repo function

        tags = repo.tags                # get all tags (that correspond to versions aproximately)
        
        for t in tags:
            if t.name.find(version) != -1:
                return t.name           # stopping after first match!  CONSIDER FURTHER ANALYSIS
        return -1   # not found
    
    #---------------------------------------------------------------------------------------------------------------------

    def get_code_churn(self, current, precedent):
        '''
        This function execute the command provided in git-chunk in order to compute the code chunk and the number of changed files.
        It uses a different command from the propposed git-churn so it can address specific versions to be compared
        :param version1: first version 
        :param version2: second version
        :return: sum of chunks of all files
        '''

        # code churn for entire history
        #command_old = "git config merge.renameLimit 999999 && set -e && git log --all -M -C --name-only --format='format:' \"$@\" | sort | grep -v '^$' | uniq -c | sort -n"
        
        # code churn between two releases
        print("in code churn fx")
        try:
            command = f"git config merge.renameLimit 999999 && set -e && git log {current}...{precedent} -M -C --name-only --format='format:' | sort | grep -v '^$' | uniq -c | sort -n"
            task = subprocess.Popen(command, shell=True, cwd=self.dir, stdout=subprocess.PIPE)
            code_churn_sum = 0
            for l in task.stdout.read().splitlines():
                l = re.findall(r'\b\d+\b', l.decode('UTF-8'))
                code_churn_sum += int(l[0])
            return code_churn_sum
        except Exception as e:
            msg = f"Error executing git churn command: {e}"
            print(msg)
            raise MyException(msg)
        return -1
    

    #---------------------------------------------------------------------------------------------------------------------
    # alternative approach: to be adapted to this project

    """def get_changed_files(self, repo_path, v1, v2):
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
        return count"""