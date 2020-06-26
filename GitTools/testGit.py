#! /usr/bin/env python

print("hello")
from github import Github

# First create a Github instance:

# using username and password
g = Github("scottdangelo", "55boat66jeep")

# or using an access token
#g = Github("access_token")

# Github Enterprise with custom hostname
#g = Github(base_url="https://api.github.com/users/scottdangelo/ai-openscale/api/v3", login_or_token="access_token")
#g = Github(base_url=""https://api.github.com/issues", login_or_token="access_token")

# Then play with your Github objects:
#for repo in g.get_user().get_repos():
#    if "testUnity" in repo.name:
#         print(repo.name)
#    print(repo.name)

# get issues
repo = g.get_repo("scottdangelo/testUnity")
#all_issues = repo.get_issues()
open_issues = repo.get_issues(state='open')
for issue in open_issues:
    #print(issue)
    num1 = repo.get_issue(number=1)
    print(num1.body)
    print("issue_id:")
    print(num1.id)
    #print(num1.get_comment("1"))
#    comment_list = num1.get_comments
#    for i in comment_list:
#        print(i)
    #if num1.comments:
    #    for comment in num1.get_comments:
    #        print(comment)
#repo.create_issue(title="This is a new issue", body="This is the issue body")
