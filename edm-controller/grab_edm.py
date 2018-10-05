from utils import utils

import yaml


edm_prod = utils.grab_edm_from_prod()
# edm_repo = utils.grab_edm_from_repo()

# deleted = []
# for x in ['associations', 'entities', 'properties']:
#     deleted[x] = []
#     deleted[x] = list(set(edm_repo[x].keys()) - set(edm_prod[x].keys()))
#
# set(edm_prod) ^ set(edm_repo)



utils.write_edm(edm_prod)
