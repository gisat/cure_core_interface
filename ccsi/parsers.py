from lxml import etree
from urllib.parse import parse_qsl, urlparse
from xmljson import Abdera


class OpenSearchDescriptionParser:
    # predelat


    # open search query XPath specification
    QUERY_STRING = '{http://a9.com/-/spec/opensearch/1.1/}Url[@rel="results"][@type="application/atom+xml"]'
    QUERY_PARAMETERS = './/{http://a9.com/-/spec/opensearch/extensions/parameters/1.0/}'

    # return parameters of OpenSearchDescriptionParser taken from urlib.url_parse
    RETURN_URL_DICT = ('scheme', 'netloc', 'path', 'params', 'fragment')

    def decode_description(self, response):
        """
        Parse xml open search description. Search for query string a his parameters.
        Input Response object
        Return JSON object with same attributes as Urllib.ParseResult. Query attribute is dict contain details of each
        query parameter
        """
        # parse xml
        xml = etree.fromstring(response.content)
        # find query string
        url_parse = urlparse(xml.findall(self.QUERY_STRING)[0].attrib.get('template'))
        parse_dict = {key: url_parse.__getattribute__(key) for key in self.RETURN_URL_DICT}
        parse_dict['query'] = {}
        # parse query string
        for key, value in sorted(parse_qsl(url_parse.query)):
            try:
                parameter = xml.findall(self.QUERY_PARAMETERS+'Parameter'+f'[@name="{key}"]')[0]
                attr = dict(parameter.attrib)
                if len(parameter.findall(self.QUERY_PARAMETERS+'Option')) > 0:
                    attr.update({'options': [option.attrib.get('value') for option in
                                             parameter.findall(self.QUERY_PARAMETERS + 'Option')]})
                parse_dict['query'].update({key: attr})
            except IndexError:
                parse_dict['query'].update({key: {'name': key, 'value': value}})
        return parse_dict, url_parse


class XMLConvertor:

    # extension of XMLJson

    def __init__(self):
        self.convertor = None

    def create(self, dict_type=dict, convention='adbera'):
        if convention =='adbera':
            self.convertor = Abdera(dict_type=dict_type)
        else:
            raise ValueError(f'Convention {convention} is not supported')
        return self

    def element_to_json(self, elements, tag):
        tags = elements.findall(tag)
        return [self.convertor.data(tag) for tag in tags]

    def json_to_xml(self, json, root=None):
        if root is not None:
            return self.convertor.etree(json, root=root)
        return self.convertor.etree(json)



open_description_parser = OpenSearchDescriptionParser()
xml_convertor = XMLConvertor().create()
