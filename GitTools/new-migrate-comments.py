#! /usr/bin/env python

import os
from github import Github

GH_TOKEN = os.environ.get('GH_TOKEN')
g = Github(GH_TOKEN)
pub_repo = g.get_repo('ibm/cloudpakfordata-telco-churn-workshop')
GHE_TOKEN = os.environ.get('GHE_TOKEN')
ghe = Github(base_url="https://github.ibm.com/api/v3", login_or_token=GHE_TOKEN)
ghe_repo = ghe.get_repo('Scott-DAngelo/test-telco')
for issue in pub_repo.get_issues():
    if issue.comments:
        comments = issue.get_comments()
        for comment in comments:
            print('comment.id: ' + str(comment.id))
            print('comment.body: ' + comment.body)
#    ret_issue = ghe_repo.create_issue(title=issue.title, body=issue.body)
