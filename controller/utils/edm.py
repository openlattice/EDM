class changeReport(object):

    def __init__(self, old, new):
        self.old = old
        self.new = new
        self.oldpropertydict = {k: _concat_fqn(v['type']) for k,v in old['propertyTypes'].items()}
        self.newpropertydict = {k: _concat_fqn(v['type']) for k,v in new['propertyTypes'].items()}
        self.oldentitydict = {k: _concat_fqn(v['type']) for k,v in old['entityTypes'].items()}
        self.newentitydict = {k: _concat_fqn(v['type']) for k,v in new['entityTypes'].items()}

    def get_property_report(self):
        propdict1 = self.old['propertyTypes']
        propdict2 = self.new['propertyTypes']
        idchanges = _get_id_changes(propdict1, propdict2)

        # get a nice list of deleted properties
        deletednames = [propertyType(propdict1[x]).fqn for x in idchanges['deletions']]
        propdel = "- "+"\n- ".join(sorted(deletednames))

        # get an overview of added properties
        stringlist = [propertyType(propdict2[x]).print() for x in idchanges['additions']]
        propadd = "\n\n".join(stringlist)

        # get an overview of changed properties
        changed = [x for x in idchanges['common'] if \
            propertyType(propdict1[x]).print() != propertyType(propdict2[x]).print()]
        propchange = ""
        for propid in changed:
            this = propertyType(propdict2[propid])
            other = propertyType(propdict1[propid])
            propchange += this.compare(other)

        propreport = '''## Changes to Property Types
        \n### Deleted property types:
        \n{propdel}
        \n### New property types:
        \n{propadd}
        \n### Changed property types:
        \n{propchange}
        '''.format(propdel=propdel, propadd = propadd, propchange = propchange)
        return propreport

    def get_entity_report(self):
        entdict1 = self.old['entityTypes']
        entdict2 = self.new['entityTypes']

        idchanges = _get_id_changes(entdict1, entdict2)

        # get a nice list of deleted entities
        deletednames = [entityType(entdict1[x], self.oldpropertydict).fqn for x in idchanges['deletions']]
        entdel = "- "+"\n- ".join(sorted(deletednames))

        # get an overview of added entities
        stringlist = [entityType(entdict2[x], self.newpropertydict).print() for x in idchanges['additions']]
        entadd = "\n\n".join(stringlist)

        # get an overview of changed entities
        changed = [x for x in idchanges['common'] if \
            entityType(entdict1[x], self.oldpropertydict).print() != entityType(entdict2[x], self.newpropertydict).print()]
        entchange = ""
        for entid in changed:
            this = entityType(entdict2[entid], self.newpropertydict)
            other = entityType(entdict1[entid], self.oldpropertydict)
            entchange += this.compare(other)

        entreport = '''## Changes to Entity Types
        \n### Deleted entity types:
        \n{entdel}
        \n### New entity types:
        \n{entadd}
        \n### Changed entity types:
        \n{entchange}
        '''.format(entdel=entdel, entadd = entadd, entchange = entchange)
        return entreport

    def get_association_report(self):
        assdict1 = self.old['associationTypes']
        assdict2 = self.new['associationTypes']

        idchanges = _get_id_changes(assdict1, assdict2)

        # get a nice list of deleted entities
        deletednames = [associationType(assdict1[x], self.oldpropertydict, self.oldentitydict).fqn for x in idchanges['deletions']]
        assdel = "- "+"\n- ".join(sorted(deletednames))

        # get an overview of added entities
        stringlist = [associationType(assdict2[x], self.newpropertydict, self.newentitydict).print() for x in idchanges['additions']]
        assadd = "\n\n".join(stringlist)

        # get an overview of changed entities
        changed = [x for x in idchanges['common'] if \
            associationType(assdict1[x], self.oldpropertydict, self.oldentitydict).print() != associationType(assdict2[x], self.newpropertydict, self.newentitydict).print()]
        asschange = ""
        for entid in changed:
            this = associationType(assdict2[entid], self.newpropertydict, self.newentitydict)
            other = associationType(assdict1[entid], self.oldpropertydict, self.oldentitydict)
            asschange += this.compare(other)

        entreport = '''## Changes to Association Types
        \n### Deleted association types:
        \n{assdel}
        \n### New association types:
        \n{assadd}
        \n### Changed association types:
        \n{asschange}
        '''.format(assdel = assdel, assadd = assadd, asschange = asschange)
        return entreport

    def get_report(self):
        propertyreport = self.get_property_report()
        entityreport = self.get_entity_report()
        associationreport = self.get_association_report()
        fullreport = "{propertyreport} \n{entityreport} \n{associationreport}".format(
            propertyreport = propertyreport,
            entityreport = entityreport,
            associationreport = associationreport
        )
        return fullreport

class propertyType(object):

    def __init__(self, propertyType):
        self.title = propertyType['title']
        self.description = propertyType['description']
        self.datatype = propertyType['datatype']
        self.analyzer = propertyType['analyzer']
        self.piiField = propertyType['piiField']
        self.multiValued = propertyType['multiValued']
        self.schemas = propertyType['schemas']
        self.fqn = _concat_fqn(propertyType['type'])

    def print(self):
        return '''**{fqn}**:
        - title: {title}
        - description: {description}
        - datatype: {datatype}
        - analyzer: {analyzer}
        - pii: {piiField}
        - multivalued: {multivalued}
        - schemas: {schemas}'''.format(
            fqn = self.fqn,
            title = self.title,
            description = self.description,
            datatype = self.datatype,
            analyzer = self.analyzer,
            piiField = self.piiField,
            multivalued = self.multiValued,
            schemas = [_concat_fqn(x) for x in self.schemas]
        )

    def compare(self, other):
        propchange = ""
        propchange += _get_table_header(self.fqn)
        for key in ['title', 'description', 'datatype', 'analyzer', 'piiField', 'multiValued', 'schemas', 'fqn']:
            diff = _compare_functions(key, other, self)
            if len(diff)> 0:
                propchange += _get_table_row(diff)
        return propchange

class entityType(object):

    def __init__(self, entityType, propdict):
        self.title = entityType['title']
        self.description = entityType['description']
        self.propertyTags = entityType['propertyTags']
        self.properties = entityType['properties']
        self.key = entityType['key']
        self.schemas = entityType['schemas']
        self.fqn = _concat_fqn(entityType['type'])
        self.propdict = propdict

    def print(self):
        return '''**{fqn}**:
        - title: {title}
        - description: {description}
        - properties: {properties}
        - key properties: {keys}
        - propertytags: {propertytags}
        - schemas: {schemas}'''.format(
            fqn = self.fqn,
            title = self.title,
            description = self.description,
            properties = ", ".join([self.propdict[x] for x in self.properties]),
            keys = ", ".join([self.propdict[x] for x in self.key]),
            propertytags = str(self.propertyTags),
            schemas = [_concat_fqn(x) for x in self.schemas]
        )

    def compare(self, other):
        entchange = ""
        entchange += _get_table_header(self.fqn)
        for key in ['title', 'description', 'properties', 'propertyTags', 'key', 'schemas', 'fqn']:
            diff = _compare_functions(key, other, self)
            if len(diff)> 0:
                entchange += _get_table_row(diff)
        return entchange

class associationType(object):

    def __init__(self, associationType, propdict, entdict):
        self.entityType = entityType(associationType['entityType'], propdict)
        self.fqn = _concat_fqn(associationType['entityType']['type'])
        self.src = associationType['src']
        self.dst = associationType['dst']
        associationType['src']
        self.bidirectional = associationType['bidirectional']
        self.propdict = propdict
        self.entdict = entdict

    def print(self):
        return '''**{fqn}**:
        - title: {title}
        - description: {description}
        - properties: {properties}
        - key properties: {keys}
        - propertytags: {propertytags}
        - schemas: {schemas}
        - src: {src}
        - dst: {dst}
        - bidirectional: {bidir}'''.format(
            fqn = self.entityType.fqn,
            title = self.entityType.title,
            description = self.entityType.description,
            properties = ", ".join([self.propdict[x] for x in self.entityType.properties]),
            keys = ", ".join([self.propdict[x] for x in self.entityType.key]),
            propertytags = str(self.entityType.propertyTags),
            src = [self.entdict[x] for x in self.src if x in self.entdict.keys()],
            dst = [self.entdict[x] for x in self.dst if x in self.entdict.keys()],
            bidir = self.bidirectional,
            schemas = [_concat_fqn(x) for x in self.entityType.schemas]
        )

    def compare(self, other):
        asschange = ""
        asschange += _get_table_header(self.fqn)
        for key in ['title', 'description', 'properties', 'propertyTags', 'key', 'schemas', 'fqn']:
            diff = _compare_functions(key, other.entityType, self.entityType)
            if len(diff)> 0:
                asschange += _get_table_row(diff)
        for key in ['src','dst','bidirectional']:
            diff = _compare_functions(key, other, self)
            if len(diff)> 0:
                asschange += _get_table_row(diff)
        return asschange


def _get_table_header(fqn):
    return '''
    \n**{fqn}**
    \n
    \n| Field | Old | New |\n| --- | --- | --- |'''.format(fqn=fqn)

def _get_table_row(oldnewdict):
    return '\n| {key} | {old} | {new} |'.format(key = oldnewdict['key'], old = oldnewdict['old'], new = oldnewdict['new'])

def _compare_functions(key, old, new):
    compare = {
        "type": _compare_types,
        "schemas": _compare_schemas,
        "datatype": _compare_strings,
        "analyzer": _compare_strings,
        "piiField": _compare_strings,
        "multiValued": _compare_strings,
        "title": _compare_strings,
        "description": _compare_strings,
        'propertyTags': _compare_propertytags,
        'properties': _compare_properties,
        'key': _compare_properties,
        'fqn': _compare_strings,
        'src': _compare_entities,
        'dst': _compare_entities,
        'bidirectional': _compare_strings
    }
    return compare[key](key,old, new)

def _compare_strings(key, old, new):
    if old.__dict__[key] == new.__dict__[key]:
        return ""
    return {"key": key, "old": old.__dict__[key], "new": new.__dict__[key]}

def _compare_types(key, old, new):
    old = _concat_fqn(old.__dict__[key])
    new = _concat_fqn(new.__dict__[key])
    if old == new:
        return ""
    return {"key": key, "old": old, "new": new}

def _compare_schemas(key, old, new):
    outstr = ''
    old = set([_concat_fqn(x) for x in old.__dict__[key]])
    new = set([_concat_fqn(x) for x in new.__dict__[key]])
    return _compare_fqn_list(key, old, new)

def _compare_propertytags(key, old, new):
    if str(old.__dict__[key]) != str(new.__dict__[key]):
        raise ValueError("Changes to propertytags not implemented yet !")
    return ""

def _compare_properties(key, old, new):
    old = [old.propdict[x] for x in old.__dict__[key]]
    new = [new.propdict[x] for x in new.__dict__[key]]
    return _compare_fqn_list(key, old, new)

def _compare_entities(key, old, new):
    old = [old.entdict[x] for x in old.__dict__[key]]
    new = [new.entdict[x] for x in new.__dict__[key]]
    return _compare_fqn_list(key, old, new)

def _compare_fqn_list(key, old, new):
    added = list(set(new) - set(old))
    deleted = list(set(old) - set(new))
    if len(added) == 0 and len(deleted) == 0:
        return ""
    old = ["**%s**"%x if x in deleted else x for x in old]
    new = ["**%s**"%x if x in added else x for x in new]
    oldstr = ", ".join(old)
    newstr = ", ".join(new)
    return {"key": key, "old": oldstr, "new": newstr}

def _get_id_changes(keydict1, keydict2):
    changes = {}
    changes['additions'] = list(set(keydict2.keys()) - set(keydict1.keys()))
    changes['deletions'] = list(set(keydict1.keys()) - set(keydict2.keys()))
    changes['common'] = list(set(keydict1.keys()).intersection(set(keydict2.keys())))
    return changes

def _concat_fqn(fqn):
    '''
    Helper function to go from fqn ({"namespace": x, "name": y}) to
    it's string version "x.y"
    '''
    return "{namespace}.{name}".format(
        namespace=fqn['namespace'],
        name=fqn['name']
        )
