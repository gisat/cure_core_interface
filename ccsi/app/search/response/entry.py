from lxml import etree
from geojson import Feature, loads
import copy


class EntryText:
    """
    Standard entry parameter to harmonize inputs from services. Input value serialized as text parameter.
    Data passed in text, attrib during th initialization are used as defaults"""

    def __init__(self, tag: str, namespace: dict,  attrib={}, text=None):
        """
        :param tag: tag name
        :param namespace: namespace definiton
        :param attrib: tag attribute value
        :param text: tag text value
        :param parser: (optional) parser setting
        """
        self.tag = tag
        self.namespace = namespace
        self.attrib = attrib
        self.text = text

    @classmethod
    def create(cls, tag, namespace, attrib=None, text=None, **ignore):
        return cls(tag, namespace, attrib, text)

    def set_value(self, value):
        self.text = value

    def to_json(self):
        if self.attrib is {}:
            return {self.tag: self.text}
        return {self.tag: self.text,
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
        return [etree.Element(self.tag, nsmap=self.namespace, **atribute_set) for atribute_set in self.attrib]

    def to_json(self):
        return {self.tag: [atr for atr in self.attrib]}


class EntryGeometry(EntryText):
    """
    Standard entry parameter to harmonize inputs from services. Derived from EntryText
    Used to harmonized coordination and projection.
    Serialized as as gml or geojson
    Data passed in text, attrib during th initialization are used as defaults"""

    def __init__(self, tag, namespace):
        self.value = None
        super().__init__(tag, namespace)

    @classmethod
    def create(cls, tag, namespace, **ignore):
        return cls(tag, namespace)

    def set_value(self, value):
        self.value = value

    def to_json(self):
        crs = {"type": "name", "properties": {"name": f'{self.value["json"]["epsg"]}'}}
        geometry = loads(self.value['json'].get('geometry'))
        return Feature(geometry=geometry, crs=crs)

    def to_xml(self):
        return [etree.fromstring(self.value['xml'].get('geometry'))]


class Entry:

    def __init__(self):
        pass

    @property
    def parameters(self) -> dict:
        """
        :return: dictionary of entry attributes
        """
        return self.__dict__

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

        # if geometry is part of entry
        if 'geometry' in self.__dict__.keys():
            entry = getattr(self, 'geometry').to_json()
            entry.properties.update(properties)
        else:
            entry = Feature(properties=properties)
        return entry

    def copy(self):
        return copy.deepcopy(self)


class EntryFactory:
    """
    class to built Entry container
    """
    ENTRY_PARAMETR_TYPE = {'text': EntryText,
                           'attribute': EntryAtribute,
                           'attribute_many': EntryAtributeMany,
                           'geometry': EntryGeometry}

    def create(self, settings: dict) -> Entry:
        # initialization of Entry container
        entry = Entry()
        # setting of entry
        for name, setting in settings.items():
            self.set_entry_parameter(entry, name, **setting)
        return entry

    def set_entry_parameter(self, entry, name, typ, tag, **ignore):
        setattr(entry, name, self.ENTRY_PARAMETR_TYPE[typ].create(**tag))

entry_factory = EntryFactory()




