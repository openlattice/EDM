from collections import OrderedDict
import yamlordereddictloader
import openapi_client
import copy
import yaml
import json
import os

def grab_edm():
    # Configure API key authorization
    baseurl = 'https://api.openlattice.com'
    configuration = openapi_client.Configuration()
    configuration.host = baseurl
    api_instance = openapi_client.EdmApi(openapi_client.ApiClient(configuration))

    edm = {}
    # get and process property types
    properties = api_instance.get_all_property_types()
    edm['properties'] = [get_human_property(x.to_dict()) for x in properties]
    propdict = {x.to_dict()['id']:".".join(x.to_dict()['type'].values()) for x in properties}

    # get and process entity types
    entities = api_instance.get_all_entity_types()
    edm['entities'] = [get_human_entity(x.to_dict(), propdict) for x in entities]
    entdict = {x.to_dict()['id']:".".join(x.to_dict()['type'].values()) for x in entities}

    # get and process association types
    associations = api_instance.get_all_association_entity_types()
    edm['associations'] = [get_human_association(x.to_dict(), propdict, entdict) for x in associations]

    return edm

def write_edm(edm):
    basedir = os.path.dirname(os.path.realpath(__file__))
    datadir = os.path.abspath(os.path.join(basedir,"../..","data"))

    propfile = os.path.join(datadir,'propertytypes.yaml')
    entfile = os.path.join(datadir,'entitytypes.yaml')
    assfile = os.path.join(datadir,'associationtypes.yaml')

    with open(propfile, 'w') as outfile:
        yaml.dump(edm['properties'], outfile, Dumper=yamlordereddictloader.Dumper,indent=4)
    with open(entfile, 'w') as outfile:
        yaml.dump(edm['entities'], outfile, Dumper=yamlordereddictloader.Dumper,indent=4)
    with open(assfile, 'w') as outfile:
        yaml.dump(edm['associations'], outfile, Dumper=yamlordereddictloader.Dumper,indent=4)
    return 0


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
