from ccsi.config import XML_NAMESPACES
from lxml.etree import Element, SubElement
from datetime import datetime


def create_SubElement(parent, tag, attrib={}, text=None, nsmap=None, **_extra):
    result = SubElement(parent, tag, attrib, nsmap, **_extra)
    result.text = text
    return result


class OpenSearchResponse:

    def __init__(self, base_url, original_args, process_request, total_results):
        self.base_url = base_url
        self.original_args = original_args
        self.process_request = process_request
        self.totalresults = total_results

    @property
    def url(self):
        return self.base_url + '?' + self.encode(self.process_request)

    @property
    def maxrecords(self):
        return int(self.process_request.get('maxrecords'))

    @property
    def startindex(self):
        return int(self.process_request.get('startindex'))

    @property
    def page(self):
        return int(self.process_request.get('page'))

    @property
    def first_page(self):
        return {'startindex': 0, 'page': 0}

    @property
    def next_page(self):
        if self.totalresults > self.startindex+self.page*self.maxrecords:
            return {'startindex': self.startindex+self.maxrecords, 'page':self.page + 1}
        else:
            return {'startindex': self.startindex, 'page':self.page}

    @property
    def last_page(self):
        return {'startindex': self.totalresults, 'page': self.totalresults // self.maxrecords}

    def encode(self, parameters: dict, delimiter='&'):
        return delimiter.join([f'{key}={value}' for key, value in parameters.items()])

    def nsmap(self):
        """return xml namespaces in for required by lxml"""
        return {prefix: ns for namespace in XML_NAMESPACES.values() for prefix, ns in namespace.items()}

    def create_link_url(self, link_parameter):
        request = {k: v for k, v in self.process_request.items() if k not in ['startindex', 'page']}
        request.update(link_parameter)
        return self.encode(request)

    def crate_json_links(self):
        self_link = {"rel": "self", "type": "application/json", "title": "self", "href": self.url}
        search_link = {"rel": "search", "type": "application/opensearchdescription+xml", "title":
            "OpenSearch Description Document", "href": f"{self.base_url}/describe.xml"}
        first_link = {"rel": "first", "type": "application/json",
                      "title": "first", "href": f"{self.base_url}&{self.create_link_url(self.first_page)}"}
        next_link = {"rel": "next", "type": "application/json",
                     "title": "next", "href": f"{self.base_url}&{self.create_link_url(self.next_page)}"}
        last_link = {"rel": "last", "type": "application/json",
                     "title": "last", "href": f"{self.base_url}&{self.create_link_url(self.last_page)}"}
        return [self_link, search_link, first_link, next_link, last_link]


    def atom_head(self):
        feed = Element('feed', nsmap=self.nsmap())
        title = create_SubElement(feed, 'title', text=f'Copernicus Core Service Interface search results for:'
                                                           f'{self.encode(self.process_request, delimiter= "; ")}')
        subtitle = create_SubElement(feed, 'subtitle', text=f'Displaying {self.totalresults} results')
        updated = create_SubElement(feed, 'updated', text=datetime.now().isoformat())
        author = create_SubElement(feed, 'author')
        name = create_SubElement(author, 'name', text='Copernicus Core Service Interface')
        id = create_SubElement(feed, 'id', text=self.url)
        totalresults = create_SubElement(feed, 'totalResults', text=str(self.totalresults))
        startindex = create_SubElement(feed, 'startIndex', text=str(self.startindex))
        itemsperpage = create_SubElement(feed, 'itemsPerPage', text=str(self.maxrecords))
        query = create_SubElement(feed, 'Query', attrib={'role': 'request',
                                                              'searchTerms': self.encode(self.process_request)})
        search_link = create_SubElement(feed, 'link', attrib={'rel': 'search',
                                                                   'type': 'application/opensearchdescription+xml',
                                                                   'href': f'{self.base_url}/description.xml'})
        self_link = create_SubElement(feed, 'link', attrib={'rel': 'self', 'type': 'application/atom+xml',
                                                                 'href': self.url})
        first_link = create_SubElement(feed, 'link', attrib={'rel': 'first', 'type': 'application/atom+xml',
                                                                  'href': f"{self.base_url}&"
                                                                          f"{self.create_link_url(self.first_page)}"})
        next_link = create_SubElement(feed, 'link', attrib={'rel': 'next', 'type': 'application/atom+xml',
                                                                  'href': f"{self.base_url}&"
                                                                          f"{self.create_link_url(self.next_page)}"})
        last_link = create_SubElement(feed, 'link', attrib={'rel': 'last', 'type': 'application/atom+xml',
                                                                 'href': f"{self.base_url}&"
                                                                         f"{self.create_link_url(self.last_page)}"})
        return feed

    def json_head(self):
        properties = {
            "totalResults": self.totalresults,
            "exactCount": True if self.maxrecords <= self.totalresults else True,
            "startIndex": self.startindex,
            "itemsPerPage": self.maxrecords,
            "query": self.original_args,
            "links": self.crate_json_links()}
        return properties


class BaseResponse(OpenSearchResponse):

    def crate_json_links(self):
        self_link = {"rel": "self", "type": "application/json", "title": "self", "href": self.url}
        search_link = {"rel": "search", "type": "application/opensearchdescription+xml", "title":
            "OpenSearch Description Document", "href": f"{self.base_url}/describe.xml"}

        return [self_link, search_link]


    def atom_head(self):
        feed = Element('feed', nsmap=self.nsmap())
        title = create_SubElement(feed, 'title', text=f'Copernicus Core Service Interface search results for:'
                                                      f'{self.encode(self.process_request, delimiter= "; ")}')
        subtitle = create_SubElement(feed, 'subtitle', text=f'Displaying {self.totalresults} results')
        updated = create_SubElement(feed, 'updated', text=datetime.now().isoformat())
        author = create_SubElement(feed, 'author')
        name = create_SubElement(author, 'name', text='Copernicus Core Service Interface')
        id = create_SubElement(feed, 'id', text=self.url)
        totalresults = create_SubElement(feed, 'totalResults', text=str(self.totalresults))
        startindex = create_SubElement(feed, 'startIndex', text=str(self.startindex))
        itemsperpage = create_SubElement(feed, 'itemsPerPage', text=str(self.maxrecords))
        query = create_SubElement(feed, 'Query', attrib={'role': 'request',
                                                         'searchTerms': self.encode(self.process_request)})
        search_link = create_SubElement(feed, 'link', attrib={'rel': 'search',
                                                              'type': 'application/opensearchdescription+xml',
                                                              'href': f'{self.base_url}/description.xml'})
        self_link = create_SubElement(feed, 'link', attrib={'rel': 'self', 'type': 'application/atom+xml',
                                                            'href': self.url})

        return feed
