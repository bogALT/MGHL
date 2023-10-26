import json
import git
import requests

from MyException import MyException


class GitUser:
    def get_commits_users_list_between_versions(self, repo_dir, version1, version2):
        """
            This method will produce the number of commits between two versions
        """
        try:
            repo = git.Repo(repo_dir)
            users = []
            commits = list(repo.iter_commits(f'{version1}..{version2}'))
            for c in commits:
                #print(git.util.get_user_id())
                users.append(c.author)

            return users
        except Exception as e:
            msg = f"I wasn't abe tro retrieve the number of commits between {version1} and {version2}: {e}"
            raise MyException(msg)
            # RAISE EXCEPTION

    #---------------------------------------------------------------------------------------------------------------------ù

    def get_users_and_contributions_of_repo(self, repo_dir):
        '''
            This method will retrieve the list of all contributors of a repository with their "user-information" like contributions, username and so on.
            :param repo_dir: path on github relative to the repository, example: "organization/repository"
            :return: Returns an array containing all users involved in repo_dir repository with their contribution score
        '''
        url = f"https://api.github.com/repos{repo_dir}/contributors?per_page=100"
        
        more_pages = True
        page_number = 1
        logins = []
        try:
            while more_pages := json.loads(requests.get(url + f"&page={page_number}").text):
                logins.extend(more_pages)
                page_number += 1
        except BaseException as be:
            msg = f"Something went wrong while quering github at url: {url} "\
                  f"and the following exception was raised: {be}. "\
                  f"This operation is mandatory, "
            raise MyException(msg)
        
        result_array = [[l['login'], l['contributions']] for l in logins]
        result_array = [l['contributions'] for l in logins]
        
        return result_array
        
        #print(logins)

        '''
        POSSIBLE VALUES IN LOGIN VARIABLE:

        "login":"apanicker-nflx",
        "id":34087882,
        "node_id":"MDQ6VXNlcjM0MDg3ODgy",
        "avatar_url":"https://avatars.githubusercontent.com/u/34087882?v=4",
        "gravatar_id":"",
        "url":"https://api.github.com/users/apanicker-nflx",
        "html_url":"https://github.com/apanicker-nflx",
        "followers_url":"https://api.github.com/users/apanicker-nflx/followers",
        "following_url":"https://api.github.com/users/apanicker-nflx/following{/other_user}",
        "gists_url":"https://api.github.com/users/apanicker-nflx/gists{/gist_id}",
        "starred_url":"https://api.github.com/users/apanicker-nflx/starred{/owner}{/repo}",
        "subscriptions_url":"https://api.github.com/users/apanicker-nflx/subscriptions",
        "organizations_url":"https://api.github.com/users/apanicker-nflx/orgs",
        "repos_url":"https://api.github.com/users/apanicker-nflx/repos",
        "events_url":"https://api.github.com/users/apanicker-nflx/events{/privacy}",
        "received_events_url":"https://api.github.com/users/apanicker-nflx/received_events",
        "type":"User",
        "site_admin":false,
        "contributions":654
        '''

    #---------------------------------------------------------------------------------------------------------------------







    #---------------------------------------------------------------------------------------------------------------------

    def get_contributors_of_repo(self, repo_path):
        
        # this actually returns the web page (html document)
        url = "https://github.com/nextcloud/server/graphs/contributors#contributors"        
        try:           
            while more_results:
                response = requests.get(url).text
                print(response)
        except BaseException as be:
            msg = f"Something went wrong while quering github at url: {url} "\
                  f"and the following exception was raised: {be}. "\
                  f"This operation is mandatory, "
            raise MyException(msg)
        
        # return 0, not using this function now
        return 0 #response