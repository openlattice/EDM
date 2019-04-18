from github import Github
import openlattice
import requests
import base64
import json
import sys
import os
#
# sys.path = ["/Users/jokedurnez/Documents/Software/PyGithub"] + sys.path
# import github

from utils import api, edm, changes, commenter
# decoder

jwt="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Impva2VAb3BlbmxhdHRpY2UuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInVzZXJfbWV0YWRhdGEiOnt9LCJhcHBfbWV0YWRhdGEiOnsicm9sZXMiOlsiQXV0aGVudGljYXRlZFVzZXIiLCJhZG1pbiJdLCJvcmdhbml6YXRpb25zIjpbIjAwMDAwMDAwLTAwMDAtMDAwMS0wMDAwLTAwMDAwMDAwMDAwMCIsImU2NmM5ZWVmLTIzNzktNGEwYy05Y2JiLWM2ZDhiMmIxM2M1ZiJdfSwibmlja25hbWUiOiJqb2tlIiwicm9sZXMiOlsiQXV0aGVudGljYXRlZFVzZXIiLCJhZG1pbiJdLCJ1c2VyX2lkIjoiZ29vZ2xlLW9hdXRoMnwxMDM3NzE3NTU1NDA4NjUyOTkyNDgiLCJpc3MiOiJodHRwczovL29wZW5sYXR0aWNlLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMzc3MTc1NTU0MDg2NTI5OTI0OCIsImF1ZCI6IktUemd5eHM2S0JjSkhCODcyZVNNZTJjcFRIemh4Uzk5IiwiaWF0IjoxNTU1NTQ5MTkzLCJleHAiOjE1NTU2MzU1OTN9.YzE7CKeR5V4caiJCh-JjCBvVLvzrd4fGUd45MqS38v4"
baseurl = 'http://localhost:8080'


# jwt = api.get_jwt()['access_token']
# baseurl = "https://api.openlattice.com"
#
# user = g.get_user()
# user.edit(name='curator-bot', email='info@openlattice.com')

EdmApi = api.get_api_instance(baseurl, jwt)

#################
## GITHUB
#################

gituser = os.environ.get("gitBotUser")
gitpw = os.environ.get("gitBotPassword")
# get the sha
g = Github(gituser, gitpw)
gitsha = os.environ.get("bambooRevision")
gitsha = 'f724dd097586ae0fcc6dc2d8cfcf6d18b2cafab2'
repo = g.get_repo("Lattice-Works/EDM")

# is this gitsha part of an open pull request?
pulls = repo.get_pulls()
thispull = []
for pullit in pulls:
    commits = pullit.get_commits()
    if commits.totalCount == 1 and commits[0].sha==gitsha:
        pull = pullit
        break
# if 'pull' in locals() and pull.title.startswith("edm changes 201"):
#     pull_request_commenter.create_comment(repo, gitsha, pull)
    #### MAKE report
else:
    print("This is probably not a commit for changes...")


###############
## GRAB EDM's
###############

master_sha = repo.get_contents('data')[0].sha
master_blob = repo.get_git_blob(master_sha)
master_edm = json.loads(base64.b64decode(master_blob.raw_data['content']))
master_key = edm.make_key_edm(master_edm)

pull_sha = repo.get_contents('data', gitsha)[0].sha
pull_blob = repo.get_git_blob(pull_sha)
pull_edm = json.loads(base64.b64decode(pull_blob.raw_data['content']))
pull_key = edm.make_key_edm(pull_edm)

prod_edm = api.request_edm(baseurl, jwt)
prod_key = edm.make_key_edm(prod_edm)

prod_change = commenter.comment(pull, master_key, pull_key, prod_key)

# diff = EdmApi.get_entity_data_model_diff(master_edm)


#############
## TRY TO MERGE PROD INTO MASTER
#############
 
#if len(pr_report) > 0:
    # 
    # 
    # 
    # 
    # const edm = fromJS({
    #   associationTypes: associationTypes.sort(fqnComparator(['entityType', 'type'])),
    #   entityTypes: entityTypes.sort(fqnComparator(['type'])),
    #   namespaces: namespaces.sort(),
    #   propertyTypes: propertyTypes.sort(fqnComparator(['type'])),
    #   schemas: schemas.sort(fqnComparator(['fqn'])),
    # }).sortBy((v, k) => k).toJS();


# branch = pull.head.label.split(":")[1]
# repo.update_file('data/edm.json', message = "add prod changes", content = prod_edm_bin, sha = '8aa8219bf55af2eb0c29b16e8c6348822c0d0689', branch = branch)
# 
# path='data/edm.json'
# 
# 
# GitBlob.GitBlob(content=prod_edm_str, encoding='utf-8')
# 
# 
# 
# 
# 
# cont = repo.get_contents('data/edm.json',gitsha)
# 
# encoded = base64.b64encode("data to be encoded")
# 
# 
# import base64
# encoded = base64.b64encode(b'data to be encoded')
# 
# new._useAttributes(attributes = {"content": prod_edm_str, "encoding": 'utf-8'})
# 
# 
# 
# 
# report = report.replace("  "," ").replace("\n\n", "\n")
# pull.create_issue_comment(report)
# 
# 
# #################
# ## ACTUALLY APPLY THE DIFFERENCES
# #################
# 
# 
# version = '00000167-1447-bdbb-0000-000000000000'
# 
# 
# entityAPI = api.get_api_instance(baseurl, jwt)
# 
# 
# prod_edm = api.request_edm(baseurl, jwt)
# prod = edm.make_key_edm(prod_edm)
# 
# report = changes.changeReport(master,prod)
# 
# prodedm = entityAPI.get_entity_data_model().__dict__
# prod_edm_decoded = decoder.decode_edm(prodedm, version)
# prod = edm.make_key_edm(prod_edm_decoded)
# 
# master_edm_decoded = decoder.decode_edm(master_edm, version)
# master_diff = entityAPI.get_entity_data_model_diff(master_edm_decoded)
# 
# edm_diff = entityAPI.get_entity_data_model_diff(prodedm)
# 
# 
# master_edm_bin = repo.get_contents('data/edm.json').content.encode()
# master_edm_str = base64.decodebytes(master_edm_bin)
# master_edm = json.dumps(prod_edm_decoded)
# 
# 
# master_edm_decoded.version
# master_diff.diff.version
# 
# 
# #################
# ## GET REPORT
# #################
# 
# report = edm.changeReport(master,new).get_report()
# 
# 
# testEDM = openapi_client.EDM()
# testEDM.version = '1234'
# 
# 
# # is this gitsha a merge?
# commit = repo.get_commit(gitsha)
# commitmessage = commit.raw_data['commit']['message']
# 
# if commitmessage.startswith("Merge pull request"):
#     # make sure pull request was approved
#     PR = commitmessage.split("#")[1].split(" ")[0]
#     pull = repo.get_pull(int(PR))
