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
old_comment_url = old_full_url + "/issues/comments"

hard_comment_url = 'https://api.github.com/repos/scottdangelo/testUnity/comments/591065149'
#hard_comment_url = 'https://api.github.com/repos/scottdangelo/testUnity/issues/comments/1'
#https://api.github.com/repos/scottdangelo/testUnity/issues/comments{/number}"
#print(old_full_url)
r = requests.get(old_full_url)
#if(r.ok):
#    repoItem = json.loads(r.text or r.content)
    #print("my repository created: " + repoItem['created_at'])
#all_issues = requests.get(old_comments_url)
if(r.ok):
    r = requests.get(hard_comment_url)
    #r = requests.get(old_comment_url + '/' + '1')
    comment_response = json.loads(r.text or r.content)
    print(comment_response)
