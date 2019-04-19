from argparse import ArgumentParser
from collections import OrderedDict
from github import Github, Issue
import numpy as np
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

parser = ArgumentParser(description = 'EDM service')
parser.add_argument('--jwt')
parser.add_argument("--baseurl")
parser.add_argument('--stage')
parser.add_argument('--gitsha')

args = parser.parse_args()

jwt = args.jwt
baseurl = args.baseurl


# jwt = api.get_jwt()['access_token']
# baseurl = "https://api.openlattice.com"
#
# user = g.get_user()
# user.edit(name='curator-bot', email='info@openlattice.com')

apiclient = api.get_api_instance(baseurl, jwt)
EdmApi = openlattice.EdmApi(apiclient)

#################
## GITHUB
#################

gituser = os.environ.get("gitBotUser")
gitpw = os.environ.get("gitBotPassword")
# get the sha
g = Github(gituser, gitpw)
gitsha = os.environ.get("bambooRevision")
gitsha = args.gitsha
repo = g.get_repo("Lattice-Works/EDM")

# is this gitsha part of an open pull request?
if args.stage == "PR":
    pulls = repo.get_pulls()
    thispull = []
    for pullit in pulls:
        commits = pullit.get_commits()
        if commits.totalCount == 1 and commits[0].sha==gitsha:
            pull = pullit
            break
    else:
        raiseValueError("This is probably not a commit for changes...")

###############
## GRAB EDM's : SHOULD RUN EVERY TIME
###############

master_sha = repo.get_contents('data')[0].sha
master_blob = repo.get_git_blob(master_sha)
master_edm = json.loads(base64.b64decode(master_blob.raw_data['content']))
master_key = edm.make_key_edm(master_edm)

prod_edm = api.request_edm(baseurl, jwt)
prod_key = edm.make_key_edm(prod_edm)

pull_sha = repo.get_contents('data', gitsha)[0].sha
pull_blob = repo.get_git_blob(pull_sha)
pull_edm = json.loads(base64.b64decode(pull_blob.raw_data['content']))
pull_key = edm.make_key_edm(pull_edm)

############
## MAKE REPORT ON PR: SHOULD RUN ON PR
############

if args.stage=='PR':
    prod_change = commenter.comment(pull, master_key, pull_key, prod_key)

############
## COMMIT PROD TO MASTER AND SUBMIT ISSUE: SHOULD RUN ON RP AND ON MERGE
############

# new_edm = json.dumps(prod_edm, indent=2, sort_keys = True)
# repo.update_file(path = "data/edm.json", message = "updates from prod", content = new_edm, sha = master_sha)
# 
# prod_report = changes.changeReport(master_key, prod_key).get_report()
# repo.create_issue(title="Oops. Somebody made changes to the EDM !", body = prod_report)

#############
## APPLY AFTER MERGE
#############

# merge in master

# which branch is this on?
# base = pull.head.ref
# head = repo.get_branch("master")
# repo.merge("master", head.commit.sha, "merge to master")
if args.stage=='merge':
    EdmApi.update_entity_data_model(master_edm)
