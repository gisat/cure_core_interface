from lxml import etree
from geojson import Feature, loads
import copy


class EntryText:
    """
    Standard entry parameter to harmonize inputs from services. Input value serialized as text parameter.
    Data passed in text, attrib during th initialization are used as defaults

    :param name: unique name o parameter, used for mapping
    :type name: str
    :param tag: tag name of xml tag or json tag property
    :type tag: str
    :param attrib: attribute data, default = {}
    :type: attrib: dict
    :param text: parameter text, serialized as xml text. In json representation as json value, default = none
    :type text: str
    :param namespace: namespace of attribute, used in xml serialization. In form {'prefix': 'namespace}
    :type namespace: dict
    :param rule: additional rule func corrigate input, default = None
    """

    def __init__(self, name, tag, namespace, attrib={}, text=None):
        self.name = name
        self.tag = tag
        self.attrib = attrib
        self.text = text
        self.namespace = namespace

    @classmethod
    def create(cls, name, tag, namespace, attrib={}, text=None, **ignore):
        if namespace['prefix'] == '':
            ns = {None: namespace['namespace']}
        else:
            ns = {namespace['prefix']: namespace['namespace']}
        return cls(name=name, tag=tag, attrib=attrib, text=text, namespace=ns)

    def set_value(self, value):
        self.text = value

    def to_json(self):
        if self.attrib is {}:
            return {self.name: self.value}
        return {self.name: self.value,
                'properties': self.attrib}

    def to_xml(self):
        element = etree.Element(self.tag, self.attrib, nsmap=self.namespace)
        element.text = self.text
        return [element]


class EntryAtribute(EntryText):
    """
    Standard entry parameter to harmonize inputs from services. Derived from EntryText
    Input value serialized as attribute parameter.
    Data passed in text, attrib during th initialization are used as defaults"""

    def set_value(self, value):
        if isinstance(value, list):
            self.attrib.update(value[0])
        else:
            self.attrib.update(value)


class EntryAtributeMany(EntryText):
    """
    Standard entry parameter to harmonize inputs from services. Derived from EntryText
    Input value is a list of dict. Serialized as list of attributes or tags with different atributes
    Data passed in text, attrib during th initialization are used as defaults"""

    def set_value(self, value):
        self.attrib = value

    def to_xml(self):
        return [etree.Element(self.name, nsmap=self.namespace, **atribute_set) for atribute_set in self.attrib]


class EntryGeometry(EntryText):
    """
    Standard entry parameter to harmonize inputs from services. Derived from EntryText
    Used to harmonized coordination and projection.
    Serialized as as gml or geojson
    Data passed in text, attrib during th initialization are used as defaults"""

    def __init__(self, name, tag, namespace):
        self.value = None
        super().__init__(name, tag, namespace)

    @classmethod
    def create(cls, name, tag, namespace, **ignore):
        return cls(name, tag, namespace)

    def set_value(self, value):
        self.value = value

    def to_json(self):
        crs = {"type": "name", "properties": {"name": f'{self.value["json"]["epsg"]}'}}
        geometry = loads(self.value['json'].get('geometry'))
        return Feature(geometry=geometry, crs=crs)

    def to_xml(self):
        return [etree.fromstring(self.value['xml'].get('geometry'))]


class Entry:
    PARAMETR_TYPE = {'text': EntryText,
                     'attribute': EntryAtribute,
                     'attribute_many': EntryAtributeMany,
                     'geometry': EntryGeometry}

    def __init__(self, properties: dict):
        for name, property in properties.items():
            setattr(self, name, self.PARAMETR_TYPE[property.get('type')].create(name, **property))

    @classmethod
    def create(cls, properties):
        return cls(properties)

    def set_attribute(self, atribute, value):
        self.__dict__[atribute].set_value(value)

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

    def copy(self):
        return copy.deepcopy(self)



