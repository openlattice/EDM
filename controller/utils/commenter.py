from github import Github
import requests
import base64
import json
import os

from . import api, edm, changes

def comment(pull, master_key, pull_key, prod_key):
    pr_report = changes.changeReport(master_key, pull_key).get_report()
    prod_report = changes.changeReport(master_key, prod_key).get_report()
    
    report = ""
    if len(prod_report) > 0:
        report += '''
                 # Changes from prod
                 Somebody made changes to prod between the previous commit and this PR.  We merged in those changes safely, but we need to avoid this from happening.
                 {prod_report}
                 '''.format(prod_report=prod_report)
        prod = True
    else:
        prod = False
        
    report += '''
            # New changes
    
            {pr_report}
            '''.format(pr_report = pr_report)

    report = report.replace("  "," ").replace("\n\n", "\n")
    pull.create_issue_comment(report)

    return prod