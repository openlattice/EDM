from github import Github
import base64
import json
import os

from utils import edm, edm_utils

# g = Github(os.environ.get("gitBotUser"), os.environ.get("gitBotPassword"))
#
# # get the pull request
# repo = g.get_repo("Lattice-Works/EDM")
# pull = repo.get_pull(16)
#
# master_edm_bin = repo.get_contents('data/edm.json').content.encode()
# master_edm_str = base64.decodebytes(master_edm_bin)
# master_edm = json.loads(master_edm_str)
# master = edm_utils.make_key_edm(master_edm)
#
# new_edm_bin = repo.get_contents('data/edm.json',pull.get_commits()[0].sha).content.encode()
# new_edm_str = base64.decodebytes(new_edm_bin)
# new_edm = json.loads(new_edm_str)
# new = edm_utils.make_key_edm(new_edm)
#
# ###### MAKE REPORT ############
#
# report = edm.changeReport(master,new).get_report()
# # pull.create_issue_comment(report)

print(os.environ.get("bamboo.planRepository.branch"))

print("ya")
