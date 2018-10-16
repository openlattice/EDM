import os
import yaml
import openapi_client


def get_fields(element):
    fielddict = {
        'entities': ['title','type', 'description', 'schemas','key','properties', 'property_tags', 'id'],
        'properties': ['title','type', 'description', 'schemas','datatype','pii_field', 'multi_valued', 'analyzer', 'id'],
        'associations': ['title','type', 'description', 'src','dst','schemas','key','properties', 'property_tags', 'id']
    }
    return fielddict[element]

def get_constants():
    constants = {}
    basedir = os.path.dirname(os.path.realpath(__file__))
    datadir = os.path.abspath(os.path.join(basedir,"../..","data"))
    constants['propfile'] = os.path.join(datadir,'propertytypes.yaml')
    constants['entfile'] = os.path.join(datadir,'entitytypes.yaml')
    constants['assfile'] = os.path.join(datadir,'associationtypes.yaml')
    constants['constantsfile'] = os.path.join(datadir,'constants.yaml')
    with open(constants['constantsfile'], 'r') as infile:
        constants['schemacodes'] = yaml.load(infile)['schemacodes']
    with open(constants['constantsfile'], 'r') as infile:
        constants['urls'] = yaml.load(infile)['urls']
    return constants

def get_api_instance(baseurl, jwt):
    configuration = openapi_client.Configuration()
    configuration.host = baseurl
    configuration.api_key_prefix['Authorization'] = 'Bearer'
    configuration.api_key['Authorization'] = jwt
    api_instance = openapi_client.EdmApi(openapi_client.ApiClient(configuration))
    return api_instance
