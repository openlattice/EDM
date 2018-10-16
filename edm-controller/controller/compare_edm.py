from . import utils
from collections import Counter

constants = utils.get_constants()

def check_consistency(edm_repo):
    ers = []
    for element in ['associations', 'entities', 'properties']:
        proplist = list(edm_repo['properties'].keys())
        entlist = list(edm_repo['entities'].keys())
        ids = []
        for k,v in edm_repo[element].items():
            if 'id' in v.keys():
                ids.append(v['id'])
            if k != v['type']:
                ers.append("INCONSISTENT KEY/TYPE: The key and type do not correspond for key %s (value %s)"%(k,v['type']))
            if element != 'properties':
                missingprops = [x for x in v['properties'] if x not in proplist]
                if len(missingprops) > 0:
                    ers.append("INCONSISTENT PROPERTIES: The entity %s contains unknown properties: %s"%(v['type'], ", ".join(missingprops)))
            if element == 'associations':
                for src in v['src']:
                    if not src in entlist:
                        ers.append("INCONSISTENT ENTITIES: The association %s contains an unknown source: %s"%(v['type'], src))
                for dst in v['dst']:
                    if not dst in entlist:
                        ers.append("INCONSISTENT ENTITIES: The association %s contains an unknown source: %s"%(v['type'], dst))
        cnts = dict(Counter(ids))
        cntsmore = {k:v for k,v in cnts.items() if v>1}
        if len(cntsmore)>0:
            ers.append("DUPLICATED IDs: There are repeated id's in the %s: %s is/are repeated.  If you're creating a new element, don't specify an id !"%(element, ", ".join(cntsmore.keys())))
    if len(ers)>0:
        raise ValueError("\n"+"\n".join(ers))
    return ers


def get_changes(edm_prod, edm_repo):
    # invert to id key
    edm_repo_inv = {element: {v['id']: v for k,v in edm_repo[element].items() if 'id' in v.keys()} for element in ['associations', 'entities', 'properties']}
    edm_prod_inv = {element: {v['id']: v for k,v in edm_prod[element].items() if 'id' in v.keys()} for element in ['associations', 'entities', 'properties']}

    # collect changes
    changes = {}
    for element in ['associations', 'entities', 'properties']:
        flds = utils.get_fields(element)
        # inverse dict and find changes
        changes[element] = {}
        # find new in repo // empty id's
        changes[element]['add'] = {k: v for k,v in edm_repo[element].items() if 'id' not in v.keys() or v['id']==None}
        # find deletes
        changes[element]['delete'] = {k: v for k,v in edm_prod_inv[element].items() if not k in edm_repo_inv[element].keys()}
        # find changes
        changes[element]['change'] = {oldkey: oldvalues for oldkey,oldvalues in edm_prod_inv[element].items() \
                if oldkey in edm_repo_inv[element].keys() and \
                "-".join([str(edm_prod_inv[element][oldkey][fld]) for fld in flds]) != "-".join([str(edm_repo_inv[element][oldkey][fld]) for fld in flds])
                }
    return changes


def check_changes(edm_repo,edm_prod,changes,api_instance):
    # propertyusages = api_instance.get_all_property_usage_summaries()
    edm_repo_inv = {element: {v['id']: v for k,v in edm_repo[element].items() if 'id' in v.keys()} for element in ['associations', 'entities', 'properties']}
    edm_prod_inv = {element: {v['id']: v for k,v in edm_prod[element].items() if 'id' in v.keys()} for element in ['associations', 'entities', 'properties']}

    changes_report = []
    for element in ['associations', 'entities', 'properties']:

        # check additions
        for k,v in changes[element]['add'].items():

            change = {
                "type": "add",
                "element": element,
                "name": k
            }

            if k in edm_prod[element]:
                change['code'] = 'error'
                change['reason'] = 'already exists'
            else:
                change['code'] = 'ok'
            changes_report.append(change)

        # check changes
        for k,v in changes[element]['change'].items():
            old = edm_prod_inv[element][k]
            new = edm_repo_inv[element][k]
            keys = utils.get_fields(element)
            changedkeys = [key for key in keys if old[key]!= new[key]]
            for changedkey in changedkeys:

                change = {
                    'type': 'change',
                    'element': element,
                    'elementname': old['type'],
                    'id': old['id'],
                    'part': changedkey,
                    'oldvalue': old[changedkey],
                    'newvalue': new[changedkey]
                }

                if changedkey == 'type':
                    change = {
                        'type': 'change',
                        'element': element,
                        'id': old['id'],
                        'part': 'type'
                    }
                    change['code'] = 'TODO'

                elif changedkey in ['datatype', 'multi_valued']:
                    change['code'] = 'error'
                    change['reason'] = 'not allowed to change %s'%changedkey

                elif changedkey == 'pii_field':
                    if old[changedkey] == True and new[changedkey] == False:
                        change['code'] = 'error'
                        change['reason'] = 'not allowed to change from non-pii to pii'
                    else:
                        change['code'] = 'ok'

                elif changedkey == 'schemas':
                    removes = set(old[changedkey])-set(new[changedkey])
                    if len(removes.intersection(set(constants['schemacodes'])))>0:
                        change['code'] = 'error'
                        change['reason'] = 'not allowed to removed a used schema code'
                    else:
                        change['code'] = 'ok'

                elif changedkey in ['properties', 'key']:
                    removes = set(old[changedkey])-set(new[changedkey])
                    del change['oldvalue']
                    del change['newvalue']
                    change['added'] = list(set(new[changedkey])-set(old[changedkey]))
                    change['removed'] = list(set(old[changedkey])-set(new[changedkey]))
                    if len(removes) > 0:
                        ## TODO: verify property usage
                        change['code'] = 'error'
                        change['reason'] = 'not allowed to remove properties %s from entity type %s.'%(", ".join(removes), old['type'])
                    else:
                        change['code'] = 'ok'
                elif changedkey in ['src', 'dst']:
                    removes = set(old[changedkey])-set(new[changedkey])
                    del change['oldvalue']
                    del change['newvalue']
                    change['added'] = list(set(new[changedkey])-set(old[changedkey]))
                    change['removed'] = list(set(old[changedkey])-set(new[changedkey]))
                    if len(removes) > 0:
                        ## TODO: verify property usage
                        change['code'] = 'error'
                        change['reason'] = 'not allowed to remove properties %s from entity type %s.'%(", ".join(removes), old['type'])
                    else:
                        change['code'] = 'ok'
                else:
                    change['code'] = 'hm?'

                changes_report.append(change)

        # check delete
        for k,v in changes[element]['delete'].items():
            old = edm_prod_inv[element][k]
            change = {
                'type': 'delete',
                'element': element,
                'id': old['id'],
                'code': 'error',
                'reason': 'Not allowed to delete element %s.  Consider adding tags.'%old['type']
            }
            changes_report.append(change)
    return changes_report
