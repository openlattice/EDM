import yamlordereddictloader
import openapi_client
import json
import yaml
import os

from utils import utils

basedir = os.path.dirname(os.path.realpath(__file__))
datadir = os.path.abspath(os.path.join(basedir,"..","data"))

# Configure API key authorization
baseurl = 'https://api.openlattice.com'

configuration = openapi_client.Configuration()
configuration.host = baseurl

api_instance = openapi_client.EdmApi(openapi_client.ApiClient(configuration))

# get and process property types
properties = api_instance.get_all_property_types()
props = [utils.get_human_property(x.to_dict()) for x in properties]
propfile = os.path.join(datadir,'propertytypes.yaml')
with open(propfile, 'w') as outfile:
    yaml.dump(props, outfile, Dumper=yamlordereddictloader.Dumper,indent=4)

propdict = {x.to_dict()['id']:".".join(x.to_dict()['type'].values()) for x in properties}

# get and process entity types
entities = api_instance.get_all_entity_types()
ents = [utils.get_human_entity(x.to_dict(), propdict) for x in entities]
entfile = os.path.join(datadir,'entitytypes.yaml')
with open(entfile, 'w') as outfile:
    yaml.dump(ents, outfile, Dumper=yamlordereddictloader.Dumper,indent=4)

entdict = {x.to_dict()['id']:".".join(x.to_dict()['type'].values()) for x in entities}


# get and process association types
associations = api_instance.get_all_association_entity_types()
ass = [utils.get_human_association(x.to_dict(), propdict, entdict) for x in associations]
assfile = os.path.join(datadir,'associationtypes.yaml')
with open(assfile, 'w') as outfile:
    yaml.dump(ass, outfile, Dumper=yamlordereddictloader.Dumper,indent=4)
