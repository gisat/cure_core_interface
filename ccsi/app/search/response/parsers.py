from ccsi.app.search.response.parameters import from_element_attributes,  from_element_text, \
    from_gdal_geometry, from_gml_geometry, from_xml_attributes_del, enclousure_from_text
from ccsi.app.search.main import ServiceOutput

from lxml import etree
from functools import partial
import gdal
from typing import Union


SET_TYPE = {'text': from_element_text,
            'attribute': from_element_attributes,
            'attribute_del': from_xml_attributes_del,
            'gdal_geom': from_gdal_geometry,
            'gml_geom': from_gml_geometry,
            'enclousure_from_text': enclousure_from_text}


class XMLParserSetting:
    """
    Class serving to strore infrormation xml parser setting i.e. where the information is located
    """
    # TODO: chande to selection by method name

    def __init__(self, func=None, namespace=None, xpath=None, find=None, findall=None):
        """
        :param tag: type of the tag information location. i.e if is in text, attribute
        :param tag: entry tag (resouce / output)
        :param namespace: entry namespace (resouce / output)
        :param xpath: xpath to resource tag
        """
        self.func = SET_TYPE[func]
        self.namespace = namespace
        self.xpath = xpath
        self.find = find
        self.findall = findall

    def set_xpath(self):
        if self.namespace is None:
            return etree.XPath(self.xpath)
        else:
            return etree.XPath(self.xpath, namespaces=self.namespace)

    def get_value(self, feed):
        """apply xpath and func on feed"""
        if self.xpath:
            xpath_func = self.set_xpath()
            element = xpath_func(feed)
        elif self.find:
            element = feed.find(self.find)
        elif self.findall:
            element = feed.findall(self.findall)

        try:
            return self.func(element)
        except IndexError:
            return None


class ParserSettingFactory:

    ENTRY_PARSER_TYPE = {'xml': XMLParserSetting}

    def create(self, settings: dict) -> dict:
        return {name: self.set_parser_setting(**setting) for name, setting in settings.items()}

    def set_parser_setting(self, parser: dict, **ignore):
        try:
            parser_type, properties = parser.values()
            return self.ENTRY_PARSER_TYPE[parser_type](**properties)
        except TypeError:
            return None


parser_setting_factory = ParserSettingFactory()


class XMLParser:
    """Service specific Xml parser, return Entry object"""

    OS = {'os': 'http://a9.com/-/spec/opensearch/1.1/'}
    ATOM = {'atom': 'http://www.w3.org/2005/Atom'}

    def __init__(self, service_name, entry, setting):
        self.service_name = service_name
        self._entry = entry
        self.setting = setting
        self._total_results = etree.XPath('os:totalResults', namespaces=self.OS)
        self._start_index = etree.XPath('os:startIndex', namespaces=self.OS)
        self._items_per_page = etree.XPath('os:itemsPerPage', namespaces=self.OS)
        self._entry_tags = etree.XPath('atom:entry', namespaces=self.ATOM)

    @classmethod
    def create(cls, service_name, entry, setting):
        return cls(service_name, entry, setting)

    def total_results(self, feed):
        """return total result from open search feed"""
        return int(self._total_results(feed)[0].text)

    def start_index(self, feed):

        return int(self._start_index(feed)[0].text)

    def item_per_page(self, feed):
        return int(self._items_per_page(feed)[0].text)

    def entry_tags(self, feed):
        return self._entry_tags(feed)

    @property
    def entry_template(self):
        return self._entry.copy()

    def parse_response(self, response):
        feed = self.get_feed(response)
        output = ServiceOutput(self.service_name)
        output.total_results = self.total_results(feed)
        output.item_per_page = self.item_per_page(feed)
        output.start_index = self.start_index(feed)

        for entry_tag in self.entry_tags(feed):
            entry = self.entry_template
            for name, atr in entry.parameters.items():
                value = self.setting[name].get_value(entry_tag)
                atr.set_value(value)
            output.entries.append(entry)
        return output

    def get_feed(self, response: 'Response'):
        return etree.fromstring(response.text.encode('utf-8'))

    def find_entry(self, xml):
        root = etree.fromstring(xml.encode('utf-8'))
        return [child for child in root.getchildren() if etree.QName(child).localname == self.entry_tag]

    def get_set_func(self, parameter_name):
        return self.set_funcs.get(parameter_name)

    @staticmethod
    def _create_set_func(func, properties):
        if properties is None:
            return XMLParser.SET_TYPE.get(func)
        return partial(XMLParser.SET_TYPE.get(func), *properties)

    @staticmethod
    def _create_set_funcs(mapped_pars):
        return {entry_parameter: XMLParser._create_set_func(**func_params) for entry_parameter, func_params
                in mapped_pars.items()}

class XMLGdalParser(XMLParser):

    def parse_response(self, response):
        feed = self.get_feed(response)
        output = ServiceOutput(self.service_name)
        output.total_results = self.total_results(feed)
        output.item_per_page = self.item_per_page(feed)
        output.start_index = self.start_index(feed)

        for entry_tag, geometry in zip(self.entry_tags(feed), self.read_geometry_with_gdal(response)):
            entry = self.entry_template
            for name, atr in entry.parameters.items():
                if name == 'geometry':
                    value = self.setting[name].func(geometry)
                    atr.set_value(value)
                else:
                    try:
                        value = self.setting[name].get_value(entry_tag)
                        atr.set_value(value)
                    except Exception:
                        pass
            output.entries.append(entry)
        return output

    def read_geometry_with_gdal(self, response):
        gdal.FileFromMemBuffer('/vsimem/temp', response.content)
        dataset = gdal.ogr.Open('/vsimem/temp')
        layer = dataset.GetLayer(0)
        for _ in range(layer.GetFeatureCount()):
            yield layer.GetNextFeature()
        layer = None
        gdal.Unlink('/vsimem/temp')


class ResponseParserFactory:
    """Parser builder return parser"""
    PARSER_TYPE = {'xml_gdal': XMLGdalParser,
                   'xml': XMLParser}

    def create(self, service_name, entry, setting, parser_type) -> Union[XMLGdalParser, XMLParser, None]:
        return self.PARSER_TYPE.get(parser_type).create(service_name, entry, setting)


response_parser_factory = ResponseParserFactory()
