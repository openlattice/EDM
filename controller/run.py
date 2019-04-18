from collections import OrderedDict
from github import Github
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

file_sha = repo.get_file_contents('data/edm.json')
prod_change = commenter.comment(pull, master_key, pull_key, prod_key)


############
## COMMIT PROD TO MASTER
############

newdict = OrderedDict()
associationTypesOrder = np.argsort([edm.concat_fqn(x['entityType']['type']) for x in prod_edm['associationTypes']])
newdict['associationTypes'] = [prod_edm['associationTypes'][x] for x in associationTypesOrder]
entityTypesOrder = np.argsort([edm.concat_fqn(x['type']) for x in prod_edm['entityTypes']])
newdict['entityTypes'] = [prod_edm['entityTypes'][x] for x in entityTypesOrder]
newdict['namespacesOrder'] = prod_edm['namespaces'].sort()
propertyTypesOrder = np.argsort([edm.concat_fqn(x['type']) for x in prod_edm['propertyTypes']])
newdict['propertyTypes'] = [prod_edm['propertyTypes'][x] for x in propertyTypesOrder]
schemasOrder = np.argsort([edm.concat_fqn(x['fqn']) for x in prod_edm['schemas']])
newdict['schemas'] = [prod_edm['schemas'][x] for x in schemasOrder]

new_edm = json.dumps(newdict, indent=4)
repo.update_file(path = "data/edm.json", message = "updates from prod", content = new_edm, sha = master_sha)
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
