from lxml.etree import Element, SubElement, tostring
from ccsi.config import XML_NAMESPACES

class DescriptionDocument:
    TAIL = {'SyndicationRight': 'open',
            'AdultContent': 'false',
            'Language': 'en',
            'OutputEncoding': 'UTF-8',
            'InputEncoding' : 'UTF-8'}

    def __init__(self, description, service):
        self.description = description
        self.service = service

    @classmethod
    def create(cls, descripton, service=None):
        return cls(descripton, service)

    @staticmethod
    def create_SubElement(parent, tag, attrib={}, text=None, nsmap=None, **_extra):
        result = SubElement(parent, tag, attrib, nsmap, **_extra)
        result.text = text
        return result

    def get_params(self) -> dict:
        if self.service:
            return {name: properties for name, properties in self.description.items() if name in self.service.input_parameters().keys()}
        else:
            return self.description

    def nsmap(self):
        """return xml namespaces in for required by lxml"""
        return {prefix: ns for namespace in XML_NAMESPACES.values() for prefix, ns in namespace.items()}

    def get_head(self):
        feed = Element('OpenSearchDescription', nsmap=self.nsmap())
        self.create_SubElement(feed, 'ShortName', text=f'CCSI')
        self.create_SubElement(feed, 'LongName', text=f'Copernicus Core Service Interface')
        self.create_SubElement(feed, 'Description', text=f'OpenSearch description document that describes how '
                                                                  f'to query data provided this endpoint')
        self.create_SubElement(feed, 'Contact', text='michal.opletal@gisat.cz')
        return feed

    @staticmethod
    def _crt_param_attrb(name, namespace, title):
        attrib = {}
        attrib['name'] = name
        attrib['value'] = f"{list(namespace.keys())[0]}:{name}"
        attrib['title']= title
        return attrib

    def _get_params_attrib(self):
        return [self._crt_param_attrb(name, **properties) for name, properties in self.get_params().items()]

    def add_param_tags(self, feed):
        for attrib in self._get_params_attrib():
            attrib['value'] = f'{{{attrib["value"]}}}'
            self.create_SubElement(feed, 'Parameter', attrib=attrib, nsmap={'param': 'http://a9.com/-/spec/opensearch/extensions/parameters/1.0/'})
        return feed

    def join_params(self, params):
        return '&'.join([f'{key}={value}' for key, value in params.items()])

    def get_url(self, feed, url, type):
        url_params = {attrib.get('name'): f"{{{attrib.get('value')}?}}" for attrib in self._get_params_attrib()}
        attrib={}
        attrib['type'] = type
        attrib['rel'] = 'result'
        attrib['template'] = f'{url}?{self.join_params(url_params)}'
        self.create_SubElement(feed, 'Url', attrib=attrib)
        return feed

    def get_tail(self, feed):
        for tag, text in DescriptionDocument.TAIL.items():
            self.create_SubElement(feed, tag, text=text)
        return feed

    def document(self, endpoint_url, type):
        feed = self.get_head()
        self.get_url(feed, endpoint_url, type)
        self.add_param_tags(feed)
        self.get_tail(feed)
        return tostring(feed, pretty_print=True).decode("utf-8")



