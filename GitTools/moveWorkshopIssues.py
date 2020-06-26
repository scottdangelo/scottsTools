#! /usr/bin/env python

import os
import time
from github import Github

REPO = os.environ.get('REPO')
WORKSHOP = os.environ.get('WORKSHOP')
GH_TOKEN = os.environ.get('TOKEN')

ISSUES = [
'Get Proposed dates from client',
'Workshop presenters are available on Scheduled date',
'Video streaming team is available on Scheduled date',
'Get module request from Account team',
'We have Existing content',
'Create new content if needed',
'Assign cards to users',
'Scope work with estimates',
'Send a pre-workshop survey to gauge background and interests (if possible)',
'Get account setup + credits',
'Install CP4D [after we are admins on the account]',
'Verify the cluster is set up correctly',
'Run through the admin guide',
'Run through as user',
'Create CP4D users',
'Add us as admins to their cloud account',
'Verify access to portals / github / cluster',
'Whitelist the workshop in firewall (or issue certificates for us)',
'Send pre-workshop (get hyped: account set up / verify access)',
'Copy survey form with unique url.',
'Create tiles and content for Portal page',
'Create tile in developer portal (copy from -> link here)',
'Link to Cluster',
'Link to demo app',
'Link to survey',
'Ensure downstream is up to date',
'Create `workshop-*` branch for workshop with naming convention for GitBook.  Edit workshop branch to update:',
'add custom SUMMARY.md for TOC',
'Add cluster specific links to notebooks, READMEs, etc',
'Delete the cluster when the credits expire',
'Distribute the slides',
'collect notes on what went well and what can be improved',
'Gather customer and client team feedback'
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

    ret_issue = repo.create_issue(title = WORKSHOP + ' ' + issue, body = issue)
