    if len(urls) > 0:
        # create github manager object
        separator()
        print("Creating GitManager")
        gm = GitManager()

        # the POM file may contain more github urls, some may be documentation, some repositories and some other things
        # but i am looking only for repositories
        repo_dir = "gh_repos/"
        repo_name = ""
        valid_gh_url = False    # even if a gh url is present it may not be consistent (i.e. pointing to an empty page, old versions, and so on)
        for url in urls:
            if url.endswith('/'):
                url = url[:-1]
            if gm.is_valid_github_url(url):
                print("Cloning ", url)
                repo_dir = gm.clone_repository(url)
                repo_name = url.replace("http://github.com/", "")
                repo_name = repo_name.replace("https://github.com/", "")
                valid_gh_url = True     # cloning went fine so the gh url is OK
                continue  # first valid occurrence is enough BUT what if there are more repos? why?
            else:
                print("This is not a valid url = ", url)

        # if I found a valid gh url and I managed to clone it: exe can continue
        if valid_gh_url:
            separator()
            # get code chunk
            try:
                code_churn = gm.get_code_churn(repo_dir)
            except MyException as me:
                terminate_app(me)
            print(f"Code churn (from the first version) = {code_churn}")

            report["Code Churn"] = code_churn
            try:
                versions = gm.get_prev_version(repo_name, v)
            except MyException as me:
                terminate_app(me)

            if versions != -1:  # I have found the version on gh
                v1 = precedent  # older
                v2 = v  # newer
                try:
                    changed_files = gm.get_changed_files(repo_name, v1, v2)
                    commits = gm.get_total_commits(repo_name, v1, v2)
                except MyException as me:
                    terminate_app(me)

                report["GitHub Nr. changed files"]  = changed_files
                report["GitHub Nr. commits"]        = commits
            else:
                text = f"No links to GitHub. GitHub parameters will not be examinated."
                report["GitHub repository"] = text
        else:
            text = f"No links to GitHub. GitHub parameters will not be examinated."
            report["GitHub repository"] = text

    else:
        text = f"No links to GitHub. GitHub parameters will not be examinated."
        report["GitHub repository"] = text