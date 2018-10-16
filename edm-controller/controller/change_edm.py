import requests
import os

def add_entities(changes, api_instance):
    header = {"Authorization": "Bearer %s"%api_instance.api_client.configuration.api_key['Authorization']}
    url = os.path.join(api_instance.api_client.configuration.host,'datastore/edm/entity/type')
    properties = api_instance.get_all_property_types()
    propdict = {x.to_dict()['id']:".".join(x.to_dict()['type'].values()) for x in properties}
    propdictinv = {v:k for k,v in propdict.items()}

    for k,v in changes['entities']['add'].items():
        newent = {}
        newent['type'] = {'namespace': k.split(".")[0], 'name': k.split(".")[1]}
        newent['schemas'] = [{'namespace': x.split(".")[0], 'name': x.split(".")[1]} for x in v['schemas']]
        newent['properties'] = [propdictinv[x] for x in v['properties']]
        newent['key'] = [propdictinv[x] for x in v['key']]
        newent['description'] = v['description']
        newent['title'] = v['title']
        newent['propertyTags'] = {propdictinv[k]:[v] for k,v in v['property_tags'].items()}
    out = requests.post(url,json=newent,headers=header)

# def change_entities(changes, api_instance):

header = {"Authorization": "Bearer %s"%api_instance.api_client.configuration.api_key['Authorization']}
url = os.path.join(api_instance.api_client.configuration.host,'datastore/edm/entity/type')
properties = api_instance.get_all_property_types()
propdict = {x.to_dict()['id']:".".join(x.to_dict()['type'].values()) for x in properties}
propdictinv = {v:k for k,v in propdict.items()}

for k,v in changes['entities']['change'].items():
    newent = {}
    newent['schemas'] = [{'namespace': x.split(".")[0], 'name': x.split(".")[1]} for x in v['schemas']]
    newent['description'] = v['description']
    newent['title'] = v['title']
    newent['propertyTags'] = {propdictinv[k]:list(v) for k,v in v['property_tags'].items()}

out = requests.get(os.path.join(url,v['id']),json=newent,headers=header)
out.text
