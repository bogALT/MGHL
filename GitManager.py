from GitRepo import GitRepo
from GitUser import GitUser
from MyException import MyException


class GitManager:
    def __init__(self, urls, current_v, precedent_v):
        self.github_api_url = "https://api.github.com"
        #l = Login() # REMOVE IF NOT USED 
        self.api_username   = "BogAlt"
        self.access_token   = "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"
        self.urls           = urls
        self.current_v      = current_v
        self.precedent_v    = precedent_v
        self.code_churn     = -1
        self.changed_files  = -1
        self.commits        = -1
        #print(f"GH manager created -------------------\nAdding {urls} to the GM object\n")

    def start(self):
        print(f"---- Starting GH manager operations")

        # create git repo handler and clone the repo
        gr = GitRepo()
        try:
            repo_url = gr.find_repo_url(self.urls)
            if repo_url == []:
                msg = f"I did not find any valid Github url in the POM file!"
                raise MyException(msg)
        except MyException as me:
            raise MyException(me)
        try:
            print(f"Trying to clone repo with url = {repo_url}")
            repo_dir = gr.clone_repository(repo_url)
        except MyException as me:
            msg = f"Error when cloning directory: {me}"
            raise MyException(msg)
        
        # updating the versions with the format from GH (ig: 1.2.3 -> v.1.2.3)
        self.current_v      = gr.get_versions(self.current_v)      # self.current_v is different than version1 in format (GH TAG)
        self.precedent_v    = gr.get_versions(self.precedent_v)    # maybe i should reassign it to self.current_v

        # if versions exists on github compare them
        if (self.precedent_v != -1) and (self.current_v != -1):
            print(f"Comparing: Current version = {self.current_v} and Precedent version {self.precedent_v}")
            try:
                num_commits, changed_files = gr.get_commits_and_changed_files_between_versions(repo_dir, self.current_v, self.precedent_v)
                self.commits = num_commits
                self.changed_files = changed_files
                print(f"---- Num commits between {self.current_v} and {self.precedent_v} = ", num_commits)
            except MyException as me:
                raise MyException(me)
        else:
            msg = f"Version(s) {self.current_v} and/or {self.precedent_v} are not listed in the repository's versions list!"
            msg = "I wasn't able to find any version of the project on GitHub! Sometimes you encounter empty repos (0 releses and 0 packages) and there are no info to fetch!"
            raise MyException(msg)

        # try to compute code churn
        try:
            code_churn = gr.get_code_churn(self.current_v, self.precedent_v)
            if code_churn != -1:
                self.code_churn = code_churn
        except MyException as me:
            raise MyException(me)

        # experimental: retrieve more information about a repo or user
        #gu = GitUser() 
        #res = gu.get_users_and_contributions_of_repo(gr.repo_path)
       
        return self.code_churn, self.changed_files, self.commits
        