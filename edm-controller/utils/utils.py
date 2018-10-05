from collections import OrderedDict
import openapi_client
import copy
import json
import os

def type_to_fqn(type):
    fqn = "%s.%s"%(type['namespace'], type['name'])
    return fqn

def get_human_entity(ent, propdict):
    entity = copy.deepcopy(ent)
    del entity['id']
    entity['type'] = type_to_fqn(entity['type'])
    entity['schemas'] = [type_to_fqn(x) for x in entity['schemas']]
    entity['key'] = [propdict[x] for x in entity['key']]
    entity['properties'] = [propdict[x] for x in entity['properties']]
    keyorder = ['title','type', 'description', 'schemas','key','properties', 'property_tags', 'basetype']
    return OrderedDict((k, entity[k]) for k in keyorder)

def get_human_property(prop):
    property = copy.deepcopy(prop)
    del property['id']
    property['type'] = type_to_fqn(property['type'])
    property['schemas'] = [type_to_fqn(x) for x in property['schemas']]
    keyorder = ['title','type', 'description', 'schemas','datatype','pii_field', 'multi_valued', 'analyzer']
    return OrderedDict((k, property[k]) for k in keyorder)

def get_human_association(ass, propdict, entdict):
    association = copy.deepcopy(ass)
    assent = get_human_entity(association['entity_type'], propdict)
    del association['entity_type']
    association.update(assent)
    srcs = []
    for key in ['src','dst']:
        association[key] = []
        for x in ass['src']:
            if x in entdict.keys():
                enttype = entdict[x]
                association[key].append(enttype)
    keyorder = ['title','type', 'description', 'src','dst','schemas','key','properties', 'property_tags', 'basetype']
    return OrderedDict((k, association[k]) for k in keyorder)
