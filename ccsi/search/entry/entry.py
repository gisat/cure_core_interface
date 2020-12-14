from ccsi.config import Config
from functools import partial
from ccsi.search.entry.parameters import from_xml_attributes, from_xml_text, from_xml_gml_geometry
from lxml import etree
from geojson import Feature, loads
import copy


class EntryParameter:
    def __init__(self, name, namespace, func, value):
        self.name = name
        self.value = value
        self.namespace = namespace
        self.set = func

    @classmethod
    def create(cls, name, namespace, func, default=None, **ignore):
        if namespace['prefix'] == '':
            ns = {None: namespace['namespace']}
        else:
            ns = {namespace['prefix']: namespace['namespace']}
        return cls(name, ns, func, default)

    def set_value(self, value):
        self.value = self.set(value)

    def to_json(self):
        return {self.name: self.value}

    def to_xml(self):
        element = etree.Element(self.name, nsmap=self.namespace)
        element.text = self.value
        return [element]


class EntryAtribute(EntryParameter):

    def to_json(self):
        return {self.name: self.value}

    def to_xml(self):
        return [etree.Element(self.name, nsmap=self.namespace, **atribute_set) for atribute_set in self.value]


class EntryGeometry(EntryParameter):

    def to_json(self):
        crs = {"type": "name", "properties": {"name": f'EPSG:{self.value["epsg"]}'}}
        geometry = loads(self.value['geometry'].ExportToJson())
        return Feature(geometry=geometry, crs=crs)

    def to_xml(self):
        return [etree.fromstring(self.value['geometry'].ExportToGML(["NAMESPACE_DECL=YES"]))]


class Entry:
    PARAMETR_TYPE = {'text': EntryParameter,
                     'attribute': EntryAtribute,
                     'geometry': EntryGeometry}

    def __init__(self, properties: dict):
        for name, property in properties.items():
            setattr(self, name, self.PARAMETR_TYPE[property.get('type')].create(name, **property))

    @classmethod
    def create(cls, properties):
        return cls(properties)

    def parse(self, element: etree.Element):
        for atribute in self.__dict__.values():
            atribute.set_value(element)
        return copy.deepcopy(self)

    def to_xml(self):
        entry = etree.Element('entry')
        for attr in self.__dict__.keys():
            for element in getattr(self, attr).to_xml():
                entry.append(element)
        return entry

    def to_json(self):
        properties = {}
        for attr in self.__dict__.keys():
            if attr != 'geometry':
                properties.update(getattr(self, attr).to_json())
        if 'geometry' in self.__dict__.keys():
            entry = getattr(self, 'geometry').to_json()
            entry.properties.update(properties)
        else:
            entry = Feature(properties=properties)
        return entry

class XMLParser:
    """Service specific Xml parser"""
    SET_TYPE = {'text': from_xml_text,
                'attribute': from_xml_attributes,
                'geometry': from_xml_gml_geometry}

    ENTRY_PARS = Config.ENTRY_PARS

    def __init__(self, mapped, entry_tag):
        self.entry_tag = entry_tag
        entry_pars = {}
        for name, pars in mapped.items():
            entry_pars.update({name: self._create_entry_pars(self.ENTRY_PARS.get(name), pars)})
        self.entry = Entry.create(entry_pars)

    @classmethod
    def create(cls, properties):
        return cls(**properties)

    def parse(self, response):
        return [self.entry.parse(entry) for entry in self.find_entry(response.content)]

    def find_entry(self, xml):
        root = etree.fromstring(xml)
        return [child for child in root.getchildren() if etree.QName(child).localname == self.entry_tag]

    def _create_set_func(self, tag, namespace, func_type):
        return partial(self.SET_TYPE.get(func_type), tag, namespace)

    def _create_entry_pars(self, entry_pars: dict, func_pars):
        func = self._create_set_func(*func_pars)
        new = entry_pars.copy()
        new.update({'func': func})
        return new



class ResponseParserBuilder:
    PARSER_TYPE = {'xml': XMLParser}

    def __init__(self):
        pass

    def build(self, response_type, properties):
        parser = self.PARSER_TYPE.get(response_type)
        if parser is not None:
            return parser.create(properties)

response_parser_builder = ResponseParserBuilder()
