import json
import os.path

import requests
from bs4 import BeautifulSoup
from git import Repo

from GitManager import GitManager


def clone_repository(url, dir):
    """
        This method checks if the repo does exist in local and if not
        clones the repository and save it in local
    """
    if os.path.exists(dir):
        print(f"Already exists: {dir}, stopping cloning")
    else:
        print(f"Cloning {url} to {dir}")
        Repo.clone_from(url, dir)
