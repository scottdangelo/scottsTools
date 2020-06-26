#! /usr/bin/env python

import requests
import json

base_url = 'https://api.github.com/repos/'
my_repo_url = 'scottdangelo'
old_repo_url = 'testUnity'
new_repo_url = 'BarcelonaTalk'
old_full_url = base_url + my_repo_url + '/' + old_repo_url
new_full_url = base_url + my_repo_url + '/' + new_repo_url
old_issues_url = old_full_url + "/issues"
new_issues_url = new_full_url + "/issues"

#print(old_full_url)
r = requests.get(old_full_url)
#if(r.ok):
#    repoItem = json.loads(r.text or r.content)
    #print("my repository created: " + repoItem['created_at'])
#all_issues = requests.get(old_issues_url)
if(r.ok):
    issue_response = json.loads(r.text or r.content)
    #print("all issues titles: " + str(issue_response['title']))
    #print("all issues: " + str(issue_response))
    #print("total num issues : " + str(issue_response['open_issues']))
    num_issues = issue_response['open_issues']
    #print(num_issues)
    for i in range(1, num_issues+1):
        r = requests.get(old_issues_url + '/' + str(i))
        issue = json.loads(r.text or r.content)
        old_title = issue['title']
        old_body = issue['body']
        print("title: " + old_title)
        print("body: " + old_body)
        new_issue_json = {
            "title": old_title,
            "body": old_body
            }
        r = requests.post(new_issues_url, json = {
            "title": old_title,
            "body": old_body
            })
        if(r.ok):
            repoItem = json.loads(r.text or r.content)
            print(repoItem)
        else:
            print("fail")
            print(r)

