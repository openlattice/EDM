import openapi_client

def decode_fqn(dictin):
    return openapi_client.FullQualifiedName(
        namespace = dictin['namespace'],
        name = dictin['name']
    )

def decode_property_type(dictin):
    return openapi_client.PropertyType(
        datatype = dictin['datatype'],
        analyzer = dictin['analyzer'],
        pii_field = dictin['piiField'],
        multi_valued = dictin['multiValued'],
        schemas = [decode_fqn(x) for x in dictin['schemas']],
        title = dictin['title'],
        type = decode_fqn(dictin['type']),
        id = dictin['id'],
        description = dictin['description']
    )

def decode_entity_type(dictin):
    return openapi_client.EntityType(
        property_tags = dictin['propertyTags'],
        schemas = [decode_fqn(x) for x in dictin['schemas']],
        properties = dictin['properties'],
        key = dictin['key'],
        title = dictin['title'],
        type = decode_fqn(dictin['type']),
        id = dictin['id'],
        category = dictin['category'],
        description = dictin['description']
    )

def decode_association_type(dictin):
    return openapi_client.AssociationType(
        entity_type = decode_entity_type(dictin['entityType']),
        src = dictin['src'],
        dst = dictin['dst'],
        bidirectional = dictin['bidirectional']
    )

def decode_schema(dictin):
    return openapi_client.Schema(
            entity_types = [decode_entity_type(x) for x in dictin['entityTypes']],
            property_types = [decode_property_type(x) for x in dictin['propertyTypes']],
            fqn = decode_fqn(dictin['fqn']))


def decode_edm(dictin, version):
    return openapi_client.EDM(
        entity_types = [decode_entity_type(x) for x in dictin['entityTypes']],
        property_types = [decode_property_type(x) for x in dictin['propertyTypes']],
        association_types = [decode_association_type(x) for x in dictin['associationTypes']],
        namespaces = dictin['namespaces'],
        schemas = [decode_schema(x) for x in dictin['schemas']],
        version = version
    )
