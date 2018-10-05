import openapi_client
import copy
import json
import os

def str_to_fqn(input):
    fqn = ".".join(list(json.loads(input.replace("'","\"")).values()))
    return fqn

def type_to_fqn(type):
    fqn = "%s.%s"%(type['namespace'], type['name'])
    return fqn

def get_property_fqn(propid, api_instance):
    proptype = api_instance.get_property_type(propid).to_dict()
    prop = type_to_fqn(proptype['type'])
    return prop

def get_human_entity(ent, api_instance):
    entity = copy.deepcopy(ent)
    del entity['id']
    entity['type'] = type_to_fqn(entity['type'])
    entity['schemas'] = [type_to_fqn(x) for x in entity['schemas']]
    entity['key'] = [get_property_fqn(x, api_instance) for x in entity['key']]
    entity['properties'] = [get_property_fqn(x, api_instance) for x in entity['properties']]
    return entity

def get_human_property(prop):
    property = copy.deepcopy(prop)
    del property['id']
    property['type'] = type_to_fqn(property['type'])
    property['schemas'] = [type_to_fqn(x) for x in property['schemas']]
    return property

def get_human_association(ass, api_instance):
    association = copy.deepcopy(ass)
    assent = get_human_entity(association['entity_type'], api_instance)
    del association['entity_type']
    association.update(assent)
    srcs = []
    for key in ['src','dst']:
        association[key] = []
        for x in ass['src']:
            try:
                enttype = api_instance.get_entity_type(x)
                type = type_to_fqn(enttype.to_dict()['type'])
                association[key].append(type)
            except openapi_client.rest.ApiException:
                continue
    return association
