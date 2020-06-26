#! /usr/bin/env python

import os
import time
from github import Github

REPO = os.environ.get('REPO')
SUBJECT = os.environ.get('SUBJECT')
GH_TOKEN = os.environ.get('TOKEN')

ISSUES = [
'README.md',
'SUMMARY.md',
'addData',
'admin-guide',
'data-visualization-and-refinery',
'db-connection-and-virtualization',
'gitIntegration',
'machine-learning-autoai',
'machine-learning-in-Jupyter-notebook',
'mlmodel-deployment-scoring',
'openscale-fastpath',
'openscale-notebook',
'pre-work',
'watson-knowledge-catalog-admin',
'watson-knowledge-catalog-user'
]

g = Github(base_url="https://github.ibm.com/api/v3", login_or_token=GH_TOKEN)
repo = g.get_repo(REPO)
print(repo.name)
i = 0
for issue in ISSUES:

    # sleep to prevent DNS
    if not i % 5:
        time.sleep(3)
        i = i + 1

    ret_issue = repo.create_issue(title = SUBJECT + ' doc changes ' + issue, body = issue)
    ret_issue_2 = repo.create_issue(title = SUBJECT + ' test ' + issue, body = issue)
