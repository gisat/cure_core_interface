from ccsi.app.search.response.parameters import from_xml_attributes, from_xml_text, from_gdal_geometry, \
    from_gml_geometry, from_xml_attributes_del
from lxml import etree
from functools import partial
import gdal


class XMLParser:
    """Service specific Xml parser, return Entry object"""
    SET_TYPE = {'text': from_xml_text,
                'attribute': from_xml_attributes,
                'attribute_del': from_xml_attributes_del,
                'gdal_geom': from_gdal_geometry,
                'gml_geom': from_gml_geometry}

    def __init__(self, entry, set_funcs, entry_tag):
        self.entry = entry
        self.set_funcs = set_funcs
        self.entry_tag = entry_tag

    @classmethod
    def create(cls, entry, mapped_pars,  entry_tag):
        set_funcs = XMLParser._create_set_funcs(mapped_pars)
        return cls(entry, set_funcs, entry_tag)

    def parse_response(self, response):
        elements = self.find_entry(response.text)
        entries = [self.entry.copy() for _ in range(len(elements))]
        for entry, element in zip(entries, elements):
            for atr in entry.__dict__.keys():
                entry.set_attribute(atr, self.get_set_func(atr)(element))
        return entries

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
        gdal.FileFromMemBuffer('/vsimem/temp', response.content)
        dataset = gdal.ogr.Open('/vsimem/temp')
        layer = dataset.GetLayer(0)
        if layer is not None:
            entries = [self.entry.copy() for _ in range(layer.GetFeatureCount())]
            for entry, feed_entry in zip(entries, self.find_entry(response.text)):
                feature = layer.GetNextFeature()
                for atr in entry.__dict__.keys():
                    if atr == 'geometry':
                        entry.set_attribute(atr, self.get_set_func(atr)(feature))
                    else:
                        entry.set_attribute(atr, self.get_set_func(atr)(feed_entry))
            layer = None
            gdal.Unlink('/vsimem/temp')
            return entries
        return []


class ResponseParserBuilder:
    """Parser builder return parser"""
    PARSER_TYPE = {'xml_gdal': XMLGdalParser,
                   'xml': XMLParser}

    def build(self, entry, parser_type: str, properties: dict, ) -> XMLParser:
        parser = self.PARSER_TYPE.get(parser_type)
        return parser.create(entry, **properties)


response_parser_builder = ResponseParserBuilder()

