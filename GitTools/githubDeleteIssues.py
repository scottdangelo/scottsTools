#! /usr/bin/env python

import os
from github import Github

REPO = os.environ.get('REPO')
WORKSHOP = os.environ.get('WORKSHOP')
GH_TOKEN = os.environ.get('TOKEN')

g = Github(base_url="https://github.ibm.com/api/v3", login_or_token=GH_TOKEN)
repo = g.get_repo(REPO)
print(repo.name)

open_issues = repo.get_issues(state='open')
for issue in open_issues:
    issue.edit(state='closed')
