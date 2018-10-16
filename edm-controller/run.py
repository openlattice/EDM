from controller import utils, get_edm, compare_edm#, change_edm
from argparse import ArgumentParser
from pprint import pprint
import openapi_client
import yaml

parser = ArgumentParser(description = 'EDM Controller: client to make changes to the EDM.')
parser.add_argument('--environment', help = 'Environment to run edm controller (local or production).')
parser.add_argument('--jwt', help = 'JWT token.')
args = parser.parse_args()

constants =  utils.get_constants()

baseurl = constants['urls'][args.environment]
jwt = args.jwt

api_instance = utils.get_api_instance(baseurl, jwt)

edm_prod = get_edm.grab_edm_from_prod(api_instance)
edm_repo = get_edm.grab_edm_from_repo()

## CHECKS FOR CONSISTENCY IN PROPOSAL ##
ers = compare_edm.check_consistency(edm_repo)

## COLLECT CHANGES ##
changes = compare_edm.get_changes(edm_prod, edm_repo)

## CHECK CHANGES ##
changereport = compare_edm.check_changes(edm_repo, edm_prod, changes, api_instance)

## RESULT ! ##
ers = [x for x in changereport if x['code'] == 'error']
if len(ers) > 0:
    print(yaml.dump(ers,default_flow_style=False, default_style=''))
    raise ValueError("Certain requested changes are not possible.")

noschema = [x for x in changereport if x['part'] != 'schemas']
if len(ers) > 0:
    print(yaml.dump(ers,default_flow_style=False, default_style=''))
    raise ValueError("Right now we can *only* change schema's.")

if len(ers) == 0 and len(changereport)>0:
    print("Yay ! These changes can be made.")

# change_edm.add_entities(changes, api_instance)
